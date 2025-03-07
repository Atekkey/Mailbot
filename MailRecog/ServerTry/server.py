# $ python3 -m http.server
# Run above in a separate terminal
globalIsOnComputer = True
import cv2
import socket
import pickle
import struct
import os
import time

import sys
sys.tracebacklimit = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if(globalIsOnComputer):
    server_socket.bind(('0.0.0.0', 8888)) # Switched from 0.0.0.0
else:
    server_socket.bind(('127.0.0.1', 8888)) # Switched from 0.0.0.0
server_socket.listen(5)
print("Server is listening...")
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} accepted")
cap = cv2.VideoCapture(0) # use 0

while True:
    ret, frame = cap.read()
    frame_data = pickle.dumps(frame)
    client_socket.sendall(struct.pack("Q", len(frame_data)))
    client_socket.sendall(frame_data)
    if globalIsOnComputer:
        try:
            cv2.imshow('Server', frame)
        except (Exception):
            pass

# cap.release()
# if globalIsOnComputer:
#     cv2.destroyAllWindows()
