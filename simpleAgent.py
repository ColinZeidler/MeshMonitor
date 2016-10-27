import sys, socket
import psutil
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.proto.api import v2c

import perffunctions


# Create SNMP engine
snmpEngine = engine.SnmpEngine()

# Transport setup

# UDP over IPv4
config.addTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('0.0.0.0', 161))
)

# SNMPv2c setup

# SecurityName <-> CommunityName mapping.
config.addV1System(snmpEngine, 'my-area', 'public')

# Allow read MIB access for this user / securityModels at VACM
config.addVacmUser(snmpEngine, 2, 'my-area', 'noAuthNoPriv', (1, 3, 6, 5))

# Create an SNMP context
snmpContext = context.SnmpContext(snmpEngine)

# --- create custom Managed Object Instance ---

mibBuilder = snmpContext.getMibInstrum().getMibBuilder()

MibScalar, MibScalarInstance = mibBuilder.importSymbols(
    'SNMPv2-SMI', 'MibScalar', 'MibScalarInstance'
)


class HostName(MibScalarInstance):
	def getValue(self, name, idx):
		return self.getSyntax().clone(
			socket.gethostname()
		)

class CPUStats(MibScalarInstance):
	def getValue(self, name, idx):
		s = ""
		if name == (1, 3, 6, 5, 1, 2):
			s = "CPU Count(1) and Usage(2)"
		if name[-2] == 2:
			if name[-1] == 1:
			# CPU Count
				s = perffunctions.getCPUCount()
			elif name[-1] == 2:
			# CPU usage
				cpus = perffunctions.getCPUPercent()
				for x in range(perffunctions.getCPUCount()):
					s += "CPU_{} {},".format(x, cpus[x])
		return self.getSyntax().clone(
			s
		)

class RAMStats(MibScalarInstance):
	def getValue(self, name, idx):
		s = ""
		if name == (1, 3, 6, 5, 1, 3):
			s = "RAM Total(1), Available(2), and Usage(3)"
		if name[-2] == 3:
			if name[-1] == 1:
			# Ram Total
				s = perffunctions.getRAMMax() / 1024
			elif name[-1] == 2:
			# Ram Available
				s = perffunctions.getRAMAvail() / 1024
			elif name[-1] == 3:
			# Ram Usage
				s = perffunctions.getRAMPercent()
		return self.getSyntax().clone(
			s
		)

class NetStats(MibScalarInstance):
	def getValue(self, name, idx):
		s = ""
		if name == (1, 3, 6, 5, 1, 4):
			s = "Nic Count(1), Nic Upload(2), and Nic Download(3)"
		elif name[-2] == 4:
			if name[-1] == 1:
			# NIC Count
				s = perffunctions.getNicCount()
			elif name[-1] == 2:
			# Per nic upload count
				up = perffunctions.getByteSent()
				for nic in up:
					s += "if_{} {},".format(nic, up[nic])
			elif name[-1] == 3:
			# Per nic download count
				down = perffunctions.getByteSent()
				for nic in down:
					s += "if_{} {},".format(nic, down[nic])
		return self.getSyntax().clone(
			s
		)

class MeshInfo(MibScalarInstance):
    def getValue(self, name, idx):
        s = ""
        if name == (1, 3, 6, 5, 1, 0, 0):
            s = "AREDNDev"
        elif name[-2] == 0:
            if name[-1] == 1:
                s = "v3.16.1.0"
            elif name[-1] == 2:
                s = 0
            elif name[-1] == 3:
                s = "45 18'N"
            elif name[-1] == 4:
                s = "75 39'W"
            elif name[-1] == 5: # Antenna model
                s = "Internal Raspberry Pi 3 wifi antenna"
            elif name[-1] == 6: # Antenna type
                s = 4
            elif name[-1] == 7: # antenna polarity unknown
                s = 2
            elif name[-1] == 8: # antenna gain unknown
                s = 0
            elif name[-1] == 9: # antenna tilt
                s = 0
            elif name[-1] == 10: # antenna beam Hwidth
                s = 360
            elif name[-1] == 11: # antenna beam Vwidth
                s = 180
            elif name[-1] == 12: # antenna direction
                s = 0
            elif name[-1] == 13: # power source
                s = 1
            elif name[-1] == 14: # power runtime
                s = 0
            elif name[-1] == 15: # power recharge
                s = 0
            
        return self.getSyntax().clone(
            s
        )


