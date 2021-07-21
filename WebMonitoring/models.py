from django.db import models
import datetime
# Create your models here.
class User(models.Model):
    username=models.CharField("用户名",unique=True,max_length=50)
    password=models.CharField("密码",max_length=30)
    createtime=models.DateTimeField("用户创建时间",default=datetime.datetime.now())
    judge=models.BooleanField("判断用户状态",default=True)
    class Meta:
        verbose_name="用户列表"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.username
class  DetictionList(models.Model):
    url=models.CharField("网址",max_length=100)
    ip=models.CharField("IP",default="",max_length=200)
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    createtime = models.DateTimeField("创建时间", default=datetime.datetime.now())
    class Meta:
        verbose_name="网址列表"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.url
class RiskUrl(models.Model):
    domainname=models.CharField("域名",max_length=200)
    url=models.CharField("危险URL",max_length=100)
    ip=models.CharField("IP",default="",max_length=200)
    keywords = models.CharField("敏感词",default="",max_length=100)
    type = models.IntegerField("危险类型", max_length=2)
    createtime = models.DateTimeField("创建时间", default=datetime.datetime.now())
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        verbose_name="安全事件"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.url
class KeyWords(models.Model):
    keywords=models.CharField("敏感词",max_length=100)
    class Meta:
        verbose_name="敏感词"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.keywords
class Company(models.Model):
    company_name=models.CharField("公司名称",max_length=200)
    assets=models.CharField("资产",max_length=100)
    class Meta:
        verbose_name="监管单位"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.company_name
class Task(models.Model):
    taskname=models.CharField("任务名称",max_length=200)
    tasktime=models.DateTimeField("创建时间", default=datetime.datetime.now())
    taskfinshtime=models.DateTimeField("完成时间", default=datetime.datetime.now())
    taskstatus=models.CharField("任务状态",max_length=200)
    class Meta:
        verbose_name="任务"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.taskname
