#!/bin/bash
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
findpython = $(ps aux|grep "gp.py" |grep -v "grep"|wc -l)
if [$findpython -eq 0]
then
    nohup /usr/bin/python3 -u $SHELL_FOLDER/gp.py > $SHELL_FOLDER/tuisong.log 2>&1 &
    echo "开启软件"
else
    echo "这破软件开着"
    echo `ps aux|grep "gp.py" |grep -v "grep"`
fi
