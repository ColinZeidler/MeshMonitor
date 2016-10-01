# MeshMonitor
SNMP based performance monitor for HSMM-Pi based mesh netowrk

## Libraries in use
 * pysmp
  * used to create the SNMP Agents and SNMP Manager
 * flask
  * provides the rest api for accessing data from SNMP Agents

### Installing
 * Ubuntu / Debian
  * sudo apt-get install gcc python-dev python-pip
  * pip install pysnmp flask psutil
