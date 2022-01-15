import re
import Defenitions



class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Defenitions.Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.vars = []

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

        speciel_keys = ['\n','=','+', '*', '-', '/', '(', ')']
        speciel_type_of_tokens = [Defenitions.TT_SEMI_COLUM, Defenitions.TT_EQ, Defenitions.TT_PLUS, Defenitions.TT_MUL, Defenitions.TT_MINUS, Defenitions.TT_DIV, Defenitions.TT_LPAREN, Defenitions.TT_RPAREN]

        # scan the file
        while self.current_char != None:
            # if it is a blank or a space ignore it
            if self.current_char in " \t":
                self.advance()
            elif re.match("[0-9]", self.current_char):
                token = self.tokenize_number()
                tokens.append(token)
            elif self.current_char in speciel_keys:
                token = Defenitions.Token(speciel_type_of_tokens[speciel_keys.index(self.current_char)],pos_start=self.pos.__copy__(),pos_end= self.pos.__copy__())
                tokens.append(token)
                self.advance()
            elif self.current_char.isalpha():
                token = self.tokenize_identifier()
                tokens.append(token)

            # if token is not in that list
            else:
                return Defenitions.IllegalCharError(self.pos.__copy__(), self.pos.__copy__(), "'{}'".format(self.current_char))

        tokens.append(Defenitions.Token(Defenitions.TT_EOF, pos_start=self.pos.__copy__(),pos_end= self.pos.__copy__()))
        return tokens



    def tokenize_number(self):
        num_str = ""
        pos_start = self.pos.__copy__()

        # maybe it can be a float
        while self.pos.index < len(self.text) and re.match("[0-9.]", self.current_char):
            # check if there is a dot inside it
            if "." in num_str and self.current_char == '.':
                break
            num_str += self.current_char
            self.advance()


        if "." in num_str:

            return Defenitions.Token(Defenitions.TT_FLOAT, float(num_str), pos_start, self.pos)
        else:
            return Defenitions.Token(Defenitions.TT_INT, int(num_str), pos_start.__copy__(), self.pos.__copy__())

    def tokenize_identifier(self):
        start_pos = self.pos.__copy__()
        current_str = ""
        type = Defenitions.TT_IDENTIFIER


        while self.pos.index < len(self.text) and self.current_char.isalpha():
            current_str += self.current_char
            self.advance()

        if current_str in Defenitions.KEYWORDS:
            type = Defenitions.TT_KEY_WORD

        return Defenitions.Token(type, current_str, start_pos, self.pos)