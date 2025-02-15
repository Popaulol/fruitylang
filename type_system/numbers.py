from abc import ABC
from dataclasses import dataclass

from type_system import Type, StringType
from unit import Unit

@dataclass(frozen=True)
class UnitNumber(Type, ABC):
    unit: Unit


@dataclass(frozen=True)
class TypedInt(UnitNumber):
    def can_add(self, other: Type) -> bool:
        if isinstance(other, TypedInt):
            return self.unit == other.unit
        elif isinstance(other, TypedFloat):
            return self.unit == other.unit
        else:
            return False

    def can_sub(self, other: Type) -> bool:
        return self.can_add(other)

    def can_mul(self, other: Type) -> bool:
        return isinstance(other, TypedInt) or isinstance(other, TypedFloat)

    def can_div(self, other: Type) -> bool:
        return self.can_sub(other)

    def can_invert(self) -> bool:
        return True

    def can_be_exponentiated_by(self, other: Type) -> bool:
        if isinstance(other, TypedInt) or isinstance(other, TypedFloat):
            return other.unit == Unit() # You can only use a number without a unit in an exponent
        return False

    def can_implicit_cast_to(self, other: Type) -> bool:
        if isinstance(other, TypedInt) and other.unit == self.unit:
            return True
        elif isinstance(other, TypedFloat) and other.unit == self.unit:
            return True
        else:
            return False

    def can_explicit_cast_to(self, other: Type) -> bool:
        if self.can_implicit_cast_to(other):
            return True
        elif isinstance(other, StringType):
            return True
        else:
            return False

@dataclass(frozen=True)
class TypedFloat(UnitNumber):
    def can_implicit_cast_to(self, other: Type) -> bool:
        if isinstance(other, TypedFloat) and other.unit == self.unit:
            return True
        else:
            return False

    def can_explicit_cast_to(self, other: Type) -> bool:
        if self.can_implicit_cast_to(other):
            return True
        elif isinstance(other, TypedInt) and other.unit == self.unit:
            return True
        elif isinstance(other, StringType):
            return True
        else:
            return False
