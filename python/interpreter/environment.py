"""This module implements variables environment."""

from scanner.token import Token
from utils.exceptions import RuntimeError


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

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
        ValueError if the variable has not been defined.

        Args:
            name: Token representing the variable.
        """

        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise RuntimeError(name, f"Undefined variable {name.lexeme}.")

    def set(self, name: Token, value: object):
        """Sets the value of the input variable. Raises
        ValueError if the variable has not been defined.

        Args:
            name: Token representing the variable.
        """

        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            return self.enclosing.set(name, value)

        raise RuntimeError(name, f"Undefined variable {name.lexeme}.")
