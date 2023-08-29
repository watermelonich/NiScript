from src.ast_1 import Stmt
from maiin.environment import Environment
from typing import List, Dict, Callable


class ValueType:
    def __init__(self, type_name: str):
        self.type_name = type_name

    def __repr__(self):
        return self.type_name


class RuntimeVal:
    def __init__(self, type: ValueType):
        self.type = type


class NullVal(RuntimeVal):
    def __init__(self):
        super().__init__(ValueType("null"))
        self.value = None


def MK_NULL() -> NullVal:
    return NullVal()


class BooleanVal(RuntimeVal):
    def __init__(self, value: bool):
        super().__init__(ValueType("boolean"))
        self.value = value


def MK_BOOL(b: bool = True) -> BooleanVal:
    return BooleanVal(b)


class NumberVal(RuntimeVal):
    def __init__(self, value: float):
        super().__init__(ValueType("number"))
        self.value = value


def MK_NUMBER(n: float = 0) -> NumberVal:
    return NumberVal(n)


class ObjectVal(RuntimeVal):
    def __init__(self, properties: Dict[str, RuntimeVal]):
        super().__init__(ValueType("object"))
        self.properties = properties


class NativeFnValue(RuntimeVal):
    def __init__(self, call: Callable[[List[RuntimeVal], Environment], RuntimeVal]):
        super().__init__(ValueType("native-fn"))
        self.call = call


def MK_NATIVE_FN(call: Callable[[List[RuntimeVal], Environment], RuntimeVal]) -> NativeFnValue:
    return NativeFnValue(call)


class FunctionValue(RuntimeVal):
    def __init__(self, name: str, parameters: List[str], declarationEnv: Environment, body: List[Stmt]):
        super().__init__(ValueType("function"))
        self.name = name
        self.parameters = parameters
        self.declarationEnv = declarationEnv
        self.body = body
