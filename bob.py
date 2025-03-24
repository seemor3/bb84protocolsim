import socket

# server configuration
server_host = "127.0.0.1"
server_port = 8080

bob_socket = socket.socket()

bob_socket.connect((server_host, server_port))

try:
    print("Connection Established")
    while True:
        bit = bob_socket.recv(1024).decode()
        if not bit:
            break
        print(f"Bob received bit: {bit}")
        bob_socket.sendall(bit.encode())
except KeyboardInterrupt:
    print("Communication interrupted.")
finally:
    bob_socket.close()