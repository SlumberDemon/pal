# Pal

A friend; a chum.

### Where

#### Stable

```sh
pip3 install -U sofapal
```

#### Development

```sh
# clone repository
pip install -U git+https://github.com/slumberdemon/pal
# create a virtual environment in the .venv directory
python3 -m venv .venv
# set up the current shell to use that virtual environment
source .venv/bin/activate
```

### Why

Pal is a command-line interface that includes a range of general features and functions. Pal is a personal exploration into creating a command-line interface using Python with aims to use as few dependencies as possible.

### How

```shell
pal
```

Pal loads configs from the `.pal` folder located in `$HOME`. Example configs can be found in [`.pal`](https://github.com/SlumberDemon/pal/tree/main/.pal). Therefore when adding/creating configurations make sure they are in that folder.

#### Create

Pal enables for quick project creation using user-created templates. Templates are written in shell and are provided one argument.

> Pal runs templates like this: `bash template.sh {name}`.

Here is an example of a template to create a sveltekit project.

```shell
npm create svelte@latest $1
cd $1
npm install
```

This file is stored in the `templates` folder. In the example `$1` is used to access the name of the project provided by pal.

It's recommended that the file name is in this format: `language-language-tool.sh`. This will make it easier to search for this template with pal.

```shell
usage: pal create [-h] [-n NAME] [-e {zed,code}]

Create project using a template

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name of the project
  -e {zed,code}, --editor {zed,code}
                        Code editor to open project with
```

#### Browse

Pal lets you quickly query text with any search engine.

> Pal opens searches in your default browser.

To use browse you will need to configure `browse.json` in your configs. The structure is as follows.

```json
{
  "engines": [
    {
      "name": "duckduckgo",
      "url": "https://duckduckgo.com/?q=%s"
    },
  ],
  "default": {
    "name": "duckduckgo",
    "url": "https://duckduckgo.com/?q=%s"
  }
}
```

Pal requires a `default` engine to be set. Any other `engines` added can be accessed by providing the `-e/--engine` option. The url for an engine needs to include `%s` as this will be replaced with the search query.

```shell
usage: pal browse [-h] [-e] query

Web related commands

positional arguments:
  query

options:
  -h, --help    show this help message and exit
  -e, --engine  Select engine to use
```

#### Weather

Pal can display information on the weather. Pal needs an [`weatherapi`](https://www.weatherapi.com) api key to do so.

Setup for weather is easy and can be done with the following.

```shell
pal weather
```

Running with the command with no configs for the first time will start the interactive configuration process. For more information on manual setup, see the examples.

```shell
usage: pal weather [-h] [-s] [-l LOCATION] [-w]

Weather information

options:
  -h, --help            show this help message and exit
  -s, --search          Search location to get information from
  -l LOCATION, --location LOCATION
                        Location to get information from
  -w, --window          Disables displaying weather information via a window
```
