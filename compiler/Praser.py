import Defenitions

class ParserOutput:
    def __init__(self, error = None, node = None):
        self.error = error
        self.node = node


    def check(self, res):
        if isinstance(res, ParserOutput):
            if res.error:
                self.error = res.error
            return res.node

        return res


    def __repr__(self):
        return "{}".format(self.node)


    def success(self, node):
        self.node = node
        return self


    def fail(self, error):
        self.error = error
        return self


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
        res = ParserOutput()
        token = self.current

        if token.type == Defenitions.TT_RPAREN:
            return (res.fail(Defenitions.InvalidSyntaxError(
                self.current.pos_start.__copy__(), self.current.pos_end.__copy__(),
                "Expected ')'")))
        # need to handle with
        if token.type in [Defenitions.TT_FLOAT, Defenitions.TT_INT]:
            res.check(self.advance())
            return res.success(Defenitions.NumberNode(token))
        if token.type in [Defenitions.TT_PLUS, Defenitions.TT_MINUS]:
            op_token = self.current
            res.check(self.advance())
            node = res.check(self.factor())

            if res.error:
                return res

            return res.success(Defenitions.UnaryOpNode(op_token, node))
        if token.type == Defenitions.TT_LPAREN:
            res.check(self.advance())
            expr = res.check(self.expr())

            if self.current.type == Defenitions.TT_RPAREN:
                res.check(self.advance())
                return expr
            else:
                return (res.fail(Defenitions.InvalidSyntaxError(
					self.current.pos_start.__copy__(), self.current.pos_end.__copy__(),
					"Expected ')'")))


    def term(self):
        res = ParserOutput()

        left = res.check(self.factor())

        while self.current.type in [Defenitions.TT_MUL, Defenitions.TT_DIV]:
            token = self.current
            res.check(self.advance())
            right = res.check(self.factor())
            if res.error:
                return res
            left = Defenitions.BinaryOpNode(left, token, right)

        return res.success(left) # in case that there is no number


    def expr(self):
        res = ParserOutput()

        if self.current == Defenitions.Token(Defenitions.TT_KEY_WORD, "VAR"):
            res.check(self.advance())
            if self.current.type == Defenitions.TT_IDENTIFIER:
                indentifier_token = self.current
                res.check(self.advance())
            else:
                return (res.fail(Defenitions.InvalidSyntaxError(
                    self.current.pos_start.__copy__(), self.current.pos_end.__copy__(),
                    "missing identifier")))

            if self.current.type == Defenitions.TT_EQ:
                res.check(self.advance())
            else:
                return (res.fail(Defenitions.InvalidSyntaxError(
					self.current.pos_start.__copy__(), self.current.pos_end.__copy__(),
					"missing =")))

            expr = res.check(self.expr())
            if res.error:
                return res.error

            return res.success(Defenitions.DelecrationNode(indentifier_token, expr))



        else:
            left = res.check(self.term())

            while self.current.type in [Defenitions.TT_PLUS, Defenitions.TT_MINUS]:
                token = self.current
                res.check(self.advance())
                right = res.check(self.term())
                if res.error:
                    return res
                left = Defenitions.BinaryOpNode(left, token, right)

            return res.success(left)  # in case that there is no number