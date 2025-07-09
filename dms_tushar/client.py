import socket

SERVER_IP = '172.30.60.'  # Replace with your server's IP
PORT = 12345
BUFFER_SIZE = 1024

def main():
    try:
        # Create a TCP/IP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORT))
        print(f" Connected to server at {SERVER_IP}:{PORT}\n")
    except Exception as e:
        print(f" Connection failed: {e}")
        return

    try:
        while True:
            message = input("Enter brake value (or type 'exit' to quit): ").strip()
            if message.lower() == 'exit':
                break

            # Send message
            client_socket.sendall(message.encode())

            # Wait for feedback
            feedback = client_socket.recv(BUFFER_SIZE).decode()
            if feedback:
                print(f" Server response: {feedback.strip()}")
            else:
                print(" No response from server. Exiting.")
                break
    finally:
        client_socket.close()
        print("🔌 Connection closed.")

if __name__ == "__main__":
    main()
