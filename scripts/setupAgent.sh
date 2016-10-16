#! /bin/bash

# manage dependencies
./libInstall.sh


# create cronjob for script if one does not exist
file="simpleAgent.py"
cd ../agent/
mydir=`pwd`
file="$mydir/$file"
echo $file
c="@reboot python2 $file"

(sudo crontab -u root -l |grep -q '$c' )|| (echo $c | sudo crontab -u root -)
