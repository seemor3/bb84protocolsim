import socket
import json
import random
import time

def start_alice():
    sock = socket.socket()
    sock.connect(("127.0.0.1", 8080))
    if sock.recv(1024).decode() == "ROLE?":
        sock.sendall(b"Alice")
    if sock.recv(1024).decode() == "START":
        print("Connected to Bob. Starting BB84...")

        bits = [random.randint(0,1) for _ in range(20)]
        bases = [random.randint(0,1) for _ in range(20)]

        print("Alice's bits: ", bits)
        print("Alice's bases: ", bases)

        for i in range(20):
            msg = json.dumps({"type": "qubit", "bit": bits[i], "basis": bases[i]}).encode()
            sock.sendall(msg)
            time.sleep(0.1)

        sock.sendall(json.dumps({"type": "basis_announcement", "bases": bases}).encode())
        bob_bases = json.loads(sock.recv(4096).decode())["bases"]

        sifted_key = [bits[i] for i in range(20) if bases[i] == bob_bases[i]]
        print("Alice's raw key:", sifted_key)
        sock.close()

start_alice()