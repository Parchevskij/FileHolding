import os
import socket
from flask import Flask, render_template, request, redirect, url_for
import numpy as np

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


@app.route('/disk', methods=['GET', 'POST'])
def disk():
    database_files = os.listdir('database/')
    database_sizes = list()
    for file in database_files:
        file_size = os.path.getsize('database/'+file)
        if file_size > 10**9:
            file_size /= 1024**3
            file_weight = 'Gb'
            size = '%.2f'%file_size+' {}'.format(file_weight)
        elif file_size > 10**6:
            file_size /= 1024**2
            file_weight = 'MB'
            size = '%.2f' % file_size + ' {}'.format(file_weight)
        else:
            file_size /= 1024
            file_weight = 'kB'
            size = '%.2f' % file_size + ' {}'.format(file_weight)

        database_sizes.append(size)
    print(database_files, database_sizes)
    data = zip(database_files, database_sizes)
    return render_template('disk.html', data=data)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4446, debug=True)

