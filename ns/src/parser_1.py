from typing import List
from src.ast_1 import (
    AssignmentExpr,
    BinaryExpr,
    CallExpr,
    Expr,
    Identifier,
    MemberExpr,
    NumericLiteral,
    ObjectLiteral,
    Program,
    Property,
    Stmt,
    VarDeclaration,
    FunctionDeclaration,
)
from src.lexer import Token, tokenize, TokenType

class Parser:
    def __init__(self):
        self.tokens: List[Token] = []

    def not_eof(self) -> bool:
        return self.tokens[0].type != TokenType.EOF

    def at(self) -> Token:
        return self.tokens[0]

    def eat(self) -> Token:
        prev = self.tokens.pop(0)
        return prev

    def expect(self, type: TokenType, err: str) -> Token:
        prev = self.tokens.pop(0)
        if not prev or prev.type != type:
            print("Parser Error:\n", err, prev, " - Expecting: ", type)
            exit(1)
        return prev

    def produceAST(self, sourceCode: str) -> Program:
        self.tokens = tokenize(sourceCode)
        program: Program = Program(kind="Program", body=[])

        while self.not_eof():
            program.body.append(self.parse_stmt())

        return program

    def parse_stmt(self) -> Stmt:
        if self.at().type in (TokenType.Let, TokenType.Const):
            return self.parse_var_declaration()
        elif self.at().type == TokenType.Fn:
            return self.parse_fn_declaration()
        else:
            return self.parse_expr()

    def parse_fn_declaration(self) -> Stmt:
        self.eat()  # eat fn keyword
        name = self.expect(
            TokenType.Identifier,
            "Expected function name following fn keyword"
        ).value

        args = self.parse_args()
        params: List[str] = [arg.symbol for arg in args if isinstance(arg, Identifier)]

        self.expect(
            TokenType.OpenBrace,
            "Expected function body following declaration"
        )
        body: List[Stmt] = []

        while self.at().type not in (TokenType.EOF, TokenType.CloseBrace):
            body.append(self.parse_stmt())

        self.expect(
            TokenType.CloseBrace,
            "Closing brace expected inside function declaration"
        )

        fn = FunctionDeclaration(
            body=body,
            name=name,
            parameters=params,
            kind="FunctionDeclaration"
        )

        return fn

    def parse_var_declaration(self) -> Stmt:
        is_constant = self.eat().type == TokenType.Const
        identifier = self.expect(
            TokenType.Identifier,
            "Expected identifier name following let | const keywords."
        ).value

        if self.at().type == TokenType.Semicolon:
            self.eat()
            if is_constant:
                raise ValueError("Must assign value to constant expression. No value provided.")
            return VarDeclaration(
                identifier=identifier,
                constant=False,
                kind="VarDeclaration"
            )

        self.expect(
            TokenType.Equals,
            "Expected equals token following identifier in var declaration."
        )

        value = self.parse_expr()
        self.expect(
            TokenType.Semicolon,
            "Variable declaration statement must end with semicolon."
        )

        return VarDeclaration(
            value=value,
            identifier=identifier,
            constant=is_constant,
            kind="VarDeclaration"
        )

    def parse_expr(self) -> Expr:
        return self.parse_assignment_expr()

    def parse_assignment_expr(self) -> Expr:
        left = self.parse_object_expr()

        if self.at().type == TokenType.Equals:
            self.eat()
            value = self.parse_assignment_expr()
            return AssignmentExpr(
                value=value,
                assigne=left,
                kind="AssignmentExpr"
            )

        return left

    def parse_object_expr(self) -> Expr:
        if self.at().type != TokenType.OpenBrace:
            return self.parse_additive_expr()

        self.eat()
        properties: List[Property] = []

        while self.not_eof() and self.at().type != TokenType.CloseBrace:
            key = self.expect(
                TokenType.Identifier,
                "Object literal key expected"
            ).value

            if self.at().type == TokenType.Comma:
                self.eat()
                properties.append(Property(key=key, kind="Property"))
                continue
            elif self.at().type == TokenType.CloseBrace:
                properties.append(Property(key=key, kind="Property"))
                continue

            self.expect(
                TokenType.Colon,
                "Missing colon following identifier in ObjectExpr"
            )
            value = self.parse_expr()

            properties.append(Property(value=value, key=key, kind="Property"))
            if self.at().type != TokenType.CloseBrace:
                self.expect(
                    TokenType.Comma,
                    "Expected comma or closing bracket following property"
                )

        self.expect(TokenType.CloseBrace, "Object literal missing closing brace.")
        return ObjectLiteral(properties=properties, kind="ObjectLiteral")

    def parse_additive_expr(self) -> Expr:
        left = self.parse_multiplicitave_expr()

        while self.at().value in ["+", "-"]:
            operator = self.eat().value
            right = self.parse_multiplicitave_expr()
            left = BinaryExpr(left=left, right=right, operator=operator, kind="BinaryExpr")

        return left

    def parse_multiplicitave_expr(self) -> Expr:
        left = self.parse_call_member_expr()

        while self.at().value in ["/", "*", "%"]:
            operator = self.eat().value
            right = self.parse_call_member_expr()
            left = BinaryExpr(left=left, right=right, operator=operator, kind="BinaryExpr")

        return left

    def parse_call_member_expr(self) -> Expr:
        member = self.parse_member_expr()

        if self.at().type == TokenType.OpenParen:
            return self.parse_call_expr(member)

        return member

    def parse_call_expr(self, caller: Expr) -> Expr:
        call_expr = CallExpr(caller=caller, args=self.parse_args(), kind="CallExpr")

        if self.at().type == TokenType.OpenParen:
            call_expr = self.parse_call_expr(call_expr)

        return call_expr

    def parse_args(self) -> List[Expr]:
        self.expect(TokenType.OpenParen, "Expected open parenthesis")
        args = [] if self.at().type == TokenType.CloseParen else self.parse_arguments_list()

        self.expect(
            TokenType.CloseParen,
            "Missing closing parenthesis inside arguments list"
        )
        return args

    def parse_arguments_list(self) -> List[Expr]:
        args = [self.parse_assignment_expr()]

        while self.at().type == TokenType.Comma and self.eat():
            args.append(self.parse_assignment_expr())

        return args

    def parse_member_expr(self) -> Expr:
        object = self.parse_primary_expr()

        while self.at().type in [TokenType.Dot, TokenType.OpenBracket]:
            operator = self.eat()
            computed = operator.type == TokenType.OpenBracket
            if not computed:
                property = self.parse_primary_expr()
                if not isinstance(property, Identifier):
                    raise ValueError("Cannot use dot operator without right-hand side being an identifier.")
            else:
                property = self.parse_expr()
                self.expect(
                    TokenType.CloseBracket,
                    "Missing closing bracket in computed value."
                )

            object = MemberExpr(object=object, property=property, computed=computed, kind="MemberExpr")

        return object

    def parse_primary_expr(self) -> Expr:
        tk = self.at().type

        if tk == TokenType.Identifier:
            return Identifier(symbol=self.eat().value, kind="Identifier")
        elif tk == TokenType.Number:
            return NumericLiteral(value=float(self.eat().value), kind="NumericLiteral")
        elif tk == TokenType.OpenParen:
            self.eat()
            value = self.parse_expr()
            self.expect(
                TokenType.CloseParen,
                "Unexpected token found inside parenthesized expression. Expected closing parenthesis."
            )
            return value
        else:
            print("Unexpected token found during parsing!", self.at())
            exit(1)
