# MeshMonitor
SNMP agent for HSMM-Pi node performance reporting

## Installing
### Ubuntu / Debian / Raspbian
 1. git clone https://github.com/ColinZeidler/MeshMonitor.git
 1. cd MeshMonitor
 1. ./scripts/setupAgent.sh  
 SNMP agent will startup automically when the system is rebooted
 
### Testing Installation
 1. sudo python2 simpleAgent.py
 1. snmpwalk -vc2 -c public localhost 1.3.6
 
This should list all of the OIDs in use and the system metrics associated with each
  
## Libraries in use
 * pysmp
  * used to create the SNMP Agents

# NodeManage
Python based tool to update settings on multiple HSMM-Pi mesh nodes at once.
Is able to update SSID and channel settings that would potentially disconnect nodes when changed, by calculating the order to access nodes so that they are only cutoff when they have already been updated.

## Usage
 1. cd to MeshMonitor/nodeManage
 1. edit systemList.txt to add the IPs of all the systems you want to update
 1. run python2 updateNodes.py
 
## Libraries in use
 * requests
  * used to interact with the HSMM-Pi web interface to update a nodes settings
