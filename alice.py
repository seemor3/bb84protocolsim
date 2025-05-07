import socket
import json
import random
import time

def start_alice():
    print("Waiting for connection to server...")
    while True:
        try:
            sock = socket.socket()
            sock.connect(("127.0.0.1", 8080))
            break
        except ConnectionRefusedError:
            print("Server not available yet. Retrying in 1 second...")
            time.sleep(1)
            
    if sock.recv(1024).decode() == "ROLE?":
        sock.sendall(b"Alice")
    if sock.recv(1024).decode() == "START":
        print("Connected to Bob. Starting BB84...")

        key_length = 20
        bits = [random.randint(0,1) for _ in range(key_length)]
        basis = [random.randint(0,1) for _ in range(key_length)]

        print("Alice's bits: ", bits)
        print("\nAlice's basis: ", basis)

        for i in range(key_length):
            msg = json.dumps({"type": "qubit", "bit": bits[i], "basis": basis[i]}).encode()
            sock.sendall(msg)
            time.sleep(0.1)
        # This compares the basis publicly to form the sifted key
        sock.sendall(json.dumps({"type": "basis_announcement", "basis": basis}).encode())
        bob_basis = json.loads(sock.recv(4096).decode())["basis"]

        print("Bob's basis: ", bob_basis)
        sifted_key = []
        print("\nSifting process (Alice):")
        for i in range(key_length):
            match = basis[i] == bob_basis[i]
            print(f"Index {i}: Alice Basis = {basis[i]}, Bob Basis = {bob_basis[i]} --> {'Match' if match else 'No match'}")
            if match:
                sifted_key.append(bits[i])

        print("\nAlice's raw key:", sifted_key)
        sock.close()

start_alice()