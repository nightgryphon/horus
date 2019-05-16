# -*- coding: utf-8 -*-
# This file is part of the Horus Project

__author__ = 'Jesús Arroyo Torrens <jesus.arroyo@bq.com>'
__copyright__ = 'Copyright (C) 2014-2016 Mundo Reader S.L.'
__license__ = 'GNU General Public License v2 http://www.gnu.org/licenses/gpl2.html'


import wx._core

from horus.util import profile
from horus.gui.engine import driver, ciclop_scan, point_cloud_roi
from horus.gui.util.custom_panels import ExpandablePanel, Slider, CheckBox, ComboBox, \
    Button, FloatTextBox, DirPicker, IntTextBox, ColorPicker


class ScanParameters(ExpandablePanel):

    def __init__(self, parent, on_selected_callback):
        ExpandablePanel.__init__(
            self, parent, _("Scan parameters"), has_undo=False, has_restore=False)
        self.main = self.GetParent().GetParent().GetParent()

    def add_controls(self):
        self.add_control('use_laser', ComboBox)

    def update_callbacks(self):
        self.update_callback('use_laser', self.set_use_laser)

    def set_use_laser(self, value):
        ciclop_scan.set_use_left_laser(value == 'Left' or value == 'Both')
        ciclop_scan.set_use_right_laser(value == 'Right' or value == 'Both')

    def on_selected(self):
        self.main.scene_view._view_roi = False
        self.main.scene_view.queue_refresh()
        profile.settings['current_panel_scanning'] = 'scan_parameters'


class RotatingPlatform(ExpandablePanel):

    def __init__(self, parent, on_selected_callback):
        ExpandablePanel.__init__(
            self, parent, _("Rotating platform"), has_undo=False)
        self.main = self.GetParent().GetParent().GetParent()

    def add_controls(self):
        self.add_control(
            'show_center', CheckBox,
            _("Shows the center of the platform using the "
              "current calibration parameters"))
        self.add_control('motor_step_scanning', FloatTextBox)
        self.add_control('motor_speed_scanning', FloatTextBox)
        self.add_control('motor_acceleration_scanning', FloatTextBox)

    def update_callbacks(self):
        self.update_callback('show_center', point_cloud_roi.set_show_center)
        self.update_callback('motor_step_scanning', ciclop_scan.set_motor_step)
        self.update_callback('motor_speed_scanning', ciclop_scan.set_motor_speed)
        self.update_callback('motor_acceleration_scanning', ciclop_scan.set_motor_acceleration)

    def on_selected(self):
        self.main.scene_view._view_roi = False
        self.main.scene_view.queue_refresh()
        profile.settings['current_panel_scanning'] = 'rotating_platform'


class PointCloudROI(ExpandablePanel):

    def __init__(self, parent, on_selected_callback):
        ExpandablePanel.__init__(self, parent, _("Point cloud ROI"))
        self.main = self.GetParent().GetParent().GetParent()

    def add_controls(self):
        self.add_control(
            'use_roi', CheckBox,
            _("Use a Region Of Interest (ROI). "
              "This cylindrical region is the one being scanned. "
              "All information outside won't be taken into account "
              "during the scanning process"))

        if profile.settings.get_max_value('roi_diameter') < profile.settings['machine_diameter']:
            profile.settings.set_max_value('roi_diameter', profile.settings['machine_diameter']+50)
        if profile.settings.get_max_value('roi_height') < profile.settings['machine_height']:
            profile.settings.set_max_value('roi_height', profile.settings['machine_height']+50)

        self.add_control('roi_diameter', Slider)
        self.add_control('roi_height', Slider)
        # self.add_control('roi_depth', Slider)
        # self.add_control('roi_width', Slider)

    def update_callbacks(self):
        self.update_callback('use_roi', self._set_use_roi)
        self.update_callback('roi_diameter', self._set_roi_diameter)
        self.update_callback('roi_height', self._set_roi_height)

    def _set_use_roi(self, value):
        if driver.is_connected and profile.settings['current_panel_scanning'] == 'point_cloud_roi':
            point_cloud_roi.set_use_roi(value)
            if value:
                point_cloud_roi.set_diameter(profile.settings['roi_diameter'])
                point_cloud_roi.set_height(profile.settings['roi_height'])
            else:
                point_cloud_roi.set_diameter(profile.settings['machine_diameter'])
                point_cloud_roi.set_height(profile.settings['machine_height'])
            self.main.scene_view._view_roi = value
            self.main.scene_view.queue_refresh()

    def _set_roi_diameter(self, value):
        profile.settings['roi_diameter'] = value
        point_cloud_roi.set_diameter(profile.settings['roi_diameter'])
        self.main.scene_view.queue_refresh()

    def _set_roi_height(self, value):
        profile.settings['roi_height'] = value
        point_cloud_roi.set_height(profile.settings['roi_height'])
        self.main.scene_view.queue_refresh()

    def on_selected(self):
        if driver.is_connected:
            value = profile.settings['use_roi']
            self.main.scene_view._view_roi = value
            self.main.scene_view.queue_refresh()
        profile.settings['current_panel_scanning'] = 'point_cloud_roi'


class PointCloudColor(ExpandablePanel):

    def __init__(self, parent, on_selected_callback):
        ExpandablePanel.__init__(
            self, parent, _("Point cloud color"), has_undo=False, has_restore=False)
        self.main = self.GetParent().GetParent().GetParent()

    def add_controls(self):
        self.add_control('texture_mode', ComboBox)
        self.add_control('point_cloud_color', ColorPicker)
        self.add_control('point_cloud_color_l', ColorPicker)
        self.add_control('point_cloud_color_r', ColorPicker)

    def update_callbacks(self):
        self.update_callback('texture_mode', lambda v: self._set_texture_mode(v) )
        self.update_callback('point_cloud_color', ciclop_scan.set_color )
        self.update_callback('point_cloud_color_l', lambda v: ciclop_scan.set_colors(0,v) )
        self.update_callback('point_cloud_color_r', lambda v: ciclop_scan.set_colors(1,v) )

    def on_selected(self):
        self.main.scene_view._view_roi = False
        self.main.scene_view.queue_refresh()
        profile.settings['current_panel_scanning'] = 'point_cloud_color'

    def _set_texture_mode(self, mode):
        ciclop_scan.set_texture_mode(mode)

        self.get_control('point_cloud_color').Hide()
        self.get_control('point_cloud_color_l').Hide()
        self.get_control('point_cloud_color_r').Hide()

        if mode == 'Flat color':
            self.get_control('point_cloud_color').Show()
        elif mode == 'Multi color':
            self.get_control('point_cloud_color_l').Show()
            self.get_control('point_cloud_color_r').Show()
        elif mode == 'Capture':
            pass
        elif mode == 'Laser BG':
            pass
        else:
            pass

        self.parent.Layout()
        self.Layout()


class Photogrammetry(ExpandablePanel):

    def __init__(self, parent, on_selected_callback):
        ExpandablePanel.__init__(
            self, parent, _("Photogrammetry"), has_undo=False, has_restore=False)
        self.main = self.GetParent().GetParent().GetParent()

    def add_controls(self):
        self.add_control('ph_save_enable', CheckBox)
        self.add_control('ph_save_folder', DirPicker)
        self.add_control('ph_save_divider', IntTextBox)

    def on_selected(self):
        self.main.scene_view._view_roi = False
        self.main.scene_view.queue_refresh()
        profile.settings['current_panel_scanning'] = 'photogrammetry'
