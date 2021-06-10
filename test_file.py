import socket
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    HOST = "127.0.0.1"
    PORT = 65431
    uploaded_file = request.files['file']
    raw = uploaded_file.read()
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        raw = uploaded_file.read()

        s.sendall(len(uploaded_file.filename).to_bytes(4, 'big'))
        s.sendall(uploaded_file.filename.encode('ascii'))
        s.sendall(len(raw).to_bytes(8, 'big'))
        s.sendall(raw)
    '''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Client Sending flag")
        flag: int = 1
        s.send(flag.to_bytes(1, 'big'))
        print("Client Sending:", uploaded_file.filename)

        s.sendall(len(uploaded_file.filename).to_bytes(4, 'big'))
        s.sendall(uploaded_file.filename.encode('ascii'))
        s.sendall(len(raw).to_bytes(8, 'big'))
        s.sendall(raw)
    print("Received")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4443, debug=True)

