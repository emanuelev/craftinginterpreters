"""This module implements the scanner logic for the jlox language
"""

import logging
from typing import List

from scanner.token import Token
from scanner.token_type import TokenType

keywords = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "fun": TokenType.FUN,
    "for": TokenType.FOR,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


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

    def peek(self) -> str:
        """Returns current char if not at end of stream, EOF otherwise.

        Returns:
            `\0' if at EOF, current char otherwise.
        """
        if self.end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        """Returns the next current char if not at end of stream, EOF
        otherwise.

        Returns:
            `\0' if at EOF, current char otherwise.
        """
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def append_token(self, token_type: TokenType, literal: object = None):
        """Appends a new token to the token list.

        Args:
            type: TokenType of the new token.
            literal: object representing the parsed token.
        """

        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, lexeme, literal, self.line))

    def end(self):
        """Checks if the scanner has consumed all the source text.

        Returns:
            A boolean indicating if the input source code has been consumed.
        """
        return self.current >= len(self.source)

    def parse_string(self):
        """Parses a multiline string and appends it to the token list.

        Example:
            "I am a string with a
             slash-n in the middle."
        """

        while self.peek() != '"' and self.end() is False:
            # Advance till we find the closing "
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.end():
            logging.error("Unterminated string")
            return

        # Consume the matching "
        self.advance()
        self.append_token(
            TokenType.STRING, self.source[self.start + 1:self.current - 1]
        )

    def parse_number(self):
        """Parses a string representing a number to a python float."""
        while self.peek().isdigit():
            self.advance()
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        number = float(self.source[self.start:self.current])
        self.append_token(TokenType.NUMBER, number)

    def parse_identifier(self):
        """Parses a string representing an identifier or a reserved keyword.

        An identifier can be either a reserved word or just an identifier,
        how to distinguish these?
        Example: print is the same prefix of the
        variable printer and the keyword print. We use the maximal munch
        principle: parse as much as possible and then verify whether the
        tokes is a keyword.
        """

        while self.peek().isalnum() or self.peek() == "_":
            self.advance()

        lexeme = self.source[self.start:self.current]
        token_type = TokenType.IDENTIFIER
        if keywords.get(lexeme) is not None:
            token_type = keywords[lexeme]
        self.append_token(token_type)

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
            case "/":
                # Slash can be either division or the start of a comment.
                if self.match("/"):
                    # A comment can span a line, so throw away characters till
                    # a newline is found.
                    while self.peek() != "\n" and self.end() is False:
                        self.advance()
                else:
                    self.append_token(TokenType.SLASH)
            case "\n":
                self.line += 1

            case '"':
                self.parse_string()

            # Ignore white spaces, carriage returns and tabs
            case " " | "\r" | "\t":
                pass
            case _:
                if c.isdigit():
                    self.parse_number()
                elif c.isalpha():
                    self.parse_identifier()
                else:
                    logging.error(f"line {self.line}: Unexpected character {c}")
