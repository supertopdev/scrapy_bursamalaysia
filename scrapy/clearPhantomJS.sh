#!/bin/bash
#run the script as "sh clearPhantomJS.sh"

echo "List of all instance of PhantomJS"
echo ""
echo ""
ps -ef | grep phantom
echo "Closing all instances of PhantomJS"
pkill -f phantom
echo ""
echo ""
echo "List of all instance of PhantomJS"
ps -ef | grep phantom
