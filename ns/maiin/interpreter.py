from maiin.values import NumberVal, RuntimeVal
from src.ast_1 import (
    AssignmentExpr,
    BinaryExpr,
    CallExpr,
    FunctionDeclaration,
    Identifier,
    NumericLiteral,
    ObjectLiteral,
    Program,
    Stmt,
    VarDeclaration,
)
from maiin.environment import Environment
from eval.statements import (
    eval_function_declaration,
    eval_program,
    eval_var_declaration,
)
from eval.expressions import (
    eval_assignment,
    eval_binary_expr,
    eval_call_expr,
    eval_identifier,
    eval_object_expr,
)

def evaluate(astNode: Stmt, env: Environment) -> RuntimeVal:
    if isinstance(astNode, NumericLiteral):
        return NumberVal(astNode.value)
    elif isinstance(astNode, Identifier):
        return eval_identifier(astNode, env)
    elif isinstance(astNode, ObjectLiteral):
        return eval_object_expr(astNode, env)
    elif isinstance(astNode, CallExpr):
        return eval_call_expr(astNode, env)
    elif isinstance(astNode, AssignmentExpr):
        return eval_assignment(astNode, env)
    elif isinstance(astNode, BinaryExpr):
        return eval_binary_expr(astNode, env)
    elif isinstance(astNode, Program):
        return eval_program(astNode, env)
    elif isinstance(astNode, VarDeclaration):
        return eval_var_declaration(astNode, env)
    elif isinstance(astNode, FunctionDeclaration):
        return eval_function_declaration(astNode, env)
    else:
        print(
            "This AST Node has not yet been set up for interpretation.\n",
            astNode
        )
        exit(0)
