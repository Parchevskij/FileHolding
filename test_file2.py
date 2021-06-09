import socket

HOST = "127.0.0.1"
PORT = 65431

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        expected_size = b""
        while len(expected_size) < 8:
            more_size = conn.recv(8 - len(expected_size))
            if not more_size:
                raise Exception("Short file length received")
            expected_size += more_size
        expected_size = int.from_bytes(expected_size, 'big')
        packet = b""  # Use bytes, not str, to accumulate
        while len(packet) < expected_size:
            buffer = conn.recv(expected_size - len(packet))
            if not buffer:
                raise Exception("Incomplete file received")
            packet += buffer
        filename = 'new_file.png'
        with open(filename, 'wb') as f:
            f.write(packet)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)