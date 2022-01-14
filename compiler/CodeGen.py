import Defenitions

class CodeGen:

    def __init__(self):
        pass
    def visit(self, node):
        name_of_method = "handle_with_" + type(node).__name__
        method = getattr(self, name_of_method)
        result = method(node)

        return result

    def handle_with_NumberNode(self, node):
        return Defenitions.Number(node.token.value)



    def handle_with_UnaryOpNode(self, node):
        right = self.visit(node.number_node)

        if node.op_token.type == Defenitions.TT_MINUS:
            right = Defenitions.Number(right.value * -1)

        return right



    def handle_with_BinaryOpNode(self, node):
        right = self.visit(node.left_node)
        left = self.visit(node.right_node)

        commands = "mov ax " + str(right.value) + "\n"
        commands += "mov bx " + str(left.value) + "\n"


        if node.op_token.type == Defenitions.TT_PLUS:
            commands += "add "
        elif node.op_token.type == Defenitions.TT_MINUS:
            commands += "sub "
        commands += "ax, bx\n"

        commands += "push ax"

        return commands





