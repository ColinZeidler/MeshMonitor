
MAX_HISTORY = 60
class Data(object):
	def __init__(self):
		systems = {}
		# systems dict of id and ips
		# {1: "127.0.0.1", 3:"10.10.10.10"}
		data_history = []
		# data history is an array of dicts, position 0 is the oldest data
		# and it gets newer towards MAX_HISTORY-1
		# [{1: {"host_name": "test", "cpu_count": 3, "cpu_use":[1.4, 0.5, 1.0]},
		# [{1: {"host_name": "test", "cpu_count": 3, "cpu_use":[8.4, 9.5, 9.0]},
		# ]
