from lexer import Lexer
from Praser import Parser
while True:
    lexer = Lexer("SDTIN",input("basic>"))
    tokens = lexer.create_tokens()
    parser = Parser(tokens)
    output = parser.parse()
    if output.error:
        print(output.error)
    else:
        print(output.node)



# for token in tokens:
#     print(token)