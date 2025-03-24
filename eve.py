import socket

def start_eve():
    
    # server configuration
    server_host = "127.0.0.1"
    server_port = 8080

    eve_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    eve_socket.connect((server_host, server_port))
    print("Eve connected to server.")

    try:
        while True:
            bit = eve_socket.recv(1024)
            if not bit:
                break
            if bit == b"ROLE?":
                # Send role to the server
                eve_socket.sendall("Eve".encode())
                continue
            print(f"Eve received encrypted bit: {bit}")
    except KeyboardInterrupt:
        print("Eve interrupted communication.")
    finally:
        print("Connection closed.")
        eve_socket.close()

start_eve()