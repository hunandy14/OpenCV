import numpy as np
import cv2

RGB_value = np.uint8([[[255,0,0 ]]])
hsv_value = cv2.cvtColor(RGB_value,cv2.COLOR_BGR2HSV)
print hsv_value