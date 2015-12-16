import cv

in_image = 'kaffee.png'
out_image = 'kaffee_out.png'
out_image_thr = 'kaffee_thr.png'

ORANGE_MIN = cv.Scalar(18, 40, 90)
ORANGE_MAX = cv.Scalar(27, 255, 255)
COLOR_MIN = ORANGE_MIN
COLOR_MAX = ORANGE_MAX

def test1():
    frame = cv.LoadImage(in_image)
    frameHSV = cv.CreateImage(cv.GetSize(frame), 8, 3)
    cv.CvtColor(frame, frameHSV, cv.CV_RGB2HSV)
    frame_threshed = cv.CreateImage(cv.GetSize(frameHSV), 8, 1)
    cv.InRangeS(frameHSV, COLOR_MIN, COLOR_MAX, frame_threshed)
    cv.SaveImage(out_image_thr, frame_threshed)