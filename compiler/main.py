from lexer import Lexer

text_input = """
 print(4 + 4 - 2);
 print("hello world");
"""

lexer = Lexer("file", "1.2 + 5")
tokens = lexer.create_tokens()
print(tokens)



# for token in tokens:
#     print(token)