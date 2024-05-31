import argparse
import os
from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

configs = Path.home().joinpath(".pal")

def run():
    parser = argparse.ArgumentParser(
        prog="pal",
        description="pal - A friend; a chum.",
        epilog='Use "%(prog)s {command} --help" for more information about a command.',
    )
    commands = parser.add_subparsers(dest="command", title="Available Commands")

    create = commands.add_parser("create", help="Create project using a template")
    create.add_argument(
        "-n", "--name", help="Name of the project", action="store", metavar=None
    )
    create.add_argument(
        "-e",
        "--editor",
        help="Code editor to open project with",
        choices=["zed", "code"],
        default="zed",
        metavar=None,
    )

    args = parser.parse_args()

    if args.command == "create":
        name = args.name
        editor = args.editor

        if not name:
            name = inquirer.text(message="Project name:").execute()

        path = configs.joinpath("templates")

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
                        Choice("code", name="Visual Studio Code", enabled=False),
                    ],
                    cycle=False,
                    long_instruction="Select code editor to open project with.",
                ).execute()

            os.system(f"{editor} {name}")
    else:
        parser.print_help()
        parser.exit()
