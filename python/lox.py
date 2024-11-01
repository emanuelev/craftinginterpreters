"""
Python implementation of a jlox interpreter
"""

import argparse
import os

from interpreter.interpreter import Interpreter
from parser.parser import Parser
from scanner.scanner import Scanner
from utils.exceptions import ErrorHandler


def parse_args():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        type=str,
        nargs="?",
        help="Path to the jlox script to be interpreted",
    )

    return parser.parse_args()

class Lox:
    def __init__(self):
        self.error_handler = ErrorHandler()
        self.interpreter = Interpreter(self.error_handler)


    def run(self, script: str):
        """Runs the input lox script

        Args:
            script: input lox script to be run.
        """
        scanner = Scanner(script)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, self.error_handler)
        expression = parser.parse()

        if self.error_handler.errors:
            self.error_handler.report_errors()
            exit(76)

        val = self.interpreter.evaluate(expression)

        if self.error_handler.runtime_error:
            self.error_handler.report_runtime_error()
            exit(76)
        print(val)


    def run_prompt(self):
        """Runs interactive ccommand line prompt"""
        while True:
            try:
                line = input("> ")
                self.run(line)
            except EOFError:
                exit(1)


def main():
    """Entry point for the lox interpreter"""
    args = parse_args()
    lox = Lox()
    if args.filepath:
        if os.path.isfile(args.filepath):
            with open(args.filepath, "r", encoding="utf-8") as file:
                script = file.read()
                lox.run(script)
        else:
            raise ValueError(f"Provided file {args.filepath} is not a file.")
    else:
        lox.run_prompt()


if __name__ == "__main__":
    main()
