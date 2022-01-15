from lexer import Lexer
import Defenitions
from Praser import Parser

file = open("code.ori", "r")
code = file.read()
file.close()
lexer = Lexer("SDTIN",code)
tokens = lexer.create_tokens()
print(tokens)
if isinstance(tokens, Defenitions.Error):
    print(tokens)
else:
    parser = Parser(tokens)
    output = parser.parse()
    print(output)
    if output.error:
        print(output.error)
    else:
        code = output.node.code_gen()
        print(code)

        file = open("code.asm", "w")
        file.write(code)
        file.close()






# for token in tokens:
#     print(token)