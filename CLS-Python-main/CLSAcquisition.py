"""
Last Modified: 6/17/2022

Main acquisition script. This class takes all the data initialized using the CLSDialog window and performs
an image acquisition based on said data. It is created in a new thread so the user isn't locked 
out from GUI interaction during acquisition (this was more relevant as a java plugin for MM).

Future Changes:
- Some aspects of image acquisition could be made more consistent. I.e. the scan_buffer during z-stacks. 

- True stage positions included in Metadata. Currently every device property is in there. Not really sure
  how to do this because stage would need to be queried but the stage is always moving! Might be impossible.

- Possibly change all image acquisiiton to Pycro-Manager acquisition. Not really sure if this is worth the trouble.
"""

from random import sample
import numpy as np
import threading
import time
import os
from pycromanager import Studio, Core
from CLSAcquisitionParameters import AcquisitionSettings, RegionSettings
from HardwareCommands import MMHardwareCommands
import QtDesignerGUI


class Acquisition(threading.Thread):
    def __init__(self, studio: Studio, core: Core, acquisition_dialog: QtDesignerGUI.AcquisitionDialog,
                 acquisition_settings: AcquisitionSettings, mm_hardware_commands: MMHardwareCommands):
        super().__init__()
        self.studio = studio
        self.core = core
        self.acquisition_dialog = acquisition_dialog
        self.acquisition_settings = acquisition_settings
        self.mm_hardware_commands = mm_hardware_commands
        self.mm_hardware_commands.reset_joystick()
        self.region_settings_list = self.acquisition_settings.region_settings_list
        self.channel_order_list = self.acquisition_settings.channel_order_list
        self.abort_dialog = QtDesignerGUI.AbortDialog()
        self.acquisition_dialog.show()
        self.directory = self.initial_dir_check(self.acquisition_settings.directory)

        self.acquisition_dialog.abort_button.clicked.connect(self.abort_button_clicked)
        self.abort_dialog.abort_button.clicked.connect(self.abort_confirm_button_clicked)
        self.abort_dialog.cancel_button.clicked.connect(self.cancel_button_clicked)

    def initial_dir_check(self, directory: str):
        path = directory + "/Acquisition"
        i = 1
        if os.path.isdir(path):
            path += str(i)
        while os.path.isdir(path):
            path = path.strip(str(i))
            i += 1
            path += str(i)
        return path

    def snap_acquisition(self, sample_num, region_num, num_time_points, region_settings: RegionSettings):
        #Takes snap with channels set in region_settings. A snap is just a single image taken at the position
        #set in region_settings.
        for channel in self.channel_order_list:
            if channel in region_settings.snap_channel_list:
                self.acquisition_dialog.acquisition_label.setText("Initializing " + channel + " snap")
                self.core.set_config(self.acquisition_settings.channel_group_name, channel)
                self.mm_hardware_commands.set_default_camera_properties(region_settings.snap_exposure_time)

                path = self.directory + "/Sample" + str(sample_num + 1) + "/Pos" + str(
                    region_num + 1) + "/snap/" + channel + "/Timepoint" + str(num_time_points + 1)
                data = self.studio.data().create_single_plane_tiff_series_datastore(path)
                
                #Takes and saves snap with current channel
                self.acquisition_dialog.acquisition_label.setText("Acquiring " + channel + " snap")
                image = self.studio.live().snap(False).get(0)
                coords = image.get_coords().copy_builder().c(self.channel_order_list.index(channel)).build()
                meta_builder = image.get_metadata().copy_builder_preserving_uuid()
                meta_builder.x_position_um(region_settings.x_position)
                meta_builder.y_position_um(region_settings.y_position)
                meta_builder.z_position_um(region_settings.z_position)
                meta = meta_builder.build()
                image = image.copy_with(coords, meta)
                data.put_image(image)

                #Closes datastore. If datastore isn't closed, potential for memory leak.
                self.acquisition_dialog.acquisition_label.setText("Saving " + channel + " snap")
                data.close()
                self.core.clear_circular_buffer()
                self.last_sequence_scan_boolean = False

                if self.abort_boolean:
                    data.close()
                    return

    def video_acquisition(self, sample_num, region_num, num_time_points, region_settings: RegionSettings):
        #Takes video with properties specified in region_settings
        for channel in self.channel_order_list:
            if channel in region_settings.video_channel_list:
                self.acquisition_dialog.acquisition_label.setText("Initializing " + channel + " video")
                self.core.set_config(self.acquisition_settings.channel_group_name, channel)
                self.mm_hardware_commands.set_default_camera_properties(region_settings.video_exposure_time)
                framerate = round(1000/region_settings.video_exposure_time)


                path = self.directory + "/Sample" + str(sample_num + 1) + "/Pos" + str(
                    region_num + 1) + "/video/" + channel + "/Timepoint" + str(num_time_points + 1)
                data = self.studio.data().create_single_plane_tiff_series_datastore(path)

                #Number of images is just the framerate times the duration
                num_images = framerate * region_settings.video_duration
                cur_frame = 0
                timeout = 0
                #sequence boolean is just to change the acquisition window to 'saving' when
                #the camera sequence is over but there are still images to be saved from the buffer
                sequence_boolean = False

                self.acquisition_dialog.acquisition_label.setText("Acquiring " + channel + " video")
                #Pycromanager gave me errors when I just used an int or float for the second parameter,
                #but double works fine.
                self.core.start_sequence_acquisition(int(num_images), np.double(0), True)

                #This run loops until the camera is done taking images and there are no images
                #in the sequence buffer
                while self.core.get_remaining_image_count() > 0 or self.core.is_sequence_running():
                    if self.abort_boolean:
                        data.close()
                        return

                    #Timeout is so that if the camera gets stuck trying to take images, camera is interrupted
                    #and video acquisition is stopped
                    elif timeout > 500:
                        self.core.stop_sequence_acquisition()
                        self.core.clear_circular_buffer()
                        self.acquisition_dialog.acquisition_label.setText(
                            "Timepoint " + str(num_time_points + 1) + " " + channel + " video failed, camera timeout")
                        self.studio.logs().log_message(
                            "Timepoint " + str(num_time_points + 1) + " " + channel + " video failed, camera timeout")

                    #Saves image if there is one in the buffer
                    elif self.core.get_remaining_image_count() > 0:
                        tagged = self.core.pop_next_tagged_image()
                        image = self.studio.data().convert_tagged_image(tagged)
                        coords = image.get_coords().copy_builder().t(cur_frame).c(self.channel_order_list.index(channel)).build()
                        meta_builder = image.get_metadata().copy_builder_preserving_uuid()
                        meta_builder.x_position_um(region_settings.x_position)
                        meta_builder.y_position_um(region_settings.y_position)
                        meta_builder.z_position_um(region_settings.z_position)
                        meta = meta_builder.build()
                        image = image.copy_with(coords, meta)
                        data.put_image(image)
                        cur_frame += 1
                        timeout = 0

                        if not self.core.is_sequence_running() and not sequence_boolean:
                            self.acquisition_dialog.acquisition_label.setText("Saving " + channel + " video")
                            sequence_boolean = True

                    #Small pause if there isn't an image in the buffer
                    else:
                        self.core.sleep(5)
                        timeout += 1

                #Ensures end of sequence acquisition and closes data
                self.core.stop_sequence_acquisition()
                data.close()
                self.core.clear_circular_buffer()
                self.last_sequence_scan_boolean = False

                if self.abort_boolean:
                    data.close()
                    return


    def z_stack_acquisition(self, sample_num, region_num, num_time_points, region_settings: RegionSettings):
        #Set z_start and z_end positions of zstack and calculates number of images
        z_start = region_settings.z_start_position
        z_end = region_settings.z_end_position
        step_size = region_settings.step_size
        num_frames = int(np.round(np.abs(z_end - z_start) / step_size))

        # This buffer is so the stage overshoots a little bit to ensure enough images are captured
        # during the sequence acquisition to end naturally. This sucks, but I think it's necessary
        # with how the acquisition is currently performed.
        scan_buffer = 10
        if z_start <= z_end:
            z_start -= scan_buffer
            z_end += scan_buffer
        else:
            z_start += scan_buffer
            z_end -= scan_buffer
        self.mm_hardware_commands.move_stage(region_settings.x_position, region_settings.y_position, z_start)

        #Sets DLSM camera properties to match z_scan_speed
        self.mm_hardware_commands.set_dslm_camera_properties(self.acquisition_settings.z_scan_speed)

        #Initializes PLC to send pulses to DAQ, which then sends pulses to the camera
        self.mm_hardware_commands.set_plc_frame_interval(step_size, self.acquisition_settings.z_scan_speed)

        for channel in self.channel_order_list:
            if channel in region_settings.z_stack_channel_list:
                self.acquisition_dialog.acquisition_label.setText("Initializing " + channel + " z stack")
                path = self.directory + "/Sample" + str(sample_num + 1) + "/Pos" + str(
                    region_num + 1) + "/zStack/" + channel + "/Timepoint" + str(num_time_points + 1)
                data = self.studio.data().create_single_plane_tiff_series_datastore(path)

                sequence_boolean = False
                timeout = 0
                cur_frame = 0

                self.mm_hardware_commands.set_zy_stage_speed(self.acquisition_settings.z_scan_speed)
                self.mm_hardware_commands.scan_setup(z_start, z_end)

                self.acquisition_dialog.acquisition_label.setText("Acquiring " + channel + " z stack")
                self.core.set_config(self.acquisition_settings.channel_group_name, channel)
                self.core.start_sequence_acquisition(int(num_frames), np.double(0), False)
                self.core.wait_for_device(self.mm_hardware_commands.cam_name)

                #Sets correct scan stage speed and starts scan
                self.mm_hardware_commands.scan_start()

                while self.core.get_remaining_image_count() > 0 or self.core.is_sequence_running():
                    #Pretty much the same acquisition as the video acquisition.
                    while cur_frame < num_frames:
                        if self.abort_boolean:
                            data.close()
                            return

                        elif timeout >= 600:
                            error = "Sample " + str(sample_num + 1) + " Region " + str(region_num + 1) + " Timepoint " + str(
                            num_time_points + 1) + " " + channel + " z stack failed, not enough images acquired, missed " + str(num_frames - cur_frame) + " images"

                            print(error)
                            self.acquisition_dialog.acquisition_label.setText(error)
                            self.studio.logs().log_message(error)

                            self.mm_hardware_commands.initialize_plc_for_continuous_lsrm(20)
                            self.core.stop_sequence_acquisition()
                            self.core.clear_circular_buffer()
                            self.mm_hardware_commands.initialize_plc_for_scan(step_size, self.acquisition_settings.z_scan_speed)
                            break

                        elif self.core.get_remaining_image_count() > 0:
                            tagged = self.core.pop_next_tagged_image()
                            image = self.studio.data().convert_tagged_image(tagged)
                            coords = image.get_coords().copy_builder().z(cur_frame).c(self.channel_order_list.index(channel)).build()
                            meta_builder = image.get_metadata().copy_builder_preserving_uuid()
                            meta_builder.x_position_um(region_settings.x_position)
                            meta_builder.y_position_um(region_settings.y_position)
                            #Since stage is running the scan command, the stage cannot be queried for its
                            #position, so instead, we just add the stepsize for each frame, which should be
                            #roughly correct. A better way to do this would be great!
                            if z_start <= z_end:
                                meta_builder.z_position_um(z_start + step_size * cur_frame)
                            else:
                                meta_builder.z_position_um(z_start - step_size * cur_frame)
                            meta = meta_builder.build()
                            image = image.copy_with(coords, meta)
                            data.put_image(image)
                            cur_frame += 1
                            timeout = 0

                            if not self.core.is_sequence_running() and not sequence_boolean:
                                self.acquisition_dialog.acquisition_label.setText("Saving " + channel + " z stack")
                                sequence_boolean = True

                        else:
                            self.core.sleep(5)
                            timeout += 1

                    self.core.stop_sequence_acquisition()
                    self.core.clear_circular_buffer()
                    data.close()
                    
                #Waits until stage and camera aren't busy before continuing.
                self.core.wait_for_device(self.mm_hardware_commands.cam_name)
                self.core.wait_for_device(self.mm_hardware_commands.zy_stage_name)
                self.core.wait_for_device(self.mm_hardware_commands.x_stage_name)
                self.mm_hardware_commands.reset_joystick()

                if self.abort_boolean:
                    data.close()
                    return

    def abort_button_clicked(self):
        self.abort_dialog.show()
        self.abort_dialog.activateWindow()

    def abort_confirm_button_clicked(self):
        self.abort_boolean = True
        self.abort_dialog.close()

    def cancel_button_clicked(self):
        self.abort_dialog.close()

    def abort_acquisition(self):
        #Aborts acquisition entirely. 
        self.acquisition_dialog.acquisition_label.setText("Aborting...")
        self.core.stop_sequence_acquisition()
        self.core.clear_circular_buffer()
        self.mm_hardware_commands.set_default_camera_properties(self.mm_hardware_commands.default_exposure)
        self.mm_hardware_commands.reset_joystick()
        self.acquisition_dialog.acquisition_label.setText("Aborted")

    def run(self):
        self.abort_boolean = False
        self.core.stop_sequence_acquisition()
        self.core.clear_circular_buffer()
        self.core.set_shutter_open(False)
        self.core.set_auto_shutter(True)
        self.mm_hardware_commands.initialize_plc_for_scan(self.region_settings_list[0][0].step_size, self.acquisition_settings.z_scan_speed)

        self.acquisition_dialog.acquisition_label.setText("Moving to start position...")
        x_pos = self.region_settings_list[0][0].x_position
        y_pos = self.region_settings_list[0][0].y_position
        z_pos = self.region_settings_list[0][0].z_position
        self.mm_hardware_commands.move_stage(x_pos, y_pos, z_pos)

        settings_num_time_points = 1
        if self.acquisition_settings.time_points_boolean == True and self.acquisition_settings.num_time_points != 0:
            settings_num_time_points = self.acquisition_settings.num_time_points

        if not self.acquisition_settings.sequential_time_series_boolean:
            for num_time_points in range(settings_num_time_points):
                start = time.time_ns()
                self.acquisition_dialog.time_point_label.setText("Time point " + str(num_time_points + 1))
                self.acquisition_dialog.acquisition_label.setText("Initializing Acquisition")

                if self.abort_boolean:
                    self.abort_acquisition()
                    return

                for sample_num in range(self.acquisition_settings.sample_dimension):
                    if self.region_settings_list[sample_num][0] == 0:
                        break
                    for region_num in range(self.acquisition_settings.region_dimension):
                        region_settings = self.acquisition_settings.region_settings_list[sample_num][region_num]
                        if region_settings == 0:
                            break
                        else:
                            if sample_num != region_num != 0:
                                self.acquisition_dialog.acquisition_label.setText("Moving to region...")
                                x_pos = region_settings.x_position
                                y_pos = region_settings.y_position
                                z_pos = region_settings.z_position
                                self.mm_hardware_commands.move_stage(x_pos, y_pos, z_pos)

                            self.acquisition_dialog.sample_label.setText("Sample " + str(sample_num + 1))
                            self.acquisition_dialog.region_label.setText("Region " + str(region_num + 1))

                            if region_settings.snap_boolean:
                                self.snap_acquisition(sample_num, region_num, num_time_points, region_settings)
                                if self.abort_boolean:
                                    self.abort_acquisition()
                                    return

                            if region_settings.video_boolean:
                                self.video_acquisition(sample_num, region_num, num_time_points, region_settings)
                                if self.abort_boolean:
                                    self.abort_acquisition()
                                    return

                            if region_settings.z_stack_boolean:
                                self.z_stack_acquisition(sample_num, region_num, num_time_points, region_settings)
                                if self.abort_boolean:
                                    self.abort_acquisition()
                                    return

                if self.abort_boolean:
                    self.abort_acquisition()
                    return

                time_points_left = self.acquisition_settings.num_time_points - num_time_points
                if self.acquisition_settings.time_points_boolean and time_points_left > 1:

                    self.acquisition_dialog.acquisition_label.setText("Moving back to start position...")
                    x_pos = self.region_settings_list[0][0].x_position
                    y_pos = self.region_settings_list[0][0].y_position
                    z_pos = self.region_settings_list[0][0].z_position
                    self.mm_hardware_commands.move_stage(x_pos, y_pos, z_pos)

                    #Time is started and ended when the stage reaches the first region position
                    #for time consistency.
                    end = time.time_ns()
                    duration_ms = np.round((end - start) / 10**6)
                    delay = self.acquisition_settings.time_points_interval * 60 * 1000

                    while delay - duration_ms > 0:
                        end = time.time_ns()
                        duration_ms = np.round((end - start) / np.power(10, 6))

                        #Displays number of minutes/seconds left until next time point
                        time_left_seconds = int(np.round((delay - duration_ms) / 1000))
                        num_minutes_left = int(np.floor(time_left_seconds / 60))
                        num_seconds_left = int(time_left_seconds % 60)
                        if num_minutes_left != 0:
                            self.acquisition_dialog.acquisition_label.setText(
                                "next time point: " + str(num_minutes_left) + " minutes " + str(
                                    num_seconds_left) + " seconds")
                        else:
                            self.acquisition_dialog.acquisition_label.setText(
                                "next time point: " + str(num_seconds_left) + " seconds")

                        if self.abort_boolean:
                            self.abort_acquisition()
                            return
        else:
            for sample_num in range(self.acquisition_settings.sample_dimension):
                if sample_num != 0 and self.region_settings_list[sample_num][0] != 0:
                    self.acquisition_dialog.acquisition_label.setText("Moving to region...")
                    x_pos = self.region_settings_list[sample_num][0].x_position
                    y_pos = self.region_settings_list[sample_num][0].y_position
                    z_pos = self.region_settings_list[sample_num][0].z_position
                    self.mm_hardware_commands.move_stage(x_pos, y_pos, z_pos)

                if self.abort_boolean:
                    self.abort_acquisition()
                    return

                if self.region_settings_list[sample_num][0] != 0:
                    for num_time_points in range(settings_num_time_points):
                        start = time.time_ns()
                        self.acquisition_dialog.time_point_label.setText("Time point " + str(num_time_points + 1))
                        self.acquisition_dialog.acquisition_label.setText("Initializing Acquisition")
                        for region_num in range(self.acquisition_settings.region_dimension):
                            region_settings = self.acquisition_settings.region_settings_list[sample_num][region_num]
                            if region_settings == 0:
                                break
                            else:
                                if region_num != 0:
                                    self.acquisition_dialog.acquisition_label.setText("Moving to region...")
                                    x_pos = region_settings.x_position
                                    y_pos = region_settings.y_position
                                    z_pos = region_settings.z_position
                                    self.mm_hardware_commands.move_stage(x_pos, y_pos, z_pos)

                                self.acquisition_dialog.sample_label.setText("Sample " + str(sample_num + 1))
                                self.acquisition_dialog.region_label.setText("Region " + str(region_num + 1))


                                if region_settings.snap_boolean:
                                    self.snap_acquisition(sample_num, region_num, num_time_points, region_settings)
                                    if self.abort_boolean:
                                        self.abort_acquisition()
                                        return

                                if region_settings.video_boolean:
                                    self.video_acquisition(sample_num, region_num, num_time_points, region_settings)
                                    if self.abort_boolean:
                                        self.abort_acquisition()
                                        return

                                if region_settings.z_stack_boolean:
                                    self.z_stack_acquisition(sample_num, region_num, num_time_points, region_settings)
                                    if self.abort_boolean:
                                        self.abort_acquisition()
                                        return

                        time_points_left = self.acquisition_settings.num_time_points - num_time_points
                        if self.acquisition_settings.time_points_boolean and time_points_left > 1:
                            self.acquisition_dialog.acquisition_label.setText("Moving back to start position...")
                            
                            x_pos = self.region_settings_list[sample_num][0].x_position
                            y_pos = self.region_settings_list[sample_num][0].y_position
                            z_pos = self.region_settings_list[sample_num][0].z_position
                            self.mm_hardware_commands.move_stage(x_pos, y_pos, z_pos)

                            #Time is started and ended when the stage reaches the first region position
                            #for time consistency.
                            duration_ms = np.round((time.time_ns() - start) / 10**6)
                            delay = self.acquisition_settings.time_points_interval * 60 * 1000

                            while delay - duration_ms > 0:
                                duration_ms = np.round((time.time_ns() - start) / 10**6)

                                #Displays number of minutes/seconds left until next time point
                                time_left_seconds = int(np.round((delay - duration_ms) / 1000))
                                num_minutes_left = int(np.floor(time_left_seconds / 60))
                                num_seconds_left = int(time_left_seconds % 60)
                                if num_minutes_left != 0:
                                    self.acquisition_dialog.acquisition_label.setText(
                                        "next time point: " + str(num_minutes_left) + " minutes " + str(
                                            num_seconds_left) + " seconds")
                                else:
                                    self.acquisition_dialog.acquisition_label.setText(
                                        "next time point: " + str(num_seconds_left) + " seconds")

                                if self.abort_boolean:
                                    self.abort_acquisition()
                                    return

                else:
                    self.acquisition_dialog.acquisition_label.setText("Moving back to start position...")
                    x_pos = self.region_settings_list[0][0].x_position
                    y_pos = self.region_settings_list[0][0].y_position
                    z_pos = self.region_settings_list[0][0].z_position
                    self.mm_hardware_commands.move_stage(x_pos, y_pos, z_pos)
                    break

        self.mm_hardware_commands.set_default_camera_properties(self.mm_hardware_commands.default_exposure)
        self.mm_hardware_commands.reset_joystick()

        self.acquisition_dialog.acquisition_label.setText("Your acquisition was successful!")
