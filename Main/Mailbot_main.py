import cv2
import socket
import pickle
import struct
from functions import imageToText
import pytesseract
import os
import sys
import subprocess
import signal
import time
from Handle_Names import generate_list, strCompareToList
from Active_Slack import notify_user, set_bot_status, notify_sender

sys.tracebacklimit = 0
globalIsOnComputer = False

def main():
    signal.signal(signal.SIGPIPE, signal.SIG_IGN) # Ignore SIGPIPE
    print("Main, PID: ", str(os.getpid()))

    # WHILE NOT KILLED::::
    while(1):

        set_bot_status("away")

        passive = subprocess.Popen(["python", "Passive_Slack.py"]) # Startup Passive_Slack.py
        print("Passive pid: ", str(passive.pid))
        passive.wait()
        if(passive.returncode != 0): # Killed
            exit(1)
                
        init_time = time.time()
        lifespan = 3 * 60 # In seconds
        stop_time = init_time + lifespan
        # Start Scanner.py
        scanner = subprocess.Popen(["python", "Scanner.py"]) # Startup Scanner.py
        print("Scanner pid: ", str(scanner.pid))
        set_bot_status("auto")
        
        time.sleep(1) # Bandaid to the race cond
        reading_from_scanner(stop_time) # Start client code, runs for lifespan
        
        os.kill((scanner.pid), signal.SIGTERM) # Send signal to Scanner.py
        
        # Kill Scanner.py
        # Head to top of loop


# This is the client side of the socket connection
def reading_from_scanner(stop_time):
    startUser = ""
    # Gen alias list
    names = generate_list()

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
            # Take in a packet
            packet = client_socket.recv(4 * 1024)  # 4K buffer size
            if not packet:
                break
            data += packet
        # If there is no data built from the packets, ignore processing
        if not data:
            break
        # Break data apart into struct data vs remainder
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
            name = strCompareToList(names, text)
            if(name != ""):
                # Notify User
                print("Reach")
                notify_user(name)
                print("Reach")
                print("SU!: ", os.environ["STARTUSER"])
                if not startUser:
                    startUser = os.environ["STARTUSER"]
                # if not startUser:
                notify_sender(name, startUser)
        
        except Exception as e:
            print(e)
            pass
    client_socket.close()
    return

main()