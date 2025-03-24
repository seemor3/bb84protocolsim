import socket
import random
import time

def generate_random_bit():
    """Generates a random bit (0 or 1)."""
    return str(random.randint(0, 1))

# server configuration
server_host = "127.0.0.1"
server_port = 8080

alice_socket = socket.socket()

alice_socket.connect((server_host, server_port))

try:
    print("Connection Established")
    
    # Wait for the start signal from the server
    start_signal = alice_socket.recv(1024).decode()
    if start_signal == "START":
        print("Bob has connected. Starting communication...")
        while True:
            bit = generate_random_bit()  # Alice sends a single random bit
            print(f"Alice sent: {bit}")
            alice_socket.sendall(bit.encode())
            time.sleep(1)  # Add a delay to simulate time between sending bits
except KeyboardInterrupt:
    print("Communication interrupted.")
finally:
    alice_socket.close()