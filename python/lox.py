"""
Python implementation of a jlox interpreter
"""

import argparse
import sys
import os

from scanning.scanner import Scanner


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


def run(script: str):
    """Runs the input lox script

    Args:
        script: input lox script to be run.
    """
    scanner = Scanner(script)
    tokens = scanner.scan_tokens()
    for t in tokens:
        print(t)


def run_prompt():
    """Runs interactive ccommand line prompt"""
    for line in sys.stdin:
        run(line)


def main():
    """Entry point for the lox interpreter"""
    args = parse_args()
    if args.filepath:
        if os.path.isfile(args.filepath):
            with open(args.filepath, "r", encoding="utf-8") as file:
                script = file.read()
                run(script)
        else:
            raise ValueError(f"Provided file {args.filepath} is not a file.")
    else:
        run_prompt()


if __name__ == "__main__":
    main()
