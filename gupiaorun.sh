#!/bin/bash
findpython = $(ps aux|grep "gp.py" |grep -v "grep"|wc -l)
if [$findpython -eq 0]
then
    nohup /usr/bin/python3 -u /home/ubuntu/gupiao/gp.py > /home/ubuntu/gupiao/tuisong.log 2>&1 &
    echo "开启软件"
else
    echo "这破软件开着"
    echo `ps aux|grep "gp.py" |grep -v "grep"`
fi
