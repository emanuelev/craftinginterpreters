"""This module implements variables environment."""

from scanner.token import Token
from utils.exceptions import RuntimeError


class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: str, value: object):
        """Defines a new variable. If the variable
        is already present in the environment, it's
        value will be replaced with the new one.

        Args:
            name: str representing the variable name.
            value: object representing the variable value.
        """

        self.values[name] = value

    def get(self, name: Token):
        """Retrieves the value of the input variable. Raises
        ValueError if the variablkke has not been defined.

        Args:
            name: Token representing the variable.
        """

        if name.lexeme in self.values:
            return self.values[name.lexeme]

        raise RuntimeError(name, f"Undefined variable {name.lexeme}.")
