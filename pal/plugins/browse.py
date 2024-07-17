import argparse
import json
import os
import webbrowser
from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.base.control import Choice


class Plugin:
    def __init__(self, commands: argparse._SubParsersAction) -> None:
        self.command = commands.add_parser(
            "browse",
            help="Open queries in your browser",
            description="Open queries in your browser",
        )
        self.function = {
            "name": "browse",
            "description": "Open queries in your browser",
            "parameters": {
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": "Search query to browse using default engine",
                    },
                    "engine": {
                        "type": "boolean",
                        "description": "When provided, displays search engine selector",
                    },
                },
                "required": ["query"],
            },
        }
        self.configs = Path.home().joinpath(".pal")

    def run(self, args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
        config = (
            self.configs.joinpath("browse.json")
            if os.path.exists(self.configs.joinpath("browse.json"))
            else None
        )

        if config:
            browse = json.loads(config.read_text(encoding="utf-8"))
            engines = browse["engines"]
            engine = browse["default"]["url"]

            if args.engine:
                searchers = [
                    Choice(engine["url"], name=engine["name"]) for engine in engines
                ]
                searchers.append(Choice(value=engine, name="Exit"))

                engine = inquirer.fuzzy(
                    message="Select engine:",
                    choices=searchers,
                    default=None,
                    max_height="50%",
                    mandatory=True,
                ).execute()

            webbrowser.open(
                f'{str(engine).replace("%s", (args.query if args.query else args.search))}'
            )
        else:

            if not os.path.exists(self.configs):
                os.mkdir(self.configs)

            parser.exit(
                1,
                message="Browse config not found. \n > Learn more: https://github.com/SlumberDemon/pal#browse ",
            )

    def setup(self) -> None:
        self.command.add_argument(
            "query",
            help="Query to browse using default engine",
            action="store",
            nargs="?",
        )
        self.command.add_argument(
            "-s",
            "--search",
            help="Search query to browse using default engine (AI)",
            action="store",
        )
        self.command.add_argument(
            "-e",
            "--engine",
            help="When provided, displays search engine selector",
            action="store_true",
        )
