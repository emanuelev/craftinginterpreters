"""This module implements evaluation of expression trees."""

from parser import expression as exp
from scanner.token_type import TokenType


class Interpreter:
    """Visitor class that recursively prints the abstract syntax tree"""

    def evaluate(self, expr: exp.ExpressionBase):
        """Visitor's entry point, invokes expressions' accept on itself.

        Args:
            expr: expression to visit.
        """
        return expr.accept(self)

    def visit_literal_expr(self, expr) -> str:
        """Visits a literal expression and returns it's value.

        Args:
            expr: expression to visit.

        Returns:
            The value of the literal object.
        """
        return expr.value

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

        # Negate the value obtained from the right subexpr.
        value = -float(right)
        return value

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
                return float(left) - float(right)
            case TokenType.PLUS:
                return float(left) + float(right)
            case TokenType.STAR:
                return float(left) * float(right)
            case TokenType.SLASH:
                return float(left) / float(right)

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
