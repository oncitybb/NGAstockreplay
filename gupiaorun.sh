#!/bin/bash
if python3 -c "import $1" >/dev/null 2>&1
then
    PYTHON3ADDRESS=$(which python3)
else
    echo "没有Python3安装，自动安装"
    sudo apt-get update >> /dev/null 2>&1 && sudo apt-get install python3 python3-pip >> /dev/null 2>&1
    pip3 install requests psutil >> /dev/null 2>&1
    if python3 -c "import $1" >/dev/null 2>&1
    then
        PYTHON3ADDRESS=$(which python3)
    else
        echo "安装python3失败"
        echo "建议自行安装"
        echo "sudo apt-get update && sudo apt-get install python3 python3-pip"
        echo "pip3 install requests psutil"
        exit 0
fi
FOLDER=$(dirname $(readlink -f "$0"))
PYTHON_FILE_NUMBER=$(find -name "*.sh" | wc -l)
PYTHONFILE=$(find -name "*.sh")
findpython = $(ps aux|grep "gp.py" |grep -v "grep"|wc -l)
if [$findpython -eq 0]
then
    if [$PYTHON_FILE_NUMBER -ne 1]
    then
        nohup $PYTHON3ADDRESS -u $SHELL_FOLDER/$PYTHONFILE > $SHELL_FOLDER/tuisong.log 2>&1 &
        echo "开启软件"
    else
        if [$PYTHON_FILE_NUMBER -eq 0]
        then
            echo “运行脚本文件夹里没有python文件”
        else
            echo “运行脚本文件夹里有多个python文件”
        fi
     fi
else
    echo "这破软件开着"
    echo `ps aux|grep "gp.py" |grep -v "grep"`
fi

anzhuang
