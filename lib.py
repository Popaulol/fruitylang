import sys

import tatsu

from AST.astgenerator import create_ast
from AST.astprinter import print_ast
from AST.astrender import render_ast


def main() -> None:
    if sys.platform != "linux":
        print(f"This program isn't tested platforms other than Linux, your current platform is: {sys.platform}. Use at your own risk!", file=sys.stderr)


    parse_result = parser.parse("fn hi(i: int s, j: int kg^34 J^-4, klaus: str) -> str: 10; 123; f(a); sassssss; {asdsd; asdsddddd; 234234324; as; 3333; 1J m^-2 - 10.345kg^-1 J^5 * (4 + 5) * 6 / 7**8 + -9 + f(123.435345 kg J m^-4, 5) + b(1)};")
    #parse_result = parser.parse("1J m^-2 - 10.345kg^-1 J^5 * (4 + 5) * 6 / 7**8 + -9 + f(123.435345 kg J m^-4, 5) + b(1);")
    ast = create_ast(parse_result)
    print_ast(ast)
    render_ast(ast, "test.dot")


with open("grammar.ebnf") as f:
    GRAMMAR = f.read()

parser = tatsu.compile(GRAMMAR, asmodel=True)
