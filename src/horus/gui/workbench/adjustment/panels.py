# -*- coding: utf-8 -*-
# This file is part of the Horus Project

__author__ = 'Jesús Arroyo Torrens <jesus.arroyo@bq.com>'
__copyright__ = 'Copyright (C) 2014-2016 Mundo Reader S.L.'
__license__ = 'GNU General Public License v2 http://www.gnu.org/licenses/gpl2.html'

from horus.util import profile, system as sys

from horus.gui.engine import image_capture, laser_segmentation

from horus.gui.workbench.adjustment.current_video import CurrentVideo
from horus.gui.util.custom_panels import ExpandablePanel, Slider, ComboBox, CheckBox

current_video = CurrentVideo()


class ScanCapturePanel(ExpandablePanel):

    def __init__(self, parent, on_selected_callback):
        ExpandablePanel.__init__(self, parent, _("Scan capture"))

    def add_controls(self):
        self.add_control('capture_mode_scanning', ComboBox)
        self.add_control(
            'brightness_texture_scanning', Slider,
            _("Image luminosity. Low values are better for environments with high ambient "
              "light conditions. High values are recommended for poorly lit places"))
        self.add_control(
            'contrast_texture_scanning', Slider,
            _("Relative difference in intensity between an image point and its "
              "surroundings. Low values are recommended for black or very dark colored "
              "objects. High values are better for very light colored objects"))
        self.add_control(
            'saturation_texture_scanning', Slider,
            _("Purity of color. Low values will cause colors to disappear from the image. "
              "High values will show an image with very intense colors"))
        self.add_control(
            'exposure_texture_scanning', Slider,
            _("Amount of light per unit area. It is controlled by the time the camera "
              "sensor is exposed during a frame capture. "
              "High values are recommended for poorly lit places"))

        self.add_control(
            'light1_texture_scanning', Slider,
            _("Photo lamp 1 brightness"))
        self.add_control(
            'light2_texture_scanning', Slider,
            _("Photo lamp 2 brightness"))


        self.add_control(
            'brightness_laser_scanning', Slider,
            _("Image luminosity. Low values are better for environments with high ambient "
              "light conditions. High values are recommended for poorly lit places"))
        self.add_control(
            'contrast_laser_scanning', Slider,
            _("Relative difference in intensity between an image point and its "
              "surroundings. Low values are recommended for black or very dark colored "
              "objects. High values are better for very light colored objects"))
        self.add_control(
            'saturation_laser_scanning', Slider,
            _("Purity of color. Low values will cause colors to disappear from the image. "
              "High values will show an image with very intense colors"))
        self.add_control(
            'exposure_laser_scanning', Slider,
            _("Amount of light per unit area. It is controlled by the time the camera "
              "sensor is exposed during a frame capture. "
              "High values are recommended for poorly lit places"))

        self.add_control(
            'light1_laser_scanning', Slider,
            _("Photo lamp 1 brightness"))
        self.add_control(
            'light2_laser_scanning', Slider,
            _("Photo lamp 2 brightness"))

        self.add_control(
            'remove_background_scanning', CheckBox,
            _("Capture an extra image without laser to remove "
              "the background in the laser's image"))

        # Initial layout
        self._set_mode_layout(profile.settings['capture_mode_scanning'])

    def update_callbacks(self):
        self.update_callback('capture_mode_scanning', lambda v: self._set_camera_mode(v))

        mode = image_capture.texture_mode
        self.update_callback('brightness_texture_scanning', mode.set_brightness)
        self.update_callback('contrast_texture_scanning', mode.set_contrast)
        self.update_callback('saturation_texture_scanning', mode.set_saturation)
        self.update_callback('exposure_texture_scanning', mode.set_exposure)
        self.update_callback('light1_texture_scanning', lambda v: mode.set_light(1,v) )
        self.update_callback('light2_texture_scanning', lambda v: mode.set_light(2,v) )

        mode = image_capture.laser_mode
        self.update_callback('brightness_laser_scanning', mode.set_brightness)
        self.update_callback('contrast_laser_scanning', mode.set_contrast)
        self.update_callback('saturation_laser_scanning', mode.set_saturation)
        self.update_callback('exposure_laser_scanning', mode.set_exposure)
        self.update_callback('light1_laser_scanning', lambda v: mode.set_light(1,v) )
        self.update_callback('light2_laser_scanning', lambda v: mode.set_light(2,v) )
        self.update_callback('remove_background_scanning', image_capture.set_remove_background)

    def on_selected(self):
        current_video.updating = True
        current_video.sync()

        # Update mode settings
        current_video.calibration = False
        current_video.mode = profile.settings['capture_mode_scanning']

        image_capture.texture_mode.read_profile('texture_scanning')
        image_capture.laser_mode.read_profile('laser_scanning')
        image_capture.set_remove_background(profile.settings['remove_background_scanning'])

        profile.settings['current_video_mode_adjustment'] = current_video.mode
        profile.settings['current_panel_adjustment'] = 'scan_capture'

        current_video.flush()
        current_video.updating = False

    def _set_camera_mode(self, mode):
        current_video.updating = True
        current_video.sync()
        # Update mode settings
        self._set_mode_layout(mode)
        current_video.mode = mode
        profile.settings['current_video_mode_adjustment'] = current_video.mode
        current_video.flush()
        current_video.updating = False

    def _set_mode_layout(self, mode):
        if mode == 'Laser':
            self.get_control('brightness_texture_scanning').Hide()
            self.get_control('contrast_texture_scanning').Hide()
            self.get_control('saturation_texture_scanning').Hide()
            self.get_control('exposure_texture_scanning').Hide()
            self.get_control('light1_texture_scanning').Hide()
            self.get_control('light2_texture_scanning').Hide()

            self.get_control('brightness_laser_scanning').Show()
            self.get_control('contrast_laser_scanning').Show()
            self.get_control('saturation_laser_scanning').Show()
            self.get_control('exposure_laser_scanning').Show()
            self.get_control('light1_laser_scanning').Show()
            self.get_control('light2_laser_scanning').Show()
            self.get_control('remove_background_scanning').Show()

        elif mode == 'Texture':
            self.get_control('brightness_texture_scanning').Show()
            self.get_control('contrast_texture_scanning').Show()
            self.get_control('saturation_texture_scanning').Show()
            self.get_control('exposure_texture_scanning').Show()
            self.get_control('light1_texture_scanning').Show()
            self.get_control('light2_texture_scanning').Show()

            self.get_control('brightness_laser_scanning').Hide()
            self.get_control('contrast_laser_scanning').Hide()
            self.get_control('saturation_laser_scanning').Hide()
            self.get_control('exposure_laser_scanning').Hide()
            self.get_control('light1_laser_scanning').Hide()
            self.get_control('light2_laser_scanning').Hide()
            self.get_control('remove_background_scanning').Hide()

        if sys.is_wx30():
            self.content.SetSizerAndFit(self.content.vbox)
        if sys.is_windows():
            self.parent.Refresh()
        self.parent.Layout()
        self.Layout()


