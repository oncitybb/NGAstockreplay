import urllib.request
import re
from time import sleep
import requests
from datetime import datetime, time
import psutil
import os

DAY_START = time(8, 30)
DAY_END = time(16, 00)

pushqiao = 0
pushhe = 0
pushniu = 0
qiaonewmessage = 'Start Running'
henewmessage = 'Start Running'
niunewmessage = 'Start Running'
qiaobangzhu = 'https://ngabbs.com/thread.php?searchpost=1&authorid=60002731' #乔帮主的回复页面
heda = 'https://ngabbs.com/thread.php?searchpost=1&authorid=5254815' #禾戈的回复页面
niu = 'https://ngabbs.com/thread.php?searchpost=1&authorid=4627122' #牛大的回复页面

def catchnew(url): 
    newmessage = 'Start Running'
    # 设定header
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Host': 'ngabbs.com',
            'Connection':'keep-alive',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            #填入自己NGA登陆后的cookies，否则无法查看他人回复
            'cookie':'填入自己NGA登陆后的cookies，否则无法查看他人回复'
    }
    # 获取url的回复，然后把得到的所有回复过滤后return出去
    while True:
        try:
            req = urllib.request.Request(url,headers=headers)
            html = urllib.request.urlopen(req, timeout=10).read().decode('gb18030')
            item = re.findall(r'id=\'postcontent\d+_\d+\'>(.*?)<\/span><\/div><\/div>', html,re.S)
            break
        except urllib.error.URLError as e:
            print('获得新消息的路上出现问题，正在重试，请等待3秒')
            if hasattr(e,"code"):
                print('reason: ',e.code)
            if hasattr(e,"reason"):
                print('reason: ',e.reason)
            sleep(3)
        except:
            print('蜜汁错误 -- 获得新消息的路上出现问题，请等待3秒')
            sleep(3)
    sleep(0.5)
    return item

def pushmessage(message, urll):

    # 把进来的html代码进行过滤然后修成推送的文字
    pushme = re.sub(r'</?\w+[^>]*>','',message)
    pushme = pushme.replace("[/quote]","\n大佬回复： ")
    pushme = re.sub(r'\[.*?\]','',pushme)
    pushme = re.sub(r'(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})','',pushme)
    pushme = pushme.replace("()",'这位小伙咨询')
    pushme = pushme.replace("Reply Post by ",'')
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    #填入自己在wxpusher的uid
    uids='输入wxpusher的uid' 
    #填入自己在wxpusher的token
    token = '输入wxpusher的token'
    url = 'https://wxpusher.zjiecode.com/api/send/message/?appToken=' + token + '&content=' + pushme + '&uid=' + uids + '&url=' + urll
    sleep(0.1)
    # 推送文字到wxpusher
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=20).text
            break
        except requests.exceptions.ConnectionError:
            print('ConnectionError -- 推送新消息的路上出现问题，请等待3秒')
            sleep(3)
        except requests.exceptions.ChunkedEncodingError:
            print('ChunkedEncodingError -- 推送新消息的路上出现问题，请等待3秒')
            sleep(3)  
        except:
            print('蜜汁错误 -- 推送新消息的路上出现问题，请等待3秒')
            sleep(3)
    sleep(0.5)

def core():
    global qiaonewmessage
    global henewmessage
    global niunewmessage
    global pushqiao
    global pushhe
    global pushniu
    #获取乔帮主的发言，取最新的4条消息进行推送,若是喜欢可以外加，从此处开始
    itemlistx = catchnew(qiaobangzhu)
    for i in range(4):
        #从第一条开始，检测是否和之前保存的最新发言有重复，有重复的话直接退出推送
        if itemlistx[i] == qiaonewmessage:
            break
        else:
            pushqiao += 1
            print('在' + datetime.now().strftime("%X") + ' push乔帮主一条新消息，今天总共push了'+str(pushqiao)+'条乔帮主的消息')
            pushmessage('乔帮主 : ' + '\n' +itemlistx[i], qiaobangzhu)
    #保存好乔帮主的最新发言
    qiaonewmessage = itemlistx[0]
    #结束乔帮主。这为一个循环。
    itemlistx = catchnew(heda)
    for i in range(4):
        if itemlistx[i] == henewmessage:
            break
        else:
            pushhe += 1
            print('在' + datetime.now().strftime("%X") + ' push禾戈一条新消息，今天总共push了'+str(pushhe)+'条禾戈的消息')
            pushmessage('禾戈 : ' + '\n' +itemlistx[i], heda)
    henewmessage = itemlistx[0]
    itemlistx = catchnew(niu)
    for i in range(4):
        if itemlistx[i] == niunewmessage:
            break
        else:
            pushniu += 1
            print('在' + datetime.now().strftime("%X") + ' push牛神一条新消息，今天总共push了'+str(pushniu)+'条牛神的消息')
            pushmessage('牛神 : ' + '\n' +itemlistx[i], niu)
    niunewmessage = itemlistx[0]
    #最后推送占用内存和时间。
    print(datetime.now().strftime("%X") + ' 三位大神检测成功 ' + u'当前进程的内存使用：%.1f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024) )

if __name__ == '__main__':
    running = False
    while True:
        current_time = datetime.now().time()
        #检测现在是否工作时间，第一个是检测时间是否在开启区间，第二个是检测是否工作日。如果开始工作会推送一条开机的推送，清零当天推送数量。每30秒运作一次
        if (DAY_START <= current_time <= DAY_END) and (datetime.now().weekday() <=4 ):
            if not running:
                pushmessage('开工！','https://www.google.com')
                print("开机")
                running = True
                pushqiao = 0
                pushhe = 0
                pushniu = 0
            core()
            sleep(15)
        else:
            #如果刚结束运行会推送一条下班的推送。每30分钟推送一次，可以检测软件是否运行。
            if running:
                pushmessage('下班！','https://www.google.com')
                print("下班")
                running = False
            print("现在是周"+ str((datetime.now().weekday() + 1)) +"的" + str(current_time.hour) +"点" + current_time.strftime("%M") + "分, 程序运作ing, " + u'当前进程的内存使用：%.1f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024) )
            sleep(1800)
