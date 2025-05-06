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

        key_length = 20
        bits = [random.randint(0,1) for _ in range(key_length)]
        bases = [random.randint(0,1) for _ in range(key_length)]

        print("Alice's bits: ", bits)
        print("\nAlice's bases: ", bases)

        for i in range(key_length):
            msg = json.dumps({"type": "qubit", "bit": bits[i], "basis": bases[i]}).encode()
            sock.sendall(msg)
            time.sleep(0.1)
        # This compares the bases publicly to form the sifted key
        sock.sendall(json.dumps({"type": "basis_announcement", "bases": bases}).encode())
        bob_bases = json.loads(sock.recv(4096).decode())["bases"]

        print("Bob's bases: ", bob_bases)
        sifted_key = []
        print("\nSifting process (Alice):")
        for i in range(key_length):
            match = bases[i] == bob_bases[i]
            print(f"Index {i}: Alice Basis = {bases[i]}, Bob Basis = {bob_bases[i]} --> {'Match' if match else 'No match'}")
            if match:
                sifted_key.append(bits[i])

        print("\nAlice's raw key:", sifted_key)
        sock.close()

start_alice()