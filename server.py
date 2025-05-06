import socket
import threading
import json

clients = {}  # Store clients by role
start_sent = False

def handle_client(client_socket, role):
    while True:
        try:
            msg = client_socket.recv(4096)
            if not msg:
                break
            for r, sock in clients.items():
                if sock != client_socket:
                    sock.sendall(msg)
        except:
            break
    client_socket.close()
    del clients[role]

def accept_clients(server_socket):
    global start_sent
    while True:
        client_socket, _ = server_socket.accept()
        client_socket.sendall(b"ROLE?")
        role = client_socket.recv(1024).decode()
        if role in clients:
            client_socket.close()
            continue
        clients[role] = client_socket
        print(f"{role} has joined the server.")
        threading.Thread(target=handle_client, args=(client_socket, role), daemon=True).start()
        if 'Alice' in clients and 'Bob' in clients and not start_sent:
            clients['Alice'].sendall(b"START")
            clients['Bob'].sendall(b"START")
            start_sent = True

def start_server():
    server = socket.socket()
    server.bind(("127.0.0.1", 8080))
    server.listen()
    print("Server running on 127.0.0.1:8080")
    try:
        accept_clients(server)
    except KeyboardInterrupt:
        print("\nServer closed.")

start_server()