class ScanSegmentationPanel(ExpandablePanel):

    def __init__(self, parent, on_selected_callback):
        ExpandablePanel.__init__(self, parent, _("Scan segmentation"))

    def add_controls(self):
        # self.add_control('red_channel_scanning', ComboBox)
        self.add_control('draw_line_scanning', CheckBox)
        self.add_control(
            'threshold_value_scanning', Slider,
            _("Remove all pixels which intensity is less that the threshold value"))
        self.add_control(
            'threshold_enable_scanning', CheckBox,
            _("Remove all pixels which intensity is less that the threshold value"))
        self.add_control(
            'blur_value_scanning', Slider,
            _("Blur with Normalized box filter. Kernel size: 2 * value + 1"))
        self.add_control(
            'blur_enable_scanning', CheckBox,
            _("Blur with Normalized box filter. Kernel size: 2 * value + 1"))
        self.add_control(
            'window_value_scanning', Slider,
            _("Filter pixels out of 2 * window value around the intensity peak"))
        self.add_control(
            'window_enable_scanning', CheckBox,
            _("Filter pixels out of 2 * window value around the intensity peak"))
        self.add_control('refinement_scanning', ComboBox)

    def update_callbacks(self):
        # self.update_callback('red_channel_scanning', laser_segmentation.set_red_channel)
        self.update_callback('draw_line_scanning', current_video.set_draw_line)
        self.update_callback('threshold_value_scanning', laser_segmentation.set_threshold_value)
        self.update_callback('threshold_enable_scanning', laser_segmentation.set_threshold_enable)
        self.update_callback('blur_value_scanning', laser_segmentation.set_blur_value)
        self.update_callback('blur_enable_scanning', laser_segmentation.set_blur_enable)
        self.update_callback('window_value_scanning', laser_segmentation.set_window_value)
        self.update_callback('window_enable_scanning', laser_segmentation.set_window_enable)
        self.update_callback('refinement_scanning', laser_segmentation.set_refinement_method)

    def on_selected(self):
        current_video.updating = True
        current_video.sync()

        # Update mode settings
        current_video.calibration = False
        current_video.mode = 'Gray'
        current_video.set_draw_line(profile.settings['draw_line_scanning'])

        image_capture.laser_mode.read_profile('laser_scanning')
        image_capture.set_remove_background(profile.settings['remove_background_scanning'])

        laser_segmentation.read_profile('scanning')

        profile.settings['current_video_mode_adjustment'] = current_video.mode
        profile.settings['current_panel_adjustment'] = 'scan_segmentation'
        current_video.flush()
        current_video.updating = False


