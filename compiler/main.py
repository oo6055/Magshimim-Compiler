from lexer import Lexer
import Defenitions
from Praser import Parser
while True:
    lexer = Lexer("SDTIN",input("basic>"))
    tokens = lexer.create_tokens()
    if isinstance(tokens, Defenitions.Error):
        print(tokens)
    else:
        parser = Parser(tokens)
        output = parser.parse()
        if output.error:
            print(output.error)
        else:
            print(output.node)




# for token in tokens:
#     print(token)