mibBuilder.exportSymbols(
    '__MY_MIB', MibScalar((1, 3, 6, 5, 1), v2c.OctetString()),
    MeshInfo((1, 3, 6, 5, 1), (0, 0), v2c.OctetString()),
    MeshInfo((1, 3, 6, 5, 1), (0, 1), v2c.OctetString()),
    MeshInfo((1, 3, 6, 5, 1), (0, 2), v2c.Integer()),
    MeshInfo((1, 3, 6, 5, 1), (0, 3), v2c.OctetString()),
    MeshInfo((1, 3, 6, 5, 1), (0, 4), v2c.OctetString()),
    MeshInfo((1, 3, 6, 5, 1), (0, 5), v2c.OctetString()),
    MeshInfo((1, 3, 6, 5, 1), (0, 6), v2c.Integer()),
    MeshInfo((1, 3, 6, 5, 1), (0, 7), v2c.Integer()),
    MeshInfo((1, 3, 6, 5, 1), (0, 8), v2c.Integer()),
    MeshInfo((1, 3, 6, 5, 1), (0, 9), v2c.Integer()),
    MeshInfo((1, 3, 6, 5, 1), (0, 10), v2c.Integer()),
    MeshInfo((1, 3, 6, 5, 1), (0, 11), v2c.Integer()),
    MeshInfo((1, 3, 6, 5, 1), (0, 12), v2c.Integer()),
    MeshInfo((1, 3, 6, 5, 1), (0, 13), v2c.Integer()),
    MeshInfo((1, 3, 6, 5, 1), (0, 14), v2c.Integer()),
    MeshInfo((1, 3, 6, 5, 1), (0, 15), v2c.Integer()),
    HostName((1, 3, 6, 5, 1), (1,), v2c.OctetString()), # host name
	CPUStats((1, 3, 6, 5, 1), (2,), v2c.OctetString()), # CPU DESC
	CPUStats((1, 3, 6, 5, 1), (2, 1,), v2c.Integer()), # CPU Count
	CPUStats((1, 3, 6, 5, 1), (2, 2,), v2c.OctetString()), # Per CPU useage
	RAMStats((1, 3, 6, 5, 1), (3,), v2c.OctetString()), # RAM DESC
	RAMStats((1, 3, 6, 5, 1), (3, 1,), v2c.Integer()),
	RAMStats((1, 3, 6, 5, 1), (3, 2,), v2c.Integer()),
	RAMStats((1, 3, 6, 5, 1), (3, 3,), v2c.Integer()),
	NetStats((1, 3, 6, 5, 1), (4,), v2c.OctetString()), # NET DESC
	NetStats((1, 3, 6, 5, 1), (4, 1,), v2c.Integer()),
	NetStats((1, 3, 6, 5, 1), (4, 2,), v2c.OctetString()),
	NetStats((1, 3, 6, 5, 1), (4, 3,), v2c.OctetString())
)

# --- end of Managed Object Instance initialization ----

# Register SNMP Applications at the SNMP engine for particular SNMP context
cmdrsp.GetCommandResponder(snmpEngine, snmpContext)
cmdrsp.NextCommandResponder(snmpEngine, snmpContext)
cmdrsp.BulkCommandResponder(snmpEngine, snmpContext)

# Register an imaginary never-ending job to keep I/O dispatcher running forever
snmpEngine.transportDispatcher.jobStarted(1)

# Run I/O dispatcher which would receive queries and send responses
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
