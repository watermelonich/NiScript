from src.ast_1 import FunctionDeclaration, Program, VarDeclaration
from maiin.environment import Environment
from maiin.interpreter import evaluate
from maiin.values import FunctionValue, MK_NULL, RuntimeVal


def eval_program(program: Program, env: Environment) -> RuntimeVal:
    last_evaluated = MK_NULL()
    for statement in program.body:
        last_evaluated = evaluate(statement, env)
    return last_evaluated


def eval_var_declaration(declaration: VarDeclaration, env: Environment) -> RuntimeVal:
    value = evaluate(declaration.value, env) if declaration.value else MK_NULL()
    return env.declare_var(declaration.identifier, value, declaration.constant)


def eval_function_declaration(
    declaration: FunctionDeclaration, env: Environment
) -> RuntimeVal:
    # Create new function scope
    fn = FunctionValue(
        name=declaration.name,
        parameters=declaration.parameters,
        declaration_env=env,
        body=declaration.body,
    )

    return env.declare_var(declaration.name, fn, constant=True)
