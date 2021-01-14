"""Module tiktalik_cli.auth"""
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

import os.path
import os
import stat
import errno
import configparser
import base64


class AuthError(Exception):
    """AuthError class"""


class SecurityError(Exception):
    """SecurityError class"""


# $HOME/.tiktalik/auth
CONFIG_DIR = os.path.expanduser("~/.tiktalik")
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, "auth")


def add_parser_arguments(parser):
    """Add args to generic parser"""
    parser.add_argument("--key", dest="api_key", required=False, help="Your API Key")
    parser.add_argument(
        "--secret", dest="api_secret", required=False, help="Your API Secret Key"
    )


def get_credentials(args):
    """Read credentials from args"""
    # cmdline credentials override those stored in config file
    if args.api_key or args.api_secret:
        if not args.api_key or not args.api_secret:
            raise AuthError(
                (
                    "Both --key and --secret must be provided "
                    "when passing auth tokens from commandline."
                )
            )

        return args.api_key, args.api_secret

    key, secret = read_from_file()
    if not key:
        raise AuthError(
            (
                "Credentials not configured. "
                "Try `tiktalik init-auth`, or use --key and --secret."
            )
        )

    return key, base64.b64decode(secret)


def read_from_file():
    """Try to read from file"""
    try:
        st = os.stat(CONFIG_FILE_PATH)
    except OSError as ex:
        if ex.errno == errno.ENOENT:
            return None, None
        else:
            print(("Unable to access %s: %s" % (CONFIG_FILE_PATH, ex)))

    if (stat.S_IMODE(st.st_mode) != 0o600) and (os.name == 'posix'):
        raise SecurityError()

    cfg = configparser.SafeConfigParser()
    cfg.read(CONFIG_FILE_PATH)

    return cfg.get("main", "key"), cfg.get("main", "secret")
