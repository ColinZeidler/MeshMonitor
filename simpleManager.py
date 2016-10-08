from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
	getCmd(
		SnmpEngine(),
		CommunityData('public'),
		UdpTransportTarget(('localhost', 161)),
		ContextData(),
		ObjectType(ObjectIdentity('1.3.6.5.1.1')),
		ObjectType(ObjectIdentity('1.3.6.5.1.2.2')),
		ObjectType(ObjectIdentity('1.3.6.5.1.3.3')),
		ObjectType(ObjectIdentity('1.3.6.5.1.4.2')),
		ObjectType(ObjectIdentity('1.3.6.5.1.4.3'))
	)
)

if errorIndication:
	print errorIndication
elif errorStatus:
	print errorStatus
else:
	for varBind in varBinds:
		print ' = '.join([x.prettyPrint() for x in varBind])
