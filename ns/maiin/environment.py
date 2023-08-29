from ast import List
from maiin.values import MK_BOOL, MK_NATIVE_FN, MK_NULL, MK_NUMBER, RuntimeVal
from typing import Optional, Dict

class Environment:
    def __init__(self, parentENV: Optional['Environment'] = None):
        self.parent = parentENV
        self.variables: Dict[str, RuntimeVal] = {}
        self.constants: set = set()

    def declareVar(self, varname: str, value: RuntimeVal, constant: bool) -> RuntimeVal:
        if varname in self.variables:
            raise Exception(f"Cannot declare variable {varname}. As it already is defined.")

        self.variables[varname] = value
        if constant:
            self.constants.add(varname)
        return value

    def assignVar(self, varname: str, value: RuntimeVal) -> RuntimeVal:
        env = self.resolve(varname)

        # Cannot assign to constant
        if varname in env.constants:
            raise Exception(f"Cannot reassign to variable {varname} as it was declared constant.")

        env.variables[varname] = value
        return value

    def lookupVar(self, varname: str) -> RuntimeVal:
        env = self.resolve(varname)
        return env.variables[varname]

    def resolve(self, varname: str) -> 'Environment':
        if varname in self.variables:
            return self

        if not self.parent:
            raise Exception(f"Cannot resolve '{varname}' as it does not exist.")

        return self.parent.resolve(varname)

def createGlobalEnv() -> Environment:
    env = Environment()
    # Create Default Global Environment
    env.declareVar("true", MK_BOOL(True), True)
    env.declareVar("false", MK_BOOL(False), True)
    env.declareVar("null", MK_NULL(), True)

    # Define a native builtin method
    env.declareVar(
        "print",
        MK_NATIVE_FN(lambda args, _scope: print(*args) or MK_NULL()),
        True
    )

    def timeFunction(_args: List[RuntimeVal], _env: Environment) -> RuntimeVal:
        import time
        return MK_NUMBER(int(time.time() * 1000))

    env.declareVar("time", MK_NATIVE_FN(timeFunction), True)

    return env
