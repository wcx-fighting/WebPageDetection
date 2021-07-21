from django.http import HttpResponse,request
from django.shortcuts import render, redirect
from django.db.models import *
import datetime
from .models import User,DetictionList,RiskUrl,Company,KeyWords,Task
from .tasks import WriteDetictionList
from django.core.paginator import Paginator
from functools import wraps
def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get("is_login")=="1":
             return f(request,*arg,**kwargs)
        else:
             return redirect("/WebMonitoring")
    return inner
# Create your views here.
def user_login(request):
    if request.method=="GET":
        return render(request,"login.html")
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        try:
           user=User.objects.get(username=username)
           if user.username==username and user.password==password and user.judge==True:
               request.session["is_login"]="1"
               request.session["user_name"] = user.username
               return redirect("index/")
           else:
               error="用户名或密码错误!"
               return render(request,"login.html",{"error":error})
        except Exception as ex:
           print("用户不存在，{}".format(ex))
           error="用户不存在!"
           return render(request,"login.html",{"error":error})
@check_login
def index(request):
    try:
         detictionList=DetictionList.objects.aggregate(num=Count(id))
         riskurl=RiskUrl.objects.aggregate(num=Count(id))
         supervisionunit1=Company.objects.values("company_name").distinct().count()
         supervisionunit2 = Company.objects.aggregate(num=Count(id))
         ChangeWebpage=RiskUrl.objects.filter(type=1).count()
         domainhijacking=RiskUrl.objects.filter(type=2).count()
         Darkchain=RiskUrl.objects.filter(type=3).count()
         Sensitiveinformation=RiskUrl.objects.filter(type=4).count()
         return render(request,"index.html",{"Testwebsite":detictionList["num"],"Dangerouswebsites":riskurl["num"],
         "Supervisionunit":supervisionunit1,"Monitoringassets":supervisionunit2["num"],"ChangeWebpage":ChangeWebpage,"domainhijacking":domainhijacking
         ,"Darkchain":Darkchain,"Sensitiveinformation":Sensitiveinformation})
    except Exception as ex:
         print("错误提示:{}".format(ex))
         return render(request, "index.html", {"Testwebsite": detictionList["num"], "Dangerouswebsites": riskurl["num"],
                                          "Supervisionunit": supervisionunit1,
                                          "Monitoringassets": supervisionunit2["num"], "ChangeWebpage": ChangeWebpage,
                                          "domainhijacking": domainhijacking
        , "Darkchain": Darkchain, "Sensitiveinformation": Sensitiveinformation})
@check_login
def taskexcute(request):
    if request.method=="GET":
       return render(request,"taskexcute.html")
    if request.method=="POST":
        taskname=request.POST.get("taskname")
        taskurl=request.POST.get("taskurl")
        taskdatetime=datetime.datetime.now()
        try:
             taskcheck=Task.objects.get(taskname=taskname)
             Tips = "任务名称重复!"
             return render(request, "taskexcute.html", {"Tips":Tips})
        except Exception as ex:
             print(ex)
        try:
            task=Task.objects.create(taskname=taskname,tasktime=taskdatetime,taskstatus="正在检测")
        except Exception as ex:
            Tips="添加任务错误!"
            print(ex)
            return render(request,"taskexcute.html",{"Tips":Tips})
        WriteDetictionList.apply_async(args=[taskurl,taskname])
        Tips="添加任务成功!"
        return render(request,"taskexcute.html",{"Tips":Tips})
@check_login
def taskmanage(request):
        page_num = request.GET.get('page', 1)
        all_data = Task.objects.all()
        paginator = Paginator(all_data, 20)
        c_page = paginator.page(int(page_num))
        #print(all_data)
        return render(request, "taskmanage.html",locals())
@check_login
def addkeyword(request):
        if request.method=="GET":
                ID1 = request.GET.get("id")
                if ID1 is not None:
                    try:
                        id_key = KeyWords.objects.get(id=ID1)
                        id_key.delete()
                        return redirect("http://127.0.0.1:8080/WebMonitoring/addkeyword/")
                    except Exception as ex:
                        print("删除错误!{}".format(ex))
                        return redirect("http://127.0.0.1:8080/WebMonitoring/addkeyword/")
                page_num = request.GET.get('page', 1)
                all_data = KeyWords.objects.all()
                paginator = Paginator(all_data, 11)
                c_page = paginator.page(int(page_num))
                return render(request, "addkeyword.html",locals())
        if request.method=="POST":
                if request.POST.get("add") is not None:
                    keyword=request.POST.get("keywords")
                    try:
                        key=KeyWords.objects.create(keywords=keyword)
                        return redirect("http://127.0.0.1:8080/WebMonitoring/addkeyword/")
                    except Exception as ex:
                        print("添加错误!{}".format(ex))
                        return redirect("http://127.0.0.1:8080/WebMonitoring/addkeyword/")
#资产管理
@check_login
def assetmanage(request):
    if request.method == "GET":
        ID1 = request.GET.get("id")
        company_name=request.GET.get("company")
        if ID1 is not None and request.GET.get("company") is  None:
            try:
                id_conpamy = Company.objects.get(id=ID1)
                id_conpamy.delete()
                return redirect("http://127.0.0.1:8080/WebMonitoring/assetmanage/")
            except Exception as ex:
                print("删除错误!{}".format(ex))
                return redirect("http://127.0.0.1:8080/WebMonitoring/assetmanage/")
        if ID1 is not None and request.GET.get("company") is not None:
             company=Company.objects.get(id=ID1)
             return redirect("http://127.0.0.1:8080/WebMonitoring/editasset/?id={}&company={}".format(company.id,company.company_name))
        page_num = request.GET.get('page', 1)
        all_data =Company.objects.all()
        paginator = Paginator(all_data, 11)
        c_page = paginator.page(int(page_num))
        return render(request, "assetmanage.html", locals())
    if request.method == "POST":
            companyName = request.POST.get("company")
            website=request.POST.get("website")
            try:
                key = Company.objects.create(company_name=companyName,assets=website)
                return redirect("http://127.0.0.1:8080/WebMonitoring/assetmanage/")
            except Exception as ex:
                print("添加错误!{}".format(ex))
                return redirect("http://127.0.0.1:8080/WebMonitoring/assetmanage/")
#对资产进行编辑操作
@check_login
def editasset(request):
    global id
    if request.method=="GET":
           id= request.GET.get("id")
           company=Company.objects.get(id=id)
           return render(request,"editasset.html",{"company_name":company.company_name,"website":company.assets})
    if request.method=="POST":
           company_name1 = request.POST.get("company")
           website = request.POST.get("website")
           if company_name1 is not None and website is not None:
                try:
                       company = Company.objects.get(id=id)
                       company.company_name = company_name1
                       company.assets = website
                       company.save()
                       return render(request, "editasset.html", {"Tips": "更改成功!", "company_name": company.company_name, "website": company.assets})
                except Exception as ex:
                        print(ex)
                        return render(request, "editasset.html",{"Tips": "更改错误!", "company_name": company.company_name, "website": company.assets})
           else:
               return render(request, "editasset.html", {"Tips": "字段不能为空!", "company_name":company_name1, "website":website})
#发现的安全事件展示
@check_login
def safeevent(request):
    page_num = request.GET.get('page', 1)
    all_data = RiskUrl.objects.all()
    paginator = Paginator(all_data, 15)
    c_page = paginator.page(int(page_num))
    # print(all_data)
    return render(request, "safeevent.html", locals())



