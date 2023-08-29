from typing import List, Union, Optional

NodeType = Union[
    # STATEMENTS
    "Program",
    "VarDeclaration",
    "FunctionDeclaration",
    # EXPRESSIONS
    "AssignmentExpr",
    "MemberExpr",
    "CallExpr",
    # Literals
    "Property",
    "ObjectLiteral",
    "NumericLiteral",
    "Identifier",
    "BinaryExpr"
]

class Stmt:
    def __init__(self, kind: NodeType):
        self.kind = kind

class Program(Stmt):
    def __init__(self, body: List[Stmt]):
        super().__init__("Program")
        self.body = body

class VarDeclaration(Stmt):
    def __init__(self, constant: bool, identifier: str, value: Optional["Expr"] = None):
        super().__init__("VarDeclaration")
        self.constant = constant
        self.identifier = identifier
        self.value = value

class FunctionDeclaration(Stmt):
    def __init__(self, parameters: List[str], name: str, body: List[Stmt]):
        super().__init__("FunctionDeclaration")
        self.parameters = parameters
        self.name = name
        self.body = body

class Expr(Stmt):
    pass

class AssignmentExpr(Expr):
    def __init__(self, assigne: "Expr", value: "Expr"):
        super().__init__("AssignmentExpr")
        self.assigne = assigne
        self.value = value

class BinaryExpr(Expr):
    def __init__(self, left: "Expr", right: "Expr", operator: str):
        super().__init__("BinaryExpr")
        self.left = left
        self.right = right
        self.operator = operator

class CallExpr(Expr):
    def __init__(self, args: List["Expr"], caller: "Expr"):
        super().__init__("CallExpr")
        self.args = args
        self.caller = caller

class MemberExpr(Expr):
    def __init__(self, object: "Expr", property: "Expr", computed: bool):
        super().__init__("MemberExpr")
        self.object = object
        self.property = property
        self.computed = computed

# LITERAL / PRIMARY EXPRESSION TYPES

class Identifier(Expr):
    def __init__(self, symbol: str):
        super().__init__("Identifier")
        self.symbol = symbol

class NumericLiteral(Expr):
    def __init__(self, value: float):
        super().__init__("NumericLiteral")
        self.value = value

class Property(Expr):
    def __init__(self, key: str, value: Optional["Expr"] = None):
        super().__init__("Property")
        self.key = key
        self.value = value

class ObjectLiteral(Expr):
    def __init__(self, properties: List[Property]):
        super().__init__("ObjectLiteral")
        self.properties = properties
