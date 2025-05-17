import cv2
import socket
import pickle
import struct
from functions import *
import pytesseract
import os

import sys
sys.tracebacklimit = 0
globalIsOnComputer = True

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if(globalIsOnComputer):
    client_socket.connect(('0.0.0.0', 8888))  
else:
    client_socket.connect(('127.0.0.1', 8888))  
data = b""
payload_size = struct.calcsize("Q")
print("Client connected")

i = 0
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # 4K buffer size
        if not packet:
            break
        data += packet
    if not data:
        break
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)  # 4K buffer size
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    i+=1
    if(i % 40 != 0): # KEEP very helpful, kills the delay
        continue
    try:
        if globalIsOnComputer:
            cv2.imshow('Client', frame)
        text = imageToText(frame)
        name = checkForName(text)
        if(name != ""):
            print("\nNAME FOUND: ", name)
    except Exception as e:
        print(e)
        pass

    
# cv2.destroyAllWindows()
