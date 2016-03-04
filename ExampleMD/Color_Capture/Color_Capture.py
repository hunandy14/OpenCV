import cv2
import numpy as np
#create a VideoCapture object
cap = cv2.VideoCapture(0)

while(1):
    # Capture Video from Camera
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    # define range of green color in HSV 
    lower_green = np.array([50,100,100])
    upper_green = np.array([70,255,255])
    # define range of red color in HSV 
    lower_red = np.array([-10,100,100])
    upper_red = np.array([10,255,255])
    # Threshold the HSV image to get only blue colors
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    # Threshold the HSV image to get only green colors
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    # Threshold the HSV image to get only red colors   
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    # Bitwise-AND mask and original image
    res_blue = cv2.bitwise_and(frame,frame, mask= mask_blue)
    res_green = cv2.bitwise_and(frame,frame, mask= mask_green)
    res_red = cv2.bitwise_and(frame,frame, mask= mask_red)
    cv2.imshow('frame',frame)
    cv2.imshow('mask_blue)',mask_blue)
    cv2.imshow('mask_green',mask_green)
    cv2.imshow('mask_red',mask_red)

    cv2.imshow('res_blue',res_blue)
    cv2.imshow('res_green',res_green)
    cv2.imshow('res_red',res_red)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()