from AST.ast import ASTUnit, Number, UnitNumber, Identifier, Exponent, Invert, Div, Mul, Sub, Add
from AST.astwalker import ASTWalker
from type_system import Type

class TypeChecker(ASTWalker[Type]):
    def walk_add[A, K](self, node: Add, *args: A, **kwargs: K) -> Type:
        pass

    def walk_sub[A, K](self, node: Sub, *args: A, **kwargs: K) -> Type:
        pass

    def walk_mul[A, K](self, node: Mul, *args: A, **kwargs: K) -> Type:
        pass

    def walk_div[A, K](self, node: Div, *args: A, **kwargs: K) -> Type:
        pass

    def walk_invert[A, K](self, node: Invert, *args: A, **kwargs: K) -> Type:
        pass

    def walk_exponent[A, K](self, node: Exponent, *args: A, **kwargs: K) -> Type:
        pass

    def walk_identifier[A, K](self, node: Identifier, *args: A, **kwargs: K) -> Type:
        pass

    def walk_unit_number[A, K](self, node: UnitNumber, *args: A, **kwargs: K) -> Type:
        pass

    def walk_number[A, K](self, node: Number, *args: A, **kwargs: K) -> Type:
        pass

    def walk_ast_unit[A, K](self, node: ASTUnit, *args: A, **kwargs: K) -> Type:
        pass