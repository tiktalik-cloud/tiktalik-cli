from .command import Command

class ListNetworks(Command):
	@classmethod
	def add_parser(cls, parent, subparser):
		subparser.add_parser("list-networks", description="List all available networks.", parents=[parent])
		return "list-networks"

	def execute(self):
		networks = self.conn.list_networks()
		for net in networks:
			print "%s %s %s %s, owned by %s" % (net.name, net.uuid, net.net, "public" if net.public else "private", net.owner)
