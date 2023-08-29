from src.ast_1 import (
    AssignmentExpr,
    BinaryExpr,
    CallExpr,
    Identifier,
    ObjectLiteral,
)
from maiin.environment import Environment
from maiin.interpreter import evaluate
from maiin.values import (
    FunctionValue,
    MK_NULL,
    NativeFnValue,
    NumberVal,
    ObjectVal,
    RuntimeVal,
)


def eval_numeric_binary_expr(lhs: NumberVal, rhs: NumberVal, operator: str) -> NumberVal:
    result = None
    if operator == "+":
        result = lhs.value + rhs.value
    elif operator == "-":
        result = lhs.value - rhs.value
    elif operator == "*":
        result = lhs.value * rhs.value
    elif operator == "/":
        # TODO: Division by zero checks
        result = lhs.value / rhs.value
    else:
        result = lhs.value % rhs.value

    return NumberVal(result)


def eval_binary_expr(binop: BinaryExpr, env: Environment) -> RuntimeVal:
    lhs = evaluate(binop.left, env)
    rhs = evaluate(binop.right, env)

    # Only currently support numeric operations
    if lhs.type == "number" and rhs.type == "number":
        return eval_numeric_binary_expr(lhs, rhs, binop.operator)

    # One or both are NULL
    return MK_NULL()


def eval_identifier(ident: Identifier, env: Environment) -> RuntimeVal:
    val = env.lookup_var(ident.symbol)
    return val


def eval_assignment(node: AssignmentExpr, env: Environment) -> RuntimeVal:
    if node.assigne.kind != "Identifier":
        raise ValueError(f"Invalid LHS inside assignment expr: {node.assigne}")

    varname = node.assigne.symbol
    return env.assign_var(varname, evaluate(node.value, env))


def eval_object_expr(obj: ObjectLiteral, env: Environment) -> RuntimeVal:
    object_val = ObjectVal(properties={})
    for prop in obj.properties:
        key = prop.key
        value = prop.value
        runtime_val = env.lookup_var(key) if value is None else evaluate(value, env)
        object_val.properties[key] = runtime_val

    return object_val


def eval_call_expr(expr: CallExpr, env: Environment) -> RuntimeVal:
    args = [evaluate(arg, env) for arg in expr.args]
    fn = evaluate(expr.caller, env)

    if fn.type == "native-fn":
        result = (fn.call)(args, env)
        return result

    if fn.type == "function":
        func = fn
        scope = Environment(parent_env=func.declaration_env)

        # Create the variables for the parameters list
        for i in range(len(func.parameters)):
            varname = func.parameters[i]
            scope.declare_var(varname, args[i], constant=False)

        result = MK_NULL()
        # Evaluate the function body line by line
        for stmt in func.body:
            result = evaluate(stmt, scope)

        return result

    raise ValueError("Cannot call value that is not a function: " + str(fn))
