# # $ python3 -m http.server
# # Run above in a separate terminal

# import cv2
# import socket
# import pickle
# import struct


# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(('0.0.0.0', 8888)) # Switched from 127.0.0.1
# server_socket.listen(5)
# print("Server is listening...")
# client_socket, client_address = server_socket.accept()
# print(f"Connection from {client_address} accepted")
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     frame_data = pickle.dumps(frame)
#     client_socket.sendall(struct.pack("Q", len(frame_data)))
#     client_socket.sendall(frame_data)
#     try:
#         cv2.imshow('Server', frame)
#     except (Exception):
#         pass

# cap.release()
# # cv2.destroyAllWindows()

import cv2
import socket
import pickle
import struct
import time  # Added for delay

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8888))  # Listen on all interfaces
server_socket.listen(5)

print("Server is listening...")
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} accepted")

cap = cv2.VideoCapture(0)  # Open USB Camera

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break  # Stop if camera fails

    try:
        # Serialize the frame
        frame_data = pickle.dumps(frame)
        message_size = struct.pack("Q", len(frame_data))

        # Send size and data
        client_socket.sendall(message_size)
        client_socket.sendall(frame_data)

        # Show the video on the server
        cv2.imshow('Server', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # Press 'q' to stop

        time.sleep(0.01)  # Reduce CPU usage

    except (BrokenPipeError, ConnectionResetError):
        print("Client disconnected. Stopping server.")
        break

cap.release()
cv2.destroyAllWindows()
client_socket.close()
server_socket.close()
print("Server stopped.")
