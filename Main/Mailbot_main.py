import cv2
import socket
import pickle
import struct
# from functions import *
import pytesseract
import os
import sys
import subprocess
import signal
import time

sys.tracebacklimit = 0
globalIsOnComputer = True

def main():
    print("Main, PID: ", str(os.getpid()))
    fork_bomb_prot = 4
    # WHILE NOT KILLED::::
    while(fork_bomb_prot > 0):
        fork_bomb_prot -= 1

        # passive = subprocess.Popen(["python", "Passive_Slack.py"]) # Startup Passive_Slack.py
        # passive.wait()
        # if(passive.returncode != 0): # Killed
        #     exit(1)
        
        init_time = time.time()
        stop_time = init_time + 2 #(3 * 60) # 3 mins in future
        # Start Scanner.py
        scanner = subprocess.Popen(["python", "Scanner.py"]) # Startup Scanner.py
        print("Got scanner pid: ", str(scanner.pid))
        while time.time() < stop_time:
            void = 0
        
        os.kill((scanner.pid), signal.SIGTERM) # Send signal to Scanner.py
        
        # Start client-code & init lifespan timer
        # Wait for lifespan to expire

        # Kill Scanner.py
        # Head to top of loop


# This is the client side of the socket connection
def reading_from_scanner(stop_time):
    # If code is running on arduino --> False. If on computer --> True 
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Arduino vs Laptop socket Connection
    if(globalIsOnComputer):
        client_socket.connect(('0.0.0.0', 8888))  
    else:
        client_socket.connect(('127.0.0.1', 8888))  
    data = b""
    payload_size = struct.calcsize("Q")
    print("Client connected")
    i = 0
    while time.time() < stop_time:
        # While the current data is less than the size of the desired payload size
        while len(data) < payload_size:
            # Take in a packet at 4K resolution
            packet = client_socket.recv(4 * 1024)  # 4K buffer size
            if not packet:
                break
            data += packet
        # If there is no data built from the packets, ignore processing
        if not data:
            break
        # Break data apart into desired data vs remainder
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
    client_socket.close()
    return

main()