import argparse
import json
import os
import urllib.request
from pathlib import Path

import pytermgui as ptg
from halo import Halo
from InquirerPy import inquirer
from InquirerPy.base.control import Choice


class Plugin:
    def __init__(self, commands: argparse._SubParsersAction) -> None:
        self.command = commands.add_parser(
            "weather", help="Weather information", description="Weather information"
        )
        self.function = {
            "name": "weather",
            "description": "Weather information",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to get information from",
                    }
                },
                "required": ["location"],
            },
        }
        self.configs = Path.home().joinpath(".pal")

    def weather_window(self, data: dict, format: str):
        with ptg.WindowManager() as manager:
            window = (
                ptg.Window(
                    "",
                    ptg.Splitter(
                        ptg.Label(
                            f"[surface+1]{data['current']['condition']['text']}",
                            parent_align=0,
                        ),
                        ptg.Label(
                            f"[surface+3]{data['current'][f'temp_{format}']}°{format.capitalize()}",
                            parent_align=2,
                        ),
                    ),
                    ptg.Container(
                        ptg.Label(
                            f"[surface+1]Feels like: [surface+3]{data['current'][f'feelslike_{format}']}°{format.capitalize()}\n[surface+1]Humidity: [surface+3]{data['current']['humidity']}%",
                            parent_align=0,
                        ),
                        box="ROUNDED",
                    ),
                )
                .set_title(f"{data['location']['name']}")
                .center()
            )
            manager.add(window)

    def run(self, args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
        config = (
            self.configs.joinpath("weather.json")
            if os.path.exists(self.configs.joinpath("weather.json"))
            else None
        )

        if config:
            weather = json.loads(config.read_text(encoding="utf-8"))
            api_key = weather["api_key"]
            location = weather["default"]
            format = str(weather["format"])[0]

            if args.search:
                name = inquirer.text(message="Search location:").execute()

                with Halo("Loading locations..."):
                    with urllib.request.urlopen(
                        f"https://api.weatherapi.com/v1/search.json?key={api_key}&q={name.replace(' ', '-')}"
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

            if location:
                with urllib.request.urlopen(
                    f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=yes"
                ) as response:
                    data = response.read()
                    details = json.loads(data)

                if args.window:
                    self.weather_window(details, format)
                else:
                    print(
                        f"{details['current']['condition']['text']} | {details['current'][f'temp_{format}']}°{format.capitalize()}\nFeels like: {details['current'][f'feelslike_{format}']}°{format.capitalize()}\nHumidity: {details['current']['humidity']}%"
                    )

        else:

            def validate_key(key: str) -> bool:
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

            with Halo("Loading locations..."):
                with urllib.request.urlopen(
                    f"https://api.weatherapi.com/v1/search.json?key={api_key}&q={name.replace(' ', '-')}"
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

            if location:
                format = inquirer.rawlist(
                    message="Select format:",
                    choices=[
                        Choice("celsius", name="Celsius", enabled=True),
                        Choice("fahrenheit", name="Fahrenheit", enabled=False),
                    ],
                    cycle=False,
                ).execute()

                if not os.path.exists(self.configs):
                    os.mkdir(self.configs)

                with open(
                    f"{self.configs.joinpath('weather.json')}", "a+", encoding="utf-8"
                ) as f:
                    json.dump(
                        {"default": location, "api_key": api_key, "format": format},
                        f,
                        ensure_ascii=False,
                        indent=2,
                    )

    def setup(self):
        config = (
            self.configs.joinpath("weather.json")
            if os.path.exists(self.configs.joinpath("weather.json"))
            else None
        )

        if config:
            self.function["parameters"]["properties"]["location"]["enum"] = [
                f"{json.loads(config.read_text(encoding='utf-8'))['default']}"
            ]

        self.command.add_argument(
            "-s",
            "--search",
            help="Search location to get information from",
            action="store_true",
        )
        self.command.add_argument(
            "-l",
            "--location",
            help="Location to get information from",
            action="store",
        )
        self.command.add_argument(
            "-w",
            "--window",
            help="Disables displaying weather information via a window",
            action="store_false",
        )
