import tatsu

from AST.astgenerator import create_ast
from AST.astprinter import print_ast
from AST.astrender import render_ast


def main() -> None:
    parse_result = parser.parse("1J m^-2 - 10.345kg^-1 J^5 * (4 + 5) * 6 / 7**8 + -9")
    ast = create_ast(parse_result)
    print_ast(ast)
    render_ast(ast, "test.dot")


with open("grammar.ebnf") as f:
    GRAMMAR = f.read()

parser = tatsu.compile(GRAMMAR, asmodel=True)
