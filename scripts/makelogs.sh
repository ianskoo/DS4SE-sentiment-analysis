#!/bin/bash
# Script to iterate over a .txt file of github links (first argument), clone the repositories in the links,
# fetch the commit log and write it to a CSV file.

file=$1
links=`cat $file`
mkdir commit_logs

for i in $links; do

	git clone $i

	# Parse name of repository from link	
	name=${i##*/}

	cd $name
	git log --pretty=format:'%h,%an,%ai,%s' > ../commit_logs/$name'.csv'
	cd ..
	rm -fr $name
done

