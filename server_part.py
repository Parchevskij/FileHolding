import socket
import os

config = {
    'HOST': '127.0.0.1',
    'PORT': 65431
}


class Server:
    def __init__(self):
        self.config = config
        self.update()
        self.path_to_database = 'database/'

    def update(self):
        for key, value in self.config.items():
            setattr(self, key, value)

    def upload_file(self, filename, data):
        with open(self.path_to_database+filename, 'wb') as f:
            f.write(data)

    def call(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            print('Server is turned on...')
            while True:
                conn, addr = s.accept()
                print("Connected by", addr)
                print("Server receiving flag")
                val = int.from_bytes(conn.recv(1), 'big')
                print(val)
                if val == 1:
                    print('Server Receiving')
                    with conn:
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

                        packet = b""
                        while len(packet) < expected_size:
                            buffer = conn.recv(expected_size - len(packet))
                            if not buffer:
                                raise Exception("Incomplete file received")
                            packet += buffer
                        filename = 'database/' + filename
                        with open(filename, 'wb') as f:
                            f.write(packet)
                else:
                    print("Server filename receiving")

                    expected_filesize = conn.recv(4)
                    filesize = int.from_bytes(expected_filesize, 'big')
                    filename = conn.recv(filesize).decode()

                    print("Server Sending")
                    with conn:
                        with open('database/' + filename, 'rb') as f:
                            raw = f.read()

                        conn.sendall(len(raw).to_bytes(8, 'big'))
                        conn.sendall(raw)


cl = Server()
cl.call()