from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
	user =  request.user
	name = user.username
	return HttpResponse(f"hello {name}")

@login_required
def logout(request):
        auth.logout(request)
        return redirect('login')

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