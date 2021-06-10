import socket

'''
Client for Sending
'''


HOST = "127.0.0.1"
PORT = 65431
filename = 'test.pdf'


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Client Sending flag")
    flag: int = 1
    s.send(flag.to_bytes(1, 'big'))
    print("Client Sending:", filename)
    with open('data/'+filename, 'rb') as f:
        raw = f.read()

    s.sendall(len(filename).to_bytes(4, 'big'))
    s.sendall(filename.encode())
    s.sendall(len(raw).to_bytes(8, 'big'))
    s.sendall(raw)