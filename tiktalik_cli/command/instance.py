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

from tiktalik.computing.objects import Instance
from tiktalik.error import TiktalikAPIError

from .command import ComputingCommand, CommandError
from . import util

class ListInstances(ComputingCommand):
	@classmethod
	def add_parser(cls, parser, subparser):
		p = subparser.add_parser("list", description="List instances", parents=[parser])
		p.add_argument("-a", action="store_true", dest="actions",
			help="Fetch recent actions for each instance")
		p.add_argument("-c", action="store_true", dest="cost",
			help="Fetch current hourly cost for each instance")
		p.add_argument("-i", action="store_true", dest="vpsimage",
			help="Fetch VPS Image details for each instance")
		p.add_argument("-v", dest="verbose", action="store_true",
			help="Print extra information (flags -a, -i, -t yield more details)")

		return "list"

	def execute(self):
		instances = Instance.list_all(self.conn, actions=self.args.actions,
				cost=self.args.cost, vpsimage=self.args.vpsimage)
		# instances = self.conn.list_instances(actions=self.args.actions, cost=self.args.cost, vpsimage=self.args.vpsimage)
		if not self.args.verbose:
			self._print_short(instances)
		else:
			map(util.print_instance, instances)

	def _print_short(self, instances):
		for instance in instances:
			print "%s  %s %s" % (instance.hostname, instance.uuid, "Running" if instance.running else "Not running")


class CreateInstance(ComputingCommand):
	@classmethod
	def add_parser(cls, parent, subparser):
		p = subparser.add_parser("create-instance", description="Create a new instance.", parents=[parent])
		p.add_argument("image_uuid", help="UUID of a VPS Image that should be used.")
		p.add_argument("size", help='Instance size (in units). Allowed values: 0.25, 0.5, 1 - 15, "cpuhog", "cpuhog4".')
		p.add_argument("hostname", help="Hostname set at installation time.")
		p.add_argument("-n", dest="networks", metavar="NETWORK_NAME", action="append",
			help="Attach these networks to the new instance. Use the list-networks command to list available networks.")
		p.add_argument("-b", dest="batch_mode", action="store_true", help="Batch mode. Don't confirm the operation.")

		return "create-instance"

	def execute(self):
		if not self.args.networks:
			raise CommandError("You must specify at least one network")

		networks = self.conn.list_networks()

		# Mapping of network names->uuids
		networks = dict((net.name, net.uuid) for net in networks)

		# Make sure all networks exist
		diff = set(self.args.networks) - set(networks.keys())
		if diff:
			raise CommandError("Some of the networks you specified don't exist: %s" % ", ".join(diff))

		# List of network uuids instead of names
		networks = [networks[n] for n in self.args.networks]

		# Validate image existence
		try:
			self.conn.get_image(self.args.image_uuid)
		except TiktalikAPIError as ex:
			if ex.http_status == 404:
				raise CommandError("Image %s not found" % self.args.image_uuid)

		size = self._parse_instance_size(self.args.size)

		if not self.args.batch_mode:
			self.yesno(
				"Creating new instance with these parameters:\n"
				"Image UUID: %s\nSize: %s\nHostname: %s\nNetworks: %s\n"
				"Is this OK?" % (self.args.image_uuid, size, self.args.hostname,
					", ".join(self.args.networks)))

		response = self.conn.create_instance(self.args.hostname, size, self.args.image_uuid, networks)

		print "Instance", self.args.hostname, "is now being installed."

	def _parse_instance_size(self, sz):
		"""
		Parse instance size passed as string and validate it.
		Valid values are: 0.25, 0.5, integers 1-15, "cpuhog", "cpuhog4"
		Raise CommandError if `sz` is not a valid size.
		"""

		if sz in ("cpuhog", "cpuhog4"):
			return sz

		try:
			sz = float(sz)
			if sz < 1:
				if sz <= 0 or sz not in (0.25, 0.5):
					sz = None
			else:
				sz = int(sz)
				if sz > 15:
					sz = None
		except ValueError:
			sz = None

		if sz is None:
			raise CommandError('Size must be 0.25, 0.5, integral value 1-15 or "cpuhog".')

		return sz


