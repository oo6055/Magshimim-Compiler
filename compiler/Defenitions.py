TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_SEMI_COLUM = 'SEMI_COLUM'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'
TT_EQ = 'EQ'
TT_IDENTIFIER = 'TT_IDENTIFIER'
TT_KEY_WORD= 'KEY_WORD'


KEYWORDS = ["VAR"]

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

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)


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

    def __repr__(self):
        return "{}".format(self.index)

    def __copy__(self):
        return Position(self.index, self.line, self.column, self.fn, self.ftxt)


class Token:
    def __init__(self, type, value = None, pos_start =  None, pos_end = None):
        self.type = type
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __repr__(self):
        if self.value:
            return '{}:{}'.format(self.type, self.value)
        else:
            return '{}'.format(self.type)


# defenitions for the par
class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return '{}'.format(self.token)

    def code_gen(self):
        commands = "push " + str(self.token.value) + "\n"
        return commands


class BinaryOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def insert_op_2_numbers(self, op):
        return op + " ax, bx\n"


    def insert_op_1_number(self, op):
        return op + " bx\n"


    def code_gen(self):
        op_dict = {TT_MINUS: "sub",
                   TT_PLUS: "add",
                   TT_MUL: "mul",
                   TT_DIV: "div"}
        commands = self.left_node.code_gen()
        commands += self.right_node.code_gen()

        if self.op_token.type in [TT_MINUS, TT_PLUS]:
            commands += "pop bx \n" # get the right
            commands += "pop ax \n"# get the left
            commands += self.insert_op_2_numbers(op_dict[self.op_token.type])
            commands += "push ax \n"  # get the right
        elif self.op_token.type in [TT_MUL, TT_DIV]:
            commands += "pop bx \n" # get the right
            commands += "pop ax \n"  # get the left
            commands += self.insert_op_1_number(op_dict[self.op_token.type])
            commands += "push ax \n"  # get the right



        return commands


    def __repr__(self):
        return "({} {} {})".format(self.left_node, self.op_token, self.right_node)

class UnaryOpNode:
    def __init__(self, op_token, number_node):
        self.op_token = op_token
        self.number_node = number_node

    def __repr__(self):
        return "({} {})".format(self.op_token, self.number_node)

    def code_gen(self):
        commands = self.number_node.code_gen()

        commands += "pop ax\n"
        if self.op_token.type == TT_MINUS:
            commands += "mul -1\n"
        commands += "push ax\n"
        return commands

class DelecrationNode:
    def __init__(self, identifier_token, value):
        self.identifier_token = identifier_token
        self.value = value


    def code_gen(self):
        commands = self.identifier_token.value + " dw ?\n"
        commands += self.value.code_gen()
        commands += "pop ax\n"
        commands += "mov " + self.identifier_token.value + ", ax\n"


        return commands


    def __repr__(self):
        return "({} {})".format(self.identifier_token, self.value)


class ProgramNode:
    def __init__(self, list_of_expr):
        self.list_of_expr = list_of_expr

    def __repr__(self):
        represnvie_string = ""
        for expr in self.list_of_expr:
            represnvie_string += str(expr) + ";"

        return represnvie_string




    def code_gen(self):
        commands = ""
        for expr in self.list_of_expr:
            commands += expr.code_gen()

        return commands
