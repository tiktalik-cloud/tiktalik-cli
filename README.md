# Tiktalik Command Line Interface

This is a command line interface utility implemented in Python, which enables the
user to perform core operations on the Tiktalik Cloud Computing service.

## Requirements

 * [tiktalik-python](https://github.com/tiktalik-cloud/tiktalik-python)
 * Python 2.7

## Installation

Install [tiktalik-python](https://github.com/tiktalik-cloud/tiktalik-python) first:

`$ pip install https://github.com/tiktalik-cloud/tiktalik-python/archive/master.zip`

Then install the CLI itself:

`$ pip install https://github.com/tiktalik-cloud/tiktalik-cli/archive/master.zip`

## Authentication

To use the CLI you need an API key. You can generate one in your
[admin panel](https://tiktalik.com/panel/#apikeys). The API authentication
information consists of an *API key* and an *API secret*. You can save this
information locally by executing:

`$ tiktalik init-auth API-KEY API-SECRET`

This saves the key and secret to `~/.tiktalik/auth`

Alternatively, if you don't want to save your API key, you can use the `--key`
and `--secret` switches on the commandline.

## Usage

The basic usage patterns is:

`$ tiktalik COMMAND`

You can get a list of commands by running `tiktalik` without arguments.
To get a help on a specific command, run:

`$ tiktalik COMMAND --help`

Commands that operate on instances (eg. `start`, `stop`) take either instance name
(`-n` argument) or UUID (`-u`).
