import socket
import json
import random
import time

def measure(bit, a_basis, b_basis):
    return bit if a_basis == b_basis else random.randint(0, 1)

def start_bob():
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
        sock.sendall(b"Bob")
    if sock.recv(1024).decode() == "START":
        print("Connected to Alice. Starting BB84...")

        key_length = 100 #length of the bits to form a key
        measured = []
        bob_basis = [random.randint(0,1) for _ in range(key_length)]
        print("Bob's basis: ", bob_basis)
        i = 0

        while True:
            msg = sock.recv(4096)
            if not msg:
                break
            data = json.loads(msg.decode())
            if data["type"] == "qubit":
                bit = measure(data["bit"], data["basis"], bob_basis[i])
                measured.append(bit)
                i += 1
            elif data["type"] == "basis_announcement":
                sock.sendall(json.dumps({"type": "basis_announcement", "basis": bob_basis}).encode())
                alice_basis = data["basis"]
                print("Alice's basis: ", alice_basis)

                sifted_key = []
                print("\nSifting process (Bob):")
                for j in range(len(alice_basis)):
                    match = alice_basis[j] == bob_basis[j]
                    print(f"Index {j}: Alice Basis = {alice_basis[j]}, Bob Basis = {bob_basis[j]} --> {'Match' if match else 'No match'}")
                    if match:
                        sifted_key.append(measured[j])

                print("\nBob's raw key:", sifted_key)
                break
        match_percentage = (len(sifted_key) / key_length) * 100
        print(f"\nPercentage of bits kept after sifting: {match_percentage:.2f}%")
        sock.close()
start_bob()