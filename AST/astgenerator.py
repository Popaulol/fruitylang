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
    UnitNumber,
)
from unit import UNIT_MAP, Unit


def create_ast(parse_result: str) -> ASTNode:
    return ASTGenerator().walk(parse_result)  # type: ignore


class ASTGenerator(NodeWalker):  # type: ignore
    def walk_object(self, node: Node) -> ASTNode:
        # pprint(node, width=20, indent=4)
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
        # pprint(node, width=20, indent=4)
        if "." in node.ast:
            return Number(float(node.ast))
        else:
            return Number(int(node.ast))

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
