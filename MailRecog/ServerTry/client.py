import cv2
import socket
import pickle
import struct
from functions import *
import pytesseract
import os
print("Reach0")
print("Reach1")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('0.0.0.0', 8888))  # Replace 'server_ip_address' with the actual server IP
data = b""
payload_size = struct.calcsize("Q")
print("Client connected")

# while True:
#     while len(data) < payload_size:
#         packet = client_socket.recv(4 * 1024)  # 4K buffer size
#         if not packet:
#             break
#         data += packet
#     if not data:
#         break
#     packed_msg_size = data[:payload_size]
#     data = data[payload_size:]
#     msg_size = struct.unpack("Q", packed_msg_size)[0]
#     while len(data) < msg_size:
#         data += client_socket.recv(4 * 1024)  # 4K buffer size
#     frame_data = data[:msg_size]
#     data = data[msg_size:]
#     frame = pickle.loads(frame_data)
#     try:
#         cv2.imshow('Client', frame)
#         text = imageToText(frame)
#         name = checkForName(text)
        
#         if(name != ""):
#             os.system("echo " + name)
#             os.system("sleep 5 ")
#             # print(name)
#     except Exception as e:
#         # print(e)
#         pass
#     # if cv2.waitKey(1) == ord("a"): # Hold the a Key to quit, FIX!
#     #     break
# cv2.destroyAllWindows()
# print("Reach2")
cap = cv2.VideoCapture(0)

# Set resolution (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open video stream from USB camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow('USB Camera', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()