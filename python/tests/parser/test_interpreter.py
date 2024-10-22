from parser.parser import Parser
from scanner.scanner import Scanner
from interpreter.interpreter import Interpreter


def test_interpret():
    source = "3 * (4 + 2)"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    exp = parser.parse()

    interpreter = Interpreter()
    res = interpreter.evaluate(exp)
    assert res == 18.0
