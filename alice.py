import socket
import random
import time

def generate_random_bit():
    """Generates a random bit (0 or 1)."""
    return str(random.randint(0, 1))

def start_alice():
    
    # server configuration
    server_host = "127.0.0.1"
    server_port = 8080

    alice_socket = socket.socket()
    alice_socket.connect((server_host, server_port))
    print("Connection Established")
        
    role_request = alice_socket.recv(1024).decode()
    if role_request == "ROLE?":
        alice_socket.sendall("Alice".encode())  # Send Alice's role
    
    try:
        # Wait for the start signal from the server
        start_signal = alice_socket.recv(1024).decode()
        if start_signal == "START":
            print("Bob has connected. Starting communication...")
            while True:
                try:
                    bit = generate_random_bit()  # Alice sends a single random bit
                    print(f"Alice sent: {bit}")
                    alice_socket.sendall(bit.encode())
                    time.sleep(1)  # Add a delay to simulate time between sending bits
                except BrokenPipeError:
                    print("Connection lost. Exiting.")
                    break
                except Exception as e:
                    print(f"An error occurred in the loop: {e}")
                    break
    except KeyboardInterrupt:
        print("Communication interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Closing connection.")
        alice_socket.close()
        print("Connection closed.")

start_alice()