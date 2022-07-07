'''
Last Modified: 6/17/2022

This file contains classes with methods that interact directly with the hardware of the microscope, 
as well as some properties for said devices. There's one class:

-MMHardwareCommands: Interacts with all hardware devices connected through Micro-Manager

Future changes:
- Perhaps put all properties into a separate class? Reason to do this would be to make commands 
  more generically usable. Could be useful in future development of image acquisitions. Would
  also be more true to the nature of MVC.

Notes:
- I just realized that there's a small, unavoidable timing error when performing a z-stack with 
  the PLC as the master. For the PLC to run at 30 Hz, it would need to pulse every 33.33 ms, but
  the PLC has a 4kHz internal clock, which means it can either pulse every 33.25 or 33.50 ms. 
  Currently, it's set to round up to avoid the camera potentially missing trigger pulses, and so
  there's an intrinsic .16 ms timing error. This translates to a 4.8 nm error (0.16 ms * 30 um/s), 
  which is negligable, but I thought it was worth noting just in case something related popped up.

- This file is a mess on this microscope due to the fact that the X-axis and Z-axis are effectively
  swapped.  What is physically labelled as the XY-stage is actually the ZY-stage, and the Z-stage is 
  the X-stage. Unfortunately, Micro-Manager has no internal way of swapping them, so I've done it 
  programmatically, which looks slightly confusing. Just note that what Micro-Manager thinks is 
  the XY-stage is actually the ZY-stage and the Z-stage is actually the X-stage.
'''


import numpy as np
from pycromanager import Studio, Core


