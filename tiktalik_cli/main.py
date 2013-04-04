#!/usr/bin/env python
# -*- coding: utf8 -*-

import argparse, textwrap, inspect

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
	except command.CommandError as e:
		print textwrap.fill("Error: " + str(e), 76)
	except auth.AuthError as e:
		print textwrap.fill("Error: " + str(e), 76)

if __name__ == "__main__":
	main()
