"""Module tiktalik_cli.command.loadbalancer"""
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

from tiktalik.loadbalancer import *
from tiktalik.error import TiktalikAPIError

from .command import LoadBalancerCommand, CommandError
from . import util


def validate_backend(ip, port, weight):
    import socket

    if port is not None:
        port = int(port)
        if port <= 0 or port >= 65536:
            raise ValueError("Port number must be between 1-65535")

    if weight is not None:
        if int(weight) < 0:
            raise ValueError("Weight must be positive or zero to suspend.")

    if ip is not None:
        socket.inet_aton(ip)
        if ip.count(".") != 3:
            raise ValueError("Invalid IPv4 address")


class ListLoadBalancers(LoadBalancerCommand):
    @classmethod
    def add_parser(cls, parser, subparser):
        p = subparser.add_parser(
            "list-load-balancers", description="List Load Balancers", parents=[parser]
        )
        p.add_argument("-v", action="store_true", dest="verbose", help="Verbose output")

        return "list-load-balancers"

    def execute(self):
        balancers = LoadBalancer.list_all(self.conn, history=self.args.verbose)
        if not self.args.verbose:
            self._print_short(balancers)
        else:
            list(map(util.print_load_balancer, balancers))

    def _print_short(self, balancers):
        for b in balancers:
            print(
                (
                    "%s  %s (%s) %s at %s:%d, backends: %s"
                    % (
                        b.name,
                        b.uuid,
                        b.status,
                        b.type,
                        "..." + b.address[b.address.rfind("-") :],
                        b.port,
                        ", ".join(
                            "%s:%i (w=%i)" % (i.ip, i.port, i.weight)
                            for i in b.backends
                        )
                        if b.backends
                        else "none",
                    )
                )
            )


class CreateLoadBalancer(LoadBalancerCommand):
    @classmethod
    def add_parser(cls, parser, subparser):
        p = subparser.add_parser(
            "create-load-balancer",
            description="Create a new Load Balancer",
            parents=[parser],
        )
        p.add_argument("name", help="Name assigned to this Load Balancer.")
        p.add_argument(
            "proto", help='Type of Load Balancer, one of "TCP", "HTTP" or "HTTPS".'
        )
        p.add_argument(
            "-a",
            dest="address",
            metavar="ADDRESS",
            action="store",
            default=None,
            help="Optional entry point to use, if not set then new entry point will be created.",
        )
        p.add_argument(
            "-p",
            dest="port",
            metavar="PORT",
            action="store",
            type=int,
            default=None,
            help="Listen port, only for TCP proto balancing.",
        )
        p.add_argument(
            "-b",
            dest="backends",
            metavar="BACKEND",
            action="append",
            default=[],
            help="Add backends to the Load Balancer configuration. Pass backends using this format: IP:PORT:WEIGHT",
        )
        p.add_argument(
            "-d",
            dest="domains",
            metavar="DOMAIN",
            action="append",
            default=[],
            help="Add domains to the HTTP proto Load Balancer.",
        )

        return "create-load-balancer"

    def execute(self):
        name = self.args.name
        backends = []

        # Roughly validate input
        for b in self.args.backends:
            try:
                ip, port, weight = b.split(":")
            except:
                raise CommandError(
                    "Invalid backend specified. Please use the IP:PORT:WEIGHT format"
                )
            try:
                validate_backend(ip, port, weight)
                backends.append((ip, int(port), int(weight)))
            except ValueError as e:
                raise CommandError(
                    "Invalid backend specified."
                    + {"": ""}.get(e.message, " " + e.message)
                )
        if not backends:
            raise CommandError("Need at least one backend specified")
        if self.args.proto not in ["TCP", "HTTP", "HTTPS"]:
            raise CommandError("Invalid balancer type")

        # still developing
        if self.args.proto == "HTTPS":
            raise CommandError("HTTPS Balancer not supported yet")

        kwargs = {"backends": backends}
        if self.args.address:
            kwargs["address"] = self.args.address
        if self.args.port:
            kwargs["port"] = self.args.port
        if self.args.domains:
            kwargs["domains"] = [
                d.decode(sys.stdin.encoding) for d in self.args.domains
            ]

        balancer = LoadBalancer.create(self.conn, name, self.args.proto, **kwargs)
        util.print_load_balancer(balancer)


class LoadBalancerCommand(LoadBalancerCommand):
    @classmethod
    def add_common_arguments(cls, parser):
        parser.add_argument("name", help="Load Balancer name.")

    def _wb_by_name(self, name, history=False):
        L = [
            x
            for x in LoadBalancer.list_all(self.conn, history=history)
            if x.name == name
        ]
        if len(L) == 1:
            return L[0]
        elif len(L) == 0:
            raise CommandError("Load Balancer %s not found" % name)
        else:
            raise CommandError("More than one balancer named '%s' found, what do?!")


class ViewLoadBalancer(LoadBalancerCommand):
    @classmethod
    def add_parser(cls, parser, subparser):
        p = subparser.add_parser(
            "view-load-balancer",
            description="View Load Balancer information",
            parents=[parser],
        )
        LoadBalancerCommand.add_common_arguments(p)
        return "view-load-balancer"

    def execute(self):
        balancer = self._wb_by_name(self.args.name, history=True)
        util.print_load_balancer(balancer)


class RemoveLoadBalancer(LoadBalancerCommand):
    @classmethod
    def add_parser(cls, parser, subparser):
        p = subparser.add_parser(
            "rm-load-balancer", description="Remove a Load Balancer", parents=[parser]
        )
        LoadBalancerCommand.add_common_arguments(p)
        return "rm-load-balancer"

    def execute(self):
        balancer = self._wb_by_name(self.args.name)
        balancer.delete()


