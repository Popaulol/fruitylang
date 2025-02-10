from __future__ import annotations

import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from .ast import (
        Add,
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


class ASTWalker[T](ABC):
    @abstractmethod
    def walk_add[A, K](self, node: Add, *args: A, **kwargs: K) -> T:
        pass

    @abstractmethod
    def walk_sub[A, K](self, node: Sub, *args: A, **kwargs: K) -> T:
        pass

    @abstractmethod
    def walk_mul[A, K](self, node: Mul, *args: A, **kwargs: K) -> T:
        pass

    @abstractmethod
    def walk_div[A, K](self, node: Div, *args: A, **kwargs: K) -> T:
        pass

    @abstractmethod
    def walk_invert[A, K](self, node: Invert, *args: A, **kwargs: K) -> T:
        pass

    @abstractmethod
    def walk_exponent[A, K](self, node: Exponent, *args: A, **kwargs: K) -> T:
        pass

    @abstractmethod
    def walk_identifier[A, K](self, node: Identifier, *args: A, **kwargs: K) -> T:
        pass

    @abstractmethod
    def walk_unit_number[A, K](self, node: UnitNumber, *args: A, **kwargs: K) -> T:
        pass

    @abstractmethod
    def walk_number[A, K](self, node: Number, *args: A, **kwargs: K) -> T:
        pass

    @abstractmethod
    def walk_ast_unit[A, K](self, node: ASTUnit, *args: A, **kwargs: K) -> T:
        pass
