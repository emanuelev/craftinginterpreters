# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from scanning.token_type import TokenType
from scanning.scanner import Scanner

expected = [
    TokenType.DOT,
    TokenType.LEFT_PAREN,
    TokenType.RIGHT_PAREN,
    TokenType.BANG_EQUAL,
    TokenType.STRING,
    TokenType.NUMBER,
    TokenType.NUMBER,
    TokenType.NUMBER,
    TokenType.DOT,
    TokenType.NUMBER,
    TokenType.AND,
    TokenType.PRINT,
    TokenType.RETURN,
    TokenType.IDENTIFIER,
]


def test_scanner():  # pylint disable=C0116
    with open("./test.lox", "r", encoding="utf-8") as f:
        source = f.read()
        scanner = Scanner(source)
        scanner.scan_tokens()
        for i, token in enumerate(scanner.tokens):
            assert expected[i] == token.token_type
