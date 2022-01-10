TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def __repr__(self):
        result = '{}:{}'.format(self.error_name, self.details)
        result += 'File {}, line {}'.format(self.pos_start.fn, self.pos_start.line)
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class Position:
    def __init__(self, index, line, column, fn, ftxt):
        self.index = index  # in the whole file
        self.line = line
        self.column = column
        self.fn = fn
        self.ftxt = ftxt


    def advance(self, current_char):
        self.index += 1
        self.column += 1

        if current_char == '\n':
            self.line += 1
            self.column = 0

        return self


class Token:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value:
            return '{}:{}'.format(self.type, self.value)
        else:
            return '{}'.format(self.type)


# defenitions for the par
#
#
# ser
class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return '{}'.format(self.token)


class BinaryOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        return "({} {} {})".format(self.left_node, self.op_token, self.right_node)