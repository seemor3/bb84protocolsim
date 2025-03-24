import socket
import threading

clients = {}  # Dictionary to store connected clients with their roles

def handle_client(client_socket, role):
    """Handles communication between Alice and Bob."""
    while True:
        try:
            bit = client_socket.recv(1024).decode()
            if not bit:
                break
            print(f"Received bit from {role}: {bit}")

            # Forward the bit to the other client
            for client_role, client in clients.items():
                if client != client_socket:
                    client.sendall(bit.encode())
        except:
            break
    
    del clients[role]
    client_socket.close()

def start_server():
    """Sets up the server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8080))
    server.listen(3) # Listens for up to 3 to include the presence of Eve
    print("Server is running...")
    
    while len(clients) < 2:  # Wait for Alice and Bob to connect
        client_socket, addr = server.accept()
        print(f"Client connected from {addr}.")
        
        # Ask the client for their role
        client_socket.sendall("ROLE?".encode())
        role = client_socket.recv(1024).decode()
        
        if role in clients:
            print(f"Role {role} is already taken. Closing connection.")
            client_socket.close()
            continue
        
        print(f"{role} connected.")
        clients[role] = client_socket
        threading.Thread(target=handle_client, args=(client_socket, role)).start()
    
    print("Both clients connected. Ready for communication.")
    # Send "START" only to Alice
    if 'Alice' in clients:
        clients['Alice'].sendall("START".encode())

start_server()