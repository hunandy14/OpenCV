# -*- coding: utf-8 -*-
# ====================================================
# FocusMulti_Drawing_5
# ====================================================
import cv2
import urllib
import numpy as np
import time
import math
# ====================================================
# 將影像過慮剩下指定區域內的顏色，並回傳該顏色的周圍輪廓的點
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
# 利用輪廓取得輪廓最左上與最右下的點，並計算其中心點
def Track_Target_Feature(img):
	Contours_Array=Transform_img(img)
	points=[]
	No_Target=1
	if Contours_Array!=[]:
		for i in Contours_Array:
			x,y,w,h = cv2.boundingRect(i)
			if w*h >=100 and w>5 and h>5:
				pt1,pt2,pt3 = (x,y),(x+w,y+h),(x+(w/2),y+(h/2))
				points.append(pt3)
				if len(points) == 0:
					No_Target = 1
				else:
					No_Target = 0
				img = Drawing_Track(x,y,w,h,img,len(points))
		Target_Track(points,img)
		print "========================================================="
	cv2.imshow("Mlitiple_Tracks",img)
# =======================
# 座標匯入的陣列，並避免跳動
Target_XY=[[-1],[-1],[-1],[-1],[-1],[-1],[-1]]
Target_Speed=[0,0,0,0,0]
TS_i=0
def Target_Track(points,img):
	global TG_C, Target_Track, Target_XY
	global Target_Speed, TS_i
	Target_Distance=50
	font = cv2.FONT_HERSHEY_SIMPLEX
	Taget_Count(points)
	# 初始化_填入座標
	# 	檢查points是否有跟Target_XY裏面的任何一個相同
	for j in range(0,len(points)):
		NewTarget_Flag=1
		# 檢查是否有相同的，如沒有就標記本次的J
		for i in range(0,len(Target_XY)):
			# print "points=",[j],points,"Target_XY=",[i],Target_XY[i]
			# 已經找到相同的座標，下面的不用找了
			if points[j] == Target_XY[i] :
				NewTarget_Flag=0
				break
		# 如果J有被標記，將目前的J值輸入有-1的地方
		if NewTarget_Flag==1:
			# print "ADD"
			# 尋找有-1的標記，將座標加入
			for k in range(0,len(Target_XY)):
				if Target_XY[k]==[-1]:
					Target_XY[k]=points[j]
	# 追蹤座標

	for j in range(0,len(Target_XY)):
		if Target_XY[j] != [-1]:
			for i in range(0,len(points)):
				if Point_Distance(Target_XY[j],points[i]) <=Target_Distance:

					if j==0:
						Speed=Point_Distance(Target_XY[j],points[i])
						Target_Speed[TS_i]=Speed
						# print "Speed",j+1,"=",Speed
						print "Target_Speed=",Target_Speed,"\n"
						print "Target_Speed",sum(Target_Speed)
						# print "	TS_i=",TS_i
						TS_i=TS_i+1
						if TS_i>=5:
							TS_i=0
					# 清除需放在最後面
					Target_XY[j]=points[i]
	# 清除碰撞目標
	for j in range(0,len(Target_XY)):
		if Target_XY[j] != [-1] :
			for i in range(j+1,len(Target_XY)):
				if Target_XY[i] != [-1] :
					if Point_Distance(Target_XY[j],Target_XY[i]) <=5:
						Target_XY[i]=[-1]
	# 丟失所有目標後重置
	if len(points)==0:
		print "No_Target"
		for i in range(0,len(Target_XY)):
			Target_XY[i]=[-1]
	# 在影像上印出座標編號
	for j in range(0,len(Target_XY)):
		if Target_XY[j] != [-1]:
			for i in range(0,len(points)):
				if Point_Distance(Target_XY[j],points[i]) <=5:
					cv2.putText(img,str(j+1),(Target_XY[j][0]-10,Target_XY[j][1]+10), font, 1,(0,0,0),1,cv2.CV_AA)
	print "Target_XY",Target_XY
	return Target_XY
# =======================
# 檢測是否有心座標加入，是否有座標遺失，目前有幾個座標
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
# 取得座標距離
def Point_Distance (P1,P2):
	x=P1[0]-P2[0]
	y=P1[1]-P2[1]
	Distance=((x*x)+(y*y))**0.5
	return Distance
# =======================
def Drawing_Track(x,y,w,h,img,Points_Amount):
	Track_img=img
	# Drawing_TrackSTR(x,y,w,h,img,Points_Amount)
	# cv2.circle(Track_img,(x+(w/2),y+(h/2)),5,(0,255,0),2) # Center_circle
	cv2.rectangle(Track_img,(x,y),(x+w,y+h),(255,0,0),2)
	# cv2.circle(Track_img,(x,y),5,(0,0,255),2)
	# cv2.circle(Track_img,(x+w,y+h),5,(0,0,255),2)
	return Track_img
# =======================
# 在座標點上標記圖形
def Drawing_TrackSTR(x,y,w,h,img,Points_Amount):
	Target=int(Points_Amount)
	Number_STR=str(Points_Amount)
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(img,Number_STR,(x+(w/2)-10,y+(h/2)-10), font, 1,(0,0,0),1,cv2.CV_AA)
# =======================
# 初始化網路影像，設定網路IP
def WebCamera_Init():
	global stream,bytes
	stream=urllib.urlopen('http://120.117.72.141:8080/?action=stream')
	bytes=''
# =======================
# 取得網路影像
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
#主程式開始
if __name__ == '__main__':
	WebCamera_Init()
# =======================
while True:
	WebCamera_Get()
	# ESC離開
	if cv2.waitKey(1) & 0xFF == 27:
		break
# ====================================================