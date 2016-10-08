import sys, socket
import psutil

def getHostName():
	return socket.gethostname()

psutil.cpu_percent()  # initialize so the first call returns useful data
def getCPUPercent():
	return psutil.cpu_percent(percpu=True)

def getCPUCount():
	return psutil.cpu_count()

def getRAMMax():
	return psutil.virtual_memory().total

def getRamAvail():
	return psutil.virtual_memory.available

def getRamPercent():
	return psutil.virtual_memory.percent

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
