# Pal

Pal is a modular command-line interface with AI function calling. Pal at its core provides a few in-built plugins, but it can easily be extended. Pal is a personal exploration project.

### Install

> [!IMPORTANT]
> Due to the `halo` library on PyPi being outdated it is not installed. Please make sure to install my fork of the library.
```sh
pip3 install git+https://github.com/SlumberDemon/halo
```

#### Stable

```sh
pip3 install -U sofapal
```

#### Development

```sh
# clone repository
pip3 install -U git+https://github.com/slumberdemon/pal
# create a virtual environment in the .venv directory
python3 -m venv .venv
# set up the current shell to use that virtual environment
source .venv/bin/activate
```

### Ai

Pal uses `OpenFunctions-v2` for its AI functionality. For optimal performance, it is recommended to have at least 16 GB of RAM. For instructions on setting up this feature, see below.

1. Install [ollama](https://ollama.sh)
2. Download the AI model file from [huggingface](https://huggingface.co/gorilla-llm/gorilla-openfunctions-v2-gguf/tree/main), I recommend `gorilla-openfunctions-v2-q4_K_M.gguf`
3. Download the [Modelfile](https://github.com/SlumberDemon/pal/blob/main/Modelfile) and modify it by changing `path_to_model_file` to the file you downloaded in step 2
4. Open a terminal in the same location as the `Modelfile` and run the following command:

```
ollama create -f Modelfile pal
```

5. Add the AI configurations by creating `.pal/ai.json` with the following content:

```json
{
  "model": "pal:latest",
  "host": "http://localhost:11434",
  "trust_mode": false
}
```

> Enabling trust mode with `true` will automatically select all commands to be run.

### Config

```shell
pal
```

Pal loads configs and plugins from the `.pal` folder located in `$HOME`. Example configs can be found in [`.pal`](https://github.com/SlumberDemon/pal/tree/main/.pal). Therefore, when creating configurations/plugins, make sure they are in that folder. When a command's configuration is missing, Pal will assist you in adding it.

### Inbuilt plugins

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
    }
  ],
  "default": {
    "name": "duckduckgo",
    "url": "https://duckduckgo.com/?q=%s"
  }
}
```

Pal requires a `default` engine to be set. Any other `engines` added can be accessed by providing the `-e/--engine` option. The url for an engine needs to include `%s` as this will be replaced with the search query.

```shell
usage: pal browse [-h] [-s SEARCH] [-e] [query]

Open queries in your browser

positional arguments:
  query                 Query to browse using default engine

options:
  -h, --help            show this help message and exit
  -s SEARCH, --search SEARCH
                        Search query to browse using default engine
  -e, --engine          When provided, displays search engine selector
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
