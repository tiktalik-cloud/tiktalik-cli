"""Module tiktalik_cli.command.auth"""
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

import os
import errno
import configparser
from .command import GeneralCommand, CommandError
from .. import auth


class InitAuth(GeneralCommand):
    """Initialise auth"""

    @classmethod
    def add_parser(cls, parser, subparser):
        p = subparser.add_parser(
            "init-auth",
            description="Store auth information " "locally %s" % auth.CONFIG_FILE_PATH,
        )
        p.add_argument("key", help="Your API Key")
        p.add_argument("secret", help="Your API Secret")

        return "init-auth"

    def execute(self):
        key, secret = auth.read_from_file()
        if key:
            raise CommandError(
                "Authentication information already "
                "exists in " + auth.CONFIG_FILE_PATH
            )

        try:
            os.mkdir(auth.CONFIG_DIR)
            os.chmod(auth.CONFIG_DIR, 0o700)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise CommandError(e)

        cfg = configparser.SafeConfigParser()
        cfg.add_section("main")
        cfg.set("main", "key", self.args.key)
        cfg.set("main", "secret", self.args.secret)

        cfg.write(open(auth.CONFIG_FILE_PATH, "w"))
        os.chmod(auth.CONFIG_FILE_PATH, 0o600)
