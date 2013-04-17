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

from tiktalik.loadbalancer.http import *
from tiktalik.error import TiktalikAPIError

from .command import HTTPBalancerCommand, CommandError
from . import util

def validate_backend(ip, port, weight):
	import socket

	if port is not None:
		port = int(port)
		if port <= 0 or port >= 65536:
			raise ValueError()

	if weight is not None:
		if int(weight) <= 0:
			raise ValueError()

	if ip is not None:
		socket.inet_aton(ip)
		if ip.count(".") != 3:
			raise ValueError()

class ListHTTPBalancers(HTTPBalancerCommand):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("list-http-balancers", description="List HTTP Balancers", parents=[parser])
		p.add_argument("-v", action="store_true", dest="verbose", help="Verbose output")

		return "list-http-balancers"

	def execute(self):
		balancers = HTTPBalancer.list_all(self.conn, history=self.args.verbose)
		if not self.args.verbose:
			self._print_short(balancers)
		else:
			map(util.print_http_balancer, balancers)
	
	def _print_short(self, balancers):
		for b in balancers:
			print "%s  %s (%s) domains: %s, backends: %s" % (b.name, b.uuid, "enabled" if b.enabled else "disabled",
				", ".join(b.domains) if b.domains else "none",
				", ".join("%s:%i (w=%i)" % (i.ip, i.port, i.weight) for i in b.backends) if b.backends else "none")

class CreateHTTPBalancer(HTTPBalancerCommand):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("create-http-balancer", description="Create a new HTTP Balancer", parents=[parser])
		p.add_argument("name", help="Name assigned to this HTTP Balancer.")
		p.add_argument("-d", dest="domains", metavar="DOMAIN", action="append", default=[],
			help="Add domains to the HTTP Balancer configuration.")
		p.add_argument("-b", dest="backends", metavar="BACKEND", action="append", default=[],
			help="Add backends to the HTTP Balancer configuration. Pass backends using this format: IP:PORT:WEIGHT")

		return "create-http-balancer"

	def execute(self):
		name = self.args.name.decode(sys.stdin.encoding)
		backends = []
		# Roughly validate input
		for b in self.args.backends:
			try:
				ip, port, weight = b.split(":")
				validate_backend(ip, port, weight)
				backends.append((ip, int(port), int(weight)))
			except ValueError:
				raise CommandError("Invalid backend specified. Please use the IP:PORT:WEIGHT format")

		balancer = HTTPBalancer.create(self.conn, name,
			[d.decode(sys.stdin.encoding) for d in self.args.domains], backends)
		util.print_http_balancer(balancer)


class HTTPBalancerCommand(HTTPBalancerCommand):
	@classmethod
	def add_common_arguments(cls, parser):
		parser.add_argument("name", help="HTTPBalancer name.")

	def _wb_by_name(self, name, history=False):
		L = filter(lambda x: x.name == name, HTTPBalancer.list_all(self.conn, history=history))
		if len(L) == 1:
			return L[0]
		elif len(L) == 0:
			raise CommandError("HTTPBalancer %s not found" % name)
		else:
			raise CommandError("More than one balancer named '%s' found, what do?!")


class ViewHTTPBalancer(HTTPBalancerCommand):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("view-http-balancer", description="View HTTPBalancer information", parents=[parser])
		HTTPBalancerCommand.add_common_arguments(p)
		return "view-http-balancer"

	def execute(self):
		balancer = self._wb_by_name(self.args.name, history=True)
		util.print_http_balancer(balancer)


class RemoveHTTPBalancer(HTTPBalancerCommand):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("rm-http-balancer", description="Remove a HTTPBalancer", parents=[parser])
		HTTPBalancerCommand.add_common_arguments(p)
		return "rm-http-balancer"

	def execute(self):
		balancer = self._wb_by_name(self.args.name)
		balancer.delete()


class DisableHTTPBalancer(HTTPBalancerCommand):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("disable-http-balancer", description="Temporarily disable a HTTP Balancer", parents=[parser])
		HTTPBalancerCommand.add_common_arguments(p)
		
		return "disable-http-balancer"

	def execute(self):
		self._wb_by_name(self.args.name).disable()


