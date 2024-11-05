from contextlib import redirect_stdout
from io import StringIO

from interpreter.interpreter import Interpreter
from parser.parser import Parser
from scanner.scanner import Scanner
from utils.exceptions import ErrorHandler


def test_interpret():
    error_handler = ErrorHandler()
    source = "3 * (4 + 2);"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens, error_handler)
    stmts = parser.parse()

    interpreter = Interpreter(error_handler)
    expr = stmts[0].expr
    res = expr.accept(interpreter)
    assert res == 18.0


def test_comparisons():
    error_handler = ErrorHandler()
    source = "1 < 2 == true;1 < 3 == 2 == 2;false == 1 > 2;"
    expected = [True, False, True]
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens, error_handler)
    stmts = parser.parse()
    interpreter = Interpreter(error_handler)
    for statement, res in zip(stmts, expected):
        assert statement.expr.accept(interpreter) == res


def test_comma():
    error_handler = ErrorHandler()
    source = "1 < 2, 3 + 4 * 5, (4 - 1) / 3;"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens, error_handler)
    stmts = parser.parse()

    interpreter = Interpreter(error_handler)
    expected = 1
    for statement in stmts:
        assert statement.expr.accept(interpreter) == expected
    assert not error_handler.errors
    assert error_handler.runtime_error is None

def test_print():
    error_handler = ErrorHandler()
    source = 'print "hello" + " world";'
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens, error_handler)
    stmts = parser.parse()

    interpreter = Interpreter(error_handler)
    f = StringIO()
    with redirect_stdout(f):
        for s in stmts:
            interpreter.evaluate(s)
    assert "hello world\n" == f.getvalue()

