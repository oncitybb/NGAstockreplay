#!/bin/bash
if python3 -c "import psutil" >/dev/null 2>&1 && python3 -c "import requests" >/dev/null 2>&1
then
    PYTHON3ADDRESS=$(which python3)
else
    echo "没有Python3安装，自动安装"
    sudo apt-get update >> /dev/null 2>&1 && sudo apt-get install python3 python3-pip -y >> /dev/null 2>&1
    pip3 install requests psutil >> /dev/null 2>&1
    if python3 -c "import psutil" >/dev/null 2>&1 && python3 -c "import requests" >/dev/null 2>&1
    then
        PYTHON3ADDRESS=$(which python3)
    else
        echo "安装python3失败"
        echo "建议自行安装"
        echo "sudo apt-get update && sudo apt-get install python3 python3-pip"
        echo "pip3 install requests psutil"
        exit 0
    fi
fi
FOLDER=$(dirname $(readlink -f "$0"))
PYTHON_FILE_NUMBER=$(find -name "*.sh" | wc -l)
PYTHONFILE=$(find -name "*.sh")
findpython = $(ps aux|grep "gp.py" |grep -v "grep"|wc -l)
if [$findpython -eq 0]
then
    if [$PYTHON_FILE_NUMBER -ne 1]
    then
        echo "开启软件"
        nohup $PYTHON3ADDRESS -u $FOLDER/$PYTHONFILE > $FOLDER/tuisong.log 2>&1 &
        findpython = $(ps aux|grep "gp.py" |grep -v "grep"|wc -l)
        if [$findpython -eq 1]
        then
            echo "开启成功"
        else
            echo "开启失败"
        fi     
    else
        if [$PYTHON_FILE_NUMBER -eq 0]
        then
            echo “运行脚本文件夹里没有python文件,自动下载python文件到当前文件夹”
            wget -P $FOLDER https://raw.githubusercontent.com/oncitybb/NGAstockreplay/master/gupiaorun.sh
            PYTHON_FILE_NUMBER=$(find -name "*.sh" | wc -l)
            if [$PYTHON_FILE_NUMBE -eq 1]
            then
                echo "下载成功，请修改python文件后再次开启"
            else
                echo "下载失败，请手动测试"
                echo "wget https://raw.githubusercontent.com/oncitybb/NGAstockreplay/master/gupiaorun.sh"
            fi


        else
            echo “运行脚本文件夹里有多个python文件”
        fi
     fi
else
    echo "这破软件开着"
    echo `ps aux|grep "gp.py" |grep -v "grep"`
fi
