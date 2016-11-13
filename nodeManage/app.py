from flask import Flask, request, render_template
from nodeMapping import createDistMap, createTopologyMap
import json
app = Flask(__name__)


@app.route('/nodes')
def node_list():
	'''
	returns a list of node objects:
	{'id': 'ip','name': 'hostname'}
	'''
	olsr_host_f = "/var/run/hosts_olsr"

	nodes = []
	with open(olsr_host_f, 'r') as f:
		for line in f:
			item = {}
			line = line.strip()
			line = line.split("#")[0]
			if line != '':
				line = line.split()
				if line[1] != 'localhost':
					item['id'] = line[0]
					item['name'] = line[1]
					nodes.append(item)

	return json.dumps(nodes)

@app.route('/topology')
def topo_map():
	'''
	returns a list of connection objects
	{'source': 'ip', 'target': 'ip'}
	'''
	return json.dumps(createTopologyMap())


@app.route('/configure', methods=['POST'])
def configure_nodes():
	'''
	systems sould be an ip, with an associated username and password
	{'127.0.0.1': {'username': 'test', 'password': 'testing'}}
	'''
	new_options = request.form['options']
	systems_d = request.form['systems']

	systems = systems_d.keys()

	systems = createDistMap(systems)
	dist = max (systems.keys())
	while dist >= 0:
		try:
			for sys in systems[dist]:
				node = NodeConnection(sys)
				node.login(systems_d[sys]['username'], systems_d[sys][password])
				node.updateSettings(new_options)
				node.reboot()
				# TODO handle connection errors
		except KeyError:
			# no need to do anything
			pass
		dist -= 1
	return "success"


@app.route('/')
def index_page():
	return render_template("index.html")


if __name__ == "__main__":
	app.run('0.0.0.0')
