import socket
import json
import random
import time


def measure(bit, a_basis, b_basis):
    """Return Bob’s measurement result (ideal channel, no detector error)."""
    return bit if a_basis == b_basis else random.randint(0, 1)


def start_bob():
    print("Waiting for connection to server…")
    while True:
        try:
            sock = socket.socket()
            sock.connect(("127.0.0.1", 8080))
            break
        except ConnectionRefusedError:
            print("Server not available yet. Retrying…")
            time.sleep(1)

    if sock.recv(1024).decode() == "ROLE?":
        sock.sendall(b"Bob")

    if sock.recv(1024).decode() != "START":
        print("Did not receive START signal. Exiting.")
        return

    print("Connected to Alice. Starting BB84…")

    KEY_LEN = 100
    bob_bases = [random.randint(0, 1) for _ in range(KEY_LEN)]
    print("Bob's bases:", bob_bases)

    measured_bits: list[int] = []
    i = 0  # number of qubits measured
    alice_basis_pending = None  # store Alice's basis list if it arrives early

    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        for line in chunk.decode().splitlines():
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            # ──────────────────────────────────
            if data["type"] == "qubit":
                if i < KEY_LEN:
                    measured_bits.append(
                        measure(data["bit"], data["basis"], bob_bases[i])
                    )
                    i += 1
                # if all qubits measured and we already have Alice's bases → sift now
                if i >= KEY_LEN and alice_basis_pending is not None:
                    alice_basis = alice_basis_pending
                    alice_basis_pending = None  # clear so we sift once
            # ──────────────────────────────────
            elif data["type"] == "basis_announcement":
                if i < KEY_LEN:
                    # Save and wait for remaining qubits
                    alice_basis_pending = data["basis"]
                    sock.sendall((json.dumps({"type": "basis_announcement", "basis": bob_bases}) + "\n").encode())
                    continue
                else:
                    sock.sendall((json.dumps({"type": "basis_announcement", "basis": bob_bases}) + "\n").encode())
                    alice_basis = data["basis"]

            # ─── if both lists ready and i == KEY_LEN, perform sifting ───
            if i >= KEY_LEN and alice_basis_pending is None and "alice_basis" in locals():
                print("Alice's bases:", alice_basis)
                sifted = []
                print("\nSifting process (Bob):")
                for j in range(KEY_LEN):
                    match = alice_basis[j] == bob_bases[j]
                    print(f"Index {j}: Alice Basis = {alice_basis[j]}, Bob Basis = {bob_bases[j]} --> {'Match' if match else 'No match'}")
                    if match:
                        sifted.append(measured_bits[j])

                print("\nBob's raw key:", sifted)
                pct = len(sifted) / KEY_LEN * 100
                print(f"\nPercentage kept after sifting: {pct:.2f}%")

                # send sifted key to Alice
                #sock.sendall((json.dumps({"type": "bob_raw_key", "key": sifted}) + "\n").encode())
                #sock.close()
                #return
                sample_size = max(1, len(sifted) // 4)
                indices = random.sample(range(len(sifted)), sample_size)
                sample_bits = [sifted[idx] for idx in indices]

                sock.sendall((json.dumps({
                    "type": "sample",
                    "indices": indices,
                    "bits": sample_bits
                }) + "\n").encode())
                sock.close()
                return

if __name__ == "__main__":
    start_bob()