class CalibrationCapturePanel(ExpandablePanel):

    def __init__(self, parent, on_selected_callback):
        ExpandablePanel.__init__(self, parent, _("Calibration capture"))

    def add_controls(self):
        self.add_control('capture_mode_calibration', ComboBox)
        self.add_control(
            'brightness_pattern_calibration', Slider,
            _("Image luminosity. Low values are better for environments with high ambient "
              "light conditions. High values are recommended for poorly lit places"))
        self.add_control(
            'contrast_pattern_calibration', Slider,
            _("Relative difference in intensity between an image point and its "
              "surroundings. Low values are recommended for black or very dark colored "
              "objects. High values are better for very light colored objects"))
        self.add_control(
            'saturation_pattern_calibration', Slider,
            _("Purity of color. Low values will cause colors to disappear from the image. "
              "High values will show an image with very intense colors"))
        self.add_control(
            'exposure_pattern_calibration', Slider,
            _("Amount of light per unit area. It is controlled by the time the camera "
              "sensor is exposed during a frame capture. "
              "High values are recommended for poorly lit places"))

        self.add_control(
            'light1_pattern_calibration', Slider,
            _("Photo lamp 1 brightness"))
        self.add_control(
            'light2_pattern_calibration', Slider,
            _("Photo lamp 2 brightness"))


        self.add_control(
            'brightness_laser_calibration', Slider,
            _("Image luminosity. Low values are better for environments with high ambient "
              "light conditions. High values are recommended for poorly lit places"))
        self.add_control(
            'contrast_laser_calibration', Slider,
            _("Relative difference in intensity between an image point and its "
              "surroundings. Low values are recommended for black or very dark colored "
              "objects. High values are better for very light colored objects"))
        self.add_control(
            'saturation_laser_calibration', Slider,
            _("Purity of color. Low values will cause colors to disappear from the image. "
              "High values will show an image with very intense colors"))
        self.add_control(
            'exposure_laser_calibration', Slider,
            _("Amount of light per unit area. It is controlled by the time the camera "
              "sensor is exposed during a frame capture. "
              "High values are recommended for poorly lit places"))

        self.add_control(
            'light1_laser_calibration', Slider,
            _("Photo lamp 1 brightness"))
        self.add_control(
            'light2_laser_calibration', Slider,
            _("Photo lamp 2 brightness"))

        self.add_control(
            'remove_background_calibration', CheckBox,
            _("Capture an extra image without laser to remove "
              "the background in the laser's image"))

        # Initial layout
        self._set_mode_layout(profile.settings['capture_mode_calibration'])

    def update_callbacks(self):
        self.update_callback('capture_mode_calibration', lambda v: self._set_camera_mode(v))

        mode = image_capture.pattern_mode
        self.update_callback('brightness_pattern_calibration', mode.set_brightness)
        self.update_callback('contrast_pattern_calibration', mode.set_contrast)
        self.update_callback('saturation_pattern_calibration', mode.set_saturation)
        self.update_callback('exposure_pattern_calibration', mode.set_exposure)
        self.update_callback('light1_pattern_calibration', lambda v: mode.set_light(1,v) )
        self.update_callback('light2_pattern_calibration', lambda v: mode.set_light(2,v) )

        mode = image_capture.laser_mode
        self.update_callback('brightness_laser_calibration', mode.set_brightness)
        self.update_callback('contrast_laser_calibration', mode.set_contrast)
        self.update_callback('saturation_laser_calibration', mode.set_saturation)
        self.update_callback('exposure_laser_calibration', mode.set_exposure)
        self.update_callback('light1_laser_calibration', lambda v: mode.set_light(1,v) )
        self.update_callback('light2_laser_calibration', lambda v: mode.set_light(2,v) )
        self.update_callback('remove_background_calibration', image_capture.set_remove_background)

    def on_selected(self):
        current_video.updating = True
        current_video.sync()

        # Update mode settings
        current_video.calibration = True
        current_video.mode = profile.settings['capture_mode_calibration']

        image_capture.pattern_mode.read_profile('pattern_calibration')
        image_capture.laser_mode.read_profile('laser_calibration')
        image_capture.set_remove_background(profile.settings['remove_background_calibration'])

        profile.settings['current_video_mode_adjustment'] = current_video.mode
        profile.settings['current_panel_adjustment'] = 'calibration_capture'
        current_video.flush()
        current_video.updating = False

    def _set_camera_mode(self, mode):
        current_video.updating = True
        current_video.sync()
        # Update mode settings
        self._set_mode_layout(mode)
        current_video.mode = mode
        profile.settings['current_video_mode_adjustment'] = current_video.mode
        current_video.flush()
        current_video.updating = False

    def _set_mode_layout(self, mode):
        if mode == 'Laser':
            self.get_control('brightness_pattern_calibration').Hide()
            self.get_control('contrast_pattern_calibration').Hide()
            self.get_control('saturation_pattern_calibration').Hide()
            self.get_control('exposure_pattern_calibration').Hide()
            self.get_control('light1_pattern_calibration').Hide()
            self.get_control('light2_pattern_calibration').Hide()

            self.get_control('brightness_laser_calibration').Show()
            self.get_control('contrast_laser_calibration').Show()
            self.get_control('saturation_laser_calibration').Show()
            self.get_control('exposure_laser_calibration').Show()
            self.get_control('light1_laser_calibration').Show()
            self.get_control('light2_laser_calibration').Show()
            self.get_control('remove_background_calibration').Show()

        elif mode == 'Pattern':
            self.get_control('brightness_pattern_calibration').Show()
            self.get_control('contrast_pattern_calibration').Show()
            self.get_control('saturation_pattern_calibration').Show()
            self.get_control('exposure_pattern_calibration').Show()
            self.get_control('light1_pattern_calibration').Show()
            self.get_control('light2_pattern_calibration').Show()

            self.get_control('brightness_laser_calibration').Hide()
            self.get_control('contrast_laser_calibration').Hide()
            self.get_control('saturation_laser_calibration').Hide()
            self.get_control('exposure_laser_calibration').Hide()
            self.get_control('light1_laser_calibration').Hide()
            self.get_control('light2_laser_calibration').Hide()
            self.get_control('remove_background_calibration').Hide()

        if sys.is_wx30():
            self.content.SetSizerAndFit(self.content.vbox)
        if sys.is_windows():
            self.parent.Refresh()
        self.parent.Layout()
        self.Layout()


