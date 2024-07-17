import argparse

# Define the plugin class


class Plugin:
    def __init__(self, commands: argparse._SubParsersAction) -> None:
        # Setup command

        self.command = commands.add_parser(
            "hello", help="Hello, World!", description="A hello world plugin"
        )

        # Define functions dict for pal AI

        self.function = {
            "name": "hello",
            "description": "A hello world plugin",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Custom message",
                    },
                },
            },
        }

    # Run the plugin

    def run(self, args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
        if args.message:  # Uses argument defined in setup
            print(args.message)

        else:
            parser.exit(1, message="Hello, World!")

    def setup(self) -> None:
        # Define default value for function arguments

        self.function["parameters"]["properties"]["message"]["enum"] = ["Hello, World!"]

        # Add additional arguments

        self.command.add_argument(
            "-m", "--message", help="Custom message", action="store"
        )
