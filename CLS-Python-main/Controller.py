"""
Last Modified: 6/17/2022

This file contains all the controller classes. There are three, one for each of the main GUI elements.

Classes:

MainController - Creates instances of controllers and hardware command classes to allow the same instances to be passed to one another.

CLSController - The main controller for CLS acquisitions. Creates an instance of AcquisitionSettings
                from CLSAcquisitionParameters to set up a CLS experiment. Most of the logic goes into
                creating the region_settings_list in acquisition_settings. A pseudo pointer object named
                region_settings is created in the controller to correctly track and update list elements.


Future Changes:
- As always, some logic could probably be made more clear.

- Not sure how to deal with new instances of region_settings when needed. When a
new instance of region_settings is created, should the GUI be the initial values?
Not sure what is best.

- All classes (other than RegionSettings) should probably be made into singletons, since we only want one instance of each.
Probably not a big deal either way.

- Error handling could be much better.
"""

import numpy as np
from pathlib import Path
import configparser
import os
import copy
from pycromanager import Studio, Core
from PyQt5 import QtCore, QtGui, QtWidgets
import QtDesignerGUI
from CLSAcquisitionParameters import RegionSettings, AcquisitionSettings
import HardwareCommands
from CLSAcquisition import Acquisition


class MainController(object):
    acquisition_settings_section = 'Acquisition Settings'
    config_file_name = 'CLSConfig.cfg'
    config = configparser.RawConfigParser()

    def __init__(self, studio: Studio, core: Core):
        self.main_window = QtDesignerGUI.MainWindow()
        MainController.config = MainController.initialize_config()

        self.studio = studio
        self.core = core

        self.mm_hardware_commands = HardwareCommands.MMHardwareCommands(self.studio, self.core)
        self.cls_controller = CLSController(self.studio, self.core, self.mm_hardware_commands)

        #initialize main window and event handlers. This flag is set to disable the
        #buttons on the top right of the window.
        self.main_window.setWindowFlags(QtCore.Qt.WindowTitleHint)
        self.main_window.cls_button.clicked.connect(self.cls_button_clicked)
        self.main_window.exit_button.clicked.connect(self.exit_button_clicked)

    def cls_button_clicked(self):
        self.cls_controller.cls_dialog.show()
        self.cls_controller.cls_dialog.activateWindow()

    def exit_button_clicked(self):
        quit()
    
    def initialize_config():
        config = configparser.RawConfigParser()
        if os.path.exists(MainController.config_file_name):
            config.read(MainController.config_file_name)

        return config

