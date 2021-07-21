import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import socket
from .models import User,DetictionList,RiskUrl,Company,Task,KeyWords,Task
import datetime
import string
import os, time

def WriteDatabase(domainname,url,type,uid_id,ip,keywords,crttime):
    try:
        record=RiskUrl.objects.create(domainname=domainname,url=url,type=type,uid_id=uid_id,ip=ip,keywords=keywords,createtime=crttime)
    except:
        print("log error!")


def ReadWeb(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) compatible Baiduspider Googlebot Sogou  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except:
        try:
            response = requests.get(url, headers=headers, timeout=5)
        except:
            return ''
        else:
            try:
                response.encoding = response.apparent_encoding
            except:
                pass
            return response.text
    else:
        try:
            response.encoding = response.apparent_encoding
        except:
            pass
        return response.text

def getip(url):
    ip = ''
    try:
        ip = socket.gethostbyname(url)
    except:
        try:
            ip = socket.gethostbyname(url)
        except:
            return ''
    finally:
        return ip

def GetTitle(url):
    if url.find('http') == -1:
        url = 'http://' + url
    domain = urlparse(url).netloc
    if domain.find(':') > -1:
        domain = domain.split(':')[0]
    ip = getip(domain)
    if ip == '':
        #print(domain + ' connect error!')
        #WriteLog(domain + ' connect error!')
        return
    webdata = ReadWeb(url)
    if webdata == '':
        print(url + " requests error!")
    webdata = webdata.replace('|', '')
    webdata = webdata.replace('\r', '')
    webdata = webdata.replace('\n', '')
    try:
        if webdata.find("indax.htm") > -1:
            keywords="have indax.htm"
            WriteDatabase(url,url,1,1,ip,keywords)
        if webdata.find("/t.cn/") > -1:
            keywords="have t.cn!!!!"
            WriteDatabase(url, url, 1, 1, ip, keywords)
    except:
        pass
    try:
        #解析网站标题
        soup = BeautifulSoup(webdata, 'html.parser')
        title = ''
        keywords = ''
        hackwords=KeyWords.objects.values("keywords")
        try:
            #获取网站标题
            title = soup.find('title').get_text()
        except:
            pass
        try:
            #获取第一个属性名name 值是keywords的标签的内容值
            keywords = soup.find(attrs={"name": "keywords"})['content']
        except:
            pass
    except:
        print(url + " soup error!")
    else:
        webinfo = url + '\t' + ip + '\t' + title + '\t' + keywords
        print(webinfo)
        webinfo1=str(webinfo)
        for i in hackwords:
            if title.find(i["keywords"])!=-1:
                webinfo_new = webinfo1 + "\t关键词匹配为:{}".format(i)
                try:
                    riskurl1 = RiskUrl.objects.get(url=url)
                    print("记录已经存在")
                    continue
                except Exception as ex:
                    print(webinfo_new)
                    ctime = datetime.datetime.now()
                    WriteDatabase(title, url, 1, 1, ip, i["keywords"], ctime)
                    break
            elif keywords.find(i["keywords"])!=-1:
                webinfo_new=webinfo1+"\t关键词匹配为:{}".format(i)
                try:
                    riskurl1=RiskUrl.objects.get(url=url)
                    print("记录已经存在")
                    continue
                except Exception as ex:
                    print(webinfo_new)
                    ctime=datetime.datetime.now()
                    WriteDatabase(title, url, 1, 1, ip,i["keywords"],ctime)
                    break
            else:
                continue
def ExcuteMonitoring(urls,taskname):
    for url in urls:
              GetTitle(url)
    task=Task.objects.get(taskname=taskname)
    task.taskstatus="已完成"
    task.save()
