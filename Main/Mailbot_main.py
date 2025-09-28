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
import threading
from Handle_Names import generate_list, strCompareToList
from Active_Slack import notify_user, set_bot_status, notify_sender, notify_sender_ended

sys.tracebacklimit = 0
globalIsOnComputer = False
evt = threading.Event() # Threading events for signal handling
evt.clear()

def handler(signum, frame):
    evt.set() # "Move on" signal

def main():
    signal.signal(signal.SIGPIPE, signal.SIG_IGN) # Ignore SIGPIPE
    print("Main, PID: ", str(os.getpid())) # For debugging purposes
    signal.signal(signal.SIGUSR1, handler) # "Move on" signal

    evt.clear()
    passive = subprocess.Popen(["python", "Passive_Slack.py"], ) # Startup Passive_Slack.py
    print("Passive pid: ", str(passive.pid)) # For debugging purposes


    while(1): # WHILE NOT KILLED -->

        evt.clear() # Clear event
        evt.wait() # Wait for "move on" signal from Passive_Slack.py

        # If here, "move on" signal received

        # Get lifespan of 120 seconds
        init_time = time.time()
        lifespan = 2 * 60 
        stop_time = init_time + lifespan

        # Start Scanner.py
        scanner = subprocess.Popen(["python", "Scanner.py"])
        print("Scanner pid: ", str(scanner.pid))
        set_bot_status("auto")

        uid = fetchUID() # Get Init User from file
        time.sleep(1) # Bandaid to the race condition
        
        reading_from_scanner(stop_time, uid) # Start client code, runs for lifespan
        
        os.kill((scanner.pid), signal.SIGTERM) # Send signal to Scanner.py to terminate
        
        notify_sender_ended(uid) # Notify Init User that scanner is closed

        

# This is the client side of the socket connection
# This code takes in the img data, turns it into text, then finds aliases within that text 
def reading_from_scanner(stop_time, uid):
    names = generate_list() # Get Alias List
    recent_names = set([]) # Avoid Double Notifications

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    if(globalIsOnComputer): # Raspberry Pi vs Laptop socket Connection
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
            packet = client_socket.recv(4 * 1024) # Take in a packet @ 4K buffer size
            if not packet: # Break if empty
                break
            data += packet
        
        if not data: # If there is no data built from the packets, ignore processing
            break
        
        packed_msg_size = data[:payload_size] # Header Data
        data = data[payload_size:] # Non-Header Data
        msg_size = struct.unpack("Q", packed_msg_size)[0] # From header, get msg size

        while len(data) < msg_size: # While data is less than msg size, keep receiving
            data += client_socket.recv(16 * 1024)  # 16K buff
        
        frame_data = data[:msg_size]
        data = data[msg_size:]
        
        
        # Also enforce minimum time interval
        # This helps to reduce lagging & Overprocessing & huge latency
        cur_time = time.time()
        if cur_time - last_process_time < process_min_interval: 
            continue
        
        try:
            frame = pickle.loads(frame_data)
            if globalIsOnComputer:
                cv2.imshow('Client', frame)
            text = imageToText(frame).upper() # Convert image to text
            
            name = strCompareToList(names, text) # Look for Aliases in text
            if(name != ""):
                if name not in recent_names: # If not duplicate
                    recent_names.add(name)
                else:
                    continue

                notify_user(name) # Notify User
                if uid:
                    notify_sender(name, uid) # Notify Init User it Processed
            
            last_process_time = cur_time
        
        except Exception as e:
            print(e)
            pass
    
    client_socket.close() # When done running (Time Exceeded), close socket
    # This then continues the loop up top.
    return

main() # Call the main function