class CLSController(object):
    """Future Changes:
    - As always, some logic could probably be made more clear.
    - Not sure how to deal with new instances of region_settings when needed. When a
      new instance of region_settings is created, should the GUI update to initial values?
      Not sure what is best.
    - There's gotta be a better way to validate user entries. Finding a nice way to do this (potentially with
      an entirely different class) would make the program much cleaner/clearer.
    - In general, write_to_config() is called when set_table() is called and both iterate through region_list
      separately. Could combine them so it only iterates through once.
    """

    def __init__(self, studio: Studio, core: Core, mm_hardware_commands: HardwareCommands.MMHardwareCommands):
        self.studio = studio
        self.core = core
        self.mm_hardware_commands = mm_hardware_commands
        self.cls_dialog = QtDesignerGUI.CLSDialog()
        self.reset_stage_dialog = QtDesignerGUI.ResetStageDialog()
        self.acquisition_settings_dialog = QtDesignerGUI.CLSAcquisitionSettingsDialog()
        self.acquisition_dialog = QtDesignerGUI.AcquisitionDialog()
        self.acquisition_settings = AcquisitionSettings()
        self.region_settings = RegionSettings()
        self.region_settings_copy = copy.deepcopy(self.region_settings)
        self.start_path = 'G:'
        self.num_images_per = 0

        self.sample_num = 0
        self.region_num = 0

        self.cls_dialog.sample_label.setText("Sample " + str(self.sample_num + 1))
        self.cls_dialog.region_label.setText("Region " + str(self.region_num + 1))

        # initialize item models
        self.cls_dialog.region_table_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.region_table_model = QtGui.QStandardItemModel()
        self.cls_dialog.region_table_view.setModel(self.region_table_model)
        self.z_stack_available_model = QtGui.QStandardItemModel()
        self.cls_dialog.z_stack_available_list_view.setModel(self.z_stack_available_model)
        self.z_stack_used_model = QtGui.QStandardItemModel()
        self.cls_dialog.z_stack_used_list_view.setModel(self.z_stack_used_model)
        self.snap_available_model = QtGui.QStandardItemModel()
        self.cls_dialog.snap_available_list_view.setModel(self.snap_available_model)
        self.snap_used_model = QtGui.QStandardItemModel()
        self.cls_dialog.snap_used_list_view.setModel(self.snap_used_model)
        self.video_available_model = QtGui.QStandardItemModel()
        self.cls_dialog.video_available_list_view.setModel(self.video_available_model)
        self.video_used_model = QtGui.QStandardItemModel()
        self.cls_dialog.video_used_list_view.setModel(self.video_used_model)
        self.channel_order_model = QtGui.QStandardItemModel()
        self.acquisition_settings_dialog.channel_order_list_view.setModel(self.channel_order_model)

        headers = ["sample #", "reg #", "x", "y", "z", "z stack", "start",
                   "end", "step", "chans", "snap", "exp", "chans", "video",
                   "dur", "exp", "chans", "# images"]
        self.region_table_model.setHorizontalHeaderLabels(headers)
        self.cls_dialog.region_table_view.resizeColumnsToContents()

        core_channel_vector = self.core.get_available_configs(self.acquisition_settings.channel_group_name)
        self.core_channel_list = []
        for i in range(core_channel_vector.size()):
            channel = core_channel_vector.get(i)
            self.core_channel_list.append(channel)

        self.acquisition_settings.channel_order_list = copy.deepcopy(self.core_channel_list)

        for channel in self.core_channel_list:
            item = QtGui.QStandardItem(channel)
            self.z_stack_available_model.appendRow(QtGui.QStandardItem(item))
            self.snap_available_model.appendRow(QtGui.QStandardItem(item))
            self.video_available_model.appendRow(QtGui.QStandardItem(item))
            self.channel_order_model.appendRow(QtGui.QStandardItem(item))

        # initialize cls_dialog line edit event handlers and validators
        self.cls_dialog.x_line_edit.textEdited.connect(self.x_line_edit_event)
        self.cls_dialog.x_line_edit.setValidator(QtGui.QIntValidator())

        self.cls_dialog.y_line_edit.textEdited.connect(self.y_line_edit_event)
        self.cls_dialog.y_line_edit.setValidator(QtGui.QIntValidator())

        self.cls_dialog.z_line_edit.textEdited.connect(self.z_line_edit_event)
        self.cls_dialog.z_line_edit.setValidator(QtGui.QIntValidator())

        self.cls_dialog.start_z_line_edit.textEdited.connect(self.start_z_line_edit_event)
        self.cls_dialog.start_z_line_edit.setValidator(QtGui.QIntValidator())

        self.cls_dialog.end_z_line_edit.textEdited.connect(self.end_z_line_edit_event)
        self.cls_dialog.end_z_line_edit.setValidator(QtGui.QIntValidator())

        self.cls_dialog.step_size_line_edit.textEdited.connect(self.step_size_line_edit_event)
        validator = QtGui.QIntValidator()
        validator.setBottom(0)
        self.cls_dialog.step_size_line_edit.setValidator(validator)

        self.cls_dialog.snap_exposure_line_edit.textEdited.connect(self.snap_exposure_line_edit_event)
        validator = QtGui.QIntValidator()
        validator.setBottom(10)
        self.cls_dialog.snap_exposure_line_edit.setValidator(validator)

        self.cls_dialog.video_duration_line_edit.textEdited.connect(self.video_duration_line_edit_event)
        validator = QtGui.QIntValidator()
        validator.setBottom(1)
        self.cls_dialog.video_duration_line_edit.setValidator(validator)

        self.cls_dialog.video_exposure_line_edit.textEdited.connect(self.video_exposure_line_edit_event)
        validator = QtGui.QIntValidator()
        validator.setBottom(10)
        self.cls_dialog.video_exposure_line_edit.setValidator(validator)

        self.cls_dialog.go_to_button.clicked.connect(self.go_to_button_clicked)
        self.cls_dialog.set_region_button.clicked.connect(self.set_region_button_clicked)
        self.cls_dialog.next_region_button.clicked.connect(self.next_region_button_clicked)
        self.cls_dialog.previous_region_button.clicked.connect(self.previous_region_button_clicked)
        self.cls_dialog.next_sample_button.clicked.connect(self.next_sample_button_clicked)
        self.cls_dialog.previous_sample_button.clicked.connect(self.previous_sample_button_clicked)
        self.cls_dialog.remove_region_button.clicked.connect(self.remove_region_button_clicked)
        self.cls_dialog.copy_region_button.clicked.connect(self.copy_button_clicked)
        self.cls_dialog.paste_region_button.clicked.connect(self.paste_button_clicked)
        self.cls_dialog.set_z_start_button.clicked.connect(self.set_z_start_button_clicked)
        self.cls_dialog.set_z_end_button.clicked.connect(self.set_z_end_button_clicked)
        self.cls_dialog.acquisition_setup_button.clicked.connect(self.acquisition_setup_button_clicked)
        self.cls_dialog.reset_stage_button.clicked.connect(self.reset_stage_button_clicked)
        self.cls_dialog.reset_joystick_button.clicked.connect(self.reset_joystick_button_clicked)
        self.cls_dialog.z_stack_check_box.clicked.connect(self.z_stack_check_clicked)
        self.cls_dialog.snap_check_box.clicked.connect(self.snap_check_clicked)
        self.cls_dialog.video_check_box.clicked.connect(self.video_check_clicked)
        self.cls_dialog.z_stack_available_list_view.doubleClicked.connect(self.z_stack_available_list_move)
        self.cls_dialog.z_stack_used_list_view.doubleClicked.connect(self.z_stack_used_list_move)
        self.cls_dialog.snap_available_list_view.doubleClicked.connect(self.snap_available_list_move)
        self.cls_dialog.snap_used_list_view.doubleClicked.connect(self.snap_used_list_move)
        self.cls_dialog.video_available_list_view.doubleClicked.connect(self.video_available_list_move)
        self.cls_dialog.video_used_list_view.doubleClicked.connect(self.video_used_list_move)

        # initialize clsAcquisitionSettingsDialog line edits event handlers and validators
        self.acquisition_settings_dialog.num_time_points_line_edit.textEdited.connect(
            self.num_time_points_line_edit_event)
        self.acquisition_settings_dialog.num_time_points_line_edit.setValidator(QtGui.QIntValidator().setBottom(0))
        self.acquisition_settings_dialog.time_points_interval_line_edit.textEdited.connect(
            self.time_points_interval_line_edit_event)
        self.acquisition_settings_dialog.time_points_interval_line_edit.setValidator(QtGui.QIntValidator().setBottom(0))
        self.acquisition_settings_dialog.browse_button.clicked.connect(self.browse_button_clicked)
        self.acquisition_settings_dialog.channel_order_move_up_button.clicked.connect(
            self.channel_move_up_button_clicked)
        self.acquisition_settings_dialog.channel_order_move_down_button.clicked.connect(
            self.channel_move_down_button_clicked)
        self.acquisition_settings_dialog.start_acquisition_button.clicked.connect(self.start_acquisition_button_clicked)
        self.acquisition_settings_dialog.time_points_check_box.clicked.connect(self.time_points_check_clicked)
        self.acquisition_settings_dialog.sequential_check_box.clicked.connect(self.sequential_check_clicked)
        self.acquisition_settings_dialog.lsrm_check_box.clicked.connect(self.lsrm_check_clicked)
        self.acquisition_settings_dialog.stage_speed_combo_box.activated.connect(self.stage_speed_combo_box_clicked)

        #Initialize ResetStageDialog event handlers
        self.reset_stage_dialog.yes_button.clicked.connect(self.reset_stage_yes_button_clicked)
        self.reset_stage_dialog.cancel_button.clicked.connect(self.reset_stage_cancel_button_clicked)

        self.initialize_from_config()

    #Writes settings to config file
    def write_to_config(self):
        config = MainController.config

        section = 'COMMENTS'
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, 'COMMENTS', 'PLEASE DO NOT EDIT UNLESS YOU KNOW WHAT YOU ARE DOING')

        section = MainController.acquisition_settings_section
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, 'time_bool', str(self.acquisition_settings.time_points_boolean))
        config.set(section, 'time_int', str(self.acquisition_settings.time_points_interval))
        config.set(section, 'num_time', str(self.acquisition_settings.num_time_points))
        config.set(section, 'scan_speed', str(self.acquisition_settings.z_scan_speed))
        config.set(section, 'lsrm_bool', str(self.acquisition_settings.lightsheet_mode_boolean))
        config.set(section, 'sequential_bool', str(self.acquisition_settings.sequential_time_series_boolean))

        
        for sample_index in range(self.acquisition_settings.sample_dimension):
            for region_index in range(self.acquisition_settings.region_dimension):
                section = 'Sample ' + str(sample_index) + ' Region ' + str(region_index)
                if config.has_section(section):
                    config.remove_section(section)
                region = self.acquisition_settings.region_settings_list[sample_index][region_index]
                if region != 0:
                    section = 'Sample ' + str(sample_index) + ' Region ' + str(region_index)
                    config.add_section(section)
                    config.set(section, 'x_pos', str(region.x_position))
                    config.set(section, 'y_pos', str(region.y_position))
                    config.set(section, 'z_pos', str(region.z_position))
                    config.set(section, 'z_bool', str(region.z_stack_boolean))
                    config.set(section, 'z_start', str(region.z_start_position))
                    config.set(section, 'z_end', str(region.z_end_position))
                    config.set(section, 'step', str(region.step_size))
                    config.set(section, 'z_stack_channels', ",".join(region.z_stack_channel_list))
                    config.set(section, 'snap_bool', str(region.snap_boolean))
                    config.set(section, 'snap_exp', str(region.snap_exposure_time))
                    config.set(section, 'snap_channels', ",".join(region.snap_channel_list))
                    config.set(section, 'video_bool', str(region.video_boolean))
                    config.set(section, 'video_dur', str(region.video_duration))
                    config.set(section, 'video_exp', str(region.video_exposure_time))
                    config.set(section, 'video_channels', ",".join(region.video_channel_list))

        with open(MainController.config_file_name, 'w') as configfile:
            config.write(configfile)
    
    #Reads values from config file and initializes GUI based on it
    def initialize_from_config(self):
        config = MainController.config
        section = MainController.acquisition_settings_section

        #Gets values from config
        if config.has_section(section):
            try:
                self.acquisition_settings.time_points_boolean = config.getboolean(section, 'time_bool')
                self.acquisition_settings.time_points_interval = config.getint(section, 'time_int')
                self.acquisition_settings.num_time_points = config.getint(section, 'num_time')
                self.acquisition_settings.z_scan_speed = config.getfloat(section, 'scan_speed')
                self.acquisition_settings.lightsheet_mode_boolean = config.getboolean(section, 'lsrm_bool')
                self.acquisition_settings.sequential_time_series_boolean = config.getboolean(section, 'sequential_bool')
            except:
                print('section line missing')
        
        #Sets acquisition settings dialog states
        self.acquisition_settings_dialog.time_points_check_box.setChecked(self.acquisition_settings.time_points_boolean)
        self.acquisition_settings_dialog.num_time_points_line_edit.setEnabled(self.acquisition_settings.time_points_boolean)
        self.acquisition_settings_dialog.num_time_points_line_edit.setText(str(self.acquisition_settings.num_time_points))
        self.acquisition_settings_dialog.time_points_interval_line_edit.setEnabled(self.acquisition_settings.time_points_boolean)
        self.acquisition_settings_dialog.time_points_interval_line_edit.setText(str(self.acquisition_settings.time_points_interval))
        self.acquisition_settings_dialog.sequential_check_box.setChecked(self.acquisition_settings.sequential_time_series_boolean)
        self.acquisition_settings_dialog.start_acquisition_button.setEnabled(False)
        self.acquisition_settings_dialog.num_images_per_line_edit.setEnabled(False)
        self.acquisition_settings_dialog.total_images_line_edit.setEnabled(False)
        self.acquisition_settings_dialog.memory_line_edit.setEnabled(False)
        self.acquisition_settings_dialog.lsrm_check_box.setChecked(self.acquisition_settings.lightsheet_mode_boolean)
        if self.acquisition_settings.z_scan_speed == 0.015:
            self.acquisition_settings_dialog.stage_speed_combo_box.setCurrentText('15 um/s')
        if self.acquisition_settings.z_scan_speed == 0.030:
            self.acquisition_settings_dialog.stage_speed_combo_box.setCurrentText('30 um/s')

        #initializes regions from config file
        for sample_index in range(self.acquisition_settings.sample_dimension):
            for region_index in range(self.acquisition_settings.region_dimension):
                section = 'Sample ' + str(sample_index) + ' Region ' + str(region_index)
                if config.has_section(section):
                    try:
                        region = RegionSettings()
                        region.x_position = config.getint(section, 'x_pos')
                        region.y_position = config.getint(section, 'y_pos')
                        region.z_position = config.getint(section, 'z_pos')
                        region.z_stack_boolean = config.getboolean(section, 'z_bool')
                        region.z_start_position = config.getint(section, 'z_start')
                        region.z_end_position = config.getint(section, 'z_end')
                        region.step_size = config.getint(section, 'step')
                        region.z_stack_channel_list = config.get(section, 'z_stack_channels').split(',')
                        region.snap_boolean = config.getboolean(section, 'snap_bool')
                        region.snap_exposure_time = config.getint(section, 'snap_exp')
                        region.snap_channel_list = config.get(section, 'snap_channels').split(',')
                        region.video_boolean = config.getboolean(section, 'video_bool')
                        region.video_duration = config.getint(section, 'video_dur')
                        region.video_exposure_time = config.getint(section, 'video_exp')
                        region.video_channel_list = config.get(section, 'video_channels').split(',')
                        self.acquisition_settings.region_settings_list[sample_index][region_index] = region

                        if sample_index == region_index == 0:
                            self.region_settings = region
                        print('Region read at sample index ' + str(sample_index) + ', region index ' + str(region_index))
                    except:
                        'section line missing'

        #Initialize gui elements baseed on regions
        initial_bool = self.acquisition_settings.region_settings_list[0][0] != 0
        self.cls_dialog.go_to_button.setEnabled(initial_bool)
        self.cls_dialog.remove_region_button.setEnabled(initial_bool)
        self.cls_dialog.next_region_button.setEnabled(initial_bool)
        self.cls_dialog.next_sample_button.setEnabled(initial_bool)
        self.cls_dialog.previous_sample_button.setEnabled(False)
        self.cls_dialog.previous_region_button.setEnabled(False)

        self.set_table()
        self.update_cls_dialog()

    def update_cls_dialog(self):
        #Updates all the GUI elements (apart from the table) to reflect the
        #values in the current region_settings instance.

        self.cls_dialog.sample_label.setText("Sample " + str(self.sample_num + 1))
        self.cls_dialog.region_label.setText("Region " + str(self.region_num + 1))

        self.cls_dialog.x_line_edit.setText(str(self.region_settings.x_position))
        self.cls_dialog.y_line_edit.setText(str(self.region_settings.y_position))
        self.cls_dialog.z_line_edit.setText(str(self.region_settings.z_position))

        z_stack_boolean = self.region_settings.z_stack_boolean
        self.cls_dialog.z_stack_check_box.setChecked(z_stack_boolean)
        self.cls_dialog.set_z_start_button.setEnabled(z_stack_boolean)
        self.cls_dialog.set_z_end_button.setEnabled(z_stack_boolean)
        self.cls_dialog.start_z_line_edit.setEnabled(z_stack_boolean)
        self.cls_dialog.end_z_line_edit.setEnabled(z_stack_boolean)
        self.cls_dialog.step_size_line_edit.setEnabled(z_stack_boolean)
        self.cls_dialog.z_stack_available_list_view.setEnabled(z_stack_boolean)
        self.cls_dialog.z_stack_used_list_view.setEnabled(z_stack_boolean)

        snap_boolean = self.region_settings.snap_boolean
        self.cls_dialog.snap_check_box.setChecked(snap_boolean)
        self.cls_dialog.snap_exposure_line_edit.setEnabled(snap_boolean)
        self.cls_dialog.snap_available_list_view.setEnabled(snap_boolean)
        self.cls_dialog.snap_used_list_view.setEnabled(snap_boolean)

        video_boolean = self.region_settings.video_boolean
        self.cls_dialog.video_check_box.setChecked(video_boolean)
        self.cls_dialog.video_duration_line_edit.setEnabled(video_boolean)
        self.cls_dialog.video_exposure_line_edit.setEnabled(video_boolean)
        self.cls_dialog.video_available_list_view.setEnabled(video_boolean)
        self.cls_dialog.video_used_list_view.setEnabled(video_boolean)

        self.cls_dialog.start_z_line_edit.setText(str(self.region_settings.z_start_position))
        self.cls_dialog.end_z_line_edit.setText(str(self.region_settings.z_end_position))
        self.cls_dialog.step_size_line_edit.setText(str(self.region_settings.step_size))

        self.cls_dialog.snap_exposure_line_edit.setText(str(self.region_settings.snap_exposure_time))

        self.cls_dialog.video_duration_line_edit.setText(str(self.region_settings.video_duration))
        self.cls_dialog.video_exposure_line_edit.setText(str(self.region_settings.video_exposure_time))

        #Sets the model list to reflect channel list in current region_settings instance
        self.z_stack_used_model.clear()
        for channel in self.region_settings.z_stack_channel_list:
            item = QtGui.QStandardItem(channel)
            self.z_stack_used_model.appendRow(item)

        self.z_stack_available_model.clear()
        for element in self.core_channel_list:
            for channel in self.region_settings.z_stack_channel_list:
                if element == channel:
                    break
            else:
                item = QtGui.QStandardItem(element)
                self.z_stack_available_model.appendRow(item)

        self.snap_used_model.clear()
        for channel in self.region_settings.snap_channel_list:
            item = QtGui.QStandardItem(channel)
            self.snap_used_model.appendRow(item)

        self.snap_available_model.clear()
        for element in self.core_channel_list:
            for channel in self.region_settings.snap_channel_list:
                if element == channel:
                    break
            else:
                item = QtGui.QStandardItem(element)
                self.snap_available_model.appendRow(item)

        self.video_used_model.clear()
        for channel in self.region_settings.video_channel_list:
            item = QtGui.QStandardItem(channel)
            self.video_used_model.appendRow(item)

        self.video_available_model.clear()
        for element in self.core_channel_list:
            for channel in self.region_settings.video_channel_list:
                if element == channel:
                    break
            else:
                item = QtGui.QStandardItem(element)
                self.video_available_model.appendRow(item)

    def set_table(self):
        self.num_images_per = 0
        self.region_table_model.clear()
        headers = ["sample #", "reg #", "x", "y", "z", "z stack", "start",
                   "end", "step", "chans", "snap", "exp", "chans", "video",
                   "dur", "exp", "chans", "# images"]
        self.region_table_model.setHorizontalHeaderLabels(headers)

        #Iterates through region_settings_list. If region is initialized, puts
        #region into the table.
        for sample_index in range(self.acquisition_settings.sample_dimension):
            for region_index in range(self.acquisition_settings.region_dimension):
                region = self.acquisition_settings.region_settings_list[sample_index][region_index]
                if region != 0:
                    num_z_stack_images = 0
                    num_snap_images = 0
                    num_video_images = 0
                    if region.z_stack_boolean:
                        num_z_stack_images = len(region.z_stack_channel_list) * int(
                            np.abs(float(region.z_start_position - region.z_end_position)) / region.step_size)
                    if region.snap_boolean:
                        num_snap_images = len(region.snap_channel_list)
                    if region.video_boolean:
                        num_video_images = len(region.video_channel_list) * int(
                            np.round(1000 / region.video_exposure_time * region.video_duration))
                    total_images = num_z_stack_images + num_video_images + num_snap_images

                    row_list = [str(sample_index + 1),
                                str(region_index + 1),
                                str(region.x_position),
                                str(region.y_position),
                                str(region.z_position),
                                str(region.z_stack_boolean),
                                str(region.z_start_position),
                                str(region.z_end_position),
                                str(region.step_size),
                                ','.join(region.z_stack_channel_list),
                                str(region.snap_boolean),
                                str(self.region_settings.snap_exposure_time),
                                ','.join(region.snap_channel_list),
                                str(region.video_boolean),
                                str(region.video_duration),
                                str(region.video_exposure_time),
                                ','.join(region.video_channel_list),
                                str(total_images)]

                    self.num_images_per += total_images
                    row_list = [QtGui.QStandardItem(element) for element in row_list]
                    self.region_table_model.appendRow(row_list)

        self.acquisition_settings_dialog.num_images_per_line_edit.setText(str(self.num_images_per))
        self.calculate_num_images()
        self.cls_dialog.region_table_view.resizeColumnsToContents()

    def calculate_num_images(self):
        #Calculates number of images in acquisition for use in acquisition settings dialog
        
        #This image size is estimated based on tif file size saved by micromanager. May not
        #be completely accurate
        image_size = 10.84
        if self.acquisition_settings.time_points_boolean:
            total_images = self.num_images_per * self.acquisition_settings.num_time_points
            self.acquisition_settings_dialog.total_images_line_edit.setText(str(total_images))
            memory = (total_images * image_size) / 1000
            self.acquisition_settings_dialog.memory_line_edit.setText(("%.3f" % memory))
        else:
            self.acquisition_settings_dialog.total_images_line_edit.setText(str(self.num_images_per))
            memory = (self.num_images_per * image_size) / 1000
            self.acquisition_settings_dialog.memory_line_edit.setText(("%.3f" % memory))

    def go_to_button_clicked(self):
        #Goes to position set in current instance of RegionSettings
         
        x_pos = self.region_settings.x_position
        y_pos = self.region_settings.y_position
        z_pos = self.region_settings.z_position

        self.mm_hardware_commands.move_stage(x_pos, y_pos, z_pos)

    def set_region_button_clicked(self):
        # Gets current stage position and creates element of region_settings_list
        # with current settings in GUI. Currently, this method and the paste_regionButton
        # are the only ways to initialize an element in the region_settings_list.

        x_pos = self.mm_hardware_commands.get_x_position()
        y_pos = self.mm_hardware_commands.get_y_position()
        z_pos = self.mm_hardware_commands.get_z_position()

        self.region_settings.x_position = x_pos
        RegionSettings.x_position = x_pos
        self.region_settings.y_position = y_pos
        RegionSettings.y_position = y_pos
        self.region_settings.z_position = z_pos
        RegionSettings.z_position = z_pos
        self.acquisition_settings.update_region_settings_list(self.region_settings, self.sample_num, self.region_num)

        #Once region is initialized, the next region can be set
        self.cls_dialog.next_region_button.setEnabled(True)
        self.cls_dialog.next_sample_button.setEnabled(True)
        self.cls_dialog.remove_region_button.setEnabled(True)
        self.cls_dialog.go_to_button.setEnabled(True)

        self.set_table()
        self.update_cls_dialog()
        self.write_to_config()

    def previous_region_button_clicked(self):
        self.region_num -= 1

        self.region_settings = self.acquisition_settings.region_settings_list[self.sample_num][self.region_num]

        if self.region_num == 0:
            self.cls_dialog.previous_region_button.setEnabled(False)

        self.cls_dialog.remove_region_button.setEnabled(True)
        self.cls_dialog.next_region_button.setEnabled(True)
        self.cls_dialog.go_to_button.setEnabled(True)

        self.update_cls_dialog()

    def next_region_button_clicked(self):
        self.region_num += 1

        region = self.acquisition_settings.region_settings_list[self.sample_num][self.region_num]

        # Worth noting that the region_settings list is initialized as a 2D list
        # with all elements equal to 0. Thus, this region != 0 statement is just
        # to check if the index has been initialized with a region_settings object.
        if region != 0:
            self.region_settings = region
            self.cls_dialog.go_to_button.setEnabled(True)
        else:
            self.region_settings = RegionSettings()
            self.cls_dialog.next_region_button.setEnabled(False)
            self.cls_dialog.remove_region_button.setEnabled(False)
            self.cls_dialog.go_to_button.setEnabled(False)

        self.cls_dialog.previous_region_button.setEnabled(True)

        self.update_cls_dialog()

    def previous_sample_button_clicked(self):
        self.sample_num -= 1
        self.region_num = 0

        self.region_settings = self.acquisition_settings.region_settings_list[self.sample_num][self.region_num]

        if self.sample_num == 0:
            self.cls_dialog.previous_sample_button.setEnabled(False)

        self.cls_dialog.previous_region_button.setEnabled(False)
        self.cls_dialog.next_region_button.setEnabled(True)
        self.cls_dialog.next_sample_button.setEnabled(True)
        self.cls_dialog.remove_region_button.setEnabled(True)
        self.cls_dialog.go_to_button.setEnabled(True)

        self.update_cls_dialog()

    def next_sample_button_clicked(self):
        self.sample_num += 1
        self.region_num = 0

        region = self.acquisition_settings.region_settings_list[self.sample_num][self.region_num]
        if region != 0:
            self.region_settings = region
            self.cls_dialog.go_to_button.setEnabled(True)
            if self.acquisition_settings.region_settings_list[self.sample_num][self.region_num + 1] != 0:
                self.cls_dialog.next_region_button.setEnabled(True)
        else:
            self.region_settings = RegionSettings()
            self.cls_dialog.next_region_button.setEnabled(False)
            self.cls_dialog.remove_region_button.setEnabled(False)
            self.cls_dialog.next_sample_button.setEnabled(False)
            self.cls_dialog.go_to_button.setEnabled(False)

        self.cls_dialog.previous_region_button.setEnabled(False)
        self.cls_dialog.previous_sample_button.setEnabled(True)

        self.update_cls_dialog()

    def remove_region_button_clicked(self):
        # Removes current region from region_settings_list. See remove_region_settings() 
        # in AcquisitionSettings class for more details.

        self.acquisition_settings.remove_region_settings(self.sample_num, self.region_num)
        if self.acquisition_settings.region_settings_list[self.sample_num][self.region_num] != 0:
            self.region_settings = self.acquisition_settings.region_settings_list[self.sample_num][self.region_num]
            self.cls_dialog.go_to_button.setEnabled(True)
        else:
            self.region_settings = RegionSettings()
            self.cls_dialog.next_region_button.setEnabled(False)
            self.cls_dialog.remove_region_button.setEnabled(False)
            self.cls_dialog.go_to_button.setEnabled(False)
            if self.region_num == 0:
                self.cls_dialog.next_sample_button.setEnabled(False)
                self.cls_dialog.previous_region_button.setEnabled(False)
                if self.sample_num == 0:
                    self.cls_dialog.previous_sample_button.setEnabled(False)

        self.set_table()
        self.update_cls_dialog()
        self.write_to_config()

    def copy_button_clicked(self):
        # Creates new object with fields of the same value as region_settings_copy
        self.region_settings_copy = copy.deepcopy(self.region_settings)

    def paste_button_clicked(self):
        # Initializes new region at current index with values from region_settings_copy.
        # Currently the only method other than set_region_button_clicked to initialize
        # region in region_settings_list

        self.region_settings = copy.deepcopy(self.region_settings_copy)
        self.acquisition_settings.update_region_settings_list(self.region_settings, self.sample_num, self.region_num)

        self.cls_dialog.next_region_button.setEnabled(True)
        self.cls_dialog.next_sample_button.setEnabled(True)
        self.cls_dialog.remove_region_button.setEnabled(True)
        self.cls_dialog.go_to_button.setEnabled(True)

        self.set_table()
        self.update_cls_dialog()
        self.write_to_config()

    def set_z_start_button_clicked(self):
        # gets current z stage position and sets it as z_start_position

        z_pos = self.mm_hardware_commands.get_z_position()
        self.region_settings.z_start_position = z_pos
        RegionSettings.z_start_position = z_pos
        self.cls_dialog.start_z_line_edit.setText(str(z_pos))

        self.set_table()
        self.write_to_config()

    def set_z_end_button_clicked(self):
        z_pos = self.mm_hardware_commands.get_z_position()
        self.region_settings.z_end_position = z_pos
        RegionSettings.z_end_position = z_pos
        self.cls_dialog.end_z_line_edit.setText(str(z_pos))

        self.set_table()
        self.write_to_config()

    def acquisition_setup_button_clicked(self):
        #Pulls up acquisition settings dialog
        self.acquisition_settings_dialog.show()
        self.acquisition_settings_dialog.activateWindow()

    def z_stack_check_clicked(self):
        # Enables/disables zStack GUI elements when checkbox is clicked.
        # Also sets z_stack_boolean in region_settings.

        z_stack_boolean = self.cls_dialog.z_stack_check_box.isChecked()
        self.region_settings.z_stack_boolean = z_stack_boolean
        RegionSettings.z_stack_boolean = z_stack_boolean
        self.cls_dialog.z_stack_check_box.setChecked(z_stack_boolean)
        self.cls_dialog.set_z_start_button.setEnabled(z_stack_boolean)
        self.cls_dialog.set_z_end_button.setEnabled(z_stack_boolean)
        self.cls_dialog.start_z_line_edit.setEnabled(z_stack_boolean)
        self.cls_dialog.end_z_line_edit.setEnabled(z_stack_boolean)
        self.cls_dialog.step_size_line_edit.setEnabled(z_stack_boolean)
        self.cls_dialog.z_stack_available_list_view.setEnabled(z_stack_boolean)
        self.cls_dialog.z_stack_used_list_view.setEnabled(z_stack_boolean)

        self.set_table()
        self.write_to_config()

    def snap_check_clicked(self):
        # Same as z_stack_check_clicked but for snap

        snap_boolean = self.cls_dialog.snap_check_box.isChecked()
        self.region_settings.snap_boolean = snap_boolean
        RegionSettings.snap_boolean = snap_boolean
        self.cls_dialog.snap_check_box.setChecked(snap_boolean)
        self.cls_dialog.snap_exposure_line_edit.setEnabled(snap_boolean)
        self.cls_dialog.snap_available_list_view.setEnabled(snap_boolean)
        self.cls_dialog.snap_used_list_view.setEnabled(snap_boolean)

        self.set_table()
        self.write_to_config()

    def video_check_clicked(self):
        # Same as z_stack_check_clicked but for video

        video_boolean = self.cls_dialog.video_check_box.isChecked()
        self.region_settings.video_boolean = video_boolean
        RegionSettings.video_boolean = video_boolean
        self.cls_dialog.video_check_box.setChecked(video_boolean)
        self.cls_dialog.video_duration_line_edit.setEnabled(video_boolean)
        self.cls_dialog.video_exposure_line_edit.setEnabled(video_boolean)
        self.cls_dialog.video_available_list_view.setEnabled(video_boolean)
        self.cls_dialog.video_used_list_view.setEnabled(video_boolean)

        self.set_table()
        self.write_to_config()

    def x_line_edit_event(self):
        # Sets x_position in region_settings
        try:
            x_pos = int(self.cls_dialog.x_line_edit.text())
            self.region_settings.x_position = x_pos
            RegionSettings.x_position = x_pos
        except ValueError:
            return 'not a number'

        self.set_table()
        self.write_to_config()

    def y_line_edit_event(self):
        try:
            y_pos = int(self.cls_dialog.y_line_edit.text())
            self.region_settings.y_position = y_pos
            RegionSettings.y_position = y_pos
        except ValueError:
            return 'not a number'

        self.set_table()
        self.write_to_config()

    def z_line_edit_event(self):
        try:
            z_pos = int(self.cls_dialog.z_line_edit.text())
            self.region_settings.z_position = z_pos
            RegionSettings.z_position = z_pos
        except ValueError:
            return 'not a number'

        self.set_table()
        self.write_to_config()

    def start_z_line_edit_event(self):
        try:
            z_start = int(self.cls_dialog.start_z_line_edit.text())
            self.region_settings.z_start_position = z_start
            RegionSettings.z_start_position = z_start
        except ValueError:
            return 'not a number'

        self.set_table()
        self.write_to_config()

    def end_z_line_edit_event(self):
        try:
            end_z = int(self.cls_dialog.end_z_line_edit.text())
            self.region_settings.z_end_position = end_z
            RegionSettings.z_end_position = end_z
        except ValueError:
            return 'not a number'

        self.set_table()
        self.write_to_config()

    def step_size_line_edit_event(self):
        try:
            step_size = int(self.cls_dialog.step_size_line_edit.text())
            self.region_settings.step_size = step_size
            RegionSettings.step_size = step_size
        except ValueError:
            return 'not a number'

        self.set_table()
        self.write_to_config()

    def snap_exposure_line_edit_event(self):
        try:
            exp = int(self.cls_dialog.snap_exposure_line_edit.text())
            self.region_settings.snap_exposure_time = exp
            RegionSettings.snap_exposure_time = exp
        except ValueError:
            return 'not a number'

        self.set_table()
        self.write_to_config()

    def video_duration_line_edit_event(self):
        try:
            duration = int(self.cls_dialog.video_duration_line_edit.text())
            self.region_settings.video_duration = duration
            RegionSettings.video_duration = duration
        except ValueError:
            return 'not a number'

        self.set_table()
        self.write_to_config()

    def video_exposure_line_edit_event(self):
        try:
            exp = int(self.cls_dialog.video_exposure_line_edit.text())
            self.region_settings.video_exposure_time = exp
            RegionSettings.video_exposure_time = exp
        except ValueError:
            return 'not a number'

        self.set_table()
        self.write_to_config()

    def z_stack_available_list_move(self):
        #on double click, switches channel from available list to used list
        channel_index = self.cls_dialog.z_stack_available_list_view.selectedIndexes()[0].row()
        channel = self.z_stack_available_model.item(channel_index).text()
        self.z_stack_available_model.removeRow(channel_index)

        item = QtGui.QStandardItem(channel)
        self.z_stack_used_model.appendRow(item)
        self.region_settings.z_stack_channel_list.append(channel)

        self.set_table()
        self.write_to_config()

    def snap_available_list_move(self):
        channel_index = self.cls_dialog.snap_available_list_view.selectedIndexes()[0].row()
        channel = self.snap_available_model.item(channel_index).text()
        self.snap_available_model.removeRow(channel_index)

        item = QtGui.QStandardItem(channel)
        self.snap_used_model.appendRow(item)
        self.region_settings.snap_channel_list.append(channel)

        self.set_table()
        self.write_to_config()

    def video_available_list_move(self):
        channel_index = self.cls_dialog.video_available_list_view.selectedIndexes()[0].row()
        channel = self.video_available_model.item(channel_index).text()
        self.video_available_model.removeRow(channel_index)

        item = QtGui.QStandardItem(channel)
        self.video_used_model.appendRow(item)
        self.region_settings.video_channel_list.append(channel)

        self.set_table()
        self.write_to_config()

    def z_stack_used_list_move(self):
        #Same as available_list_move except from used list to available list
        channel_index = self.cls_dialog.z_stack_used_list_view.selectedIndexes()[0].row()
        channel = self.z_stack_used_model.item(channel_index).text()
        self.z_stack_used_model.removeRow(channel_index)
        self.region_settings.z_stack_channel_list.remove(channel)

        item = QtGui.QStandardItem(channel)
        self.z_stack_available_model.appendRow(item)

        self.set_table()
        self.write_to_config()

    def snap_used_list_move(self):
        channel_index = self.cls_dialog.snap_used_list_view.selectedIndexes()[0].row()
        channel = self.snap_used_model.item(channel_index).text()
        self.snap_used_model.removeRow(channel_index)
        self.region_settings.snap_channel_list.remove(channel)

        item = QtGui.QStandardItem(channel)
        self.snap_available_model.appendRow(item)

        self.set_table()
        self.write_to_config()

    def video_used_list_move(self):
        channel_index = self.cls_dialog.video_used_list_view.selectedIndexes()[0].row()
        channel = self.video_used_model.item(channel_index).text()
        self.video_used_model.removeRow(channel_index)
        self.region_settings.video_channel_list.remove(channel)

        item = QtGui.QStandardItem(channel)
        self.video_available_model.appendRow(item)

        self.set_table()
        self.write_to_config()

    def browse_button_clicked(self):
        #Choose save location. Acquisition button is only enabled after setting save location.
        browse = QtDesignerGUI.BrowseDialog()
        path = str(browse.getExistingDirectory(browse, 'Select Directory', self.start_path))
        self.acquisition_settings_dialog.save_location_line_edit.setText(path)

        if path != '':
            self.start_path = str(Path(path).parent)
            self.acquisition_settings.directory = path
            self.acquisition_settings_dialog.start_acquisition_button.setEnabled(True)

    def channel_move_up_button_clicked(self):
        #Moves channel one index lower in channel_order_list. The channel_order_list
        #determines the channel order in which an acquisition is performed.
        channel_index = self.acquisition_settings_dialog.channel_order_list_view.selectedIndexes()[0].row()
        if channel_index > 0:
            channel = self.channel_order_model.takeRow(channel_index)
            self.channel_order_model.insertRow(channel_index - 1, channel)
            new_index = self.channel_order_model.indexFromItem(channel[0])
            self.acquisition_settings_dialog.channel_order_list_view.setCurrentIndex(new_index)

            self.acquisition_settings.channel_order_list = []
            for index in range(0, self.channel_order_model.rowCount()):
                item = self.channel_order_model.item(index, 0).text()
                self.acquisition_settings.channel_order_list.append(item)

    def channel_move_down_button_clicked(self):
        #Same as move_up_button but moves up one index.
        channel_index = self.acquisition_settings_dialog.channel_order_list_view.selectedIndexes()[0].row()
        if channel_index < self.channel_order_model.rowCount() - 1:
            channel = self.channel_order_model.takeRow(channel_index)
            self.channel_order_model.insertRow(channel_index + 1, channel)
            new_index = self.channel_order_model.indexFromItem(channel[0])
            self.acquisition_settings_dialog.channel_order_list_view.setCurrentIndex(new_index)

            self.acquisition_settings.channel_order_list = []
            for index in range(0, self.channel_order_model.rowCount()):
                item = self.channel_order_model.item(index, 0).text()
                self.acquisition_settings.channel_order_list.append(item)

    def start_acquisition_button_clicked(self):
        #Starts acquisition with current acquisition_settings.
        acquisition = Acquisition(self.studio, self.core, self.acquisition_dialog, self.acquisition_settings,
                                  self.mm_hardware_commands)
        self.acquisition_settings_dialog.start_acquisition_button.setEnabled(False)
        acquisition.start()
    
    def reset_stage_button_clicked(self):
        self.reset_stage_dialog.show()
    
    def reset_stage_yes_button_clicked(self):
        try:
            self.mm_hardware_commands.reset_stage()
            self.mm_hardware_commands.reset_joystick()
            self.reset_stage_dialog.setVisible(False)
        except:
            print('Stage Resetting')
            self.reset_stage_dialog.setVisible(False)
    
    def reset_stage_cancel_button_clicked(self):
        self.reset_stage_dialog.setVisible(False)

    def reset_joystick_button_clicked(self):
        self.mm_hardware_commands.reset_joystick()

    def time_points_check_clicked(self):
        #Sets state of time_points GUI elements to match state of checkbox
        time_points_boolean = self.acquisition_settings_dialog.time_points_check_box.isChecked()
        self.acquisition_settings.time_points_boolean = time_points_boolean
        self.acquisition_settings_dialog.num_time_points_line_edit.setEnabled(time_points_boolean)
        self.acquisition_settings_dialog.time_points_interval_line_edit.setEnabled(time_points_boolean)
        self.acquisition_settings_dialog.sequential_check_box.setEnabled(time_points_boolean)
        self.write_to_config()
        self.calculate_num_images()
    
    def sequential_check_clicked(self):
        self.acquisition_settings.sequential_time_series_boolean = self.acquisition_settings_dialog.sequential_check_box.isChecked()
        self.write_to_config()

    def lsrm_check_clicked(self):
        #Enables LSRM in acquisition
        self.acquisition_settings.lightsheet_mode_boolean = self.acquisition_settings_dialog.lsrm_check_box.isChecked()

    def stage_speed_combo_box_clicked(self):
        #Sets stage speed for use in z-stacks in acquisition
        if self.acquisition_settings_dialog.stage_speed_combo_box.currentText() == '30 um/s':
            self.acquisition_settings.z_scan_speed = 0.030

        if self.acquisition_settings_dialog.stage_speed_combo_box.currentText() == '15 um/s':
            self.acquisition_settings.z_scan_speed = 0.015

    def num_time_points_line_edit_event(self):
        #Sets number of time points
        try:
            self.acquisition_settings.num_time_points = int(self.acquisition_settings_dialog.num_time_points_line_edit.text())
            self.write_to_config()
            self.calculate_num_images()
                
        except ValueError:
            return 'not a number'

    def time_points_interval_line_edit_event(self):
        #Sets interval between time points
        try:
            self.acquisition_settings.time_points_interval = int(self.acquisition_settings_dialog.time_points_interval_line_edit.text())
            self.write_to_config()
        except ValueError:
            return 'not a number'
