import socket

def start_bob():
    server_host = "127.0.0.1"
    server_port = 8080

    bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bob_socket.connect((server_host, server_port))
    print("Bob connected to server.")

    try:
        while True:
            bit = bob_socket.recv(1024).decode()
            if not bit:
                break
            print(f"Bob received bit: {bit}")
    except KeyboardInterrupt:
        print("Bob interrupted communication.")
    finally:
        bob_socket.close()

start_bob()
