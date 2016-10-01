import sys, socket
import psutil

class HostName(MibScalarInstance):
	def getValue(self, name, idx):
		return self.getSyntax().clone(
			socket.gethostname()
		)
