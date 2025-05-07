import socket
import threading
import json

clients = {}  # role → socket
start_sent = False

def relay_from_eve():
    """Background thread: read newline‑delimited JSON coming FROM Eve and
    forward it to Bob (qubits/basis) or Alice (bob_raw_key)."""
    eve = clients["Eve"]
    buf = ""
    while True:
        try:
            chunk = eve.recv(4096).decode()
            if not chunk:
                break  # Eve disconnected
            buf += chunk
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                if not line.strip():
                    continue
                # Simply relay depending on message type
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if data.get("type") in ("qubit", "basis_announcement"):
                    if "Bob" in clients:
                        clients["Bob"].sendall((line + "\n").encode())
                elif data.get("type") == "bob_raw_key":
                    if "Alice" in clients:
                        clients["Alice"].sendall((line + "\n").encode())
        except Exception:
            break
    print("Eve relay thread terminating")


def handle_client(sock, role):
    buf = ""
    while True:
        try:
            chunk = sock.recv(4096).decode()
            if not chunk:
                break
            buf += chunk
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                if not line.strip():
                    continue
                # parse for routing only (no modification)
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if role == "Alice":
                    # send to Eve if present, else Bob
                    target = clients.get("Eve") or clients.get("Bob")
                    if target:
                        target.sendall((line + "\n").encode())
                elif role == "Bob":
                    # Bob → Alice always
                    if "Alice" in clients:
                        clients["Alice"].sendall((line + "\n").encode())
                elif role == "Eve":
                    # Eve shouldn't reach here; relay thread handles her output
                    pass
        except Exception:
            break
    sock.close()
    del clients[role]
    print(f"{role} disconnected.")


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
        if role == "Eve":
            threading.Thread(target=relay_from_eve, daemon=True).start()
        else:
            threading.Thread(target=handle_client, args=(client_socket, role), daemon=True).start()
        if 'Alice' in clients and 'Bob' in clients and not start_sent:
            clients['Alice'].sendall(b"START")
            clients['Bob'].sendall(b"START")
            start_sent = True


def start_server():
    srv = socket.socket()
    srv.bind(("127.0.0.1", 8080))
    srv.listen()
    print("Server running on 127.0.0.1:8080")
    try:
        accept_clients(srv)
    except KeyboardInterrupt:
        print("Server closed.")

start_server()