"""This file is autogenerated by generate_ast.py
    do not modify manually the content."""

# pylint: disable=C0114,C0115,C0116

from dataclasses import dataclass

from scanner.token import Token


class ExpressionBase:  # pylint: disable=too-few-public-methods
    """Base class for expression classes"""


@dataclass
class LiteralExpr(ExpressionBase):
    """Data class for expressions of type Literal"""

    value: object

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


@dataclass
class UnaryExpr(ExpressionBase):
    """Data class for expressions of type Unary"""

    token: Token
    expr: ExpressionBase

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


@dataclass
class BinaryExpr(ExpressionBase):
    """Data class for expressions of type Binary"""

    left: ExpressionBase
    token: Token
    right: ExpressionBase

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)


@dataclass
class GroupingExpr(ExpressionBase):
    """Data class for expressions of type Grouping"""

    expr: ExpressionBase

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)
