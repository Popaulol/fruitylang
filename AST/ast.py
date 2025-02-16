from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from unit import Unit

from .astwalker import ASTWalker


@dataclass
class ASTNode(ABC):
    @abstractmethod
    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        pass


@dataclass
class Definition(ASTNode, ABC):
    pass

@dataclass
class Expr(Definition, ABC):
    pass


@dataclass
class Add(Expr):
    left: Expr
    right: Expr

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_add(self, *args, **kwargs)


@dataclass
class Sub(Expr):
    left: Expr
    right: Expr

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_sub(self, *args, **kwargs)


@dataclass
class Mul(Expr):
    left: Expr
    right: Expr

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_mul(self, *args, **kwargs)


@dataclass
class Div(Expr):
    left: Expr
    right: Expr

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_div(self, *args, **kwargs)


@dataclass
class Invert(Expr):
    right: Expr

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_invert(self, *args, **kwargs)


@dataclass
class Exponent(Expr):
    left: Expr
    right: Expr

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_exponent(self, *args, **kwargs)


@dataclass
class Identifier(Expr):
    name: str

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_identifier(self, *args, **kwargs)


@dataclass
class UnitNumber(Expr):
    number: Number
    unit: ASTUnit | None

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_unit_number(self, *args, **kwargs)


@dataclass
class Number(Expr):
    value: int | float

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_number(self, *args, **kwargs)


@dataclass
class ASTUnit(Expr):
    unit: Unit

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_ast_unit(self, *args, **kwargs)

@dataclass
class Call(Expr):
    callee: Expr
    arguments: list[Expr]

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_call(self, *args, **kwargs)


@dataclass
class Program(ASTNode):
    definitions: list[Definition]


    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_program(self, *args, **kwargs)

@dataclass
class Block(Expr):
    expressions: list[Expr]
    return_expression: Expr | None

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_block(self, *args, **kwargs)

@dataclass
class Function(Definition):
    name: Identifier
    arguments: list[tuple[Expr, Type]]
    return_type: Type
    body: Expr

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_function(self, *args, **kwargs)


@dataclass
class Type(ASTNode):
    name: Identifier
    units: ASTUnit | None

    def walk[T, A, K](self, walker: ASTWalker[T], *args: A, **kwargs: K) -> T:
        return walker.walk_type(self, *args, **kwargs)