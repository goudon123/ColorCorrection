import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

#######################################################################################
#https://github.com/lighttransport/colorcorrectionmatrix

def gamma_table(gamma_r, gamma_g, gamma_b, gain_r=1.0, gain_g=1.0, gain_b=1.0):
    r_tbl = [min(255, int((x / 255.) ** (gamma_r) * gain_r * 255.)) for x in range(256)]
    g_tbl = [min(255, int((x / 255.) ** (gamma_g) * gain_g * 255.)) for x in range(256)]
    b_tbl = [min(255, int((x / 255.) ** (gamma_b) * gain_b * 255.)) for x in range(256)]
    return r_tbl + g_tbl + b_tbl

def deGamma(img, gamma=2.2):
    return img.point(gamma_table(gamma, gamma, gamma))

def sRGB2XYZ(img):
    # D50
    rgb2xyz = (0.4360747,  0.3850649 , 0.1430804,0,
               0.2225045,  0.7168786,  0.0606169,0,
               0.0139322,  0.0971045,  0.7141733,0)
    return img.convert("RGB", rgb2xyz)


def correctColor(img, ccm):
    return img.convert("RGB", tuple(ccm.transpose().flatten()))

def XYZ2sRGB(img):
    # D50
    xyz2rgb = (3.1338561, -1.6168667 ,-0.4906146,0,
               -0.9787684 , 1.9161415, 0.0334540, 0,
               0.0719453, -0.2289914 , 1.4052427,0)
    return img.convert("RGB", xyz2rgb)

def applyGamma(img, gamma=2.2):
    inv_gamma = 1. / gamma
    return img.point(gamma_table(inv_gamma, inv_gamma, inv_gamma))
#######################################################################################
#https://www.pythonf.cn/read/173225
#https://chowdera.com/2020/12/20201211100511430e.html

image = cv2.imread('/hdr/without.jpeg')
detector = cv2.mcc.CCheckerDetector_create()
detector.process(image, cv2.mcc.MCC24, 1)

checkers = detector.getListColorChecker()
for checker in checkers:
    cdraw = cv2.mcc.CCheckerDraw_create(checker)
    img_draw = image.copy()
    cdraw.draw(img_draw)
    
    chartsRGB = checker.getChartsRGB()
    width, height = chartsRGB.shape[:2]
    roi = chartsRGB[0:width,1]
    print (roi)
    rows = int(roi.shape[:1][0])
    src = chartsRGB[:,1].copy().reshape(int(rows/3), 1, 3)
    src /= 255


    model = cv2.ccm_ColorCorrectionModel(src, cv2.ccm.COLORCHECKER_Macbeth)
    model.setColorSpace(cv2.ccm.COLOR_SPACE_sRGB)
    model.setCCM_TYPE(cv2.ccm.CCM_3x3)
    model.setDistance(cv2.ccm.DISTANCE_CIE2000)
    model.setLinear(cv2.ccm.LINEARIZATION_GAMMA)
    model.setLinearGamma(2.2)
    model.setLinearDegree(3)
    model.setSaturatedThreshold(0, 0.98)
    model.run()

    ccm = model.getCCM()
    row = [1,1,1]
    ccm = np.vstack([ccm, row])

    print ('ccm:\n{}\n'.format(ccm))
    loss = model.getLoss()
    print ('loss:\n{}\n'.format(loss))



###############################################################################################
  #  input_img = Image.open('download.jpeg', 'r').convert("RGB")
  #  input_img = deGamma(input_img, gamma=2.2)
  #  input_img = sRGB2XYZ(input_img)
  #  input_img = correctColor(input_img, ccm)
  #  input_img = XYZ2sRGB(input_img)
  #  out_img = applyGamma(input_img, gamma=2.2)
  #  input_img.save('output.jpg');
###############################################################################################
    #img = cv2.imread('with.jpeg')
    img_ = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_ = img_.astype(np.float64)
    img_ = img_/255
    calibratedImage = model.infer(img_)
    out_ = calibratedImage * 255
    out_[out_ < 0] = 0
    out_[out_ > 255] = 255
    out_ = out_.astype(np.uint8)
    out_ = cv2.cvtColor(out_, cv2.COLOR_RGB2BGR)

    cv2.imshow('out_img', out_)
    cv2.imshow("Image",image)
    cv2.imshow('img_draw', img_draw)
   # input_img.show()
    cv2.waitKey(0)

    cv2.destroyAllWindows()
