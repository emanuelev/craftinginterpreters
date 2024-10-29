"""This module implements evaluation of expression trees."""

import logging

from utils.exceptions import RuntimeError
from parser import expression as exp
from scanner.token import Token
from scanner.token_type import TokenType


class Interpreter:
    """Visitor class that recursively prints the abstract syntax tree"""

    def evaluate(self, expr: exp.ExpressionBase):
        """Visitor's entry point, invokes expressions' accept on itself.

        Args:
            expr: expression to visit.
        """
        try:
            value = expr.accept(self)
            return value
        except RuntimeError:
            return None

    def visit_literal_expr(self, expr) -> str:
        """Visits a literal expression and returns it's value.

        Args:
            expr: expression to visit.

        Returns:
            The value of the literal object.
        """
        return expr.value

    def is_true(self, obj: object) -> bool:
        """Returns true if the obj is not none or the
        actual value if obj is of boolean value.

        Args:
            obj: value to check.

        Returns:
            obj if type(obj) == True or True if obj is not None.
        """

        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def visit_unary_expr(self, expression) -> str:
        """Visits a unary expression and returns the formatted operator and
        child expression.

        Args:
            expr: expression to visit.

        Returns:
            A formatted string representing the literal value.
        """
        # Evaluate the sub-expression first.
        right = self.evaluate(expression.expr)
        match expression.token.token_type:
            case TokenType.MINUS:
                self.check_operands(expression.token, right)
                # Negate the value obtained from the right subexpr.
                value = -float(right)
                return value
            case TokenType.BANG:
                return self.is_true(right)

    def visit_binary_expr(self, expression) -> str:
        """Visits a binary expression and returns the formatted operator and
        child expressions.

        Args:
            expression: expression to visit.

        Returns:
            A formatted string representing the literal value.
        """
        # Format left and right sub-expressions.
        left = self.evaluate(expression.left)
        right = self.evaluate(expression.right)

        match expression.token.token_type:
            case TokenType.MINUS:
                self.check_operands(expression.token, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                else:
                    self.check_operands(expression.token, left, right)
                    return float(left) + float(right)
            case TokenType.STAR:
                self.check_operands(expression.token, left, right)
                return float(left) * float(right)
            case TokenType.SLASH:
                self.check_operands(expression.token, left, right)
                return float(left) / float(right)
            case TokenType.GREATER:
                self.check_operands(expression.token, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_operands(expression.token, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_operands(expression.token, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.check_operands(expression.token, left, right)
                return float(left) <= float(right)
            case TokenType.EQUAL:
                return left == right
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.COMMA:
                return right

    def visit_grouping_expr(self, expression) -> str:
        """Visits a binary expression and returns the formatted operator and
        child expressions.

        Args:
            expression: expression to visit.

        Returns:
            A formatted string representing the literal value.
        """
        # Format left and right sub-expressions.
        return self.evaluate(expression.expr)

    def report(self, token: Token, message: str):
        """Reports a runtime error for a given operator.

        Args:
            token: Token
                Token at which the logging event occurred.
            message: str
                String representing the message to be logged.
        """
        logging.error(message + f" {token}")

    def check_operands(self, token: Token, *operands: object):
        for op in operands:
            if not isinstance(op, float):
                self.report(token, "Operand(s) must be numbers.")
                raise RuntimeError()
