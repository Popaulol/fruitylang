from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Type(ABC):
    @abstractmethod
    def can_implicit_cast_to(self, other: Type) -> bool:
        pass

    @abstractmethod
    def can_explicit_cast_to(self, other: Type) -> bool:
        pass

    @abstractmethod
    def can_add(self, other: Type) -> bool:
        pass

    @abstractmethod
    def can_sub(self, other: Type) -> bool:
        pass

    @abstractmethod
    def can_mul(self, other: Type) -> bool:
        pass

    @abstractmethod
    def can_div(self, other: Type) -> bool:
        pass

    @abstractmethod
    def can_invert(self) -> bool:
        pass

    @abstractmethod
    def can_be_exponentiated_by(self, other: Type) -> bool:
        pass

class StringType(Type):
    def can_add(self, other: Type) -> bool:
        return isinstance(other, StringType)

    def can_sub(self, other: Type) -> bool:
        return False

    def can_mul(self, other: Type) -> bool:
        return False

    def can_div(self, other: Type) -> bool:
        return False

    def can_invert(self) -> bool:
        return False

    def can_be_exponentiated_by(self, other: Type) -> bool:
        return False

    def can_implicit_cast_to(self, other: Type) -> bool:
        return False

    def can_explicit_cast_to(self, other: Type) -> bool:
        from type_system.numbers import UnitNumber

        if isinstance(other, StringType):
            return True
        elif isinstance(other, UnitNumber):
            return True

        return False
