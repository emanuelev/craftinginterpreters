# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from parser import expression as exp
from parser.astprinter import ASTFormatter
from scanner.token import Token
from scanner.token_type import TokenType


def test_ast_formatter():  # pylint disable=C0116
    lhs = exp.LiteralExpr(1.2)
    rhs = exp.LiteralExpr(4.0)
    neg = exp.UnaryExpr(Token(TokenType.MINUS, "-", None, 0), rhs)
    sum = exp.BinaryExpr(lhs, Token(TokenType.PLUS, "+", None, 0), neg)

    expected = "(+ 1.2 (- 4.0))"

    formatter = ASTFormatter()
    res = formatter.visit(sum)
    assert expected == res


def test_grouping():  # pylint disable=C0116
    lhs = exp.LiteralExpr(1.2)
    rhs = exp.LiteralExpr(4.0)
    sum1 = exp.BinaryExpr(lhs, Token(TokenType.PLUS, "+", None, 0), rhs)
    group = exp.GroupingExpr(sum1)

    lhs = exp.LiteralExpr(3.2)
    div = exp.BinaryExpr(lhs, Token(TokenType.SLASH, "/", None, 0), group)

    expected = "(/ 3.2 ((+ 1.2 4.0)))"

    formatter = ASTFormatter()
    res = formatter.visit(div)
    assert expected == res
