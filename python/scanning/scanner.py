"""This module implements the scanner logic for the jlox language
"""

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
