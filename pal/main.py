import argparse
import json
import os
import urllib.request
import webbrowser
from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from .spinner_util import spinner
from .window_util import weather_window

configs = Path.home().joinpath(".pal")


def run():
    parser = argparse.ArgumentParser(
        prog="pal",
        description="pal - A friend; a chum.",
        epilog='Use "%(prog)s {command} --help" for more information about a command.',
    )
    commands = parser.add_subparsers(dest="command", title="Available Commands")

    create = commands.add_parser(
        "create",
        help="Create project using a template",
        description="Create project using a template",
    )
    create.add_argument("-n", "--name", help="Name of the project", action="store")
    create.add_argument(
        "-e",
        "--editor",
        help="Code editor to open project with",
        choices=["zed", "code"],
    )

    browse = commands.add_parser(
        "browse", help="Web related commands", description="Web related commands"
    )
    browse.add_argument("query", action="store")
    browse.add_argument(
        "-e", "--engine", help="Select engine to use", action="store_true"
    )

    weather = commands.add_parser(
        "weather", help="Weather information", description="Weather information"
    )
    weather.add_argument(
        "-s",
        "--search",
        help="Search location to get information from",
        action="store_true",
    )
    weather.add_argument(
        "-l",
        "--location",
        help="Location to get information from",
        action="store",
    )
    weather.add_argument(
        "-w",
        "--window",
        help="Disables displaying weather information via a window",
        action="store_false",
    )

    args = parser.parse_args()

    if args.command == "create":
        name = args.name
        editor = args.editor

        if not name:
            name = inquirer.text(message="Project name:").execute()

        path = (
            configs.joinpath("templates")
            if os.path.exists(configs.joinpath("templates"))
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
            parser.exit(
                1,
                message="Create config not found. \n > Learn more: https://github.com/SlumberDemon/pal#create ",
            )

    elif args.command == "browse":
        config = (
            configs.joinpath("browse.json")
            if os.path.exists(configs.joinpath("browse.json"))
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
            parser.exit(
                1,
                message="Browse config not found. \n > Learn more: https://github.com/SlumberDemon/pal#browse ",
            )

    elif args.command == "weather":
        config = (
            configs.joinpath("weather.json")
            if os.path.exists(configs.joinpath("weather.json"))
            else None
        )

        if config:
            weather = json.loads(config.read_text(encoding="utf-8"))
            api_key = weather["api_key"]
            location = weather["default"]
            format = str(weather["format"])[0]

            if args.search:
                name = inquirer.text(message="Search location:").execute()

                with spinner("Loading locations..."):
                    with urllib.request.urlopen(
                        f"https://api.weatherapi.com/v1/search.json?key={api_key}&q={name}"
                    ) as response:
                        data = response.read()
                        results = json.loads(data)

                locations = [
                    Choice(
                        result["url"],
                        name=f"{result['name']} > {result['region']} > {result['country']}",
                    )
                    for result in results
                ]
                locations.append(Choice(value=None, name="Exit"))

                location = inquirer.fuzzy(
                    message="Choose location:",
                    choices=locations,
                    max_height="50%",
                    mandatory=True,
                ).execute()

            if args.location:
                location = args.location

            with urllib.request.urlopen(
                f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=yes"
            ) as response:
                data = response.read()
                details = json.loads(data)

            if args.window:
                weather_window(details, format)
            else:
                print(
                    f"{details['current']['condition']['text']} | {details['current'][f'temp_{format}']}°{format.capitalize()}\nFeels like: {details['current'][f'feelslike_{format}']}°{format.capitalize()}\nHumidity: {details['current']['humidity']}%"
                )

        else:

            def validate_key(key: str):
                try:
                    with urllib.request.urlopen(
                        f"http://api.weatherapi.com/v1/current.json?key={key}&q=london"
                    ) as response:
                        if response.getcode() == 200:
                            return True
                        else:
                            return False
                except:
                    return False

            api_key = inquirer.secret(
                message="Api key:",
                validate=lambda key: validate_key(key),
                invalid_message="Api key not found.",
                long_instruction="Get a free api key from https://www.weatherapi.com",
                mandatory=True,
            ).execute()

            name = inquirer.text(message="Default location name:").execute()

            with spinner("Loading locations..."):
                with urllib.request.urlopen(
                    f"https://api.weatherapi.com/v1/search.json?key={api_key}&q={name}"
                ) as response:
                    data = response.read()
                    results = json.loads(data)

            locations = [
                Choice(
                    result["url"],
                    name=f"{result['name']} > {result['region']} > {result['country']}",
                )
                for result in results
            ]
            locations.append(Choice(value=None, name="Exit"))

            location = inquirer.fuzzy(
                message="Choose location:",
                choices=locations,
                max_height="50%",
                mandatory=True,
            ).execute()

            format = inquirer.rawlist(
                message="Select format:",
                choices=[
                    Choice("celsius", name="Celsius", enabled=True),
                    Choice("fahrenheit", name="Fahrenheit", enabled=False),
                ],
                cycle=False,
            ).execute()

            with open(
                f"{configs.joinpath('weather.json')}", "w", encoding="utf-8"
            ) as f:
                json.dump(
                    {"default": location, "api_key": api_key, "format": format},
                    f,
                    ensure_ascii=False,
                    indent=2,
                )

    else:
        parser.print_help()
        parser.exit()
