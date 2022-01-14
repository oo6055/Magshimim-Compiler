from lexer import Lexer
import Defenitions
from Praser import Parser
from CodeGen import CodeGen
while True:
    lexer = Lexer("SDTIN",input())
    tokens = lexer.create_tokens()
    if isinstance(tokens, Defenitions.Error):
        print(tokens)
    else:
        parser = Parser(tokens)
        output = parser.parse()
        print(output)
        if output.error:
            print(output.error)
        else:
            print(output.node.code_gen())




# for token in tokens:
#     print(token)