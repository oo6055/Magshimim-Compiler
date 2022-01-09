from lexer import Lexer

lexer = Lexer("file", "1.2 + 5")
tokens = lexer.create_tokens()
print(tokens)



# for token in tokens:
#     print(token)