import sys, socket
import psutil

def getHostName():
	return socket.gethostname()

psutil.cpu_percent()  # initialize so the first call returns useful data
def getCPUPercent():
	a = psutil.cpu_percent(percpu=True)
	cpus = [int(x*100) for x in a]
	return cpus

def getCPUCount():
	return psutil.cpu_count()

def getRAMMax():
	return psutil.virtual_memory().total

def getRAMAvail():
	return psutil.virtual_memory().available

def getRAMPercent():
	return (psutil.virtual_memory().percent) * 100

def getByteSent():
	a = psutil.net_io_counters(pernic=True)
	b = {}
	for nic in a:
		b[nic] = a[nic].bytes_sent
	return b

def getByteRecv():
	a = psutil.net_io_counters(pernic=True)
	b = {}
	for nic in a:
		b[nic] = a[nic].bytes_recv
	return b

def getNicCount():
	return len(psutil.net_io_counters(pernic=True))
