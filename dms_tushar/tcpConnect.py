import socket

def connectCMViaTCP():
    SERVER_IP = '172.30.60.28'  # Replace with your server's IP
    PORT = 12345
    BUFFER_SIZE = 1024



    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))
    print(f" Connected to server at {SERVER_IP}:{PORT}\n")
