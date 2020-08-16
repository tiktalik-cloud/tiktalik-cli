"""Module tiktalik_cli.command.command"""
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

import sys
from tiktalik.computing import ComputingConnection
from tiktalik.loadbalancer import LoadBalancerConnection
from .. import auth


class CommandError(Exception):
    """Command threw an error"""


class CommandAborted(Exception):
    """Command aborted"""


class Command:
    """Basic command"""

    def __init__(self, args, keyid, secret, connection_cls):
        self.args = args
        if connection_cls is not None:
            self.conn = connection_cls(keyid, secret)

    @classmethod
    def add_parser(cls, parser, subparser):
        """Parse command's args"""
        return None

    @classmethod
    def get_cmd_group_name(cls):
        """Return command group"""
        return "General commands"

    def execute(self):
        """Not implemented"""
        raise NotImplementedError()

    def yesno(self, message, abort=True):
        """Listen for a yes/no answers"""
        print(message)

        answer = None
        while answer not in ("yes", "no"):
            answer = input("Please answer 'yes' or 'no' > ")

        if answer == "yes":
            return True

        if abort:
            print("Aborted")
            sys.exit(1)
        else:
            return False

class GeneralCommand(Command):
    def __init__(self, args, keyid, secret):
        super(GeneralCommand, self).__init__(args, keyid, secret, None)


class ComputingCommand(Command):
    def __init__(self, args, keyid, secret):
        super(ComputingCommand, self).__init__(args, keyid, secret, ComputingConnection)

    @classmethod
    def get_cmd_group_name(cls):
        return "Computing commands"


class ComputingImageCommand(ComputingCommand):
    @classmethod
    def get_cmd_group_name(cls):
        return "Computing image commands"


class ComputingNetworkCommand(ComputingCommand):
    @classmethod
    def get_cmd_group_name(cls):
        return "Computing network commands"


class LoadBalancerCommand(Command):
    def __init__(self, args, keyid, secret):
        super(LoadBalancerCommand, self).__init__(
            args, keyid, secret, LoadBalancerConnection
        )

    @classmethod
    def get_cmd_group_name(cls):
        return "Load balancer commands"
