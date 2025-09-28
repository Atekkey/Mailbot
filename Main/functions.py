# Help from: https://builtin.com/data-science/python-ocr
from PIL import Image
import pytesseract
import numpy as np
import cv2
import os

globalIsOnComputer = False

def imageToText(img):
    img = np.array(img)

    # Img Processing (See link above)
    norm_img = np.zeros((img.shape[0], img.shape[1]))
    img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
    img = cv2.GaussianBlur(img, (1, 1), 0) 

    # Img to Text
    text = pytesseract.image_to_string(img)
    return text
    
def fetchUID(): # Fetches the stored Init User ID from a text file
    path = "uid.txt"
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return ""

def setUID(uid): # Sets the Init User ID in a text file
    path = "uid.txt"
    with open(path, "w") as f:
        f.write(uid)