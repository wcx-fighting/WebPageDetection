from django.urls import path,include
from WebMonitoring import views

urlpatterns = [
    path('',views.user_login),
    path('index/',views.index),
    path('taskexcute/',views.taskexcute),
    path('taskmanage/',views.taskmanage),
    path('addkeyword/', views.addkeyword),
    path('assetmanage/', views.assetmanage),
    path('safeevent/', views.safeevent),
]
