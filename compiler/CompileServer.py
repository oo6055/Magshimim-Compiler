import socket
import sys
from lexer import Lexer
import Defenitions
from Praser import Parser

def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('0.0.0.0', 123)
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

            data = connection.recv(1024).decode()

            if len(data):
                lexer = Lexer(text=data)
                tokens = lexer.create_tokens()

                if isinstance(tokens, Defenitions.Error):
                    code = str(tokens)
                else:
                    parser = Parser(tokens)
                    output = parser.parse()

                    if output.error:
                        code = str(output.error)
                    else:
                        code = str(output.node.code_gen())

                print('finish.....\nsending data back to the client')
                connection.sendall(code.encode())
                connection.close()
        finally:
            connection.close()


if __name__ == "__main__":
    main()