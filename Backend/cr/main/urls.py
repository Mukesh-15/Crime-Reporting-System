from django.urls import path
from .views import *

urlpatterns=[
    path('home',testview,name="home"),
    path('login',login,name="login"),
    path('logout',logout,name="logout"),
    path('register',signin,name='register'),
    path('report-form',crimeReporting,name="crime reporting"),
    path('Submit-crime',saveReport,name="save report"),
    path('',home,name="user_home"),
    ]