"""This module implements evaluation of expression trees."""

import logging
from typing import List

from interpreter.environment import Environment
from parser import expression as exp
from parser import statement as stmt
from scanner.token import Token
from scanner.token_type import TokenType
from utils.exceptions import RuntimeError, ErrorHandler


class Interpreter:
    """Visitor class that recursively prints the abstract syntax tree"""

    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler
        self.environment = Environment()

    def interpret(self, statements: List[stmt.StatementBase]):
        """Interpreter entry point, evaluates a list of statements.

        Args:
            statements: list of statements to interpret.
        """
        try:
            for statement in statements:
                statement.accept(self)
        except RuntimeError as e:
            self.error_handler.runtime_error = e

    def evaluate(self, statement: stmt.StatementBase):
        """Visitor's entry point, invokes expressions' accept on itself.

        Args:
            expr: expression to visit.
        """
        try:
            value = statement.accept(self)
            return value
        except RuntimeError as e:
            self.error_handler.runtime_error = e

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
        right = expression.expr.accept(self)
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
        left = expression.left.accept(self)
        right = expression.right.accept(self)

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
            case TokenType.EQUAL_EQUAL:
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
        return expression.expr.accept(self)

    def visit_variable_expr(self, expression) -> str:
        """Visits a variable expression and returns it's value.

        Args:
            expression: variable expression to visit.

        Returns:
            A formatted string representing the literal value.
        """
        return self.environment.get(expression.name)

    def check_operands(self, token: Token, *operands: object):
        for op in operands:
            if not isinstance(op, float):
                raise RuntimeError(token, "Operand(s) must be numbers.")

    def visit_expression_stmt(self, expression_stmt):
        """Visits an expression statement and returns it's value.

        Args:
            expression_stmt: statement expression to visit.

        Returns:
            The value of the statement.
        """

        return expression_stmt.expr.accept(self)

    def visit_print_stmt(self, statement):
        """Visits an expression statement and returns it's value.

        Args:
            expression_stmt: statement expression to visit.

        Returns:
            The value of the statement.
        """

        print(statement.expr.accept(self))

    def visit_var_stmt(self, statement):
        """Visits var statement and returns it's value.

        Args:
            statement: statement expression to visit.
        """
        val = None
        if statement.initialiser is not None:
            val = statement.initialiser.accept(self)
        self.environment.define(statement.name.lexeme, val)
