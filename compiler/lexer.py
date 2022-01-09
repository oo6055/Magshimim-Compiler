import re
import Defenitions



class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Defenitions.Position(-1, 0, -1, fn, text)
        self.current_char = None

        # initiate the system
        self.advance()

    def advance(self):
        # advance the pos object
        self.pos.advance(self.current_char)

        # put in current char the right index
        if self.pos.index < len(self.text):
            self.current_char = self.text[self.pos.index]
        else:
            self.current_char = None

    def create_tokens(self):
        tokens = []

        speciel_keys = ['+', '*', '-', '/', '(', ')']
        speciel_type_of_tokens = [Defenitions.TT_PLUS, Defenitions.TT_MUL, Defenitions.TT_MINUS, Defenitions.TT_DIV, Defenitions.TT_LPAREN, Defenitions.TT_RPAREN]

        # scan the file
        while self.current_char != None:
            # if it is a blank or a space ignore it
            if self.current_char in " \t":
                self.advance()
            elif re.match("[0-9]", self.current_char):
                token = self.tokenize_number()
                tokens.append(token)
            elif self.current_char in speciel_keys:
                token = Defenitions.Token(speciel_type_of_tokens[speciel_keys.index(self.current_char)])
                tokens.append(token)
            # if token is not in that list
            else:
                return [], Defenitions.IllegalCharError(self.pos, self.pos, "'{}'".format(self.current_char))
        return tokens



    def tokenize_number(self):
        num_str = ""

        # maybe it can be a float
        while self.pos.index < len(self.text) and re.match("[0-9.]", self.current_char):
            # check if there is a dot inside it
            if "." in num_str and self.current_char == '.':
                break
            num_str += self.current_char
            self.advance()


        if "." in num_str:

            return Defenitions.Token(Defenitions.TT_FLOAT, float(num_str))
        else:
            return Defenitions.Token(Defenitions.TT_INT, int(num_str))