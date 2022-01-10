import Defenitions

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.advance()

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current = self.tokens[self.index]
        return self.current

    def parse(self):
        result = self.expr()
        return result

    def factor(self):
        token = self.current

        if token.type in [Defenitions.TT_RPAREN]:
            self.advance()
            return Defenitions.
        if token.type in [Defenitions.TT_FLOAT, Defenitions.TT_INT]:
            self.advance()
            return Defenitions.NumberNode(token)

    def term(self):
        left = self.factor()

        while self.current.type in [Defenitions.TT_MUL, Defenitions.TT_DIV]:
            token = self.current
            self.advance()
            right = self.factor()
            left = Defenitions.BinaryOpNode(left, token, right)

        return left # in case that there is no number


    def expr(self):
        left = self.term()

        while self.current.type in [Defenitions.TT_PLUS, Defenitions.TT_MINUS]:
            token = self.current
            self.advance()
            right = self.term()
            left = Defenitions.BinaryOpNode(left, token, right)

        return left  # in case that there is no number



