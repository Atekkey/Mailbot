# FROM: https://builtin.com/data-science/python-ocr
from PIL import Image
import pytesseract
import numpy as np
import cv2

globalIsOnComputer = False

def imageToText(img):
    img = np.array(img)
    norm_img = np.zeros((img.shape[0], img.shape[1]))
    img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
    # print("1--")
    img = cv2.GaussianBlur(img, (1, 1), 0)
    # print("2--")
    text = pytesseract.image_to_string(img)
    # print("3--")
    # print("text: ", text, " --")
    return text


def checkForName(textIn):
    textIn = pList.preproccess(textIn)
    name = pList.strCompareToList1(textIn)
    if(name == ""):
        return ""
    else:
        return name
    

