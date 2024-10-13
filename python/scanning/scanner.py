"""This module implements the scanner logic for the jlox language
"""

import logging
from typing import List

from scanning.token import Token
from scanning.token_type import TokenType


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
        self.current = 0
        self.line = 1

    def advance(self) -> str:
        """Returns the current character and advances the current index.

        Returns:
            The last character consumed.
        """
        c = self.source[self.current]
        self.current = self.current + 1
        return c

    def match(self, expected: str) -> bool:
        """Matches the expected character to the current one and returns true
        and advances current if the match is successful.

        Returns:
            True if match is successful, false otherwise.
        """
        c = self.source[self.current]
        if expected == c:
            self.current = self.current + 1
            return True
        return False

    def append_token(self, token_type: TokenType, literal: object = None):
        """Appends a new token to the token list.

        Args:
            type: TokenType of the new token.
            literal: object representing the parsed token.
        """

        lexeme = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, lexeme, literal, self.line))

    def end(self):
        """Checks if the scanner has consumed all the source text.

        Returns:
            A boolean indicating if the input source code has been consumed.
        """
        return self.current >= len(self.source)

    def scan_tokens(self) -> List[Token]:
        """Parses the source code and returns the corresponding list of tokens

        Returns:
            a List[Token] representing the source code as a token list
        """
        while not self.end():
            self.start = self.current
            self.scan_token()
        return self.tokens

    def scan_token(self):
        """Parses the current token and adds it to the token list."""

        c = self.advance()
        logging.warning(f"Matching {c}")
        match c:
            case "(":
                self.append_token(TokenType.LEFT_PAREN)
            case ")":
                self.append_token(TokenType.RIGHT_PAREN)
            case "{":
                self.append_token(TokenType.LEFT_BRACE)
            case "}":
                self.append_token(TokenType.RIGHT_BRACE)
            case ",":
                self.append_token(TokenType.COMMA)
            case ".":
                self.append_token(TokenType.DOT)
            case "-":
                self.append_token(TokenType.MINUS)
            case "+":
                self.append_token(TokenType.PLUS)
            case ";":
                self.append_token(TokenType.SEMICOLON)
            case "/":
                self.append_token(TokenType.SLASH)
            case "*":
                self.append_token(TokenType.STAR)
            case "!":
                self.append_token(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
            case "=":
                self.append_token(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case ">":
                self.append_token(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case "<":
                self.append_token(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case _:
                logging.error(f"line {self.line}: Unexpected character {c}")
