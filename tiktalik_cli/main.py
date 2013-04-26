#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (c) 2013 Techstorage sp. z o.o.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the "Software"), to deal in 
# the Software without restriction, including without limitation the rights to 
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of 
# the Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse, textwrap, inspect

from tiktalik.error import TiktalikAPIError
from . import command, auth

def main():
	parent_parser = argparse.ArgumentParser(add_help=False)
	auth.add_parser_arguments(parent_parser)

	parser = argparse.ArgumentParser()
	subparser = parser.add_subparsers(title="Commands", dest="command")

	cmd2cls = {}

	# Autodiscover commands; map all commands to their names, as returned by Command.add_parser
	for cls in dir(command):
		cls = getattr(command, cls)
		if inspect.isclass(cls) and issubclass(cls, command.Command):
			name = cls.add_parser(parent_parser, subparser)
			if name:
				cmd2cls[name] = cls

	args = parser.parse_args()

	try:
		if args.command != "init-auth":
			keyid, secret = auth.get_credentials(args) 
		else:
			keyid, secret = None, None

		cls = cmd2cls[args.command]

		cls(args, keyid, secret).execute()
	except auth.SecurityError:
		msg = """File %s has too liberal access permissions.
The file should be readable and writable by the owner only.
You can fix this by executing:
""" % auth.CONFIG_FILE_PATH

		print "Security error"
		print textwrap.fill(msg, 76)
		print
		print '    chmod 600 %s' % auth.CONFIG_FILE_PATH
	except (command.CommandError, TiktalikAPIError) as e:
		print textwrap.fill("Error: " + str(e), 76)
	except auth.AuthError as e:
		print textwrap.fill("Error: " + str(e), 76)

if __name__ == "__main__":
	main()
