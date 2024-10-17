# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from parser.expression import *
from parser.astprinter import ASTFormatter
from scanner.token import Token
from scanner.token_type import TokenType


1.2 + (-4.0)


def test_ast_formatter():  # pylint disable=C0116
    lhs = LiteralExpr(1.2)
    rhs = LiteralExpr(4.0)
    neg = UnaryExpr(Token(TokenType.MINUS, "-", None, 0), rhs)
    sum = BinaryExpr(lhs, Token(TokenType.PLUS, "+", None, 0), neg)

    expected = "(+ 1.2 (- 4.0))"

    formatter = ASTFormatter()
    res = formatter.visit(sum)
    assert expected == res

def test_grouping():  # pylint disable=C0116
    lhs = LiteralExpr(1.2)
    rhs = LiteralExpr(4.0)
    sum1 = BinaryExpr(lhs, Token(TokenType.PLUS, "+", None, 0), rhs)
    group = GroupingExpr(sum1)

    lhs = LiteralExpr(3.2)
    div = BinaryExpr(lhs, Token(TokenType.SLASH, "/", None, 0), group)

    expected = "(/ 3.2 ((+ 1.2 4.0)))"

    formatter = ASTFormatter()
    res = formatter.visit(div)
    assert expected == res