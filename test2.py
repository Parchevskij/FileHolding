import socket
HOST = "127.0.0.1"
PORT = 65431


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    val = int(input("write 1 or 2 \n"))
    if val == 1:
        filename = 'test.pdf'
        print("Client Sending:", filename)
        with open('data/'+filename, 'rb') as f:
            raw = f.read()

        s.sendall(len(filename).to_bytes(4, 'big'))
        s.sendall(filename.encode())
        #print(len(filename.encode()))
        s.sendall(len(raw).to_bytes(8, 'big'))
        s.sendall(raw)

    else:
        print('Client Receiving')
        txt = s.recv(1024)
        print(txt)

