import argparse
import os
from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.base.control import Choice


class Plugin:
    def __init__(self, commands: argparse._SubParsersAction) -> None:
        self.command = commands.add_parser(
            "create",
            help="Create project using a template",
            description="Create project using a template",
        )
        self.function = {
            "name": "create",
            "description": "Create project using a template",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the project"},
                    "editor": {
                        "type": "string",
                        "enum": ["zed", "code", "helix", "nvim"],
                        "description": "Code editor to open project with",
                    },
                },
                "required": ["name"],
            },
        }
        self.configs = Path.home().joinpath(".pal")

    def run(self, args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
        name = args.name
        editor = args.editor

        if not name:
            name = inquirer.text(message="Project name:").execute()

        path = (
            self.configs.joinpath("templates")
            if os.path.exists(self.configs.joinpath("templates"))
            else None
        )

        if path:
            templates = [
                Choice(
                    template.name,
                    name=" ".join(str(template.name).removesuffix(".sh").split("-")),
                    enabled=False,
                )
                for template in path.iterdir()
            ]
            templates.append(Choice(value=None, name="Exit"))
            templating = inquirer.fuzzy(
                message="Select template:",
                choices=templates,
                default=None,
                max_height="50%",
                mandatory=True,
            ).execute()

            if templating:
                os.system(f"bash {path}/{templating} {name}")

                if not editor:
                    editor = inquirer.rawlist(
                        message="Open in:",
                        choices=[
                            Choice("zed", name="Zed", enabled=True),
                            Choice("helix", name="Helix", enabled=False),
                            Choice("nvim", name="Neovim", enabled=False),
                            Choice("code", name="Visual Studio Code", enabled=False),
                        ],
                        cycle=False,
                        long_instruction="Select code editor to open project with.",
                    ).execute()

                os.system(f"{editor} {name}")
        else:

            if not os.path.exists(self.configs):
                os.mkdir(self.configs)

            parser.exit(
                1,
                message="Create config not found. \n > Learn more: https://github.com/SlumberDemon/pal#create ",
            )

    def setup(self) -> None:
        self.command.add_argument(
            "-n", "--name", help="Name of the project", action="store"
        )
        self.command.add_argument(
            "-e",
            "--editor",
            help="Code editor to open project with",
            choices=["zed", "code"],
        )
