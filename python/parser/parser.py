"""This module implements a recursive decent parser for the lox language.

The parsed grammar is in this form:

expression     → comma
comma          → equality (, equality)*
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary
               | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")" ;

Notice that the production at the top have lower precedence in the evaluation
compared to the bottom.
"""

from dataclasses import dataclass
import logging
from typing import List

from parser import expression as exp
from scanner.token import Token, TokenType


@dataclass
class Parser:
    tokens: List[Token]

    current: int = 0

    def parse(self):
        try:
            return self.expression()
        except ValueError:
            return None

    def end(self) -> bool:
        """Checks if the input tokens have been consumed,
        returns true in that case.
        """
        return self.peek().token_type == TokenType.EOF

    def previous(self) -> Token:
        """Returns the last consumed token."""
        return self.tokens[self.current - 1]

    def peek(self):
        """Returns the current token without consuming it.

        Returns:
            The token at the current position.
        """

        return self.tokens[self.current]

    def match(self, expected: List[TokenType]) -> bool:
        """Check if the current token is in the expected list of
        token types.

        Args:
            expected: list of expected token types.

        Returns:
            A boolean representing if a match has been found.
        """
        if not self.end() and self.tokens[self.current].token_type in expected:
            self.current += 1
            return True
        return False

    def consume(self, expected: TokenType, error: str):
        """Consumes the next token if it matches the expected type.
        Throws error otherwise.

        Args:
            expected: TokenType
                The exected token type to match.
            error: str
                String to be reported in case of type mismatch.

        Raises:
            ValueError: unexpected token type.
        """

        c = self.tokens[self.current]
        if expected == c.token_type:
            self.current += 1
            return c

        self.error(c, error)

    def expression(self):
        """Parses an expression rule."""
        return self.comma()

    def comma(self):
        """Parses comma rule.

        The production rule is:
            comma          → equality (, equality)*
        """
        expr = self.equality()
        while self.match([TokenType.COMMA]):
            operator = self.previous()
            right = self.equality()
            expr = exp.BinaryExpr(expr, operator, right)
        return expr

    def equality(self) -> exp.ExpressionBase:
        """Parses an equality rule.

        The production rule for equality is the following:
            equality       → comparison ( ( "!=" | "==" ) comparison )* ;
        It matches one comparison expression followed by zero or more
        != or == comparison occurrences. E.g.
            1. a < b == c < d
            2. a < b
            3. a < b == c < d != e > f
        """
        expr = self.comparison()  # leftmost production rule.

        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            # If there's a match of the != and == operators, retrieve
            # the matched token.
            operator = self.previous()
            # Parse the right comparison
            right = self.comparison()
            # Update the expression expr value.
            # Notice that this is the crucial recursive step,
            # where we expand to the right the current expression with
            # more comparisons:
            # expr1 == expr2 != expr3 ... == exprn
            expr = exp.BinaryExpr(expr, operator, right)
        return expr

    def comparison(self):
        """Parses the comparison rule.

        The production rule for comparison is the following:
            comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
        """

        expr = self.term()

        comp = [
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ]

        while self.match(comp):
            operator = self.previous()
            right = self.term()
            expr = exp.BinaryExpr(expr, operator, right)

        return expr

    def term(self):
        """Parses the comparison rule.

        The production rule for term is the following:
            term           → factor ( ( "-" | "+" ) factor )* ;
        """
        expr = self.factor()

        while self.match([TokenType.MINUS, TokenType.PLUS]):
            operator = self.previous()
            right = self.factor()
            expr = exp.BinaryExpr(expr, operator, right)

        return expr

    def factor(self):
        """Parses the factor rule.

        The production rule for term is the following:
            factor         → unary ( ( "/" | "*" ) unary )* ;
        """
        expr = self.unary()

        while self.match([TokenType.SLASH, TokenType.STAR]):
            operator = self.previous()
            right = self.unary()
            expr = exp.BinaryExpr(expr, operator, right)

        return expr

    def unary(self):
        """Parses the unary rule.

        The production rule for term is the following:
            unary          → ( "!" | "-" ) unary | primary ;
        """

        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()
            expr = exp.UnaryExpr(operator, right)
        else:
            expr = self.primary()

        return expr

    def primary(self):
        """Parses the unary rule.

        The production rule for term is the following:
            primary        → NUMBER | STRING | "true" | "false" | "nil"
                            | "(" expression ")" ;
        """

        if self.match([TokenType.TRUE]):
            return exp.LiteralExpr(True)
        if self.match([TokenType.FALSE]):
            return exp.LiteralExpr(False)
        if self.match([TokenType.NIL]):
            return exp.LiteralExpr(None)
        if self.match([TokenType.NUMBER, TokenType.STRING]):
            token = self.previous()
            return exp.LiteralExpr(token.literal)

        if self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ) after expression.")
            return exp.GroupingExpr(expr)

        self.error(self.peek(), "Expected expression")

    def synchronize(self):
        self.advance()

        while self.end() is False:
            if self.previous().type == TokenType.SEMICOLON:
                return

            match self.peek().type:
                case (
                    self.CLASS
                    | self.FUN
                    | self.VAR
                    | self.FOR
                    | self.IF
                    | self.WHILE
                    | self.PRINT
                    | self.RETURN
                ):
                    return

            self.advance()

    def report(self, token: Token, message: str):
        """Logs a message at a given input token.

        Args:
            token: Token
                Token at which the logging event occurred.
            message: str
                String representing the message to be logged.
        """
        if token.token_type == TokenType.EOF:
            logging.error(str(token.line) + " at end: " + message)
        else:
            logging.error(
                str(token.line) + " at " + token.lexeme + ": " + message
            )

    def error(self, token: Token, message: str):
        """Logs a message at a given input token.

        Args:
            token: Token
                Token at which the logging event occurred.
            message: str
                String representing the message to be logged.
        Raises:
            ValueError: unexpected token type.
        """

        self.report(token, message)
        raise ValueError()
