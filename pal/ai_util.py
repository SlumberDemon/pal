import ast
import json
import os
import sys
import urllib.request
from pathlib import Path

from halo import Halo

delimiter = "<<function>>"


def prompt(query: str, functions: list[dict]) -> str:
    config = json.loads(
        Path.home().joinpath(".pal").joinpath("ai.json").read_text(encoding="utf-8")
    )

    functions.append(
        {
            "name": "fallback",
            "description": "Pal responds to the user when an error occurs or there is not enough information provided",
            "parameters": {
                "type": "object",
                "properties": {
                    "response": {
                        "type": "string",
                        "description": "The fallback response",
                    }
                },
                "required": ["response"],
            },
        }
    )

    payload = {
        "model": f"{config["model"]}",
        "stream": False,
        "prompt": f"### Instruction: <<function>>{json.dumps(functions)}\n<<question>>{query}\n### Response: ",
    }

    with urllib.request.urlopen(
        f"{config['host']}/api/generate", json.dumps(payload).encode("utf-8")
    ) as response:
        data = response.read()
        output = json.loads(data)["response"]

    return output


def extract_functions(response: str) -> list[str]:
    return [element.strip() for element in response.split(delimiter) if element.strip()]


def process_ast_node(node):
    if isinstance(node, ast.Call):
        return ast.unparse(node)
    else:
        node_str = ast.unparse(node)
        return eval(node_str)


def parse_function(fuction: str) -> dict:
    tree = ast.parse(bytes(fuction, "utf8"))
    expr = tree.body[0]

    call_node = expr.value
    function_name = (
        call_node.func.id
        if isinstance(call_node.func, ast.Name)
        else str(call_node.func)
    )

    parameters = {}
    noNameParam = []

    for arg in call_node.args:
        noNameParam.append(process_ast_node(arg))

    for kw in call_node.keywords:
        parameters[kw.arg] = process_ast_node(kw.value)

    if noNameParam:
        parameters["None"] = noNameParam

    functions_dict = {"name": function_name, "arguments": parameters}
    return functions_dict


def format_response(response: str) -> list[dict]:
    extracted_functions = extract_functions(response)
    return [parse_function(function) for function in extract_functions(response)]
