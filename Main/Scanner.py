globalIsOnComputer = False
import cv2
import socket
import pickle
import struct
import os
import time
import signal
import sys

sys.tracebacklimit = 0
cap = None

def signal_handler(sig, frame): # Safely kill this process
    if cap is not None:
        cap.release()
    exit(0)

signal.signal(signal.SIGPIPE, signal.SIG_IGN) # Ignore SIGPIPE
signal.signal(signal.SIGINT, signal_handler) # Handle Ctrl+C
signal.signal(signal.SIGTERM, signal_handler) # Handle Termination

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Init Socket

if(globalIsOnComputer): # If running locally for testing
    server_socket.bind(('0.0.0.0', 8888)) 
else:
    server_socket.bind(('127.0.0.1', 8888)) 

server_socket.listen(5) # Listens for connections

client_socket, client_address = server_socket.accept() # Accept a connection

cap = cv2.VideoCapture(0) # Init Camera

while True:
    ret, frame = cap.read() # Fetch image info
    frame_data = pickle.dumps(frame)
    client_socket.sendall(struct.pack("Q", len(frame_data))) # Send image info header
    client_socket.sendall(frame_data) # Send image info

    if globalIsOnComputer: # If testing locally, display images
        try:
            cv2.imshow('Server', frame)
        except (Exception):
            pass

