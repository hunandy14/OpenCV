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
TG_C_Temp=0
TG_C=0
def Track_Target_Feature(img):
	global Target_StarFlag,TG_C_Temp,TG_C
	global Target,Target1,Target2
	Contours_Array=Transform_img(img)
	points=[]
	No_Target=1
	if Contours_Array!=[]:
		print "Start"
		for i in Contours_Array:
			x,y,w,h = cv2.boundingRect(i)
			if w*h >=500 and w>10 and h>10:
				pt1,pt2,pt3 = (x,y),(x+w,y+h),(x+(w/2),y+(h/2))
				points.append(pt3)
				Center_points = len(points)

				if Center_points==0:
					No_Target=1
				else:
					No_Target=0

				# if TG_C_Temp<=Center_points:
				# 	TG_C=TG_C+1
				# 	TG_C_Temp=Center_points
				# print "TG_C=",TG_C
				print "Points_Amount =",Center_points
				print "Center_Point  = ",pt3
				print "========================="
				# ======Target1======
				if Target1==[] and Center_points>=1:
					Target1=pt3
				if len(Target1) == 2:
					if Point_Distance(Target1,pt3) <=50:
						Target1=pt3
						# print "Target1",Target1
						font = cv2.FONT_HERSHEY_SIMPLEX
						cv2.putText(img,"1",(Target1[0]-10,Target1[1]+10), font, 1,(0,0,0),1,cv2.CV_AA)
				# ======Target1======
				# ======Target2======
				if Target2==[] and Center_points>=2:
					Target2=pt3
				if len(Target2) == 2:
					# print "Target2",Target2
					if Point_Distance(Target2,pt3) <=50:
						Target2=pt3
						font = cv2.FONT_HERSHEY_SIMPLEX
						cv2.putText(img,"2",(Target2[0]-10,Target2[1]+10), font, 1,(0,0,0),1,cv2.CV_AA)
				# ======Target2======
				# if target tough reset
				if len(Target1) == 2 and len(Target2) == 2:
					if Point_Distance(Target1,Target2)<=50:
						print "Tough"
						Target1=[]
						Target2=[]
				# if no target reset
				# img = Drawing_Track(x,y,w,h,img,Center_points)
		# print '	points',points
		# cv2.circle(img,(points[0][0],points[0][1]),5,(0,0,255),2)

	if No_Target==1:
		print "No_Target"
		Target1=[]
		Target2=[]
	print "Target1",Target1
	print "Target2",Target2
	cv2.imshow("Mlitiple_Tracks",img)
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