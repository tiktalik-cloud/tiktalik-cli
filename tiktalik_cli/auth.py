import os.path, os, stat, errno, ConfigParser

class AuthError(Exception):
	pass

class SecurityError(Exception):
	pass

# $HOME/.tiktalik/auth
CONFIG_DIR = os.path.expanduser("~/.tiktalik")
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, "auth")

def add_parser_arguments(parser):
	parser.add_argument("--key", dest="api_key", required=False, help="Your API Key")
	parser.add_argument("--secret", dest="api_secret", required=False, help="Your API Secret Key")

def get_credentials(args):
	# cmdline credentials override those stored in config file
	if args.api_key or args.api_secret:
		if not args.api_key or not args.api_secret:
			raise AuthError("Both --key and --secret must be provided when passing auth tokens from commandline.")

		return args.api_key, args.api_secret

	key, secret = read_from_file()
	if not key:
		raise AuthError("Credentials not configured. Try `tiktalik init-auth`, or use --key and --secret.")

	return key, secret.decode("base64")


def read_from_file():
	try:
		st = os.stat(CONFIG_FILE_PATH)
	except OSError as ex:
		if ex.errno == errno.ENOENT:
			return None, None
		else:
			print "Unable to access %s: %s" % (CONFIG_FILE_PATH, ex)

	if stat.S_IMODE(st.st_mode) != 0600:
		raise SecurityError()
	
	cfg = ConfigParser.SafeConfigParser()
	cfg.read(CONFIG_FILE_PATH)

	return cfg.get("main", "key"), cfg.get("main", "secret")
