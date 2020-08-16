"""Module tiktalik_cli.command.network"""
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

from .command import ComputingNetworkCommand


class ListNetworks(ComputingNetworkCommand):
    @classmethod
    def add_parser(cls, parent, subparser):
        subparser.add_parser(
            "list-networks",
            description="List all available networks.",
            parents=[parent],
        )
        return "list-networks"

    def execute(self):
        networks = self.conn.list_networks()
        for net in networks:
            print(
                (
                    "%s %s %s %s, owned by %s"
                    % (
                        net.name,
                        net.uuid,
                        net.net,
                        "public" if net.public else "private",
                        net.owner,
                    )
                )
            )


class CreateNetwork(ComputingNetworkCommand):
    @classmethod
    def add_parser(cls, parent, subparser):
        p = subparser.add_parser(
            "create-network", description="Create a new network.", parents=[parent]
        )
        p.add_argument("name", help="Network name - as part of local domain.")

        return "create-network"

    def execute(self):
        network = self.conn.create_network(self.args.name)
        print(
            (
                "%s %s %s %s, owned by %s"
                % (
                    network.name,
                    network.uuid,
                    network.net,
                    "public" if network.public else "private",
                    network.owner,
                )
            )
        )
