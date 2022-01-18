from flask import Flask,render_template
from flask import request
import socket

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
    server_address = ('0.0.0.0', 123)
    sock.connect(server_address)

    try:

        # Send data
        sock.sendall(text.encode())

        data = sock.recv(1024)
        sock.close()

    finally:
        sock.close()

    return render_template("index.html", code=text, content=data.decode())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)