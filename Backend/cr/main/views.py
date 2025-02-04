from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserReports
import datetime
from time import strftime
# Create your views here.

@login_required
def home(request):
	user =  request.user
	if(user.is_staff): return staffHome(request)
	name = user.username
	return render(request,'usr_home_pg.html',{'username':name,'tm':part_of_day()})

@login_required
def crimeReporting(request):
	crimeList = ["Violent crime","Kidnapping","Theft","Sexual assault","Drug offences","Fraud","Other"]

	return render(request,'reporting.html',{'crimeLis':crimeList})

@login_required
def saveReport(request):
	if(request.method == 'POST'):
		type = request.POST['type_of_report']
		disc = request.POST['dis']
		newReport = UserReports(title=type,dis=disc)
		newReport.save()
		#just testing
		return HttpResponse("<h1>REPORTED</h1>")
	
	return HttpResponseRedirect("report-form")

@login_required
def logout(request):
        auth.logout(request)
        return redirect('login')

def part_of_day():
	present_time = int(datetime.datetime.now().strftime ("%H"))
	if present_time >= 0 and present_time <= 12:
		return 'good morning,have a nice day'
	elif present_time > 12 and present_time < 16:
		return 'good afternoon' 
	elif present_time >= 16 and present_time <=18:
		return 'good evening'
	else:
		return 'good night'
	
@login_required
def staffHome(request):
	items = UserReports.objects.all()
	return render(request,'todo.html',{'content':items})


def testview(request):
	return render(request,'welcome.html')

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			if user.is_authenticated:
				return redirect('/')
		else:
			messages.info(request,'Incorrect password or username') 
			return redirect('/') 		
	else:
		user = request.user
		if user.is_authenticated:
			return redirect('/')
		else:
			return render(request,'login.html')
		
def signin(request):
	if request.method == 'POST':
		email = request.POST['email']
		first_name = request.POST['firstname']
		last_name = request.POST['lastname']
		username = request.POST['username']
		password = request.POST['password']
		conform_password = request.POST['conform_password']
		if password == conform_password:
			if User.objects.filter(username=username).exists():
				messages.info(request,'Username is already taken')
				return redirect('register')
			elif User.objects.filter(email=email).exists():
				messages.info(request,'Email is already used')
				return redirect('register')
			else:
				user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
				user.save()
		else:
			messages.info(request,'password doesnot match')
			return redirect('register')
		return redirect('login')
	
	else:
		user = request.user
		if user.is_authenticated:
			return redirect('/')
		else:
			return render(request,'signin.html')