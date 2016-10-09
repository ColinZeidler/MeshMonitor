#! /bin/bash

sudo apt install python-pip
sudo apt install python-dev

echo "Installing pysnmp"
`/usr/bin/pip -q install pysnmp` && echo "pysnmp installed"

if [ "$1" == "Manager" ]; then
	echo "Installing flask"
	`/usr/bin/pip -q install flask` && echo "flask installed"
fi
