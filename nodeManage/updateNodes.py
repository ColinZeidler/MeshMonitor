from readSysList import getSystems
import requests, json

WEB_PORT = 8080
JSON_PORT = 9090

def createDistMap(systems):
	"""
	takes an array for system ips
	returns a map of system ips and hop counts
	"""
	distMap = {}
	jsonurl = "http://localhost:{port}".format(JSON_PORT)
	r = requests.get(jsonurl)
	r.raise_for_status()

	j = json.loads(r.text)['routes']
	for node in j:
		if node['destination'] in systems:
			distMap[node['destination']] = node['metric']
			print "{ip} is {dist} hops away".format(node['destination'], node['metric'])
	
	return distMap


class NodeConnection(object):
	def __init__(self, ip):
		self.ip = ip
		self.session = requests.Session()

	def login(self, username, password):
		loginurl = "http://{ip}:{port}/hsmm-pi/users/login".format(ip=self.ip, port=WEB_PORT)
		data = {"data[User][username]": username,
                "data[User][password]": password}
		r = self.session.post(loginurl, data = data)

		r.raise_for_status()
		print "Logged into {ip} successfully".format(ip=self.ip)

	def updateSettings(self, newSettingMap):
		# read old settings
		# apply changes 
		# post in settings
		pass

	def reboot():
		rebooturl = "http://{ip}:{port}/hsmm-pi/system".format(ip=self.ip, port=WEB_PORT)
		r = self.session.get(rebooturl)

		r.raise_for_status()
		print "Reboot request successful, system will reboot in 2 minutes"


if __name__ == "__main__":
	pass
