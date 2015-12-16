# -*- coding: utf-8 -*-
# ====================================================
# FocusMulti_Drawing_4
# 已經完成功能，測試可用，備份檔案
# ====================================================
import cv2
import urllib
import numpy as np
import time
import math
# ====================================================
def Transform_img(img):
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	# cv2.imshow("HSV_Image",hsv)
	Lower_HSV = np.array([45,60,60])
	Upper_HSV = np.array([65,255,255])
	Binarization = cv2.inRange(hsv,Lower_HSV,Upper_HSV)
	Only_Focus = cv2.bitwise_and(img,img, mask= Binarization)
	# cv2.imshow("Binarization_Image",Binarization)
	# cv2.imshow("Only_Focus",Only_Focus)
	Contours_Array, hierarchy = cv2.findContours(Binarization ,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	return Contours_Array
# =======================
Target1=[]
Target2=[]
Target=[]
Target_StarFlag=1
def Track_Target_Feature(img):
	global Target_StarFlag
	global Target,Target1,Target2
	Contours_Array=Transform_img(img)
	points=[]
	No_Target=1
	if Contours_Array!=[]:
		for i in Contours_Array:
			x,y,w,h = cv2.boundingRect(i)
			if w*h >=100 and w>5 and h>5:
				pt1,pt2,pt3 = (x,y),(x+w,y+h),(x+(w/2),y+(h/2))
				points.append(pt3)
				Center_points = len(points)

				if Center_points==0:
					No_Target=1
				else:
					No_Target=0
				img = Drawing_Track(x,y,w,h,img,Center_points)
		print "========================================="
		Target_Track(points,img)
	cv2.imshow("Mlitiple_Tracks",img)
# =======================
Target_XY=[[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]]
def Target_Track(points,img):
	global TG_C,Target_Track,Target_XY
	Target_Distance=50
	font = cv2.FONT_HERSHEY_SIMPLEX
	Taget_Count(points)
	# 初始化_填入座標
	for i in range(0,len(points)):
		if Target_XY[i][0]==-1:
			Target_XY[i]=points[i]
	# 追蹤座標
	for j in range(0,len(Target_XY)):
		if Target_XY[j] != [-1]:
			for i in range(0,len(points)):
				if Point_Distance(Target_XY[j],points[i]) <=Target_Distance:
					Target_XY[j]=points[i]
	# 清除碰撞目標
	Target_XY_Q=0
	# 	計算有多少有效座標
	# for i in range(0,len(Target_XY)):
	# 	if Target_XY[i] != [-1]:
	# 		Target_XY_Q=Target_XY_Q+1
	# 	發生碰撞將數字較大的清除為"-1"
	for j in range(0,len(Target_XY)): #Target_XY_Q更動為len(Target_XY)
		if Target_XY[j] != [-1] :
			for i in range(j+1,len(Target_XY)):
				if Target_XY[i] != [-1] :
					if Target_XY[j]==Target_XY[i]:
						Target_XY[i]=[-1]
					# print "	j,i=",j,i
					# print "	Target_XY",Target_XY[j],Target_XY[i]
	print "Target_XY",Target_XY,"\n","\n"
	# 在影像上印出座標編號
	for j in range(0,len(Target_XY)):
		if Target_XY[j] != [-1]:
			for i in range(0,len(points)):
				if Point_Distance(Target_XY[j],points[i]) <=10:
					cv2.putText(img,str(j+1),(Target_XY[j][0]-10,Target_XY[j][1]+10), font, 1,(0,0,0),1,cv2.CV_AA)

# =======================
# TG_C[0] = New Taget++
# TG_C[2] = Loss Taget++
# TG_C[3] = Target quantity
TG_C=[0,0,0]
TG_C_Temp=0
def Taget_Count(points):
	global TG_C_Temp, TG_C,Target_Track,i
	if TG_C_Temp < len(points):
		TG_C[0]=TG_C[0] + (len(points)-TG_C_Temp)
	elif TG_C_Temp > len(points):
		TG_C[1]=TG_C[1] + (TG_C_Temp-len(points))
	TG_C_Temp=len(points)
	TG_C[2]=TG_C[0]-TG_C[1]
	return TG_C
# =======================
def Point_Distance (P1,P2):
	x=P1[0]-P2[0]
	y=P1[1]-P2[1]
	Distance=((x*x)+(y*y))**0.5
	return Distance
# =======================
def Drawing_Track(x,y,w,h,img,Center_points):
	Track_img=img
	# Drawing_TrackSTR(x,y,w,h,img,Center_points)
	# cv2.circle(Track_img,(x+(w/2),y+(h/2)),5,(0,255,0),2) # Center_circle
	cv2.rectangle(Track_img,(x,y),(x+w,y+h),(255,0,0),2)
	# cv2.circle(Track_img,(x,y),5,(0,0,255),2)
	# cv2.circle(Track_img,(x+w,y+h),5,(0,0,255),2)
	return Track_img
# =======================
def Drawing_TrackSTR(x,y,w,h,img,Center_points):
	Target=int(Center_points)
	Number_STR=str(Center_points)
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(img,Number_STR,(x+(w/2)-10,y+(h/2)-10), font, 1,(0,0,0),1,cv2.CV_AA)
# =======================
def count_speed(s):
	global speed1
	for j in xrange(s-30,s-1):
		# print i,"=","(",px1[i],",",py[i],")"
		distance_X = (px1[j+1]-px1[j])
		distance_Y = (py1[j+1]-py1[j])
		speed1 += math.sqrt((distance_X*distance_X)+(distance_Y*distance_Y))
	print "speed1=",speed1
# =======================
def WebCamera_Init():
	global stream,bytes
	stream=urllib.urlopen('http://120.117.72.141:8080/?action=stream')
	bytes=''
# =======================
def WebCamera_Get():
	global stream,bytes
	bytes+=stream.read(1024)
	xd8 = bytes.find('\xff\xd8')
	xd9 = bytes.find('\xff\xd9')
	if xd8!=-1 and xd9!=-1:
		jpg = bytes[xd8:xd9+2]
		bytes= bytes[xd9+2:]
		# Orignal_Video = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
		# cv2.imshow('Orignal_Video',Orignal_Video)
		img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
		Track_Target_Feature(img)
# ====================================================
if __name__ == '__main__':
	global flag,distance_X1,distance_Y1,distance_X2,distance_Y2,speed1,speed2
	global point,px1,py1,px2,py2,px,py
	flag = distance_X1 = distance_Y1 = speed1 = distance_X2 = distance_Y2 = speed2 = 0
	# px = np.zeros((100,2),int)
	# py = np.zeros((100,2),int)
	px1,py1,px2,py2,point = [],[],[],[],[]
	print "Start"
	WebCamera_Init()
# =======================
while True:
	WebCamera_Get()
	if cv2.waitKey(1) & 0xFF == 27:
		break
# ====================================================