class InstanceCommand(ComputingCommand):
	"""
	Base class for commands that operate on existing instances, eg. start, stop, info.
	"""

	@classmethod
	def add_common_arguments(cls, parser):
		parser.add_argument("-n", dest="hostname", help="Instance hostname. Use -u if it is not unique.")
		parser.add_argument("-u", dest="uuid", help="Instance UUID, can be specified instead of name.")

	def _instance_from_args(self, actions=False, vpsimage=False, cost=False):
		if self.args.hostname and self.args.uuid:
			raise CommandError("Both hostname and UUID can't be specified. Decide on one!")
		if not self.args.hostname and not self.args.uuid:
			raise CommandError("Either hostname or UUID must be provided.")

		try:
			if self.args.hostname:
				instances = Instance.get_by_hostname(self.conn, self.args.hostname,
						actions, vpsimage, cost)
				if len(instances) > 1:
					msg = ", ".join(i.uuid for i in instances)
					raise CommandError("There are %s instances matching hostname %s: %s"
							% (len(instances), self.args.hostname, msg))

				instance = instances[0]
			else:
				instance = Instance.get_by_uuid(self.conn, self.args.uuid,
						actions, vpsimage, cost)

			return instance
		except TiktalikAPIError as ex:
			if ex.http_status == 404:
				raise CommandError("No such instance.")
			raise


class StartInstance(InstanceCommand):
	@classmethod
	def add_parser(cls, parent, subparser):
		p = subparser.add_parser("start", description="Start an instance. Either name or UUID must be specified.", 
				parents=[parent])
		InstanceCommand.add_common_arguments(p)
		return "start"

	def execute(self):
		instance = self._instance_from_args()
		instance.start()
		print "Instance %s (%s) is now being started" % (instance.hostname, instance.uuid)


class StopInstance(InstanceCommand):
	@classmethod
	def add_parser(cls, parent, subparser):
		p = subparser.add_parser("stop", description="Stop an instance. Either name or UUID must be specified.", 
				parents=[parent])
		InstanceCommand.add_common_arguments(p)
		p.add_argument("-f", dest="force", action="store_true", help="Stop the instance forcefuly.")

		return "stop"

	def execute(self):
		instance = self._instance_from_args()

		if self.args.force:
			instance.force_stop()
		else:
			instance.stop()

		print "Instance %s (%s) is now being stopped%s" \
			% (instance.hostname, instance.uuid, " forcefuly" if self.args.force else "")


class BackupInstance(InstanceCommand):
	@classmethod
	def add_parser(cls, parent, subparser):
		p = subparser.add_parser("backup", description="Backup an instance. Either name or UUID must be specified.", 
				parents=[parent])
		InstanceCommand.add_common_arguments(p)
		return "backup"

	def execute(self):
		instance = self._instance_from_args()
		if instance.running:
			raise CommandError("Instance is running. Please stop it before starting backup.")

		instance.backup()
		print "Instance %s (%s) is now being backed up" % (instance.hostname, instance.uuid)


class InstanceInfo(InstanceCommand):
	@classmethod
	def add_parser(cls, parent, subparser):
		p = subparser.add_parser("info", description="Display instance information.", parents=[parent])
		InstanceCommand.add_common_arguments(p)
		return "info"

	def execute(self):
		instance = self._instance_from_args(actions=True, vpsimage=True, cost=True)
		util.print_instance(instance)


class AddInterface(InstanceCommand):
	@classmethod
	def add_parser(cls, parent, subparser):
		p = subparser.add_parser("add-interface", description="Add a new interface to an instance.", parents=[parent])
		p.add_argument("network_uuid", help="UUID of a Network that should be attached to this interface")
		p.add_argument("seq", help="Seq number of the interface, eg. 2 maps to eth2")
		InstanceCommand.add_common_arguments(p)

		return "add-interface"

	def execute(self):
		instance = self._instance_from_args()
		instance.add_interface(self.args.network_uuid, self.args.seq)

