#! /usr/bin/bash

source ../../pygame/env/bin/activate
if [[ $# -gt 1 ]]
then
	echo "Usage: ./start.sh [script_name]"
	exit
elif [[ $# -eq 0 ]]
then
	script=forstart.py
else
	script=$1
fi

if [[ !( -f $script ) ]]
then
	echo "The file '$script' does not exist or is not a regular file"
	exit
fi
python3 $script
