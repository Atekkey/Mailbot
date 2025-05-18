# $ python3 -m http.server
# Run above in a separate terminal
globalIsOnComputer = True
import cv2
import socket
import pickle
import struct
import os
import time
import signal
import sys

# print("Scanner, PID: ", str(os.getpid()))

sys.tracebacklimit = 0
cap = None
def signal_handler(sig, frame):
    # print("KILLED")
    if cap is not None:
        cap.release()
    exit(0)

signal.signal(signal.SIGPIPE, signal.SIG_IGN) # Ignore SIGPIPE
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if(globalIsOnComputer):
    server_socket.bind(('0.0.0.0', 8888)) # Switched from 0.0.0.0
else:
    server_socket.bind(('127.0.0.1', 8888)) # Switched from 0.0.0.0
server_socket.listen(5)
# print("Server is listening...")
client_socket, client_address = server_socket.accept()
# print(f"Connection from {client_address} accepted")

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

# if globalIsOnComputer:
#     cv2.destroyAllWindows()
