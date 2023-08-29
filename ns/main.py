from src.parser_1 import Parser
from maiin.environment import createGlobalEnv
from maiin.interpreter import evaluate
import asyncio

async def run(filename: str):
    parser = Parser()
    env = createGlobalEnv()

    with open(filename, "r") as file:
        input_code = file.read()

    program = parser.produceAST(input_code)

    _result = evaluate(program, env)
    # print(result)

# Call the run function with the filename
asyncio.run(run("./test.txt"))
