import cv2
import socket
import pickle
import struct
from functions import imageToText, fetchUID
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

def handler(signum, frame):
    print("GOT SIGNAL")

def main():
    signal.signal(signal.SIGPIPE, signal.SIG_IGN) # Ignore SIGPIPE
    print("Main, PID: ", str(os.getpid()))
    signal.signal(signal.SIGUSR1, handler)

    # WHILE NOT KILLED::::
    while(1):

        set_bot_status("away")

        passive = subprocess.Popen(["python", "Passive_Slack.py"], ) # Startup Passive_Slack.py
        print("Passive pid: ", str(passive.pid))
        passive.wait()
        if(passive.returncode == -1): # Killed
            exit(1)
        print("REACH LOW")
                
        init_time = time.time()
        lifespan = 1 * 60 # In seconds
        stop_time = init_time + lifespan
        # Start Scanner.py
        scanner = subprocess.Popen(["python", "Scanner.py"]) # Startup Scanner.py
        print("Scanner pid: ", str(scanner.pid))
        set_bot_status("auto")

        uid = fetchUID() # Get user from file
        time.sleep(1) # Bandaid to the race cond
        reading_from_scanner(stop_time, uid) # Start client code, runs for lifespan
        
        os.kill((scanner.pid), signal.SIGTERM) # Send signal to Scanner.py
        
        # Kill Scanner.py
        # Head to top of loop


# This is the client side of the socket connection
def reading_from_scanner(stop_time, uid):
    # Gen alias list
    names = generate_list()
    recent_names = set([])

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
    last_process_time = 0
    process_min_interval = 0.200 # 200 ms

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
            data += client_socket.recv(16 * 1024)  # 16K buff
        frame_data = data[:msg_size]
        data = data[msg_size:]
        
        # Also enforce minimum time interval
        cur_time = time.time()
        if cur_time - last_process_time < process_min_interval:
            continue
        
        try:
            frame = pickle.loads(frame_data)
            if globalIsOnComputer:
                cv2.imshow('Client', frame)
            text = imageToText(frame).upper()
            print("Text: ", text)
            name = strCompareToList(names, text)
            if(name != ""):
                if name not in recent_names:
                    recent_names.add(name)
                else:
                    continue
                # Notify User
                notify_user(name)
                if uid:
                    notify_sender(name, uid)
            last_process_time = cur_time
        
        except Exception as e:
            print(e)
            pass
    client_socket.close()
    return

main()