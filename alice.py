import socket
import json
import random
import time
import websockets
import asyncio

async def start_alice():
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        await ws.send(json.dumps({"role": "Alice", "type": "connected"}))
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

            # Send qubits to Bob
            for i in range(key_length):
                msg = json.dumps({"type": "qubit", "bit": bits[i], "basis": basis[i]}).encode()
                await ws.send(json.dumps({"role": "Alice", "type": "qubit_sent", "index": i, "bit": bits[i], "basis": basis[i]}))
                sock.sendall(msg + b"\n")  # Add a newline delimiter
                print(f"Sent qubit: {bits[i]} with basis {basis[i]}")
                #time.sleep(1) # Simulate time delay for sending qubits

            # Send basis announcement
            try:
                print("basis announcement sent: ", basis)
                await ws.send(json.dumps({"role": "Alice", "type": "basis_announcement", "basis": basis}))
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
            
            # Sifting process
            print("Bob's basis: ", bob_basis)
            sifted_key = []
            print("\nSifting process (Alice):")
            min_length = min(len(basis), len(bob_basis))
            for i in range(min_length):
                match = basis[i] == bob_basis[i]
                await ws.send(json.dumps({"role": "Alice", "type": "basis_match" if match else "basis_nomatch", "index": i}))
                print(f"Index {i}: Alice Basis = {basis[i]}, Bob Basis = {bob_basis[i]} --> {'Match' if match else 'No match'}")
                if match:
                    sifted_key.append(bits[i])

            # Show sifting results
            print("\nAlice's raw key:", sifted_key)
            match_percentage = (len(sifted_key) / min_length) * 100
            print(f"\nPercentage of bits kept after sifting: {match_percentage:.2f}%")
            await ws.send(json.dumps({"role": "Alice", "type": "sifting_complete", "sifted_length": len(sifted_key), "percentage": match_percentage}))
            
            
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
                            
                        await ws.send(json.dumps({"role": "Alice", "type": "error_check", "errors": errors, "sample_size": len(idx), "error_pct": error_pct}))
                        await ws.send(json.dumps({"role": "Alice", "type": "result", "safe": error_pct <= 11}))
                        if error_pct > 11:
                            print(f"\nToo many errors. Key is compromised.")
                        sock.close()
                        return

if __name__ == "__main__":
    asyncio.run(start_alice())