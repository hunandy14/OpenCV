import cv2
import urllib
import numpy as np
import time
import math

def track_Target_feature(img):
	global speed1,speed2
	#convert RGB to HSV
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	cv2.imshow("hsv",hsv)
	#range of red color on hsv BGR
	lower_Purple = np.array([45,60,60])
	upper_Purple = np.array([65,200,200])
	#hsv image to get only red colors and Anti-White
	Purple_Anti_White = cv2.inRange(hsv,lower_Purple,upper_Purple)
	cv2.imshow("Purple_Anti_White",Purple_Anti_White)
	#Find  contour
	contours, hierarchy = cv2.findContours(Purple_Anti_White,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.imshow("Find_contours",Purple_Anti_White)
	points=[]
	if contours == []:
		print "No area"
	for cnt in contours:
		x,y,w,h = cv2.boundingRect(cnt)
		if w*h >=150:
			pt1 = (x,y)
			pt2 = (x+w,y+h)
			pt3 = (x+(w/2),y+(h/2))

			points.append(pt3)
			Center_points = len(points)
			print "Center_points=",Center_points
			print 'pt3=',pt3
			points.sort()

			if Center_points == 1:
				# px[Center_points]=pt3[0]
				# py[Center_points]=pt3[1]
				# print px[Center_points], py[Center_points]
			        px1.append(pt3[0])
			        py1.append(pt3[1])
			        # print px1, py1
			        # print "[px1,py1]=",px1,py1
			print len(px1)
			if  len(px1)>=70:
			        count_speed(len(px1))

			speed1 = 0
			if len(px1)>=100:
				del px1[0:31]
				print "len(px1)=",len(px1)
			if Center_points ==2:
				px2.append(pt3[0])
				py2.append(pt3[1])
				# print "[px2,py2]=",px2,py2
			if  len(px2)>=70:
			        for j in xrange(len(px2)-30,len(px2)-1):
			            # print i,"=","(",px2[i],",",py[i],")"
			            distance_X = (px2[j+1]-px2[j])
			            distance_Y = (py2[j+1]-py2[j])
			            speed2 += math.sqrt((distance_X*distance_X)+(distance_Y*distance_Y))
			print "speed2=",speed2
			speed2 = 0
			if len(px2)>=70:
			        for i in range(len(px2)-31,0,-1):
			             # print "i=",i
			             px2[i]=''
			             py2[i]=''

			print "contours=",len(contours)
			print "------------------------------------"
			cv2.circle(img,(x+(w/2),y+(h/2)),5,(0,255,0),2)
			 # draw rectangle in blue color)
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			cv2.circle(img,(x,y),5,(0,0,255),2)
			cv2.circle(img,(x+w,y+h),5,(0,0,255),2)
	cv2.imshow("Mlitiple_tracks",img)
def count_speed(s):
	global speed1
	for j in xrange(s-30,s-1):
		# print i,"=","(",px1[i],",",py[i],")"
		distance_X = (px1[j+1]-px1[j])
		distance_Y = (py1[j+1]-py1[j])
		speed1 += math.sqrt((distance_X*distance_X)+(distance_Y*distance_Y))
	print "speed1=",speed1

stream=urllib.urlopen('http://120.117.72.141:8080/?action=stream')
bytes=''
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
# ====================================================
while True:
	bytes+=stream.read(1024)
	a = bytes.find('\xff\xd8')
	b = bytes.find('\xff\xd9')
	if a!=-1 and b!=-1:
		jpg = bytes[a:b+2]
		bytes= bytes[b+2:]
		img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
		track_Target_feature(img)
		# cv2.imshow('img',img)
	if cv2.waitKey(1) & 0xFF == 27:
		break