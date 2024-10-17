"""This module implements pretty printing for expression trees."""


from parser.expression import ExpressionBase

class ASTFormatter:
    """Visitor class that recursively prints the abstract syntax tree"""

    def visit(self, expr: ExpressionBase):
        """Visitor's entry point, invokes expressions' accept on itself.

        Args:
            expr: expression to visit.
        """
        return expr.accept(self)

    def visit_literal_expr(self, expr) -> str:
        """Visits a literal expression and returns it's value formatted.

        Args:
            expr: expression to visit.

        Returns:
            A formatted string representing the literal value.
        """
        return f"{expr.value}"

    def visit_unary_expr(self, expression) -> str:
        """Visits a unary expression and returns the formatted operator and
        child expression.

        Args:
            expr: expression to visit.

        Returns:
            A formatted string representing the literal value.
        """
        # Get the operator lexeme.
        lexeme = expression.token.lexeme
        # Recursavily format the child expression.
        rest = expression.expr.accept(self)
        return f"({lexeme} {rest})"

    def visit_binary_expr(self, expression) -> str:
        """Visits a binary expression and returns the formatted operator and
        child expressions.

        Args:
            expression: expression to visit.

        Returns:
            A formatted string representing the literal value.
        """
        # Get the operator lexeme.
        lexeme = expression.token.lexeme
        # Format left and right sub-expressions.
        left = expression.left.accept(self)
        right = expression.right.accept(self)
        return f"({lexeme} {left} {right})"

    def visit_grouping_expr(self, expression) -> str:
        """Visits a binary expression and returns the formatted operator and
        child expressions.

        Args:
            expression: expression to visit.

        Returns:
            A formatted string representing the literal value.
        """
        # Format left and right sub-expressions.
        nested = expression.expr.accept(self)
        return f"({nested})"
