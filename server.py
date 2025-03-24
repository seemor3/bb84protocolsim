import socket
import threading
import time

def send_bits_to_bob(client_socket, partner_socket):
    """Alice sends random bits to Bob."""
    try:
        # Notify Alice that Bob has connected
        client_socket.sendall("START".encode())
        
        while True:
            bit = client_socket.recv(1024).decode()
            if not bit:
                break
            print(f"Alice sent bit: {bit}")
            partner_socket.sendall(bit.encode())
    except Exception as e:
        print(f"Error in send_bits_to_bob: {e}")
    finally:
        client_socket.close()
        partner_socket.close()

def receive_bits_from_alice(client_socket):
    """Bob receives bits from Alice."""
    try:
        while True:
            bit = client_socket.recv(1024).decode()
            if not bit:
                print("Bob has not received the message")
                break
            print(f"Bob received bit: {bit}")
    except Exception as e:
        print(f"Error in receive_bits_from_alice: {e}")
    finally:
        client_socket.close()

def create_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print("Server is waiting for connections...")
    
    alice_socket, alice_addr = server_socket.accept()
    print(f"Alice connected from {alice_addr}")
    
    bob_socket, bob_addr = server_socket.accept()
    print(f"Bob connected from {bob_addr}")
    
    # Alice sends bits, Bob receives them
    threading.Thread(target=send_bits_to_bob, args=(alice_socket, bob_socket), daemon=True).start()
    threading.Thread(target=receive_bits_from_alice, args=(bob_socket,), daemon=True).start()
    
    try:
        while True:
            time.sleep(0.1)  # Add a small sleep interval to reduce CPU load
    except KeyboardInterrupt:
        print("Shutting down server.")
        server_socket.close()

if __name__ == "__main__":
    create_server("127.0.0.1", 8080)