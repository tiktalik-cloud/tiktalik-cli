# Tiktalik Command Line Interface

This is a command line interface utility implemented in Python, which enables the
user to perform core operations on the [Tiktalik Cloud Computing](http://www.tiktalik.com) service.

## Requirements

 * [tiktalik-python](https://github.com/tiktalik-cloud/tiktalik-python)
 * Python 2.7

Note that package dependencies are automatically installed by pip.

## Installation

Install using pip:

`$ pip install tiktalik-cli`

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

We also have [a tutorial](http://articles.tiktalik.com/content/help/using-tiktalik-command-line-utility/) to quickly get
you started.

## License

Copyright (c) 2013 Techstorage sp. z o.o.

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of 
the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

