from lexer import Lexer
from Praser import Parser
while True:
    lexer = Lexer("SDTIN",input("basic>"))
    tokens = lexer.create_tokens()
    parser = Parser(tokens)

    print(parser.parse())



# for token in tokens:
#     print(token)