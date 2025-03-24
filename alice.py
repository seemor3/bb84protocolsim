import socket
import random
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def generate_random_bit():
    """Generates a random bit (0 or 1)."""
    return str(random.randint(0, 1))

def encrypt_message(message, key, iv):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_message

def start_alice():
    
    # server configuration
    server_host = "127.0.0.1"
    server_port = 8080

    key = b'0123456789abcdef'  # 16-byte key for AES-128
    iv = b'abcdef9876543210'   # 16-byte IV for AES

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
                    encrypted_bit = encrypt_message(bit, key, iv)
                    alice_socket.sendall(encrypted_bit)
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