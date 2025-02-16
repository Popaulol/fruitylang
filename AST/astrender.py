from abc import ABC
from typing import TextIO

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
from unit import Unit


def render_ast(ast: ASTNode, filename: str) -> None:
    with open(filename, "w") as f:
        walker = ASTRender(f)
        walker.preamble()
        ast.walk(walker)
        walker.postamble()


class ASTRender(ASTWalker[str]):
    def walk_type[A, K](self, node: Type, *args: A, **kwargs: K) -> str:
        current_id = self.get_id()
        self.file.write(f'    {current_id} [label="Type"]\n')
        name = node.name.walk(self)
        self.file.write(f'    {current_id} -> {name} [label="name"]\n')

        if node.units:
            unit = node.units.walk(self)
            self.file.write(f'    {current_id} -> {unit} [label="unit"]\n')

        return current_id

    def walk_function[A, K](self, node: Function, *args: A, **kwargs: K) -> str:
        current_id = self.get_id()
        self.file.write(f'    {current_id} [label="Function"]\n')
        name = node.name.walk(self)
        self.file.write(f'    {current_id} -> {name} [label="name"]\n')
        for n, argument in enumerate(node.arguments):
            argument_id = argument[0].walk(self)
            type_id = argument[1].walk(self)
            self.file.write(f'    {current_id} -> {{{argument_id} {type_id}}} [label="arg {n}"]\n')

        return_type = node.return_type.walk(self)
        self.file.write(f'    {current_id} -> {return_type} [label="return"]\n')

        body = node.body.walk(self)
        self.file.write(f'    {current_id} -> {body} [label="body"]\n')

        return current_id

    def walk_program[A, K](self, node: Program, *args: A, **kwargs: K) -> str:
        current_id = self.get_id()
        self.file.write(f'    {current_id} [label="Program"]\n')
        for n, definition in enumerate(node.definitions):
            self.file.write(f'    {current_id} -> {definition.walk(self)} [label="{n}"]\n')

        return current_id

    def walk_block[A, K](self, node: Block, *args: A, **kwargs: K) -> str:
        current_id = self.get_id()
        self.file.write(f'    {current_id} [label="Block"]\n')
        for n, expression in enumerate(node.expressions):
            self.file.write(f'    {current_id} -> {expression.walk(self)} [label="{n}"]\n')

        return_expression = node.return_expression.walk(self)
        self.file.write(f'    {current_id} -> {return_expression}[label="return_expression"]\n')

        return current_id


    def walk_call[A, K](self, node: Call, *args: A, **kwargs: K) -> str:
        current_id = self.get_id()
        self.file.write(f'    {current_id}[label="call"]\n')
        callee = node.callee.walk(self)
        self.file.write(f'    {current_id} -> {callee}[label="callee"]\n')
        for n, argument in enumerate(node.arguments):
            argument = argument.walk(self)
            self.file.write(f'    {current_id} -> {argument}[label="argument {n}"]\n')

        return current_id

    def __init__(self, file: TextIO) -> None:
        self.id_tracker = 0
        self.file = file

    def binary_operator(
        self, node: Add | Sub | Mul | Div | Exponent, operator: str
    ) -> str:
        current_id = self.get_id()
        left = node.left.walk(self)
        right = node.right.walk(self)
        self.file.write(f'    {current_id}[label="{operator}"]\n')
        self.file.write(f'    {current_id} -> {left}[label="lhs"]\n')
        self.file.write(f'    {current_id} -> {right}[label="rhs"]\n')
        return current_id

    def preamble(self) -> None:
        self.file.write("digraph AST {\n")

    def postamble(self) -> None:
        self.file.write("}")

    def get_id(self) -> str:
        self.id_tracker += 1
        return "node_" + str(self.id_tracker)

    def walk_add[A, K](self, node: Add, *args: A, **kwargs: K) -> str:
        return self.binary_operator(node, "+")

    def walk_sub[A, K](self, node: Sub, *args: A, **kwargs: K) -> str:
        return self.binary_operator(node, "-")

    def walk_mul[A, K](self, node: Mul, *args: A, **kwargs: K) -> str:
        return self.binary_operator(node, "*")

    def walk_div[A, K](self, node: Div, *args: A, **kwargs: K) -> str:
        return self.binary_operator(node, "/")

    def walk_invert[A, K](self, node: Invert, *args: A, **kwargs: K) -> str:
        current_id = self.get_id()
        right = node.right.walk(self)
        self.file.write(f'    {current_id}[label="-"]\n')
        self.file.write(f'    {current_id} -> {right}[label="rhs"]\n')
        return current_id

    def walk_exponent[A, K](self, node: Exponent, *args: A, **kwargs: K) -> str:
        return self.binary_operator(node, "**")

    def walk_identifier[A, K](self, node: Identifier, *args: A, **kwargs: K) -> str:
        current_id = self.get_id()
        self.file.write(f'    {current_id}[label="{node.name}"]\n')
        return current_id

    def walk_unit_number[A, K](self, node: UnitNumber, *args: A, **kwargs: K) -> str:
        current_id = self.get_id()
        number = node.number.walk(self)

        self.file.write(f'    {current_id}[label="unit_number"]\n')
        self.file.write(f'    {current_id} -> {number}\n')


        if node.unit and node.unit.unit != Unit():
            unit = node.unit.walk(self)
            self.file.write(f'    {current_id} -> {unit}\n')

        return current_id

    def walk_number[A, K](self, node: Number, *args: A, **kwargs: K) -> str:
        current_id = self.get_id()
        self.file.write(f'    {current_id}[label="{node.value}"]\n')
        return current_id

    def walk_ast_unit[A, K](self, node: ASTUnit, *args: A, **kwargs: K) -> str:
        current_id = self.get_id()
        self.file.write(f'    {current_id}[label="{node.unit}"]\n')
        return current_id
