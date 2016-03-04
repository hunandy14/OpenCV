import cv2
import numpy as np
#=====================================================
def Create_Canvas_X():
    global Canvas
    Canvas_X=300
    Canvas_Y=100
    Canvas = np.zeros((Canvas_Y,Canvas_X,3), np.uint8)
    cv2.imwrite("IMG_RGB.png",Canvas)

def Load_Picture():
    global img
    img = cv2.imread('IMG_RGB.png')
    cv2.imshow('Get_Img_RGB',img)

def Drawing_Picture():
    global img
    for x in range(100):
        for y in range(100):
            img[y,x]=[0,0,255]
    for x in range(100):
        for y in range(100):
            img[y,x+100]=[0,255,0]
    for x in range(100):
        for y in range(100):
            img[y,x+200]=[255,0,0]
    cv2.imshow('Get_Img_RGB',img)
    cv2.imwrite("IMG_RGB.png",img)
def Print_RGB():
    # img[y.x]
    print "   (0,0)   RGB =",img[0,0]
    print " (100,0) RGB =",img[0,100]
    print " (200,0) RGB =",img[0,200]
    print ""
    # img = [B,G,R]
    print "(0,0) R=",img[0,0,2],"(0,0) G=",img[0,0,1],"(0,0) B=",img[0,0,0]
#=====================================================
Create_Canvas_X()
Load_Picture()
Drawing_Picture()
Print_RGB()
while True:
    k = cv2.waitKey(0) & 0xFF
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
#=====================================================