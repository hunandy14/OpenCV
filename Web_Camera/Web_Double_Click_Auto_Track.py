# ====================================================
# Duble click GET:
    # HSV value
    # RGB value
    # (X,Y ) value

# DATA 2015/08/15
# By : Charlotte.HonG
# ====================================================
import cv2
import urllib
import numpy as np
# cap = cv2.VideoCapture(0)
# ==================================

# ====================================================
def init_windows():
    # ret = cap.set(3,320)
    # ret = cap.set(4,240)
    global Hl,Sl,Vl,Hu,Su,Vu,Revise_Flag
    global frame
    Hl=0
    Sl=50
    Vl=50
    Hu=180
    Su=200
    Vu=200
    Revise_Flag=0
    show_windows()
    cv2.setMouseCallback('frame',mouse_click)
# ==================================
def show_windows():
    global Hl,Sl,Vl,Hu,Su,Vu
    global frame
    # ret, frame = cap.read()
    WebCamera_Get()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array( [Hl,Sl,Vl] )
    upper_blue = np.array( [Hu,Su,Vu] )
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('frame',frame)
# ==================================
def print_hsv():
    print ("lower_blue = ",Hl,Sl,Vl)
    print ("upper_blue = ",Hu,Su,Vu)
    print ("=============================")
# ==================================
def take_picture():
    global img
    cv2.imwrite("HSV.png",frame)
    img = cv2.imread('HSV.png')
# ==================================
def get_rgb():
    global B,G,R
    BGR = img[iy,ix]
    B = img[iy,ix,0]
    G = img[iy,ix,1]
    R = img[iy,ix,2]
    print "RGB=",R,",",G,",",B
# ==================================
def mouse_click(event,x,y,flags,param):
    global ix,iy,drawing,mode
    global Hl,Sl,Vl,Hu,Su,Vu
    ix,iy = x,y
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print "X,Y = (",ix,",",iy,")"
        take_picture()
        get_rgb()
        RGB_to_HSV()
        Hl=HSV_value[0][0][0]-10
        Hu=HSV_value[0][0][0]+10
        # Sl=HSV_value[0][0][1]-50
        # Su=HSV_value[0][0][1]+50
        # Vl=HSV_value[0][0][2]-50
        # Vu=HSV_value[0][0][2]+50
        print_hsv()
# ==================================
def key_san():
    global key
    key = cv2.waitKey(5) & 0xFF
# ==================================
def RGB_to_HSV():
    global HSV_value
    RGB_value = np.uint8([[[B,G,R ]]])
    HSV_value = cv2.cvtColor(RGB_value,cv2.COLOR_BGR2HSV)
    # print "HSV=",HSV_value
    # print "HSV=",HSV_value[0][0]
    # print "H=",HSV_value[0][0][0]
    # print "S=",HSV_value[0][0][1]
    # print "V=",HSV_value[0][0][2]
# ==================================
def WebCamera_Init():
    global stream,bytes
    stream=urllib.urlopen('http://120.117.72.141:8080/?action=stream')
    bytes=''
# =======================
def WebCamera_Get():
    global stream,bytes,WebCamera,frame
    bytes+=stream.read(1024)
    xd8 = bytes.find('\xff\xd8')
    xd9 = bytes.find('\xff\xd9')
    if xd8!=-1 and xd9!=-1:
        jpg = bytes[xd8:xd9+2]
        bytes= bytes[xd9+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
        cv2.imshow('WebCamera',frame)
# ==================================
# ==================================
# ====================================================
#Main Program Start
# ====================================================
WebCamera_Init()
init_windows()
while True:
    show_windows()
    key_san()
    # Exit
    if key == 27 and Revise_Flag==0:
        break
    # Enter Revise
    if key == ord( ' ' ):
        print "Now revise Hl"
        Revise_Flag=1
        print_hsv()
    # Revise_H
    if Revise_Flag==1:
        if key == ord( 's' ):
            if Hl<Hu:
                Hl=Hl+1
            print_hsv()
        if key == ord( 'a' ):
            if Hl>0 :
                Hl=Hl-1
            print_hsv()
        if key == ord( 'x' ):
            if Hu<180:
                Hu=Hu+1
            print_hsv()
        if key == ord( 'z' ):
            if Hu>Hl :
                Hu=Hu-1
            print_hsv()
        # Revise_S
        if key == ord( 'f' ):
            if Sl<Su :
                Sl=Sl+1
            print_hsv()
        if key == ord( 'd' ):
            if Sl>0 :
                Sl=Sl-1
            print_hsv()
        if key == ord( 'v' ):
            if Su<255:
                Su=Su+1
            print_hsv()
        if key == ord( 'c' ):
            if Su>Sl:
                Su=Su-1
            print_hsv()
        # Revise_V
        if key == ord( 'h' ):
            if Vl<Vu :
                Vl=Vl+1
            print_hsv()
        if key == ord( 'g' ):
            if Vl>0 :
                Vl=Vl-1
            print_hsv()
        if key == ord( 'n' ):
            if Vu<255:
                Vu=Vu+1
            print_hsv()
        if key == ord( 'b' ):
            if Vu>Vl:
                Vu=Vu-1
            print_hsv()
        if key == 27 :
            Revise_Flag=0
            print "Revise end"
cv2.destroyAllWindows()
# ====================================================