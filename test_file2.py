import socket
'''
Server part
'''

HOST = "127.0.0.1"
PORT = 65431

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            expected_filesize = conn.recv(4)
            filesize = int.from_bytes(expected_filesize, 'big')
            filename = conn.recv(filesize).decode()
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

            with open(filename, 'wb') as f:
                f.write(packet)