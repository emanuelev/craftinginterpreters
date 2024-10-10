"""This module implements the scanner logic for the jlox language
"""

from typing import List

from scanning.token import Token


class Scanner:
    """Class implementing text scanning for the lox language.

    Attributes:
        source: str
            A string represeting the source code of the lox program.
        tokens: List[Token]
            A list of Token objects obtained from the source code.
        start: int
            Index to the first character of the lexeme being currently scanned.
        current: int
            Index to the current character being parsed.
        line: int
            Number of the current line in the source code.
    """

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.end = 0
        self.line = 0
