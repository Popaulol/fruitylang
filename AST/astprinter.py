from abc import ABC

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
    UnitNumber, Call, Program, Block, Function, Type,
)
from AST.astwalker import ASTWalker


def print_ast(node: ASTNode) -> None:
    print(node.walk(ASTPrinter()))


class ASTPrinter(ASTWalker[str]):
    def walk_type[A, K](self, node: Type, *args: A, **kwargs: K) -> str:
        return f"Type({node.name.walk(self)}{' ' + node.units.walk(self) if node.units else ''})"

    def walk_function[A, K](self, node: Function, *args: A, **kwargs: K) -> str:
        return f"{node.name}({','.join(f'{name.walk(self)},{typ.walk(self)}' for name, typ in node.arguments)}) -> {node.return_type.walk(self)}: {node.body.walk(self)}"

    def walk_program[A, K](self, node: Program, *args: A, **kwargs: K) -> str:
        return ";\n".join(definition.walk(self) for definition in node.definitions)

    def walk_call[A, K](self, node: Call, *args: A, **kwargs: K) -> str:
        return node.callee.walk(self) + "(" + ", ".join(argument.walk(self) for argument in node.arguments) + ")"

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

    def walk_block[A, K](self, node: Block, *args: A, **kwargs: K) -> str:
        return "{\n" + ";\n".join(expression.walk(self) for expression in node.expressions) + (node.return_expression.walk(self) + "\n" if node.return_expression else "") + "}"