class MMHardwareCommands(object):
    def __init__(self, studio: Studio, core: Core):
        self.studio = studio
        self.core = core

        #PLC property names and properties
        self.plc_name = "PLogic:E:36"
        self.prop_position = "PointerPosition"
        self.prop_cell_type = "EditCellCellType"
        self.prop_cell_config = "EditCellConfig"
        self.prop_cell_input_1 = "EditCellInput1"
        self.prop_cell_input_2 = "EditCellInput2"
        self.val_input = "0 - input"
        self.val_constant = "0 - constant"
        self.val_output = "2 - output (push-pull)"
        self.val_and = "5 - 2-input AND"
        self.val_or = "6 - 2-input OR"
        self.val_one_shot = "8 - one shot"
        self.val_delay = "9 - delay"
        self.addr_clk = 192
        self.addr_bnc_1 = 33
        self.addr_stage_ttl= 34
        self.addr_delay_1 = 1
        self.addr_or = 2
        self.addr_and = 3
        self.addr_delay_2 = 4
        self.addr_one_shot = 5
        self.addr_constant = 6
        
        #Camera property names
        self.trigger_mode_prop = "Triggermode"
        
        #Camera parameters
        self.cam_name = self.core.get_camera_device()
        self.default_trigger_mode = "Internal"
        self.scan_trigger_mode = "External"
        self.default_exposure = 20
        
        #Stage property names
        self.x_speed_property = "Speed-S"
        self.y_speed_property = "Speed-S"
        self.z_speed_property = "Speed-S"
        self.serial = "SerialCommand"
        
        #Stage properties
        self.zy_stage_name = self.core.get_xy_stage_device()
        self.x_stage_name = self.core.get_focus_device()
        self.scan_properties = "SCAN X=1 Y=0 Z=0"
        self.scan_start_command = "SCAN"
        self.x_stage_speed = 1.0
        self.zy_stage_speed = 1.0
    
    def set_property(self, device, prop, value):
        self.core.set_property(device, prop, value)

    def initialize_plc_for_scan(self, step_size, z_scan_speed):
        """
        The PLC (programmable logic card) is used to create logic circuits through software.
        The circuit here creates a pulse matching the stage speed and step size during 
        a z-stack. This pulse is sent to the camera as an external trigger. If the stage
        scan speed is set to 0.030 mm/s and the step size is 1um, then the PLC output
        will pulse at 30 Hz.

        For a full realization of this circuit, lease see the developer guide.
        """

        #factor of 4 in frame interval is because the plc clock runs at 4 khz, so 4 clock
        #ticks is 1 ms
        trigger_pulse_width = 20
        frame_interval = np.ceil((step_size / z_scan_speed) * 4)
        
        self.set_property(self.plc_name, self.prop_position, self.addr_stage_ttl)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_input)

        self.set_property(self.plc_name, self.prop_position, self.addr_delay_1)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_delay)
        self.set_property(self.plc_name, self.prop_cell_config, 0)
        self.set_property(self.plc_name, self.prop_cell_input_1, self.addr_stage_ttl)
        self.set_property(self.plc_name, self.prop_cell_input_2, self.addr_clk)

        self.set_property(self.plc_name, self.prop_position, self.addr_or)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_or)
        self.set_property(self.plc_name, self.prop_cell_config, 0)
        self.set_property(self.plc_name, self.prop_cell_input_1, self.addr_delay_1)
        self.set_property(self.plc_name, self.prop_cell_input_2, self.addr_delay_2)

        self.set_property(self.plc_name, self.prop_position, self.addr_and)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_and)
        self.set_property(self.plc_name, self.prop_cell_config, 0)
        self.set_property(self.plc_name, self.prop_cell_input_1, self.addr_or)
        self.set_property(self.plc_name, self.prop_cell_input_2, self.addr_stage_ttl)

        self.set_property(self.plc_name, self.prop_position, self.addr_delay_2)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_delay)
        self.set_property(self.plc_name, self.prop_cell_config, frame_interval)
        self.set_property(self.plc_name, self.prop_cell_input_1, self.addr_and)
        self.set_property(self.plc_name, self.prop_cell_input_2, self.addr_clk)

        self.set_property(self.plc_name, self.prop_position, self.addr_one_shot)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_one_shot)
        self.set_property(self.plc_name, self.prop_cell_config, trigger_pulse_width)
        self.set_property(self.plc_name, self.prop_cell_input_1, self.addr_delay_2)
        self.set_property(self.plc_name, self.prop_cell_input_2, self.addr_clk)

        self.set_property(self.plc_name, self.prop_position, self.addr_bnc_1)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_output)
        self.set_property(self.plc_name, self.prop_cell_config, self.addr_one_shot)
        self.set_property(self.plc_name, self.prop_cell_input_1, 0)
        self.set_property(self.plc_name, self.prop_cell_input_2, 0)
    
    def initialize_plc_for_continuous_lsrm(self, framerate):
        # Same as the last PLC function except it pulses on its own.

        trigger_pulse_width = 4
        frame_interval = np.ceil(1.0 / framerate * 1000 * 4)

        self.set_property(self.plc_name, self.prop_position, self.addr_delay_1)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_delay)
        self.set_property(self.plc_name, self.prop_cell_config, 0)
        self.set_property(self.plc_name, self.prop_cell_input_1, self.addr_constant)
        self.set_property(self.plc_name, self.prop_cell_input_2, self.addr_clk)

        self.set_property(self.plc_name, self.prop_position, self.addr_or)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_or)
        self.set_property(self.plc_name, self.prop_cell_config, 0)
        self.set_property(self.plc_name, self.prop_cell_input_1, self.addr_delay_1)
        self.set_property(self.plc_name, self.prop_cell_input_2, self.addr_delay_2)

        self.set_property(self.plc_name, self.prop_position, self.addr_and)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_and)
        self.set_property(self.plc_name, self.prop_cell_config, 0)
        self.set_property(self.plc_name, self.prop_cell_input_1, self.addr_or)
        self.set_property(self.plc_name, self.prop_cell_input_2, self.addr_constant)

        self.set_property(self.plc_name, self.prop_position, self.addr_delay_2)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_delay)
        self.set_property(self.plc_name, self.prop_cell_config, frame_interval)
        self.set_property(self.plc_name, self.prop_cell_input_1, self.addr_and)
        self.set_property(self.plc_name, self.prop_cell_input_2, self.addr_clk)

        self.set_property(self.plc_name, self.prop_position, self.addr_one_shot)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_one_shot)
        self.set_property(self.plc_name, self.prop_cell_config, trigger_pulse_width)
        self.set_property(self.plc_name, self.prop_cell_input_1, self.addr_delay_2)
        self.set_property(self.plc_name, self.prop_cell_input_2, self.addr_clk)

        self.set_property(self.plc_name, self.prop_position, self.addr_bnc_1)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_output)
        self.set_property(self.plc_name, self.prop_cell_config, self.addr_one_shot)
        self.set_property(self.plc_name, self.prop_cell_input_1, 0)
        self.set_property(self.plc_name, self.prop_cell_input_2, 0)

        self.set_property(self.plc_name, self.prop_position, self.addr_constant)
        self.set_property(self.plc_name, self.prop_cell_type, self.val_constant)
        self.set_property(self.plc_name, self.prop_cell_config, 1)

    def set_dslm_camera_properties(self, z_scan_speed):
        #Sets camera properties for a DSLM zstack
        self.studio.live().set_live_mode_on(False)
        exposure = 20
        self.core.set_exposure(exposure)
        self.set_property(self.cam_name, self.trigger_mode_prop, self.scan_trigger_mode)

    def set_default_camera_properties(self, exposure):
        #Sets camera properties to default.
        self.studio.live().set_live_mode_on(False)
        self.set_property(self.cam_name, self.trigger_mode_prop, self.default_trigger_mode)
        self.core.set_exposure(exposure)

    def set_x_stage_speed(self, speed):
        #Sets x-stage speed
        self.set_property(self.x_stage_name, self.x_speed_property, speed)

    def set_zy_stage_speed(self, speed):
        #Sets zy-stage speed. Used to switch between z-stage speed when
        #moving to new position and the speed used during scans.
        self.set_property(self.zy_stage_name, self.z_speed_property, speed)

    def scan_setup(self, start_z, end_z):
        """
        SCAN is a module on the ASI stage. Please read the ASI manual for more details
        The '2' in all of the commands is the address of the Z Stage card as opposed to the
        XY Stage, which is '1'. An ASI stage scan is achieved by doing the following:

        1. Scan properties are set as "2 SCAN Y=0 Z=0 F=0". This is simply
           to tell the stage what axis will be scaning.
        2. Positions are set with SCANR X=[StartPosition] Y=[EndPosition]
           where positions are in units of mm. SCANR means raster scan.
        3. "2 SCAN" is sent. When the stage reaches the first position, the TTL 
           port goes high. This is what triggers the PLC to pulse. Once it reaches
           the end, TTL goes low and the stage resets to the start position.
        """
        start_z = np.round(start_z) / 1000.
        end_z = np.round(end_z) / 1000.
        scan_r_properties = "SCANR X=" + str(start_z) + " Y=" + str(end_z)
        self.set_property(self.zy_stage_name, self.serial, self.scan_properties)
        self.set_property(self.zy_stage_name, self.serial, scan_r_properties)

    def scan_start(self):
        #Start scan with properties set in scan_setup.
        self.set_property(self.zy_stage_name, self.serial, self.scan_start_command)
    
    def move_stage(self, x_position, y_position, z_position):
        self.set_zy_stage_speed(self.zy_stage_speed)
        self.set_x_stage_speed(self.x_stage_speed)
       
        #Reason for this is to ensure capillaries dpn't hit the objective. These conditions
        #should be changed to match the geometry of the holder.
        current_x_position = self.get_x_position()
        if current_x_position > x_position:
            self.core.set_xy_position(self.zy_stage_name, z_position, y_position)
            self.core.wait_for_device(self.zy_stage_name)
            self.core.set_position(self.x_stage_name, x_position)
            self.core.wait_for_device(self.x_stage_name)
        else:
            self.core.set_position(self.x_stage_name, x_position)
            self.core.wait_for_device(self.x_stage_name)
            self.core.set_xy_position(self.zy_stage_name, z_position, y_position)
            self.core.wait_for_device(self.zy_stage_name)

    def get_x_position(self):
        #Gets current x-position from xy-stage
        x_pos =  int(np.round(self.core.get_position(self.x_stage_name)))
        return x_pos

    def get_y_position(self):
        #Gets current y-position from xy-stage
        y_pos =  int(np.round(self.core.get_y_position(self.zy_stage_name)))
        return y_pos

    def get_z_position(self):
        #Gets current y-position from z-stage
        z_pos =  int(np.round(self.core.get_x_position(self.zy_stage_name)))
        return z_pos
    
    def reset_joystick(self):
        #The joystick tends to bug out after the SCAN command. This resets
        #the joystick so that it works correctly. See the ASI documentation 
        #for more details.
        self.set_property(self.zy_stage_name, self.serial, "J X+ Y+ Z+")
        self.core.wait_for_device(self.zy_stage_name)
        self.set_property(self.zy_stage_name, self.serial, "J X=4 Y=3 Z=2")
        self.core.wait_for_device(self.zy_stage_name)

    def reset_stage(self):
        self.set_property(self.zy_stage_name, self.serial, "RESET")
        self.core.wait_for_device(self.zy_stage_name)