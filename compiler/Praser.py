import Defenitions


class ParserOutput:
    def __init__(self, error=None, node=None):
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
        self.index = 0
        self.vars = []
        self.current = self.tokens[self.index]

    def advance(self):
        """
        this function move the next token
        :return: the current token
        """
        self.index += 1
        if self.index < len(self.tokens):
            self.current = self.tokens[self.index]
        return self.current

    def parse(self):
        res = ParserOutput()
        list_of_expr = []

        # while the code didn't finished
        while self.current.type != Defenitions.TT_EOF or self.index < len(
                self.tokens) and self.current.type == Defenitions.TT_SEMI_COLUM:

            # get expression
            expr = res.check(self.expr())
            if hasattr(expr, 'error') and expr.error:
                return expr

            # add it tp the list
            list_of_expr.append(expr)
            self.advance()


        # return a program node
        return res.success(Defenitions.ProgramNode(list_of_expr))

    def factor(self):
        res = ParserOutput()
        token = self.current

        # if there is ) before (
        if token.type == Defenitions.TT_RPAREN:
            return (res.fail(Defenitions.InvalidSyntaxError(
                self.current.pos_start.__copy__(), self.current.pos_end.__copy__(),
                "Expected ')'")))

        # if there is identifier
        if token.type == Defenitions.TT_IDENTIFIER:
            self.advance()

            # if the program saw the token before
            if token.value in self.vars:
                return res.success(Defenitions.NumberNode(token))
            else:
                return (res.fail(Defenitions.InvalidSyntaxError(
                    self.current.pos_start.__copy__(), self.current.pos_end.__copy__(),
                    "undelcrated identifier ")))

        # if there is a number
        if token.type in [Defenitions.TT_FLOAT, Defenitions.TT_INT]:
            self.advance()

            return res.success(Defenitions.NumberNode(token))

        # if there is a plus or minus
        if token.type in [Defenitions.TT_PLUS, Defenitions.TT_MINUS]:
            op_token = self.current
            self.advance()
            node = res.check(self.factor())

            if res.error:
                return res

            return res.success(Defenitions.UnaryOpNode(op_token, node))

        # if there is (
        if token.type == Defenitions.TT_LPAREN:
            self.advance()
            # get the expression inside
            expr = res.check(self.expr())

            # search for )
            if self.current.type == Defenitions.TT_RPAREN:
                self.advance()
                return expr
            else:
                return (res.fail(Defenitions.InvalidSyntaxError(
                    self.current.pos_start.__copy__(), self.current.pos_end.__copy__(),
                    "Expected ')'")))
        else:
            return (res.fail(Defenitions.InvalidSyntaxError(
                self.current.pos_start.__copy__(), self.current.pos_end.__copy__(),
                "invalid syntax ")))

    def term(self):
        res = ParserOutput()

        # get the left factor
        left = res.check(self.factor())

        while self.current.type in [Defenitions.TT_MUL, Defenitions.TT_DIV]:
            token = self.current
            self.advance()
            right = res.check(self.factor())
            if res.error:
                return res

            # define a binary node as left
            left = Defenitions.BinaryOpNode(left, token, right)

        return res.success(left)  # in case that there is no number

    def expr(self):
        res = ParserOutput()

        # if the syntax is like VAR a = 5
        if self.current == Defenitions.Token(Defenitions.TT_KEY_WORD, "VAR"):
            self.advance()

            # take the identifier
            if self.current.type == Defenitions.TT_IDENTIFIER:
                indentifier_token = self.current
                self.advance()

            else:
                return (res.fail(Defenitions.InvalidSyntaxError(
                    self.current.pos_start.__copy__(), self.current.pos_end.__copy__(),
                    "missing identifier")))

            # then search for the =
            if self.current.type == Defenitions.TT_EQ:
                self.advance()
            else:
                return (res.fail(Defenitions.InvalidSyntaxError(
                    self.current.pos_start.__copy__(), self.current.pos_end.__copy__(),
                    "missing =")))

            # then take the expression
            expr = res.check(self.expr())
            if res.error:
                return res


            # add to the vars list the new key
            if indentifier_token.value in self.vars:
                first = False
            else:
                first = True
                self.vars.append(indentifier_token.value)

            return res.success(Defenitions.DeclarationNode(indentifier_token, expr, first))
        else:
            # the other syntax option is term PULS/MINUS term
            left = res.check(self.term())

            while self.current.type in [Defenitions.TT_PLUS, Defenitions.TT_MINUS]:
                token = self.current
                self.advance()
                right = res.check(self.term())

                if res.error:
                    return res
                left = Defenitions.BinaryOpNode(left, token, right)

            return res.success(left)  # in case that there is no number