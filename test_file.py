import socket
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

HOST = "127.0.0.1"
PORT = 65431


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        raw = uploaded_file.read()

        s.sendall(len(uploaded_file.filename).to_bytes(4, 'big'))
        s.sendall(uploaded_file.filename.encode('ascii'))
        s.sendall(len(raw).to_bytes(8, 'big'))
        s.sendall(raw)

    print("Received")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4443, debug=True)

