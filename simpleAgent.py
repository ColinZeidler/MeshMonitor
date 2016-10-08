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
    udp.UdpTransport().openServerMode(('127.0.0.1', 161))
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

class CPUPercent(MibScalarInstance):
	def getValue(self, name, idx):
		cpus = perffunctions.getCPUPercent()
		s = ""
		for x in range(perffunctions.getCPUCount()):
			s += "CPU_{} {},".format(x, cpus[x])
		if name[-1] == 3:
			s = cpus[0]
		return self.getSyntax().clone(
			s
		)



mibBuilder.exportSymbols(
    '__MY_MIB', MibScalar((1, 3, 6, 5, 1), v2c.OctetString()),
    HostName((1, 3, 6, 5, 1), (1,), v2c.OctetString()),
	CPUPercent((1, 3, 6, 5, 1), (2,), v2c.OctetString()),
	CPUPercent((1, 3, 6, 5, 1), (3,), v2c.Integer())
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
