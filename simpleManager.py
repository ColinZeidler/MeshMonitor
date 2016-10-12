from pysnmp.hlapi import *
import sys

if len(sys.argv) < 2:
	host = 'localhost'
else:
	host = sys.argv[1]
pDesc = [
	'Host Name',
	'CPU Count',
	'CPU Use',
	'RAM Total',
	'RAM Avail',
	'RAM Use%',
	'Nic Count',
	'Send total',
	'Recv total'
]
errorIndication, errorStatus, errorIndex, varBinds = next(
	getCmd(
		SnmpEngine(),
		CommunityData('public'),
		UdpTransportTarget((host, 161)),
		ContextData(),
		ObjectType(ObjectIdentity('1.3.6.5.1.1')),
		ObjectType(ObjectIdentity('1.3.6.5.1.2.1')),
		ObjectType(ObjectIdentity('1.3.6.5.1.2.2')),
		ObjectType(ObjectIdentity('1.3.6.5.1.3.1')),
		ObjectType(ObjectIdentity('1.3.6.5.1.3.2')),
		ObjectType(ObjectIdentity('1.3.6.5.1.3.3')),
		ObjectType(ObjectIdentity('1.3.6.5.1.4.1')),
		ObjectType(ObjectIdentity('1.3.6.5.1.4.2')),
		ObjectType(ObjectIdentity('1.3.6.5.1.4.3'))
	)
)

if errorIndication:
	print errorIndication
elif errorStatus:
	print errorStatus
else:
	for i in range(len(varBinds)):
		print ' = '.join([varBinds[i][1], pDesc[i]])
