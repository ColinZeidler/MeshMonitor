from flask import Flask, request, render_template
from nodeMapping import createDistMap, createTopologyMap
import json
app = Flask(__name__)


@app.route('/topology')
def topo_map():
	'''
	returns a list of connection objects
	{ 'source': 'ip', 'dest': 'ip'}
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
