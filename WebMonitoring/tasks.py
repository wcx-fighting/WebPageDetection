from WebpageDetection.celery import app
from celery import shared_task
from celery.schedules import crontab
from django.contrib.auth.models import User
from .models import User,DetictionList,RiskUrl,Company,Task,KeyWords,Task
from .MonitoringEngine import getip,ExcuteMonitoring
import datetime
import os
@shared_task()
def WriteDetictionList(urls,taskname):
    CheckUrls=[]
    storge=urls.split("\r\n")
    for url in storge:
       ip = getip(url)
       if ip=="":
           continue
       createtime = datetime.datetime.now()
       try:
         detictionList = DetictionList.objects.create(url=url, ip=ip, createtime=createtime, uid_id=1)
       except Exception as ex:
          print("存储数据错误!")
          print(ex)
       CheckUrls.append(url)
    ExcuteMonitoring(CheckUrls,taskname)
    task=Task.objects.get(taskname=taskname)
    task.taskfinshtime = datetime.datetime.now()
    task.save()
    return CheckUrls
