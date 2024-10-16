"""This module defines the Token class for the lox scanner.
"""

from dataclasses import dataclass
from scanner.token_type import TokenType


@dataclass
class Token:
    """Class representing a lox token."""

    token_type: TokenType
    lexeme: str
    literal: object
    line: int
