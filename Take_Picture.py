import cv2
import time
import numpy.core.multiarray
# setup video capture
cap = cv2.VideoCapture(0)
gaussFlag = False
pic = None

while True:
    ret, im = cap.read() 
    blur = cv2.GaussianBlur(im, (0, 0), 5)

    if gaussFlag is True:
        cv2.imshow('camera', blur)
    else:
        cv2.imshow('camera', im)

    # key = cv2.waitKey(10)
    key = cv2.waitKey(5) & 0xFF
    if key == 27:
        break

    if key == ord('g'):
        if gaussFlag is True:
            gaussFlag = False
        else:
            gaussFlag = True

    if key == ord(' '):
        img_name = 'pic_cap_' + time.strftime('%Y-%m-%d %H-%M-%S') + '.jpg'
        if gaussFlag is False:
            cv2.imwrite(img_name, im)
        else:
            cv2.imwrite(img_name, blur)

cap.release()
cv2.destroyAllWindows()