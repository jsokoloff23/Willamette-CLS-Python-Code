"""
Last Modified: 4/12/2022

Auto-generated code from QtDesigner UI files. I just copy pasted the code from each 
generated file into one big GUI file. 

To make the QtDesigner .ui file into a .py file, you must put the following into cmd:

python -m PyQt5.uic.pyuic [filepath][filename].ui -o [filepath][filename].py -x
"""


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AbortDialog(object):
    def setupUi(self, AbortDialog):
        AbortDialog.setObjectName("AbortDialog")
        AbortDialog.resize(362, 112)
        self.abort_label = QtWidgets.QLabel(AbortDialog)
        self.abort_label.setGeometry(QtCore.QRect(70, 20, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.abort_label.setFont(font)
        self.abort_label.setAlignment(QtCore.Qt.AlignCenter)
        self.abort_label.setObjectName("abort_label")
        self.abort_button = QtWidgets.QPushButton(AbortDialog)
        self.abort_button.setGeometry(QtCore.QRect(190, 70, 75, 23))
        self.abort_button.setObjectName("abort_button")
        self.cancel_button = QtWidgets.QPushButton(AbortDialog)
        self.cancel_button.setGeometry(QtCore.QRect(80, 70, 75, 23))
        self.cancel_button.setObjectName("cancel_button")

        self.retranslateUi(AbortDialog)
        QtCore.QMetaObject.connectSlotsByName(AbortDialog)

    def retranslateUi(self, AbortDialog):
        _translate = QtCore.QCoreApplication.translate
        AbortDialog.setWindowTitle(_translate("AbortDialog", "Dialog"))
        self.abort_label.setText(_translate("AbortDialog", "Abort Acquisition?"))
        self.abort_button.setText(_translate("AbortDialog", "Abort"))
        self.cancel_button.setText(_translate("AbortDialog", "Cancel"))

class Ui_AcquisitionDialog(object):
    def setupUi(self, AcquisitionDialog):
        AcquisitionDialog.setObjectName("AcquisitionDialog")
        AcquisitionDialog.resize(420, 176)
        self.sample_label = QtWidgets.QLabel(AcquisitionDialog)
        self.sample_label.setGeometry(QtCore.QRect(190, 30, 47, 16))
        self.sample_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sample_label.setObjectName("sample_label")
        self.region_label = QtWidgets.QLabel(AcquisitionDialog)
        self.region_label.setGeometry(QtCore.QRect(190, 50, 47, 13))
        self.region_label.setAlignment(QtCore.Qt.AlignCenter)
        self.region_label.setObjectName("region_label")
        self.acquisition_label = QtWidgets.QLabel(AcquisitionDialog)
        self.acquisition_label.setGeometry(QtCore.QRect(0, 60, 421, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.acquisition_label.setFont(font)
        self.acquisition_label.setAlignment(QtCore.Qt.AlignCenter)
        self.acquisition_label.setObjectName("acquisition_label")
        self.abort_button = QtWidgets.QPushButton(AcquisitionDialog)
        self.abort_button.setGeometry(QtCore.QRect(180, 140, 75, 23))
        self.abort_button.setObjectName("abort_button")
        self.time_point_label = QtWidgets.QLabel(AcquisitionDialog)
        self.time_point_label.setGeometry(QtCore.QRect(170, 10, 91, 16))
        self.time_point_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_point_label.setObjectName("time_point_label")

        self.retranslateUi(AcquisitionDialog)
        QtCore.QMetaObject.connectSlotsByName(AcquisitionDialog)

    def retranslateUi(self, AcquisitionDialog):
        _translate = QtCore.QCoreApplication.translate
        AcquisitionDialog.setWindowTitle(_translate("AcquisitionDialog", "Dialog"))
        self.sample_label.setText(_translate("AcquisitionDialog", "Sample 1"))
        self.region_label.setText(_translate("AcquisitionDialog", "Region 1"))
        self.acquisition_label.setText(_translate("AcquisitionDialog", "Starting Acquisition"))
        self.abort_button.setText(_translate("AcquisitionDialog", "Abort"))
        self.time_point_label.setText(_translate("AcquisitionDialog", "Time point 1"))

class Ui_CLSAcquisitionSettingsDialog(object):
    def setupUi(self, CLSAcquisitionSettingsDialog):
        CLSAcquisitionSettingsDialog.setObjectName("CLSAcquisitionSettingsDialog")
        CLSAcquisitionSettingsDialog.resize(416, 433)
        self.time_points_check_box = QtWidgets.QCheckBox(CLSAcquisitionSettingsDialog)
        self.time_points_check_box.setGeometry(QtCore.QRect(60, 80, 81, 17))
        self.time_points_check_box.setObjectName("time_points_check_box")
        self.num_time_points_line_edit = QtWidgets.QLineEdit(CLSAcquisitionSettingsDialog)
        self.num_time_points_line_edit.setGeometry(QtCore.QRect(80, 110, 61, 20))
        self.num_time_points_line_edit.setObjectName("num_time_points_line_edit")
        self.time_points_interval_line_edit = QtWidgets.QLineEdit(CLSAcquisitionSettingsDialog)
        self.time_points_interval_line_edit.setGeometry(QtCore.QRect(80, 140, 61, 20))
        self.time_points_interval_line_edit.setObjectName("time_points_interval_line_edit")
        self.channel_order_move_up_button = QtWidgets.QPushButton(CLSAcquisitionSettingsDialog)
        self.channel_order_move_up_button.setGeometry(QtCore.QRect(210, 110, 75, 23))
        self.channel_order_move_up_button.setObjectName("channel_order_move_up_button")
        self.channel_order_move_down_button = QtWidgets.QPushButton(CLSAcquisitionSettingsDialog)
        self.channel_order_move_down_button.setGeometry(QtCore.QRect(210, 150, 75, 23))
        self.channel_order_move_down_button.setObjectName("channel_order_move_down_button")
        self.channel_order_list_view = QtWidgets.QListView(CLSAcquisitionSettingsDialog)
        self.channel_order_list_view.setGeometry(QtCore.QRect(290, 90, 101, 101))
        self.channel_order_list_view.setObjectName("channel_order_list_view")
        self.label = QtWidgets.QLabel(CLSAcquisitionSettingsDialog)
        self.label.setGeometry(QtCore.QRect(290, 60, 101, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(CLSAcquisitionSettingsDialog)
        self.label_2.setGeometry(QtCore.QRect(40, 110, 31, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(CLSAcquisitionSettingsDialog)
        self.label_3.setGeometry(QtCore.QRect(30, 140, 51, 16))
        self.label_3.setObjectName("label_3")
        self.browse_button = QtWidgets.QPushButton(CLSAcquisitionSettingsDialog)
        self.browse_button.setGeometry(QtCore.QRect(160, 330, 75, 23))
        self.browse_button.setObjectName("browse_button")
        self.save_location_line_edit = QtWidgets.QLineEdit(CLSAcquisitionSettingsDialog)
        self.save_location_line_edit.setGeometry(QtCore.QRect(190, 360, 113, 20))
        self.save_location_line_edit.setObjectName("save_location_line_edit")
        self.label_4 = QtWidgets.QLabel(CLSAcquisitionSettingsDialog)
        self.label_4.setGeometry(QtCore.QRect(110, 360, 71, 20))
        self.label_4.setObjectName("label_4")
        self.stage_speed_combo_box = QtWidgets.QComboBox(CLSAcquisitionSettingsDialog)
        self.stage_speed_combo_box.setGeometry(QtCore.QRect(300, 220, 69, 22))
        self.stage_speed_combo_box.setObjectName("stage_speed_combo_box")
        self.stage_speed_combo_box.addItem("")
        self.stage_speed_combo_box.addItem("")
        self.lsrm_check_box = QtWidgets.QCheckBox(CLSAcquisitionSettingsDialog)
        self.lsrm_check_box.setGeometry(QtCore.QRect(230, 250, 161, 20))
        self.lsrm_check_box.setObjectName("lsrm_check_box")
        self.label_5 = QtWidgets.QLabel(CLSAcquisitionSettingsDialog)
        self.label_5.setGeometry(QtCore.QRect(230, 220, 71, 20))
        self.label_5.setObjectName("label_5")
        self.start_acquisition_button = QtWidgets.QPushButton(CLSAcquisitionSettingsDialog)
        self.start_acquisition_button.setGeometry(QtCore.QRect(140, 400, 111, 23))
        self.start_acquisition_button.setObjectName("start_acquisition_button")
        self.total_images_label = QtWidgets.QLabel(CLSAcquisitionSettingsDialog)
        self.total_images_label.setGeometry(QtCore.QRect(30, 240, 71, 16))
        self.total_images_label.setObjectName("total_images_label")
        self.total_images_line_edit = QtWidgets.QLineEdit(CLSAcquisitionSettingsDialog)
        self.total_images_line_edit.setGeometry(QtCore.QRect(110, 240, 61, 20))
        self.total_images_line_edit.setObjectName("total_images_line_edit")
        self.memory_label = QtWidgets.QLabel(CLSAcquisitionSettingsDialog)
        self.memory_label.setGeometry(QtCore.QRect(30, 270, 71, 16))
        self.memory_label.setObjectName("memory_label")
        self.memory_line_edit = QtWidgets.QLineEdit(CLSAcquisitionSettingsDialog)
        self.memory_line_edit.setGeometry(QtCore.QRect(110, 270, 61, 20))
        self.memory_line_edit.setObjectName("memory_line_edit")
        self.num_images_per_label = QtWidgets.QLabel(CLSAcquisitionSettingsDialog)
        self.num_images_per_label.setGeometry(QtCore.QRect(10, 210, 91, 20))
        self.num_images_per_label.setObjectName("num_images_per_label")
        self.num_images_per_line_edit = QtWidgets.QLineEdit(CLSAcquisitionSettingsDialog)
        self.num_images_per_line_edit.setGeometry(QtCore.QRect(110, 210, 61, 20))
        self.num_images_per_line_edit.setObjectName("num_images_per_line_edit")
        self.line = QtWidgets.QFrame(CLSAcquisitionSettingsDialog)
        self.line.setGeometry(QtCore.QRect(200, 190, 391, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.line.setFont(font)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(4)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(CLSAcquisitionSettingsDialog)
        self.line_2.setGeometry(QtCore.QRect(190, 60, 20, 251))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(4)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(CLSAcquisitionSettingsDialog)
        self.line_3.setGeometry(QtCore.QRect(-60, 300, 531, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.line_3.setFont(font)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setLineWidth(4)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setObjectName("line_3")
        self.label_6 = QtWidgets.QLabel(CLSAcquisitionSettingsDialog)
        self.label_6.setGeometry(QtCore.QRect(80, 20, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.line_4 = QtWidgets.QFrame(CLSAcquisitionSettingsDialog)
        self.line_4.setGeometry(QtCore.QRect(-60, 50, 531, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.line_4.setFont(font)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_4.setLineWidth(4)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setObjectName("line_4")
        self.memory_unit_label = QtWidgets.QLabel(CLSAcquisitionSettingsDialog)
        self.memory_unit_label.setGeometry(QtCore.QRect(170, 270, 21, 16))
        self.memory_unit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.memory_unit_label.setObjectName("memory_unit_label")

        self.retranslateUi(CLSAcquisitionSettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(CLSAcquisitionSettingsDialog)

    def retranslateUi(self, CLSAcquisitionSettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        CLSAcquisitionSettingsDialog.setWindowTitle(_translate("CLSAcquisitionSettingsDialog", "Dialog"))
        self.time_points_check_box.setText(_translate("CLSAcquisitionSettingsDialog", "Time points"))
        self.channel_order_move_up_button.setText(_translate("CLSAcquisitionSettingsDialog", "Move Up"))
        self.channel_order_move_down_button.setText(_translate("CLSAcquisitionSettingsDialog", "Move Down"))
        self.label.setText(_translate("CLSAcquisitionSettingsDialog", "Channel Order"))
        self.label_2.setText(_translate("CLSAcquisitionSettingsDialog", "Count:"))
        self.label_3.setText(_translate("CLSAcquisitionSettingsDialog", "Interval:"))
        self.browse_button.setText(_translate("CLSAcquisitionSettingsDialog", "Browse..."))
        self.label_4.setText(_translate("CLSAcquisitionSettingsDialog", "Save Location:"))
        self.stage_speed_combo_box.setItemText(0, _translate("CLSAcquisitionSettingsDialog", "30 um/s"))
        self.stage_speed_combo_box.setItemText(1, _translate("CLSAcquisitionSettingsDialog", "15 um/s"))
        self.lsrm_check_box.setText(_translate("CLSAcquisitionSettingsDialog", "Lightsheet Readout Mode"))
        self.label_5.setText(_translate("CLSAcquisitionSettingsDialog", "Stage Speed:"))
        self.start_acquisition_button.setText(_translate("CLSAcquisitionSettingsDialog", "Start Acquisition"))
        self.total_images_label.setText(_translate("CLSAcquisitionSettingsDialog", "Total Images:"))
        self.memory_label.setText(_translate("CLSAcquisitionSettingsDialog", "Total Memory:"))
        self.num_images_per_label.setText(_translate("CLSAcquisitionSettingsDialog", "Images per point:"))
        self.label_6.setText(_translate("CLSAcquisitionSettingsDialog", "Acquisition Settings"))
        self.memory_unit_label.setText(_translate("CLSAcquisitionSettingsDialog", "Gb"))


class Ui_CLSDialog(object):
    def setupUi(self, CLSDialog):
        CLSDialog.setObjectName("CLSDialog")
        CLSDialog.resize(859, 899)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        CLSDialog.setFont(font)
        self.cls_region_label = QtWidgets.QLabel(CLSDialog)
        self.cls_region_label.setGeometry(QtCore.QRect(270, 10, 301, 61))
        self.cls_region_label.setAlignment(QtCore.Qt.AlignCenter)
        self.cls_region_label.setObjectName("cls_region_label")
        self.region_label = QtWidgets.QLabel(CLSDialog)
        self.region_label.setGeometry(QtCore.QRect(390, 90, 61, 16))
        self.region_label.setAlignment(QtCore.Qt.AlignCenter)
        self.region_label.setObjectName("region_label")
        self.sample_label = QtWidgets.QLabel(CLSDialog)
        self.sample_label.setGeometry(QtCore.QRect(380, 70, 71, 16))
        self.sample_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sample_label.setObjectName("sample_label")
        self.x_label = QtWidgets.QLabel(CLSDialog)
        self.x_label.setGeometry(QtCore.QRect(320, 170, 47, 16))
        self.x_label.setAlignment(QtCore.Qt.AlignCenter)
        self.x_label.setObjectName("x_label")
        self.y_label = QtWidgets.QLabel(CLSDialog)
        self.y_label.setGeometry(QtCore.QRect(320, 200, 47, 16))
        self.y_label.setAlignment(QtCore.Qt.AlignCenter)
        self.y_label.setObjectName("y_label")
        self.z_label = QtWidgets.QLabel(CLSDialog)
        self.z_label.setGeometry(QtCore.QRect(320, 230, 47, 21))
        self.z_label.setAlignment(QtCore.Qt.AlignCenter)
        self.z_label.setObjectName("z_label")
        self.x_line_edit = QtWidgets.QLineEdit(CLSDialog)
        self.x_line_edit.setGeometry(QtCore.QRect(360, 170, 113, 20))
        self.x_line_edit.setObjectName("x_line_edit")
        self.y_line_edit = QtWidgets.QLineEdit(CLSDialog)
        self.y_line_edit.setGeometry(QtCore.QRect(360, 200, 113, 20))
        self.y_line_edit.setObjectName("y_line_edit")
        self.z_line_edit = QtWidgets.QLineEdit(CLSDialog)
        self.z_line_edit.setGeometry(QtCore.QRect(360, 230, 113, 20))
        self.z_line_edit.setObjectName("z_line_edit")
        self.set_region_button = QtWidgets.QPushButton(CLSDialog)
        self.set_region_button.setGeometry(QtCore.QRect(380, 140, 75, 23))
        self.set_region_button.setObjectName("set_region_button")
        self.previous_sample_button = QtWidgets.QPushButton(CLSDialog)
        self.previous_sample_button.setGeometry(QtCore.QRect(144, 270, 101, 23))
        self.previous_sample_button.setObjectName("previous_sample_button")
        self.previous_region_button = QtWidgets.QPushButton(CLSDialog)
        self.previous_region_button.setGeometry(QtCore.QRect(250, 270, 101, 23))
        self.previous_region_button.setObjectName("previous_region_button")
        self.next_region_button = QtWidgets.QPushButton(CLSDialog)
        self.next_region_button.setGeometry(QtCore.QRect(490, 270, 81, 23))
        self.next_region_button.setObjectName("next_region_button")
        self.next_sample_button = QtWidgets.QPushButton(CLSDialog)
        self.next_sample_button.setGeometry(QtCore.QRect(580, 270, 91, 23))
        self.next_sample_button.setObjectName("next_sample_button")
        self.remove_region_button = QtWidgets.QPushButton(CLSDialog)
        self.remove_region_button.setGeometry(QtCore.QRect(364, 270, 111, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.remove_region_button.setFont(font)
        self.remove_region_button.setObjectName("remove_region_button")
        self.snap_exposure_line_edit = QtWidgets.QLineEdit(CLSDialog)
        self.snap_exposure_line_edit.setGeometry(QtCore.QRect(382, 360, 61, 20))
        self.snap_exposure_line_edit.setObjectName("snap_exposure_line_edit")
        self.snap_exposure_time_label = QtWidgets.QLabel(CLSDialog)
        self.snap_exposure_time_label.setGeometry(QtCore.QRect(290, 360, 91, 16))
        self.snap_exposure_time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.snap_exposure_time_label.setObjectName("snap_exposure_time_label")
        self.snap_exposure_unit_label = QtWidgets.QLabel(CLSDialog)
        self.snap_exposure_unit_label.setGeometry(QtCore.QRect(410, 360, 91, 16))
        self.snap_exposure_unit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.snap_exposure_unit_label.setObjectName("snap_exposure_unit_label")
        self.start_z_label = QtWidgets.QLabel(CLSDialog)
        self.start_z_label.setGeometry(QtCore.QRect(50, 360, 47, 21))
        self.start_z_label.setAlignment(QtCore.Qt.AlignCenter)
        self.start_z_label.setObjectName("start_z_label")
        self.start_z_line_edit = QtWidgets.QLineEdit(CLSDialog)
        self.start_z_line_edit.setGeometry(QtCore.QRect(100, 360, 113, 20))
        self.start_z_line_edit.setObjectName("start_z_line_edit")
        self.end_z_label = QtWidgets.QLabel(CLSDialog)
        self.end_z_label.setGeometry(QtCore.QRect(50, 390, 47, 21))
        self.end_z_label.setAlignment(QtCore.Qt.AlignCenter)
        self.end_z_label.setObjectName("end_z_label")
        self.end_z_line_edit = QtWidgets.QLineEdit(CLSDialog)
        self.end_z_line_edit.setGeometry(QtCore.QRect(100, 390, 113, 20))
        self.end_z_line_edit.setObjectName("end_z_line_edit")
        self.step_size_label = QtWidgets.QLabel(CLSDialog)
        self.step_size_label.setGeometry(QtCore.QRect(50, 420, 47, 21))
        self.step_size_label.setAlignment(QtCore.Qt.AlignCenter)
        self.step_size_label.setObjectName("step_size_label")
        self.step_size_line_edit = QtWidgets.QLineEdit(CLSDialog)
        self.step_size_line_edit.setGeometry(QtCore.QRect(100, 420, 111, 20))
        self.step_size_line_edit.setObjectName("step_size_line_edit")
        self.start_z_unit_label = QtWidgets.QLabel(CLSDialog)
        self.start_z_unit_label.setGeometry(QtCore.QRect(180, 360, 91, 16))
        self.start_z_unit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.start_z_unit_label.setObjectName("start_z_unit_label")
        self.end_z_unit_label = QtWidgets.QLabel(CLSDialog)
        self.end_z_unit_label.setGeometry(QtCore.QRect(180, 390, 91, 16))
        self.end_z_unit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.end_z_unit_label.setObjectName("end_z_unit_label")
        self.step_size_unit_label = QtWidgets.QLabel(CLSDialog)
        self.step_size_unit_label.setGeometry(QtCore.QRect(190, 420, 71, 16))
        self.step_size_unit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.step_size_unit_label.setObjectName("step_size_unit_label")
        self.x_unit_label = QtWidgets.QLabel(CLSDialog)
        self.x_unit_label.setGeometry(QtCore.QRect(440, 170, 91, 16))
        self.x_unit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.x_unit_label.setObjectName("x_unit_label")
        self.y_unit_label = QtWidgets.QLabel(CLSDialog)
        self.y_unit_label.setGeometry(QtCore.QRect(440, 200, 91, 16))
        self.y_unit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.y_unit_label.setObjectName("y_unit_label")
        self.z_unit_label = QtWidgets.QLabel(CLSDialog)
        self.z_unit_label.setGeometry(QtCore.QRect(440, 230, 91, 16))
        self.z_unit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.z_unit_label.setObjectName("z_unit_label")
        self.video_exposure_line_edit = QtWidgets.QLineEdit(CLSDialog)
        self.video_exposure_line_edit.setGeometry(QtCore.QRect(672, 390, 61, 20))
        self.video_exposure_line_edit.setObjectName("video_exposure_line_edit")
        self.video_exposure_unit_label = QtWidgets.QLabel(CLSDialog)
        self.video_exposure_unit_label.setGeometry(QtCore.QRect(700, 390, 91, 16))
        self.video_exposure_unit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.video_exposure_unit_label.setObjectName("video_exposure_unit_label")
        self.video_exposure_time_label = QtWidgets.QLabel(CLSDialog)
        self.video_exposure_time_label.setGeometry(QtCore.QRect(580, 390, 91, 16))
        self.video_exposure_time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.video_exposure_time_label.setObjectName("video_exposure_time_label")
        self.video_duration_line_edit = QtWidgets.QLineEdit(CLSDialog)
        self.video_duration_line_edit.setGeometry(QtCore.QRect(670, 360, 61, 20))
        self.video_duration_line_edit.setText("")
        self.video_duration_line_edit.setObjectName("video_duration_line_edit")
        self.video_duration_unit_label = QtWidgets.QLabel(CLSDialog)
        self.video_duration_unit_label.setGeometry(QtCore.QRect(700, 360, 91, 16))
        self.video_duration_unit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.video_duration_unit_label.setObjectName("video_duration_unit_label")
        self.video_duration_label = QtWidgets.QLabel(CLSDialog)
        self.video_duration_label.setGeometry(QtCore.QRect(590, 360, 91, 16))
        self.video_duration_label.setAlignment(QtCore.Qt.AlignCenter)
        self.video_duration_label.setObjectName("video_duration_label")
        self.region_table_view = QtWidgets.QTableView(CLSDialog)
        self.region_table_view.setGeometry(QtCore.QRect(30, 690, 801, 161))
        self.region_table_view.setObjectName("region_table_view")
        self.line = QtWidgets.QFrame(CLSDialog)
        self.line.setGeometry(QtCore.QRect(0, 300, 911, 16))
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(8)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(CLSDialog)
        self.line_2.setGeometry(QtCore.QRect(260, 310, 20, 371))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(8)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(CLSDialog)
        self.line_3.setGeometry(QtCore.QRect(530, 310, 20, 371))
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setLineWidth(8)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(CLSDialog)
        self.line_4.setGeometry(QtCore.QRect(0, 670, 911, 16))
        self.line_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_4.setLineWidth(8)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setObjectName("line_4")
        self.acquisition_setup_button = QtWidgets.QPushButton(CLSDialog)
        self.acquisition_setup_button.setGeometry(QtCore.QRect(360, 860, 111, 23))
        self.acquisition_setup_button.setObjectName("acquisition_setup_button")
        self.z_stack_available_list_view = QtWidgets.QListView(CLSDialog)
        self.z_stack_available_list_view.setGeometry(QtCore.QRect(60, 490, 71, 121))
        self.z_stack_available_list_view.setObjectName("z_stack_available_list_view")
        self.video_used_label = QtWidgets.QLabel(CLSDialog)
        self.video_used_label.setGeometry(QtCore.QRect(700, 470, 47, 13))
        self.video_used_label.setAlignment(QtCore.Qt.AlignCenter)
        self.video_used_label.setObjectName("video_used_label")
        self.used_z_stack_label = QtWidgets.QLabel(CLSDialog)
        self.used_z_stack_label.setGeometry(QtCore.QRect(160, 470, 47, 13))
        self.used_z_stack_label.setAlignment(QtCore.Qt.AlignCenter)
        self.used_z_stack_label.setObjectName("used_z_stack_label")
        self.snap_available_label = QtWidgets.QLabel(CLSDialog)
        self.snap_available_label.setGeometry(QtCore.QRect(320, 470, 71, 20))
        self.snap_available_label.setAlignment(QtCore.Qt.AlignCenter)
        self.snap_available_label.setObjectName("snap_available_label")
        self.snap_channel_label = QtWidgets.QLabel(CLSDialog)
        self.snap_channel_label.setGeometry(QtCore.QRect(366, 450, 61, 20))
        self.snap_channel_label.setAlignment(QtCore.Qt.AlignCenter)
        self.snap_channel_label.setObjectName("snap_channel_label")
        self.video_channel_label = QtWidgets.QLabel(CLSDialog)
        self.video_channel_label.setGeometry(QtCore.QRect(646, 450, 61, 20))
        self.video_channel_label.setAlignment(QtCore.Qt.AlignCenter)
        self.video_channel_label.setObjectName("video_channel_label")
        self.z_stack_used_list_view = QtWidgets.QListView(CLSDialog)
        self.z_stack_used_list_view.setGeometry(QtCore.QRect(150, 490, 71, 121))
        self.z_stack_used_list_view.setObjectName("z_stack_used_list_view")
        self.snap_used_label = QtWidgets.QLabel(CLSDialog)
        self.snap_used_label.setGeometry(QtCore.QRect(420, 470, 47, 13))
        self.snap_used_label.setAlignment(QtCore.Qt.AlignCenter)
        self.snap_used_label.setObjectName("snap_used_label")
        self.video_used_list_view = QtWidgets.QListView(CLSDialog)
        self.video_used_list_view.setGeometry(QtCore.QRect(690, 490, 71, 121))
        self.video_used_list_view.setObjectName("video_used_list_view")
        self.available_z_stack_label = QtWidgets.QLabel(CLSDialog)
        self.available_z_stack_label.setGeometry(QtCore.QRect(66, 470, 51, 20))
        self.available_z_stack_label.setAlignment(QtCore.Qt.AlignCenter)
        self.available_z_stack_label.setObjectName("available_z_stack_label")
        self.snap_used_list_view = QtWidgets.QListView(CLSDialog)
        self.snap_used_list_view.setGeometry(QtCore.QRect(410, 490, 71, 121))
        self.snap_used_list_view.setObjectName("snap_used_list_view")
        self.z_stack_channel_label = QtWidgets.QLabel(CLSDialog)
        self.z_stack_channel_label.setGeometry(QtCore.QRect(116, 450, 51, 20))
        self.z_stack_channel_label.setAlignment(QtCore.Qt.AlignCenter)
        self.z_stack_channel_label.setObjectName("z_stack_channel_label")
        self.snap_available_list_view = QtWidgets.QListView(CLSDialog)
        self.snap_available_list_view.setGeometry(QtCore.QRect(320, 490, 71, 121))
        self.snap_available_list_view.setObjectName("snap_available_list_view")
        self.video_available_label = QtWidgets.QLabel(CLSDialog)
        self.video_available_label.setGeometry(QtCore.QRect(600, 470, 71, 20))
        self.video_available_label.setAlignment(QtCore.Qt.AlignCenter)
        self.video_available_label.setObjectName("video_available_label")
        self.video_available_list_view = QtWidgets.QListView(CLSDialog)
        self.video_available_list_view.setGeometry(QtCore.QRect(600, 490, 71, 121))
        self.video_available_list_view.setObjectName("video_available_list_view")
        self.copy_region_button = QtWidgets.QPushButton(CLSDialog)
        self.copy_region_button.setGeometry(QtCore.QRect(154, 170, 91, 23))
        self.copy_region_button.setObjectName("copy_region_button")
        self.paste_region_button = QtWidgets.QPushButton(CLSDialog)
        self.paste_region_button.setGeometry(QtCore.QRect(154, 200, 91, 23))
        self.paste_region_button.setObjectName("paste_region_button")
        self.set_z_start_button = QtWidgets.QPushButton(CLSDialog)
        self.set_z_start_button.setGeometry(QtCore.QRect(10, 360, 41, 23))
        self.set_z_start_button.setObjectName("set_z_start_button")
        self.set_z_end_button = QtWidgets.QPushButton(CLSDialog)
        self.set_z_end_button.setGeometry(QtCore.QRect(10, 390, 41, 23))
        self.set_z_end_button.setObjectName("set_z_end_button")
        self.go_to_button = QtWidgets.QPushButton(CLSDialog)
        self.go_to_button.setGeometry(QtCore.QRect(380, 110, 75, 23))
        self.go_to_button.setObjectName("go_to_button")
        self.z_stack_check_box = QtWidgets.QCheckBox(CLSDialog)
        self.z_stack_check_box.setGeometry(QtCore.QRect(100, 320, 70, 17))
        self.z_stack_check_box.setObjectName("z_stack_check_box")
        self.snap_check_box = QtWidgets.QCheckBox(CLSDialog)
        self.snap_check_box.setGeometry(QtCore.QRect(380, 320, 70, 17))
        self.snap_check_box.setObjectName("snap_check_box")
        self.video_check_box = QtWidgets.QCheckBox(CLSDialog)
        self.video_check_box.setGeometry(QtCore.QRect(670, 320, 70, 17))
        self.video_check_box.setObjectName("video_check_box")
        self.reset_joystick_button = QtWidgets.QPushButton(CLSDialog)
        self.reset_joystick_button.setGeometry(QtCore.QRect(600, 860, 111, 23))
        self.reset_joystick_button.setObjectName("reset_joystick_button")
        self.reset_stage_button = QtWidgets.QPushButton(CLSDialog)
        self.reset_stage_button.setGeometry(QtCore.QRect(120, 860, 111, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.reset_stage_button.setFont(font)
        self.reset_stage_button.setObjectName("reset_stage_button")

        self.retranslateUi(CLSDialog)
        QtCore.QMetaObject.connectSlotsByName(CLSDialog)

    def retranslateUi(self, CLSDialog):
        _translate = QtCore.QCoreApplication.translate
        CLSDialog.setWindowTitle(_translate("CLSDialog", "Dialog"))
        self.cls_region_label.setText(_translate("CLSDialog", "<html><head/><body><p><span style=\" font-size:20pt;\">CLS Region Setup</span></p></body></html>"))
        self.region_label.setText(_translate("CLSDialog", "Region 1"))
        self.sample_label.setText(_translate("CLSDialog", "Sample 1"))
        self.x_label.setText(_translate("CLSDialog", "X:"))
        self.y_label.setText(_translate("CLSDialog", "Y:"))
        self.z_label.setText(_translate("CLSDialog", "Z:"))
        self.set_region_button.setText(_translate("CLSDialog", "Set"))
        self.previous_sample_button.setText(_translate("CLSDialog", "Previous Sample"))
        self.previous_region_button.setText(_translate("CLSDialog", "Previous Region"))
        self.next_region_button.setText(_translate("CLSDialog", "Next Region"))
        self.next_sample_button.setText(_translate("CLSDialog", "Next Sample"))
        self.remove_region_button.setText(_translate("CLSDialog", "Remove Region"))
        self.snap_exposure_time_label.setText(_translate("CLSDialog", "Exposure Time:"))
        self.snap_exposure_unit_label.setText(_translate("CLSDialog", "ms"))
        self.start_z_label.setText(_translate("CLSDialog", "Start Z:"))
        self.end_z_label.setText(_translate("CLSDialog", "End Z:"))
        self.step_size_label.setText(_translate("CLSDialog", "Stepsize:"))
        self.start_z_unit_label.setText(_translate("CLSDialog", "um"))
        self.end_z_unit_label.setText(_translate("CLSDialog", "um"))
        self.step_size_unit_label.setText(_translate("CLSDialog", "um"))
        self.x_unit_label.setText(_translate("CLSDialog", "um"))
        self.y_unit_label.setText(_translate("CLSDialog", "um"))
        self.z_unit_label.setText(_translate("CLSDialog", "um"))
        self.video_exposure_unit_label.setText(_translate("CLSDialog", "ms"))
        self.video_exposure_time_label.setText(_translate("CLSDialog", "Exposure Time:"))
        self.video_duration_unit_label.setText(_translate("CLSDialog", "sec"))
        self.video_duration_label.setText(_translate("CLSDialog", "Duration:"))
        self.acquisition_setup_button.setText(_translate("CLSDialog", "Acquisition Setup"))
        self.video_used_label.setText(_translate("CLSDialog", "Used"))
        self.used_z_stack_label.setText(_translate("CLSDialog", "Used"))
        self.snap_available_label.setText(_translate("CLSDialog", "Available"))
        self.snap_channel_label.setText(_translate("CLSDialog", "Channels"))
        self.video_channel_label.setText(_translate("CLSDialog", "Channels"))
        self.snap_used_label.setText(_translate("CLSDialog", "Used"))
        self.available_z_stack_label.setText(_translate("CLSDialog", "Available"))
        self.z_stack_channel_label.setText(_translate("CLSDialog", "Channels"))
        self.video_available_label.setText(_translate("CLSDialog", "Available"))
        self.copy_region_button.setText(_translate("CLSDialog", "Copy Region"))
        self.paste_region_button.setText(_translate("CLSDialog", "Paste Region"))
        self.set_z_start_button.setText(_translate("CLSDialog", "Set"))
        self.set_z_end_button.setText(_translate("CLSDialog", "Set"))
        self.go_to_button.setText(_translate("CLSDialog", "Go To"))
        self.z_stack_check_box.setText(_translate("CLSDialog", "Z Stack"))
        self.snap_check_box.setText(_translate("CLSDialog", "Snap"))
        self.video_check_box.setText(_translate("CLSDialog", "Video"))
        self.reset_joystick_button.setText(_translate("CLSDialog", "Reset Joystick"))
        self.reset_stage_button.setText(_translate("CLSDialog", "Reset Stage"))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(511, 263)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lsfm_label = QtWidgets.QLabel(self.centralwidget)
        self.lsfm_label.setGeometry(QtCore.QRect(30, 0, 451, 61))
        self.lsfm_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lsfm_label.setObjectName("lsfm_label")
        self.cls_button = QtWidgets.QPushButton(self.centralwidget)
        self.cls_button.setGeometry(QtCore.QRect(200, 100, 111, 31))
        self.cls_button.setObjectName("cls_button")
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(200, 180, 111, 31))
        self.exit_button.setObjectName("exit_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 511, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lsfm_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Willamette LSFM Control Software</span></p></body></html>"))
        self.cls_button.setText(_translate("MainWindow", "CLS Setup"))
        self.exit_button.setText(_translate("MainWindow", "Exit"))

class Ui_ResetStageDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 176)
        self.reset_stage_label = QtWidgets.QLabel(Dialog)
        self.reset_stage_label.setGeometry(QtCore.QRect(40, -20, 311, 161))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.reset_stage_label.setFont(font)
        self.reset_stage_label.setAlignment(QtCore.Qt.AlignCenter)
        self.reset_stage_label.setWordWrap(True)
        self.reset_stage_label.setObjectName("reset_stage_label")
        self.yes_button = QtWidgets.QPushButton(Dialog)
        self.yes_button.setGeometry(QtCore.QRect(240, 130, 75, 23))
        self.yes_button.setObjectName("yes_button")
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        self.cancel_button.setGeometry(QtCore.QRect(80, 130, 75, 23))
        self.cancel_button.setObjectName("cancel_button")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.reset_stage_label.setText(_translate("Dialog", "Are you sure you want to reset the stage? Resetting the stage will set its origin position (0,0,0) to the current position, making all positions set in Region Setup obselete."))
        self.yes_button.setText(_translate("Dialog", "Yes"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))


class AbortDialog(QtWidgets.QDialog, Ui_AbortDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class AcquisitionDialog(QtWidgets.QDialog, Ui_AcquisitionDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class CLSDialog(QtWidgets.QDialog, Ui_CLSDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class CLSAcquisitionSettingsDialog(QtWidgets.QDialog, Ui_CLSAcquisitionSettingsDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class BrowseDialog(QtWidgets.QFileDialog):
    def __init__(self):
        super().__init__()

class ResetStageDialog(QtWidgets.QDialog, Ui_ResetStageDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
