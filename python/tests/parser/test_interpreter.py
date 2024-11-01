from interpreter.interpreter import Interpreter
from parser.parser import Parser
from scanner.scanner import Scanner
from utils.exceptions import ErrorHandler


def test_interpret():
    error_handler = ErrorHandler()
    source = "3 * (4 + 2)"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens, error_handler)
    exp = parser.parse()

    interpreter = Interpreter(error_handler)
    res = interpreter.evaluate(exp)
    assert res == 18.0

def test_comparisons():
    error_handler = ErrorHandler()
    source = ['1 < 2 == true', '1 < 3 == 2 == 2', 'false == 1 > 2']
    expected = [True, False, True]
    for line, res in zip(source, expected):
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens, error_handler)
        exp = parser.parse()
        print(line)
        print(exp)

        interpreter = Interpreter(error_handler)
        assert interpreter.evaluate(exp) == res

