"""This module implements a recursive decent parser for the lox language.

The parsed grammar is in this form:

program        → declaration* EOF ;

declaration    → varDecl
               | statement ;

varDecl        -> "var" IDENTIFIER ("=" expression)? ";"

statement      → expressionStmt | printStmt | blockStmt | ifStmt | whileStmt
ifStmt         → "if (" expression ")" statement ("else" statement)?
expressionStmt → expression ";"
printStmt      → "print" expression ";"
whileStmt      → "while (" expression ")" statement
forStmt        → "for" "(" ( varDecl | exprStmt | ";" )
                 expression? ";"
                 expression? ")" statement ;
blockStmt      → "{" declaration "}"
statement      → expression ";" | print
expression     → assignment;
assignment     → IDENTIFIER "=" assignment | logic_or;
logic_or       → logic_and ("or" logic_and)* ;
logic_and      → comma ("and" comma)* ;
comma          → equality (, equality)*;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary
               | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")"  | IDENTIFIER;

Notice that the production at the top have lower precedence in the evaluation
compared to the bottom.
"""

from dataclasses import dataclass
import logging
from typing import List

from parser import expression as exp
from parser import statement as stmt
from scanner.token import Token, TokenType
from utils.exceptions import ParserError, ErrorHandler


@dataclass
class Parser:
    tokens: List[Token]
    error_handler: ErrorHandler

    current: int = 0

    def parse(self):
        statement_list = []
        while not self.end():
            decl = self.declaration()
            if decl is not None:
                statement_list.append(decl)
        return statement_list

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

    def advance(self):
        """Advances the current token."""
        if not self.end():
            self.current += 1

    def declaration(self):
        try:
            if self.match([TokenType.VAR]):
                return self.varDecl()
            return self.statement()
        except ParserError as e:
            self.error_handler.errors.append(e)
            self.synchronize()
        return None

    def statement(self):
        """Parses statement rule"""
        if self.match([TokenType.IF]):
            return self.ifStatement()
        elif self.match([TokenType.PRINT]):
            expr = self.expression()
            statement = stmt.PrintStmt(expr)
            self.consume(
                TokenType.SEMICOLON, "Expect ; at the end of statement."
            )
            return statement
        elif self.match([TokenType.WHILE]):
            return self.whileStatement()
        elif self.match([TokenType.FOR]):
            return self.forStatement()
        elif self.match([TokenType.LEFT_BRACE]):
            statement = stmt.BlockStmt(self.block())
            return statement
        else:
            return self.expressionStatement()

    def expressionStatement(self):
        statement = stmt.ExpressionStmt(self.expression())
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return statement

    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match([TokenType.ELSE]):
            else_branch = self.statement()

        return stmt.IfStmt(condition, then_branch, else_branch)

    def whileStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(
            TokenType.RIGHT_PAREN, "Expect ')' after while condition."
        )
        body = self.statement()
        return stmt.WhileStmt(condition, body)

    def forStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        # If next token is a semicolon, it means we skipped the
        # initialiser.
        if self.match([TokenType.SEMICOLON]):
            initialiser = stmt.ExpressionStmt(exp.LiteralExpr(True))
        else:
            if self.match([TokenType.VAR]):
                initialiser = self.varDecl()
            else:
                initialiser = self.expressionStatement()

        if self.match([TokenType.SEMICOLON]):
            condition = stmt.ExpressionStmt(exp.LiteralExpr(True))
        else:
            condition = self.expressionStatement()

        if self.match([TokenType.RIGHT_PAREN]):
            increment = stmt.ExpressionStmt(exp.LiteralExpr(True))
        else:
            increment = stmt.ExpressionStmt(self.expression())
            self.consume(
                TokenType.RIGHT_PAREN, "Expect ')' after for increment."
            )

        for_body = self.statement()
        while_body = stmt.BlockStmt([for_body, increment])
        while_stmt = stmt.WhileStmt(condition.expr, while_body)

        block_stmt = stmt.BlockStmt([initialiser, while_stmt])

        return block_stmt

    def varDecl(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        expr = None
        if self.match([TokenType.EQUAL]):
            expr = self.expression()
        self.consume(
            TokenType.SEMICOLON,
            "Expect semicolon at the end of declaration.",
        )
        return stmt.VarStmt(name, expr)

    def block(self):
        statements = []
        while (
            self.peek().token_type != TokenType.RIGHT_BRACE and not self.end()
        ):
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def expression(self):
        """Parses an expression rule."""
        return self.assignment()

    def assignment(self):
        """Parses an assignment rule."""

        # With a one character lookahead parser we can't decide whether the next
        # statement is an assignment or not. Example:
        # > print x;
        # x is an identifier, but in this case is NOT part of an assignment.
        # How to disambiguate between these two cases?
        # > print x;
        # > x = 2.0;
        # Hack: treat the left handside as a normal expression. If its
        # evaluation is followed by an equal token, expect it's type to have
        # been resolved to an IDENTIFIER expression. This allow us to cover way
        # more complex assignments, for instance:
        # > Foo(2.0, 3.0).y = 4.0;
        # but it will correctly throw an error for when an r-value is used as
        # l-value:
        # > a + b = c;
        expr = self.logical_or()
        if self.match([TokenType.EQUAL]):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, exp.VariableExpr):
                return exp.AssignmentExpr(expr.name, value)
            else:
                self.error(equals, "Invalid assignment target.")
        return expr

    def logical_or(self):
        left = self.logical_and()
        if self.match([TokenType.OR]):
            op = self.previous()
            right = self.logical_or()
            return exp.LogicalExpr(left, op, right)
        return left

    def logical_and(self):
        left = self.comma()
        if self.match([TokenType.AND]):
            op = self.previous()
            right = self.logical_and()
            return exp.LogicalExpr(left, op, right)
        return left

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
            self.consume(TokenType.RIGHT_PAREN, "Expect ) after expression.")
            return exp.GroupingExpr(expr)

        if self.match([TokenType.IDENTIFIER]):
            token = self.previous()
            return exp.VariableExpr(token)

        self.error(self.peek(), "Expect expression.")

    def synchronize(self):
        self.advance()

        while self.end() is False:
            if self.previous().token_type == TokenType.SEMICOLON:
                return

            match self.peek().token_type:
                case (
                    TokenType.CLASS
                    | TokenType.FUN
                    | TokenType.VAR
                    | TokenType.FOR
                    | TokenType.IF
                    | TokenType.WHILE
                    | TokenType.PRINT
                    | TokenType.RETURN
                ):
                    print(f"Found synch token {self.peek()}")
                    return

            self.advance()

    def error(self, token: Token, message: str):
        """Raises an error at the given token with the
           provided message.

        Args:
            token: Token
                Token at which the logging event occurred.
            message: str
                String representing the message to be logged.
        Raises:
            ParseError: unexpected token type.
        """
        raise ParserError(token, message)
