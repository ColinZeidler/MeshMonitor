from readSysList import getSystems
from htmlParsing import FormDefaultParser
import requests, json

WEB_PORT = 8080
JSON_PORT = 9090
UNAME = 'admin'
PWORD = 'rzeidler'

def createDistMap(systems):
	"""
	takes an array for system ips
	returns a map of hop distance and ips
	{3: ['10.1.1.1', '10.1.2.1'],
	2: ['10.2.1.2']}
	"""
	distMap = {}
	jsonurl = "http://localhost:{port}".format(port=JSON_PORT)
	r = requests.get(jsonurl)
	r.raise_for_status()

	j = json.loads(r.text)['routes']
	for node in j:
		if node['destination'] in systems:
			try:
				distMap[node['metric']].append(node['destination'])
			except KeyError:
				distMap[node['metric']] = node['destination']
			print "{ip} is {dist} hops away".format(ip=node['destination'], dist=node['metric'])

	if 'localhost' in systems or '127.0.0.1' in systems:
		distMap[0] = 'localhost'
	
	return distMap


class NodeConnection(object):
	def __init__(self, ip):
		self.ip = ip
		self.session = requests.Session()

		self.loginurl = "http://{ip}:{port}/hsmm-pi/users/login".format(ip=self.ip, port=WEB_PORT)
		self.rebooturl = "http://{ip}:{port}/hsmm-pi/system".format(ip=self.ip, port=WEB_PORT)
		self.settingsurl = "http://{ip}:{port}/hsmm-pi/network_settings/edit/1".format(ip=self.ip, port=WEB_PORT)

	def login(self, username, password):
		data = {"data[User][username]": username,
                "data[User][password]": password}
		r = self.session.post(self.loginurl, data = data)

		r.raise_for_status()
		print "Logged into {ip} successfully".format(ip=self.ip)

	def updateSettings(self, newSettingMap):
		# read old settings
		parser = FormDefaultParser()
		r = self.session.get(self.settingsurl)
		r.raise_for_status()

		parser.feed(r.text)
		default_settings = parser.form_defaults_map

		# apply changes 
		default_settings.update(newSettingMap)
		# post in settings
		r = self.session.post(self.settingsurl, data = default_settings)
		r.raise_for_status()
		print "Successfully updated settings"

	def writeDefaultSettings(self, filename):
		r = self.session.get(self.settingsurl)
		r.raise_for_status()

		parser = FormDefaultParser()
		parser.feed(r.text)
		jdata = json.dumps(parser.form_defaults_map)

		with open(filename, "w") as f:
			f.write(jdata)

	def reboot():
		r = self.session.get(self.rebooturl)

		r.raise_for_status()
		print "Reboot request successful, system will reboot in 2 minutes"


if __name__ == "__main__":
	systems = getSystems()

	systems = createDistMap(systems)
	dist = max(systems.keys())
	print systems
	while dist >= 0:
		try:
			for sys in systems[dist]:
				node = NodeConnection(sys)
				node.login(UNAME, PWORD)
				node.writeDefaultSettings("defaults.json")
				newSettings = {}
				#node.updateSettings(newSettings)
				#node.reboot()
		except KeyError:
			print "No systems {dist} hops away".format(dist=dist)
		dist -= 1