class DisableLoadBalancer(LoadBalancerCommand):
    @classmethod
    def add_parser(cls, parser, subparser):
        p = subparser.add_parser(
            "disable-load-balancer",
            description="Temporarily disable a Load Balancer",
            parents=[parser],
        )
        LoadBalancerCommand.add_common_arguments(p)

        return "disable-load-balancer"

    def execute(self):
        self._wb_by_name(self.args.name).disable()


class EnableLoadBalancer(LoadBalancerCommand):
    @classmethod
    def add_parser(cls, parser, subparser):
        p = subparser.add_parser(
            "enable-load-balancer",
            description="Enable a Load Balancer",
            parents=[parser],
        )
        LoadBalancerCommand.add_common_arguments(p)

        return "enable-load-balancer"

    def execute(self):
        self._wb_by_name(self.args.name).enable()


class RenameLoadBalancer(LoadBalancerCommand):
    @classmethod
    def add_parser(cls, parser, subparser):
        p = subparser.add_parser(
            "rename-load-balancer",
            description="Enable a Load Balancer",
            parents=[parser],
        )
        LoadBalancerCommand.add_common_arguments(p)
        p.add_argument("new_name", help="New name")

        return "rename-load-balancer"

    def execute(self):
        self._wb_by_name(self.args.name).rename(self.args.new_name)


class RemoveLoadBalancerDomain(LoadBalancerCommand):
    @classmethod
    def add_parser(cls, parser, subparser):
        p = subparser.add_parser(
            "rm-load-balancer-domain",
            description="Remove a domain from a HTTP Balancer's domain list",
            parents=[parser],
        )
        LoadBalancerCommand.add_common_arguments(p)
        p.add_argument("domain", help="Domain to remove")

        return "rm-load-balancer-domain"

    def execute(self):
        balancer = self._wb_by_name(self.args.name)
        domain = self.args.domain
        balancer.remove_domain(domain)


class AddLoadBalancerDomain(LoadBalancerCommand):
    @classmethod
    def add_parser(cls, parser, subparser):
        p = subparser.add_parser(
            "add-load-balancer-domain",
            description="Add a domain to a HTTP Balancer's domain list",
            parents=[parser],
        )
        LoadBalancerCommand.add_common_arguments(p)
        p.add_argument("domain", help="Domain to add")

        return "add-load-balancer-domain"

    def execute(self):
        balancer = self._wb_by_name(self.args.name)
        domain = self.args.domain
        if domain in balancer.domains:
            raise CommandError("Domain '%s' already exists" % self.args.domain)

        balancer.add_domain(self.args.domain)


class AddLoadBalancerBackend(LoadBalancerCommand):
    @classmethod
    def add_parser(cls, parser, subparser):
        p = subparser.add_parser(
            "add-load-balancer-backend",
            description="Add a backend to a Load Balancer's backend list",
            parents=[parser],
        )
        LoadBalancerCommand.add_common_arguments(p)

        p.add_argument("ip", help="Backend IP address")
        p.add_argument("port", type=int, help="Backend port")
        p.add_argument("weight", type=int, default=10, help="Backend's weight value")

        return "add-load-balancer-backend"

    def execute(self):
        try:
            validate_backend(self.args.ip, self.args.port, self.args.weight)
        except ValueError as e:
            raise CommandError(
                "Invalid backend specified." + {"": ""}.get(e.message, " " + e.message)
            )

        balancer = self._wb_by_name(self.args.name)
        balancer.add_backend(self.args.ip, self.args.port, self.args.weight)


class RemoveLoadBalancerBackend(LoadBalancerCommand):
    @classmethod
    def add_parser(cls, parser, subparser):
        p = subparser.add_parser(
            "rm-load-balancer-backend",
            description="Remove a backend from a Load Balancer's backend list",
            parents=[parser],
        )
        LoadBalancerCommand.add_common_arguments(p)
        p.add_argument("uuid", help="Backend UUID")

        return "rm-load-balancer-backend"

    def execute(self):
        balancer = self._wb_by_name(self.args.name)
        if not [b for b in balancer.backends if b.uuid == self.args.uuid]:
            raise CommandError("No such backend")
        balancer.remove_backend(self.args.uuid)


class ModifyLoadBalancerBackend(LoadBalancerCommand):
    @classmethod
    def add_parser(cls, parser, subparser):
        p = subparser.add_parser(
            "modify-load-balancer-backend",
            description="Modify a Load Balancer's backend",
            parents=[parser],
        )
        LoadBalancerCommand.add_common_arguments(p)
        p.add_argument("uuid", help="Backend UUID")
        p.add_argument("-i", dest="ip", help="Change the IP address")
        p.add_argument("-p", dest="port", type=int, help="Change the port")
        p.add_argument("-w", dest="weight", type=int, help="Change the weight value")

        return "modify-load-balancer-backend"

    def execute(self):
        if not self.args.ip and not self.args.port and self.args.weight == None:
            raise CommandError(
                "Nothing to do. Please supply parameters that you want to modify."
            )

        balancer = self._wb_by_name(self.args.name)
        for backend in balancer.backends:
            if backend.uuid == self.args.uuid:
                break
        else:
            raise CommandError("No such backend")

        try:
            validate_backend(self.args.ip, self.args.port, self.args.weight)
        except ValueError as e:
            raise CommandError(
                "Invalid parameters" + {"": ""}.get(e.message, ". " + e.message)
            )

        balancer.modify_backend(
            self.args.uuid,
            ip=self.args.ip,
            port=self.args.port,
            weight=self.args.weight,
        )
