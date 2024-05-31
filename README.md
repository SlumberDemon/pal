# Pal

A friend; a chum.

### Where

```sh
pip install -U sofapal
```

```sh
pipx install sofapal
```

```sh
pip install git+https://github.com/slumberdemon/pal
```

### Why

Pal is a command-line interface that includes a range of general features and functions. Pal is a personal exploration into creating a command-line interface in Python.

### How

```shell
pal
```

Pal loads configs from the `.pal` folder located in `$HOME`. Example configs can be found in the in [.pal](https://github.com/SlumberDemon/pal/tree/main/.pal).

#### Create

Pal enables for quick project creation using user-created templates. Templates are written in shell and are provided one argument.

Pal uses templates like this: 'bash template.sh {name}'.

Here is an example of a template to create a sveltekit project.

```shell
npm create svelte@latest $1
cd $1
npm install
```

This file is stored in `.pal/templates`. In the example `$1` is used to access the name of the project provided by pal.

It's recommended that the file name is in this format: `language-language-tool.sh`. This will make it easier to search for this template with pal.

---

```shell
usage: pal create [-h] [-n NAME] [-e {zed,code}]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name of the project
  -e {zed,code}, --editor {zed,code}
                        Code editor to open project with
```
