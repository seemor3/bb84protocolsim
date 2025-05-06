import socket
import json
import random

def measure(bit, a_basis, b_basis):
    return bit if a_basis == b_basis else random.randint(0, 1)

def start_bob():
    sock = socket.socket()
    sock.connect(("127.0.0.1", 8080))
    if sock.recv(1024).decode() == "ROLE?":
        sock.sendall(b"Bob")
    if sock.recv(1024).decode() == "START":
        print("Connected to Alice. Starting BB84...")

        measured = []
        bob_bases = [random.randint(0,1) for _ in range(20)]
        print("Bob's bases: ", bob_bases)
        i = 0

        while True:
            msg = sock.recv(4096)
            if not msg:
                break
            data = json.loads(msg.decode())
            if data["type"] == "qubit":
                bit = measure(data["bit"], data["basis"], bob_bases[i])
                measured.append(bit)
                i += 1
            elif data["type"] == "basis_announcement":
                sock.sendall(json.dumps({"type": "basis_announcement", "bases": bob_bases}).encode())
                alice_bases = data["bases"]
                print("Alice's bases: ", alice_bases)

                sifted_key = []
                print("\nSifting process (Bob):")
                for j in range(len(alice_bases)):
                    match = alice_bases[j] == bob_bases[j]
                    print(f"Index {j}: Alice Basis = {alice_bases[j]}, Bob Basis = {bob_bases[j]} --> {'Match' if match else 'No match'}")
                    if match:
                        sifted_key.append(measured[j])

                print("\nBob's raw key:", sifted_key)
                break
        sock.close()
start_bob()