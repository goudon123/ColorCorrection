# ColorCorrection
This is working on the Color Correction Calibration with 24-Color Patch ColorChecker board

There are three different methods of ColorCorrection

(a) ColorCorrection using Photo Editor Software(ON1 Photo Raw 2022)

(b) ColorCorrection using Imatest Software

(c) ColorCorrection using OpenCV




# (a) ColorCorrection using ON1 Photo Raw 2022

This method is to use the X-Rite Camera Calibration Tool to create a Camera Profile by converting a RAW file (TIFF format) into standard ICC Profile, then a Ultimate Photo Editor,ON1 Photo Raw software is use for color correction by utilise the Camera Profile generated from X-Rite tool, and other images is sync by using the Camera Profile.

Detail Implementation is described in ColorCorrection_ON1Software_Sync.docx



Required Software : 

X-Rite Camera Calibration Tool

https://www.xrite.com/service-support/downloads/c/colorchecker_camera_calibration_v2_2_0

On1 Photo Raw 2022 

https://www.on1.com/products/photo-raw/download


# (b) ColorCorrection using Imatest Software

Imatest is a software that provides customers with charts and equipment to meet and exceed image quality testing standards, and test the image capture technology.
There are two methods for color correction.

(i) Color Correction using Imatest Software by following the steps described on the link
https://www.imatest.com/docs/colormatrix/

(ii) Color Correction using Imatest Software to calculate the ColorCorrectionMatrix(CCM), and correct given image using CCM (PYTHON)

Detail Implementation is described in ColorCorrection_Imatest.docx 

ColorCorrection Code: https://github.com/goudon123/colorcorrectionmatrix

It is forked version from https://github.com/lighttransport/colorcorrectionmatrix

Required Software : 

Imatest Master

https://www.imatest.com/support/download/


# (c) ColorCorrection using OpenCV

Macbeth ColorChecker is used as a reference model to compute the 3x3 Color Correction Matrix to correct the input image color.

Code is inside the OpenCV_ColorCorrect Folder



