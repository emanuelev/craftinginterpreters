from parser.parser import Parser
from parser.astprinter import ASTFormatter
from scanner.scanner import Scanner
from utils.exceptions import ErrorHandler


def test_math_expression():
    source = "3 * (4 + 2);"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    error_handler = ErrorHandler()
    parser = Parser(tokens, error_handler)

    stmt = parser.parse()
    assert len(stmt) == 1

    formatter = ASTFormatter()
    res = formatter.visit(stmt[0])
    expected = "(* 3.0 ((+ 4.0 2.0)))"  # all numbers are doubles
    assert expected == res


def test_parsing_error():
    source = "3 * (4 5 + 2);"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    error_handler = ErrorHandler()
    parser = Parser(tokens, error_handler)
    parser.parse()
    assert error_handler.errors is not None


def test_comma():
    source = "3 * (4 + 2), 5 * 7;"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    error_handler = ErrorHandler()
    parser = Parser(tokens, error_handler)

    stmt = parser.parse()
    error_handler.report_errors()
    assert len(stmt) == 1

    formatter = ASTFormatter()
    res = formatter.visit(stmt[0])
    expected = "(, (* 3.0 ((+ 4.0 2.0))) (* 5.0 7.0))"
    assert res == expected


def test_print_expression():
    source = "print 4 + 2;"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    error_handler = ErrorHandler()
    parser = Parser(tokens, error_handler)

    stmt = parser.parse()
    assert len(stmt) == 1

    formatter = ASTFormatter()
    res = formatter.visit(stmt[0])
    expected = "(print (+ 4.0 2.0))"  # all numbers are doubles
    assert expected == res
