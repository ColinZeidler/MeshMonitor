from flask import Flask

app = Flask(__name__)

@app.route("/systems/")
def system_list():
	# {'id': 1, 'ip': '10.10.10.10', 'host-name': 'Test'}
	return 'array of systems, with id, ip, and hostname'


@app.route("/systems/new", methods=['POST'])
def system_add():
	pass


@app.route("/systems/<id>/")
def all_system_stats(id):
	return 'dict of most recent system stats'
