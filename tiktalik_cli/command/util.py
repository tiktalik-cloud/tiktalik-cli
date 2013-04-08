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
		print "  recent operations:"
		map(print_action, i.actions)
	
	if i.gross_cost_per_hour:
		print "  cost per hour: %.5f PLN/h" % i.gross_cost_per_hour
