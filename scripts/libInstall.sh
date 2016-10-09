#! /bin/bash

echo "apt installing python-pip, python-dev (to compile python libraries), and gcc"

sudo apt install python-pip python-dev gcc

echo "Installing pysnmp and psutil"
`/usr/bin/pip -q install pysnmp psutil` && echo "pysnmp and psutil installed"

if [ "$1" == "Manager" ]; then
	echo "Installing flask"
	`/usr/bin/pip -q install flask` && echo "flask installed"
fi
