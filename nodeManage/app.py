from flask import Flask, request
app = Flask(__name__)

@app.route('/topology')
def topo_map():
	'''
	returns a list of connection objects
	{ 'source': 'ip', 'dest': 'ip',
	  'link_type': 'eth / wifi', 'link_cost': 1.4}
	'''
	pass

@app.route('/configure', methods=['POST'])
def configure_nodes():
	'''
	systems sould be an ip, with an associated username and password
	{'127.0.0.1': {'username': 'test', 'password': 'testing'}}
	'''
	new_options = request.form['options']
	systems = request.form['systems']
