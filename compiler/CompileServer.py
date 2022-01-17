import socket
import sys
from lexer import Lexer
import Defenitions
from Praser import Parser

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen()

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from', client_address)

        # like HTTP server
        data = connection.recv(1024).decode()

        data = data.replace('\r','')

        print(data)
        print("receve")
        if len(data):
            lexer = Lexer("SDTIN", data)
            tokens = lexer.create_tokens()
            print(tokens)
            if isinstance(tokens, Defenitions.Error):
                code = str(tokens)
            else:
                parser = Parser(tokens)
                output = parser.parse()
                print(output)
                if output.error:
                    code = str(output.error)
                else:
                    code = str(output.node.code_gen())



            print('finish.....\nsending data back to the client')
            connection.sendall(code.encode())
            connection.close()
    finally:
        connection.close()