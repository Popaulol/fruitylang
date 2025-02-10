from AST.ast import (
    Add,
    ASTNode,
    ASTUnit,
    Div,
    Exponent,
    Identifier,
    Invert,
    Mul,
    Number,
    Sub,
    UnitNumber,
)
from AST.astwalker import ASTWalker


def print_ast(node: ASTNode) -> None:
    print(node.walk(ASTPrinter()))


class ASTPrinter(ASTWalker[str]):
    def walk_add[A, K](self, node: Add, *args: A, **kwargs: K) -> str:
        return "(" + node.left.walk(self) + "+" + node.right.walk(self) + ")"

    def walk_sub[A, K](self, node: Sub, *args: A, **kwargs: K) -> str:
        return "(" + node.left.walk(self) + "-" + node.right.walk(self) + ")"

    def walk_mul[A, K](self, node: Mul, *args: A, **kwargs: K) -> str:
        return "(" + node.left.walk(self) + "*" + node.right.walk(self) + ")"

    def walk_div[A, K](self, node: Div, *args: A, **kwargs: K) -> str:
        return "(" + node.left.walk(self) + "/" + node.right.walk(self) + ")"

    def walk_invert[A, K](self, node: Invert, *args: A, **kwargs: K) -> str:
        return "(- " + node.right.walk(self) + ")"

    def walk_exponent[A, K](self, node: Exponent, *args: A, **kwargs: K) -> str:
        return "(" + node.left.walk(self) + "**" + node.right.walk(self) + ")"

    def walk_identifier[A, K](self, node: Identifier, *args: A, **kwargs: K) -> str:
        return node.name

    def walk_unit_number[A, K](self, node: UnitNumber, *args: A, **kwargs: K) -> str:
        return node.number.walk(self) + (node.unit.walk(self) if node.unit else "")

    def walk_number[A, K](self, node: Number, *args: A, **kwargs: K) -> str:
        return str(node.value)

    def walk_ast_unit[A, K](self, node: ASTUnit, *args: A, **kwargs: K) -> str:
        return str(node.unit)
