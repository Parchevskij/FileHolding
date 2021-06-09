import socket
#from test0 import filename
HOST = "127.0.0.1"
PORT = 65431


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    filename = 'test.pdf'
    print("Sending:", filename)
    with open(filename, 'rb') as f:
        raw = f.read()
    #s.sendall(filename.encode('ascii'))
    s.sendall(len(raw).to_bytes(8, 'big'))
    s.sendall(raw)

