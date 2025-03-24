import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def decrypt_message(encrypted_message, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_message) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode()

def start_bob():
    
    # server configuration
    server_host = "127.0.0.1"
    server_port = 8080

    key = b'0123456789abcdef'  # 16-byte key for AES-128
    iv = b'abcdef9876543210'   # 16-byte IV for AES

    bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bob_socket.connect((server_host, server_port))
    print("Bob connected to server.")
    
    # Send role to the server
    role_request = bob_socket.recv(1024).decode()
    if role_request == "ROLE?":
        bob_socket.sendall("Bob".encode())  # Send Alice's role

    try:
        while True:
            encrypted_bit = bob_socket.recv(1024)
            if not encrypted_bit:
                break
            bit = decrypt_message(encrypted_bit, key, iv)
            print(f"Bob received bit: {bit}")
    except KeyboardInterrupt:
        print("Bob interrupted communication.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        bob_socket.close()
        print("Connection closed.")

start_bob()