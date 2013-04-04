import os, errno, ConfigParser
from .command import Command, CommandError
from .. import auth

class InitAuth(Command):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("init-auth", description="Store auth information locally %s" % auth.CONFIG_FILE_PATH)
		p.add_argument("key", help="Your API Key")
		p.add_argument("secret", help="Your API Secret")

		return "init-auth"

	def execute(self):
		key, secret = auth.read_from_file()
		if key:
			raise CommandError("Authentication information already exists in " + auth.CONFIG_FILE_PATH)

		try:
			os.mkdir(auth.CONFIG_DIR)
			os.chmod(auth.CONFIG_DIR, 0700)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise CommandError(e)

		cfg = ConfigParser.SafeConfigParser()
		cfg.add_section("main")
		cfg.set("main", "key", self.args.key)
		cfg.set("main", "secret", self.args.secret)

		cfg.write(file(auth.CONFIG_FILE_PATH, "w"))
		os.chmod(auth.CONFIG_FILE_PATH, 0600)
	
