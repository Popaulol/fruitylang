import sys
import traceback
from _ast import Return
from pprint import pprint

from tatsu.objectmodel import Node
from tatsu.walkers import NodeWalker

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
    UnitNumber, Call, Program, Definition, Block, Function, Type,
)
from unit import UNIT_MAP, Unit


def create_ast(parse_result: str) -> ASTNode:
    return ASTGenerator().walk(parse_result)  # type: ignore


class ASTGenerator(NodeWalker):  # type: ignore
    def walk_object(self, node: Node) -> ASTNode:
        # pprint(node, width=20, indent=4)
        traceback.print_stack()
        print("UNPARSED NODE: " + str(type(node)) + " ", file=sys.stderr)
        return Identifier("UNPARSED NODE: " + str(type(node)))

    def walk_Add(self, node: Node) -> ASTNode:
        return Add(self.walk(node.left), self.walk(node.right))

    def walk_Subtract(self, node: Node) -> ASTNode:
        return Sub(self.walk(node.left), self.walk(node.right))

    def walk_Multiply(self, node: Node) -> ASTNode:
        return Mul(self.walk(node.left), self.walk(node.right))

    def walk_Divide(self, node: Node) -> ASTNode:
        return Div(self.walk(node.left), self.walk(node.right))

    def walk_Exponentiate(self, node: Node) -> ASTNode:
        return Exponent(self.walk(node.base), self.walk(node.exponent))

    def walk_Invert(self, node: Node) -> ASTNode:
        return Invert(self.walk(node.value))

    def walk_Unit_number(self, node: Node) -> ASTNode:
        # pprint(node, width=20, indent=4)
        return UnitNumber(self.walk(node.value), self.walk(node.units))

    def walk_Number(self, node: Node) -> ASTNode:
        #pprint(node, width=20, indent=4)
        #print(node)
        try:
            if "." in node.ast:
                return Number(float(node.ast))
            else:

                    return Number(int(node.ast))
        except ValueError as e:
            return Identifier(f"NUMBER Failed: {e}")

    def walk_units(self, node: Node) -> ASTNode:
        combined_unit = Unit()
        for unit in node.units:
            combined_unit = combined_unit.combined(self.walk(unit).unit)
        return ASTUnit(combined_unit)

    def walk_Unit(self, node: Node) -> ASTNode:
        if node.ast["name"].name in UNIT_MAP.keys():
            return ASTUnit(UNIT_MAP[node.ast["name"].name][0])
        else:
            assert False, f"Unit {node.ast["name"].name} is not a known unit"

    def walk_Subexpression(self, node: Node) -> ASTNode:
        return self.walk(node.expr)  # type: ignore

    def walk_Call(self, node: Node) -> ASTNode:
        callee = self.walk(node.callee)
        arguments = self.walk(node.args)

        if not isinstance(arguments, list):
            arguments = [arguments]

        return Call(callee, arguments)

    def walk_Access(self, node: Node) -> ASTNode:
        return self.walk(node.name)

    def walk_Ident(self, node: Node) -> ASTNode:
        return Identifier(str(node.ast))

    def walk_Program(self, node: Node) -> ASTNode:
        definitions = []
        for definition in node.definitions:
            #print(definition)
            definitions.append(self.walk(definition))

        return Program(definitions)

    def walk_Block(self, node: Node) -> ASTNode:
        expressions = []

        for expression in node.exprs:
            #print(expression)
            if not expression:
                continue
            expressions.append(self.walk(expression[0]))

        return_expression = self.walk(node.return_expr)

        return Block(expressions, return_expression)

    def walk_Function(self, node: Node) -> ASTNode:

        #print(node)
        name = self.walk(node.name)
        args = []
        for arg in node.args:
            args.append((
                self.walk(arg[0]),
                self.walk(arg[2])
            ))

        return_type = self.walk(node.return_type)

        body = self.walk(node.body)

        return Function(name=name, arguments=args, return_type=return_type, body=body)

    def walk_Type(self, node: Node) -> ASTNode:
        return Type(
            Identifier(node.type),
            self.walk(node.units) if node.units else None
        )
