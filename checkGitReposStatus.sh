#!/bin/sh

CLEAN="nothing to commit, working tree clean"

for repo in $(ls -A);do
    if [ -d ${repo} ];then
	echo --
        echo "Repository => ${repo}"
        cd ${repo}
        git status | grep "${CLEAN}" > /dev/null 2>&1
	if [ $? == 0 ];then
	    echo Clear!
        else
	    git status
	fi
        cd ..
    fi
done
