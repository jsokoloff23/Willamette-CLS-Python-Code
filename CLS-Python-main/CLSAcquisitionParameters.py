"""
Last Modified: 4/12/2022

The "Model" part of the CLS program. Holds settings to be used during
CLS Acquisition.

Worth noting that sample_num and region_num refer to the the region_settings_list
index trackers in the CLSController class in Controller.py.

Future Changes:
- Currently uses public attributes but could be changed to a getter/setter design?
  Not sure if encapsulation really matters that much.

- remove_region_settings() method could probably be done in a more beautiful way.

- region_settings class currently contains no methods: could be made into dictionary
  if someone felt inclined.
  """


class AcquisitionSettings(object):
    def __init__(self):
        self.sample_dimension = 50
        self.region_dimension = 100
        self.region_settings_list = [[0 for i in range(self.region_dimension)] for j in range(self.sample_dimension)]

        self.channel_group_name = "Channel"
        self.channel_order_list = []

        self.directory = "G:\\"

        self.num_images = 0
        self.time_points_boolean = False
        self.time_points_interval = 0
        self.num_time_points = 1

        self.z_scan_speed = 0.030
        self.lightsheet_mode_boolean = False

    def update_region_settings_list(self, region_settings, sample_num, region_num):
        self.region_settings_list[sample_num][region_num] = region_settings
    
    def remove_region_settings(self, sample_num, region_num):
        """
        First, removes index from region_settings_list. If there exists an element of
        region_settings_list with the same sample_num index as the removed region but a
        higher region_num index, it moves down to replace the removed region. It
        wouldn't make sense for there to be a region 2 without a region 1, for example.

        If the region removed was the only region in the list with its sample_num index
        AND there exists a region at a greater sample_num than the removed region, the
        sample_num index of all the regions with a higher index than the region removed
        gets lowered by one. This is to prevent there from being a set of regions with
        sample_num = 1 when there aren't even any regions with sample_num = 0, for example.

        There's probably a better way to do this...
        """

        self.region_settings_list[sample_num][region_num] = 0
        found_boolean = False
        for region_index in range(0, self.region_dimension-1):
            if self.region_settings_list[sample_num][region_index] != 0:
                found_boolean = True
                if region_index > region_num:
                    self.region_settings_list[sample_num][region_index-1] = self.region_settings_list[sample_num][region_index]
                    self.region_settings_list[sample_num][region_index] = 0
        if self.region_settings_list[sample_num + 1][0] != 0 and not found_boolean:
            self.region_settings_list[sample_num:self.sample_dimension] = self.region_settings_list[sample_num+1:self.sample_dimension+1]
            self.region_settings_list.append([0] * self.region_dimension)


class RegionSettings(object):
    x_position = 0
    y_position = 0
    z_position = 0
        
    z_stack_boolean = False
    z_start_position = 0
    z_end_position = 0
    step_size = 1
    z_stack_channel_list = []

    snap_boolean = False
    snap_exposure_time = 5
    snap_channel_list = []
    
    video_boolean = False
    video_duration = 5
    video_exposure_time = 20
    video_channel_list = []

    def __init__(self):
        self.x_position = RegionSettings.x_position
        self.y_position = RegionSettings.y_position
        self.z_position = RegionSettings.z_position
        
        self.z_stack_boolean = RegionSettings.z_stack_boolean
        self.z_start_position = RegionSettings.z_start_position
        self.z_end_position = RegionSettings.z_end_position
        self.step_size = RegionSettings.step_size
        self.z_stack_channel_list = RegionSettings.z_stack_channel_list

        self.snap_boolean = RegionSettings.snap_boolean
        self.snap_exposure_time = RegionSettings.snap_exposure_time
        self.snap_channel_list = RegionSettings.snap_channel_list
        
        self.video_boolean = RegionSettings.video_boolean
        self.video_duration = RegionSettings.video_duration
        self.video_exposure_time = RegionSettings.video_exposure_time
        self.video_channel_list = RegionSettings.video_channel_list
