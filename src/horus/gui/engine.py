# -*- coding: utf-8 -*-
# This file is part of the Horus Project

__author__ = 'Jesús Arroyo Torrens <jesus.arroyo@bq.com>'
__copyright__ = 'Copyright (C) 2014-2016 Mundo Reader S.L.'
__license__ = 'GNU General Public License v2 http://www.gnu.org/licenses/gpl2.html'

#from horus.engine.driver.driver import Driver
from horus.engine.driver.driver import driver
from horus.engine.scan.ciclop_scan import CiclopScan
from horus.engine.scan.current_video import CurrentVideo
from horus.engine.calibration.pattern import pattern
from horus.engine.calibration.calibration_data import calibration_data
from horus.engine.calibration.camera_intrinsics import CameraIntrinsics
from horus.engine.calibration.autocheck import Autocheck
from horus.engine.calibration.laser_triangulation import LaserTriangulation
from horus.engine.calibration.platform_extrinsics import PlatformExtrinsics
from horus.engine.calibration.combo_calibration import ComboCalibration
#from horus.engine.calibration.cloud_correction import CloudCorrection

from horus.engine.algorithms.image_capture import ImageCapture
from horus.engine.algorithms.image_detection import ImageDetection
from horus.engine.algorithms.aruco_detection import aruco_detection
from horus.engine.algorithms.laser_segmentation import LaserSegmentation
from horus.engine.algorithms.point_cloud_generation import PointCloudGeneration
from horus.engine.algorithms.point_cloud_roi import PointCloudROI


# Instances of engine modules

#driver = Driver()
ciclop_scan = CiclopScan()
current_video = CurrentVideo() # no params
#pattern = Pattern()
#calibration_data = CalibrationData()
camera_intrinsics = CameraIntrinsics() # no params
scanner_autocheck = Autocheck() # no params
laser_triangulation = LaserTriangulation()
platform_extrinsics = PlatformExtrinsics()
combo_calibration = ComboCalibration()
image_capture = ImageCapture()
image_detection = ImageDetection() # no params
laser_segmentation = LaserSegmentation()
point_cloud_generation = PointCloudGeneration() # no params
point_cloud_roi = PointCloudROI()
#cloud_correction = CloudCorrection()
