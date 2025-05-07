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

        key_length = 100  # Length of the bits to form a key
        bits = [random.randint(0, 1) for _ in range(key_length)]
        basis = [random.randint(0, 1) for _ in range(key_length)]

        print("Alice's bits: ", bits)
        print("\nAlice's basis: ", basis)

        for i in range(key_length):
            msg = json.dumps({"type": "qubit", "bit": bits[i], "basis": basis[i]}).encode()
            sock.sendall(msg + b"\n")  # Add a newline delimiter
            print(f"Sent qubit: {bits[i]} with basis {basis[i]}")
            #time.sleep(1) # Simulate time delay for sending qubits

        # Send basis announcement
        try:
            print("basis announcement sent: ", basis)
            sock.sendall(json.dumps({"type": "basis_announcement", "basis": basis}).encode() + b"\n")
        except BrokenPipeError:
            print("Connection to server lost while sending basis announcement. Aborting.")
            sock.close()
            return

        # Receive Bob's basis announcement
        buffer = ""  # Initialize the buffer
        while True:
            try:
                data = sock.recv(4096).decode()
            except ConnectionResetError:
                print("Connection reset by peer while waiting for basis announcement.")
                sock.close()
                return
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line.strip():
                    continue
                response = json.loads(line)
                if response.get("type") == "basis_announcement":
                    bob_basis = response["basis"]
                    break
            else:
                continue  # Continue outer while loop
            break  # Break outer while loop if announcement received

        print("Bob's basis: ", bob_basis)
        sifted_key = []
        print("\nSifting process (Alice):")
        min_length = min(len(basis), len(bob_basis))
        for i in range(min_length):
            match = basis[i] == bob_basis[i]
            print(f"Index {i}: Alice Basis = {basis[i]}, Bob Basis = {bob_basis[i]} --> {'Match' if match else 'No match'}")
            if match:
                sifted_key.append(bits[i])

        print("\nAlice's raw key:", sifted_key)
        match_percentage = (len(sifted_key) / min_length) * 100
        print(f"\nPercentage of bits kept after sifting: {match_percentage:.2f}%")
        
        buffer = ""
        while True:
            chunk = sock.recv(4096).decode()
            if not chunk:
                break
            buffer += chunk
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line.strip():
                    continue
                msg = json.loads(line)
                if msg.get("type") == "sample":
                    idx       = msg["indices"]
                    bob_bits  = msg["bits"]
                    errors = sum(1 for k, b in zip(idx, bob_bits) if sifted_key[k] != b)
                    error_pct = errors / len(idx) * 100 if idx else 0
                    print(f"\nError-checking sample ({len(idx)} bits): "
                        f"{errors} errors → {error_pct:.2f}%")
                    if error_pct > 11:
                        print(f"\nToo many errors. Key is compromised.")
                    sock.close()
                    return

if __name__ == "__main__":
    start_alice()