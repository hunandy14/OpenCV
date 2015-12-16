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
	cv2.imshow("Only_Focus",Only_Focus)
	contours, hierarchy = cv2.findContours(Binarization ,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	return contours
# =======================
def Track_Target_Feature(img):
	global speed1,speed2
	# Transform_img get
	contours=Transform_img(img)
	Track_img=img

	points=[]
	if contours == []:
		print "No area"

	for cnt in contours:
		x,y,w,h = cv2.boundingRect(cnt)
		if w*h >=500 and w>10 and h>10:
			pt1 = (x,y)
			pt2 = (x+w,y+h)
			pt3 = (x+(w/2),y+(h/2))

			points.append(pt3)
			Center_points = len(points)
			print "Center_points=",Center_points
			print 'pt3=',pt3
			points.sort()

			# if Center_points == 1:
			# 	# px[Center_points]=pt3[0]
			# 	# py[Center_points]=pt3[1]
			# 	# print px[Center_points], py[Center_points]
			#         px1.append(pt3[0])
			#         py1.append(pt3[1])
			#         # print px1, py1
			#         # print "[px1,py1]=",px1,py1
			# print len(px1)
			# if  len(px1)>=70:
			#         count_speed(len(px1))

			# speed1 = 0
			# if len(px1)>=100:
			# 	del px1[0:31]
			# 	print "len(px1)=",len(px1)
			# if Center_points ==2:
			# 	px2.append(pt3[0])
			# 	py2.append(pt3[1])
			# 	# print "[px2,py2]=",px2,py2
			# if  len(px2)>=70:
			#         for j in xrange(len(px2)-30,len(px2)-1):
			#             # print i,"=","(",px2[i],",",py[i],")"
			#             distance_X = (px2[j+1]-px2[j])
			#             distance_Y = (py2[j+1]-py2[j])
			#             speed2 += math.sqrt((distance_X*distance_X)+(distance_Y*distance_Y))
			# print "speed2=",speed2
			# speed2 = 0
			# if len(px2)>=70:
			#         for i in range(len(px2)-31,0,-1):
			#              # print "i=",i
			#              px2[i]=''
			#              py2[i]=''

			print "------------------------------------"
			Track_img = Drawing_Track(x,y,w,h,Track_img,Center_points)
	cv2.imshow("Mlitiple_Tracks",Track_img)
# =======================
def Drawing_Track(x,y,w,h,img,Center_points):
	Track_img=img
	Drawing_TrackSTR(x,y,w,h,img,Center_points)
	cv2.circle(Track_img,(x+(w/2),y+(h/2)),5,(0,255,0),2)
	cv2.rectangle(Track_img,(x,y),(x+w,y+h),(255,0,0),2)
	cv2.circle(Track_img,(x,y),5,(0,0,255),2)
	cv2.circle(Track_img,(x+w,y+h),5,(0,0,255),2)
	return Track_img
# =======================
DT_Number=0
DT_Temp=0
def Drawing_TrackSTR(x,y,w,h,img,Center_points):
	global DT_Number,DT_Temp
	Target=int(Center_points)

	# if DT_Temp<Target:
	# 	DT_Temp=Target
	# 	DT_Number=DT_Number+1
	# 	print "*******************************"
	# else DT_Temp=>Target
	# 	DT_Temp=Target

	Number_STR=str(Center_points)
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(img,Number_STR,(x+(w/2)-10,y+(h/2)-10), font, 1,(0,0,0),2,cv2.CV_AA)
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
		img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
		Track_Target_Feature(img)
		# cv2.imshow('Orignal_Video',img)
# ====================================================
if __name__ == '__main__':
	global flag,distance_X1,distance_Y1,distance_X2,distance_Y2,speed1,speed2
	global point,px1,py1,px2,py2,px,py
	flag = distance_X1 = distance_Y1 = speed1 = distance_X2 = distance_Y2 = speed2 = 0
	# px = np.zeros((100,2),int)
	# py = np.zeros((100,2),int)
	point = []
	px1 = []
	py1 = []
	px2 = []
	py2 = []
	print "Start"
	WebCamera_Init()
# ====================================================
while True:
	WebCamera_Get()
	if cv2.waitKey(1) & 0xFF == 27:
		break
# ====================================================