class CalibrationSegmentationPanel(ExpandablePanel):

    def __init__(self, parent, on_selected_callback):
        ExpandablePanel.__init__(self, parent, _("Calibration segmentation"))

    def add_controls(self):
        # self.add_control('red_channel_calibration', ComboBox)
        self.add_control(
            'threshold_value_calibration', Slider,
            _("Remove all pixels which intensity is less that the threshold value"))
        self.add_control(
            'threshold_enable_calibration', CheckBox,
            _("Remove all pixels which intensity is less that the threshold value"))
        self.add_control(
            'blur_value_calibration', Slider,
            _("Blur with Normalized box filter. Kernel size: 2 * value + 1"))
        self.add_control(
            'blur_enable_calibration', CheckBox,
            _("Blur with Normalized box filter. Kernel size: 2 * value + 1"))
        self.add_control(
            'window_value_calibration', Slider,
            _("Filter pixels out of 2 * window value around the intensity peak"))
        self.add_control(
            'window_enable_calibration', CheckBox,
            _("Filter pixels out of 2 * window value around the intensity peak"))
        self.add_control('refinement_calibration', ComboBox)

    def update_callbacks(self):
        # self.update_callback('red_channel_calibration', laser_segmentation.set_red_channel)
        self.update_callback('threshold_value_calibration', laser_segmentation.set_threshold_value)
        self.update_callback(
            'threshold_enable_calibration', laser_segmentation.set_threshold_enable)
        self.update_callback('blur_value_calibration', laser_segmentation.set_blur_value)
        self.update_callback('blur_enable_calibration', laser_segmentation.set_blur_enable)
        self.update_callback('window_value_calibration', laser_segmentation.set_window_value)
        self.update_callback('window_enable_calibration', laser_segmentation.set_window_enable)
        self.update_callback('refinement_calibration', laser_segmentation.set_refinement_method)

    def on_selected(self):
        current_video.updating = True
        current_video.sync()

        # Update mode settings
        current_video.calibration = True
        current_video.mode = 'Gray'

        image_capture.laser_mode.read_profile('laser_calibration')
        image_capture.set_remove_background(profile.settings['remove_background_calibration'])

        laser_segmentation.read_profile('calibration')

        profile.settings['current_video_mode_adjustment'] = current_video.mode
        profile.settings['current_panel_adjustment'] = 'calibration_segmentation'
        current_video.flush()
        current_video.updating = False