class EnableHTTPBalancer(HTTPBalancerCommand):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("enable-http-balancer", description="Enable a HTTPBalancer", parents=[parser])
		HTTPBalancerCommand.add_common_arguments(p)
		
		return "enable-http-balancer"

	def execute(self):
		self._wb_by_name(self.args.name).enable()


class RenameHTTPBalancer(HTTPBalancerCommand):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("rename-http-balancer", description="Enable a HTTPBalancer", parents=[parser])
		HTTPBalancerCommand.add_common_arguments(p)
		p.add_argument("new_name", help="New name")
		
		return "rename-http-balancer"

	def execute(self):
		self._wb_by_name(self.args.name).rename(self.args.new_name)


class RemoveHTTPBalancerDomain(HTTPBalancerCommand):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("rm-http-balancer-domain", description="Remove a domain from a HTTPBalancer's list", parents=[parser])
		HTTPBalancerCommand.add_common_arguments(p)
		p.add_argument("domain", help="Domain to remove")

		return "rm-http-balancer-domain"

	def execute(self):
		balancer = self._wb_by_name(self.args.name)
		domain = self.args.domain.decode(sys.stdin.encoding)
		balancer.remove_domain(domain)


class AddHTTPBalancerDomain(HTTPBalancerCommand):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("add-http-balancer-domain", description="Add a domain to a HTTPBalancer's list", parents=[parser])
		HTTPBalancerCommand.add_common_arguments(p)
		p.add_argument("domain", help="Domain to add")

		return "add-http-balancer-domain"

	def execute(self):
		balancer = self._wb_by_name(self.args.name)
		domain = self.args.domain.decode(sys.stdin.encoding)
		if domain in balancer.domains:
			raise CommandError("Domain '%s' already exists" % self.args.domain)

		balancer.add_domain(self.args.domain)


class AddHTTPBalancerBackend(HTTPBalancerCommand):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("add-http-balancer-backend", description="Add a backend to a HTTPBalancer's list", parents=[parser])
		HTTPBalancerCommand.add_common_arguments(p)

		p.add_argument("ip", help="Backend IP address")
		p.add_argument("port", type=int, help="Backend port")
		p.add_argument("weight", type=int, default=10, help="Backend's weight value")

		return "add-http-balancer-backend"

	def execute(self):
		try:
			validate_backend(self.args.ip, self.args.port, self.args.weight)
		except ValueError:
			raise CommandError("Invalid backend parameters specified")

		balancer = self._wb_by_name(self.args.name)
		balancer.add_backend(self.args.ip, self.args.port, self.args.weight)


class RemoveHTTPBalancerBackend(HTTPBalancerCommand):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("rm-http-balancer-backend", description="Remove a backend from a HTTPBalancer's list", parents=[parser])
		HTTPBalancerCommand.add_common_arguments(p)
		p.add_argument("uuid", help="Backend UUID")

		return "rm-http-balancer-backend"

	def execute(self):
		balancer = self._wb_by_name(self.args.name)
		if not filter(lambda b: b.uuid == self.args.uuid, balancer.backends):
			raise CommandError("No such backend")
		balancer.remove_backend(self.args.uuid)

class ModifyHTTPBalancerBackend(HTTPBalancerCommand):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("modify-http-balancer-backend", description="Modify a HTTPBalancer's backend", parents=[parser])
		HTTPBalancerCommand.add_common_arguments(p)
		p.add_argument("uuid", help="Backend UUID")
		p.add_argument("-i", dest="ip", help="Change the IP address")
		p.add_argument("-p", dest="port", type=int, help="Change the port")
		p.add_argument("-w", dest="weight", type=int, help="Change the weight value")

		return "modify-http-balancer-backend"

	def execute(self):
		if not self.args.ip and not self.args.port and not self.args.weight:
			raise CommandError("Nothing to do. Please supply parameters that you want to modify.")

		balancer = self._wb_by_name(self.args.name)
		for backend in balancer.backends:
			if backend.uuid == self.args.uuid:
				break
		else:
			raise CommandError("No such backend")

		try:
			validate_backend(self.args.ip, self.args.port, self.args.weight)
		except ValueError as e:
			raise CommandError("Invalid parameters")

		balancer.modify_backend(self.args.uuid, ip=self.args.ip, port=self.args.port, weight=self.args.weight)

