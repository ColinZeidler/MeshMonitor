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
