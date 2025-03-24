import socket
import threading

clients = {}  # Dictionary to store connected clients with their roles
start_sent = False  # Flag to track if the "START" signal has been sent

def handle_client(client_socket, role):
    """Handles communication between Alice and Bob."""
    while True:
        try:
            bit = client_socket.recv(1024)
            if not bit:
                break
            print(f"Received bit from {role}: {bit}")

            # Forward the bit to the other clients
            for client_role, client in clients.items():
                if client != client_socket:
                    try:
                        client.sendall(bit)
                    except BrokenPipeError:
                        print(f"Connection to {client_role} lost.")
                        del clients[client_role]
                        client.close()
        except Exception as e:
            print(f"An error occurred with {role}: {e}")
            break
    
    del clients[role]
    client_socket.close()

def accept_clients(server_socket):
    """Accepts new clients and assigns roles."""
    global start_sent
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Client connected from {addr}.")
        
        # Ask the client for their role
        client_socket.sendall("ROLE?".encode())
        role = client_socket.recv(1024).decode()
        
        if role in clients:
            print(f"Role {role} is already taken. Closing connection.")
            client_socket.close()
            continue
        
        clients[role] = client_socket
        print(f"{role} connected.")
        threading.Thread(target=handle_client, args=(client_socket, role)).start()
        
        # Send "START" only to Alice if both Alice and Bob are connected
        if 'Alice' in clients and 'Bob' in clients and not start_sent:
            clients['Alice'].sendall("START".encode())
            start_sent = True

def start_server():
    """Sets up the server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8080))
    server.listen(3) # Listens for up to 3 to include the presence of Eve
    print("Server is running...")
    
    threading.Thread(target=accept_clients, args=(server,), daemon=True).start()
    
    try:
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        print("Shutting down server.")
        server.close()

start_server()