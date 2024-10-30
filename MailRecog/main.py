# pip install opencv-python
# pip install pytesseract
from PIL import Image
import pytesseract

import numpy as np
import cv2

# Yoinked from https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/
import cv2
import time as time

cam_port = 1
cam = cv2.VideoCapture(cam_port) 

# reading the input using the camera 
result, image = cam.read() 

if result: 

	cv2.imshow("Me", image) 

	cv2.imwrite("./outputs/Me.png", image) 

	cv2.waitKey(0) 
	cv2.destroyWindow("Me") 

else: 
	print("No image detected. Please! try again") 

