import argparse
import importlib
import json
import os
import pkgutil
import re
import sys
from pathlib import Path

from halo import Halo
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from .ai_util import format_response, prompt

configs = Path.home().joinpath(".pal")


parser = argparse.ArgumentParser(
    prog="pal",
    description="pal - A friend; a chum.",
    epilog='Use "%(prog)s {command} --help" for more information about a command.',
)
commands = parser.add_subparsers(dest="command", title="Available Commands")

plugins = {}


def load_plugins(path: str):
    sys.path.insert(0, path)

    for _, name, _ in pkgutil.iter_modules([path]):
        module = importlib.import_module(name)
        if hasattr(module, "Plugin"):
            klass = getattr(module, "Plugin")
            instance = klass(commands)
            instance.setup()

            plugins[name] = instance


load_plugins(f"{os.path.dirname(os.path.abspath(__file__))}/plugins")
load_plugins(f"{configs}/plugins")

do = commands.add_parser("do", help="Pal AI", description="Pal AI")
do.add_argument("prompt", nargs="*", help="Prompt inputted to the AI", action="store")

args = parser.parse_args()


def run():

    if args.command in plugins:
        plugins[args.command].run(args, parser)

    elif args.command == "do":
        config = (
            configs.joinpath("ai.json")
            if os.path.exists(configs.joinpath("ai.json"))
            else None
        )

        if config:
            if args.prompt:
                data = json.loads(config.read_text(encoding="utf-8"))
                functions = [plugin.function for plugin in list(plugins.values())]
                query = " ".join(args.prompt)

                with Halo("Thinking..."):
                    response = format_response(prompt(query, functions))

                if re.match(r"^fallback$", response[0]["name"], re.IGNORECASE):
                    print(response[0]["arguments"]["response"])
                    parser.exit(
                        1,
                    )

                commands = []

                for cmd in response:
                    arguments = ""
                    for name, dict_ in cmd["arguments"].items():
                        arguments += f"--{name} '{dict_}' "

                    commands.append(
                        Choice(
                            f"pal {cmd['name']} {arguments}",
                            name=str(cmd["name"]).capitalize(),
                            enabled=(True if data["trust_mode"] else False),
                        ),
                    )

                runs = inquirer.checkbox(
                    message="Select commands to run:",
                    choices=commands,
                    cycle=False,
                    raise_keyboard_interrupt=False,
                    mandatory=False,
                    transformer=lambda result: "Running %s command%s..."
                    % (len(result), "s" if len(result) > 1 else ""),
                ).execute()

                if runs:
                    for run in runs:
                        os.system(run)
        else:

            if not os.path.exists(configs):
                os.mkdir(configs)

            parser.exit(
                1,
                message="Ai config not found. \n > Learn more: https://github.com/SlumberDemon/pal#ai ",
            )

    else:
        parser.print_help()
        parser.exit()
