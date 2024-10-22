from parser.parser import Parser
from parser.astprinter import ASTFormatter
from scanner.scanner import Scanner


def test_math_expression():
    source = "3 * (4 + 2)"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)

    exp = parser.parse()

    formatter = ASTFormatter()
    res = formatter.visit(exp)
    expected = "(* 3.0 ((+ 4.0 2.0)))"  # all numbers are doubles
    assert expected == res


def test_parsing_error():
    source = "3 * (4 5 + 2)"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)

    exp = parser.parse()
    assert exp is None
