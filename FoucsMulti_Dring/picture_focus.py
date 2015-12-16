import cv2
import numpy as np
def  track(frame):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('hsv',hsv)
    # define range of blue color in HSV
    lower_blue = np.array([105,50,50])
    upper_blue = np.array([117,200,200])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    moments = cv2.moments(mask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)#Take X coordinate
        centroid_y = int(moments['m01']/m00)#Take Y coordinate
    # print 'x=',centroid_x,
    # print 'y=',centroid_y

    if centroid_x != None and centroid_y !=None:
        ctr = (centroid_x, centroid_y)
        print ctr
        # Put black circle in at centroid in image
        cv2.circle(frame, ctr, 15, (0,0,255))
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('frame',frame)
    return ctr

#cv2.destroyAllWindows()
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

while True:
    # Take each frame
    ret, frame = cap.read()
    track(frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break
        cv2.destroyAllWindows()