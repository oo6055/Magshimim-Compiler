from flask import Flask,render_template
from flask import request
import socket
import sys

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("index.html", content="")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    sock.connect(server_address)

    try:

        # Send data
        message = b'This is the message.  It will be repeated.'
        sock.sendall(message)





        data = sock.recv(1024)
        print('received "%s"' % data)

    finally:
        sock.close()

    return render_template("index.html", code=text, content=text.upper())

if __name__ == "__main__":
    app.run()