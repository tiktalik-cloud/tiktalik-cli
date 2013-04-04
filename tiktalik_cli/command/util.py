def print_iface(n):
	print "    eth%i addr: %s mac: %s network: %s" % (n.seq, n.ip, n.mac, n.network.name)

def print_action(a):
	s = "%s started at %s" % (a.description, a.start_time)
	if a.end_time:
		s += " ended at %s" % a.end_time
	else:
		s = "(In progress) " + s
	print "     " + s

def print_instance(i):
	"""
	Helper for printing instance details.
	"""

	print "%s (%s) - %s" % (i.hostname, i.uuid, "Running" if i.running else "Not running")

	if not i.interfaces:
		print "  no network interfaces"
	else:
		print "  network interfaces:"
		map(print_iface, i.interfaces)

	if i.vpsimage:
		print "  running image %s (%s)" % (i.vpsimage.name, i.vpsimage.uuid)

	if i.actions:
		print "  lastest operations:"
		map(print_action, i.actions)
	
	if i.gross_cost_per_hour:
		print "  cost per hour: %.5f PLN/h" % i.gross_cost_per_hour
