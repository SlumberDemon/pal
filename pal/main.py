import argparse
import json
import os
import webbrowser
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

    create = commands.add_parser("create", help="Create project using a template", description="Create project using a template")
    create.add_argument("-n", "--name", help="Name of the project", action="store")
    create.add_argument(
        "-e",
        "--editor",
        help="Code editor to open project with",
        choices=["zed", "code"],
        default="zed",
    )

    browse = commands.add_parser("browse", help="Web related commands", description="Web related commands")
    browse.add_argument("query", action="store")
    browse.add_argument(
        "-e", "--engine", help="Select engine to use", action="store_true"
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

    elif args.command == "browse":
        browse = json.loads(configs.joinpath("browse.json").read_text(encoding="utf-8"))
        engines = browse["engines"]
        engine = browse["default"]["url"]

        if args.engine:
            searchers = [
                Choice(engine["url"], name=engine["name"]) for engine in engines
            ]
            searchers.append(Choice(value=None, name="Exit"))
            engine = inquirer.fuzzy(
                message="Select engine:",
                choices=searchers,
                default=None,
                max_height="50%",
                mandatory=True,
            ).execute()

        webbrowser.open(f'{str(engine).replace("%s", args.query)}')

    else:
        parser.print_help()
        parser.exit()
