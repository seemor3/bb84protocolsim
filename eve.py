import socket
import json
import random


def measure(bit, a_basis, e_basis):
    """Simulate Eve's measurement in (possibly) the wrong basis."""
    return bit if a_basis == e_basis else random.randint(0, 1)


def start_eve():
    sock = socket.socket()
    sock.connect(("127.0.0.1", 8080))
    if sock.recv(1024).decode() == "ROLE?":
        sock.sendall(b"Eve")
    print("Eve is intercepting messages between Alice and Bob...")

    buffer = ""
    while True:
        chunk = sock.recv(4096).decode()
        if not chunk:
            print("Connection closed by server.")
            break
        buffer += chunk
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                print("Bad JSON from server:", e)
                continue

            if data.get("type") == "qubit":
                eve_basis = random.randint(0, 1)
                new_bit = measure(data["bit"], data["basis"], eve_basis)
                out = {"type": "qubit", "bit": new_bit, "basis": data["basis"]}
            else:
                out = data

            sock.sendall((json.dumps(out) + "\n").encode())
    sock.close()
    print("Eve connection closed.")


if __name__ == "__main__":
    start_eve()
