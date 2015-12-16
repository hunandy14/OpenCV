# ====================================================
# Name : WebCamera_Show
# ====================================================
import cv2
import urllib
import numpy as np
# ====================================================
def WebCamera_Init():
	global stream,bytes
	stream=urllib.urlopen('http://120.117.72.141:8080/?action=stream')
	bytes=''
# =======================
def WebCamera_Get():
	global stream,bytes,WebCamera
	bytes+=stream.read(1024)
	xd8 = bytes.find('\xff\xd8')
	xd9 = bytes.find('\xff\xd9')
	if xd8!=-1 and xd9!=-1:
		jpg = bytes[xd8:xd9+2]
		bytes= bytes[xd9+2:]
		WebCamera = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
		cv2.imshow('WebCamera',WebCamera)
# ====================================================
WebCamera_Init()
while True:
	WebCamera_Get()
	if cv2.waitKey(1) & 0xFF == 27:
		break
# =======================================================