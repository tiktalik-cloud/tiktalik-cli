from tiktalik.computing import ComputingConnection
from .. import auth

class CommandError(Exception):
	pass

class CommandAborted(Exception):
	pass

class Command(object):
	def __init__(self, args, keyid, secret):
		self.args = args
		self.conn = ComputingConnection(keyid, secret)

	@classmethod
	def add_parser(cls, parser, subparser):
		return None

	def execute(self):
		raise NotImplementedError()

	def yesno(self, message, abort=True):
		print message

		answer = None
		while answer not in ("yes", "no"):
			answer = raw_input("Please answer 'yes' or 'no' > ")

		if answer == "yes":
			return True

		if abort:
			raise CommandAborted()
		else:
			return False

