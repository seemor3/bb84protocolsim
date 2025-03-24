import socket
import threading

clients = []  # List to store connected clients

def handle_client(client_socket):
    """Handles communication between Alice and Bob."""
    while True:
        try:
            bit = client_socket.recv(1024).decode()
            if not bit:
                break
            print(f"Received bit: {bit}")

            # Forward the bit to the other client
            for client in clients:
                if client != client_socket:
                    client.sendall(bit.encode())
        except:
            break
    
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    """Sets up the server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8080))
    server.listen(3) # Listens for up to 3 to include the presence of Eve
    print("Server is running...")
    
    while len(clients) < 2:  # Wait for Alice and Bob to connect
        client_socket, addr = server.accept()
        print(f"Client {addr} connected.")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()
    
    print("Both clients connected. Ready for communication.")
    for client in clients:
        client.sendall("START".encode())
start_server()
