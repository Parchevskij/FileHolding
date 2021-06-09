import socket
from flask import Flask, render_template, request, redirect, url_for

"""
awith socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    filename = '/Users/evgenij/Downloads/123.png'
    print("Sending:", filename)
    with open(filename, 'rb') as f:
        raw = f.read()

    s.sendall(len(raw).to_bytes(8, 'big'))
    s.sendall(raw)

    data = s.recv(1024)
    s.close()

print("Received", repr(data))"""

app = Flask(__name__)

HOST = "127.0.0.1"
PORT = 65431


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']#.read()
    #start_connections(host, int(port), int(num_conns), uploaded_file)
    #process_connection()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        #filename = '/Users/evgenij/Downloads/123.png'
        #print("Sending:", filename)
        #with open(filename, 'rb') as f:
            #raw = f.read()
        raw = uploaded_file.read()

        s.sendall(len(raw).to_bytes(8, 'big'))
        s.sendall(raw)

        #data = s.recv(1024)
        #s.close()

    print("Received")
    #if uploaded_file.filename != '':
        #uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4443, debug=True)

