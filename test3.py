import socket

'''
Client for Receiving
'''


HOST = "127.0.0.1"
PORT = 65431
filename = 'test.pdf'


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    print("Client Sending flag")
    flag: int = 2
    s.send(flag.to_bytes(1, 'big'))

    print('Client Receiving')
    with s:

        s.sendall(len(filename).to_bytes(4, 'big'))
        s.sendall(filename.encode())

        #expected_filesize = s.recv(4)
        #filesize = int.from_bytes(expected_filesize, 'big')
        #filename = s.recv(filesize).decode()
        expected_size = b""
        while len(expected_size) < 8:
            more_size = s.recv(8 - len(expected_size))
            if not more_size:
                raise Exception("Short file length received")
            expected_size += more_size
        expected_size = int.from_bytes(expected_size, 'big')

        packet = b""
        while len(packet) < expected_size:
            buffer = s.recv(expected_size - len(packet))
            if not buffer:
                raise Exception("Incomplete file received")
            packet += buffer
        filename = 'save/new_2_' + filename
        with open(filename, 'wb') as f:
            f.write(packet)