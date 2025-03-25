from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserCrimeReport
import datetime
from .forms import CrimeReportForm
from django.shortcuts import render, get_object_or_404, redirect
# Part of Day Function
def part_of_day():
    present_time = datetime.datetime.now().hour
    if present_time < 12:
        return 'Good morning, have a nice day'
    elif present_time < 16:
        return 'Good afternoon'
    elif present_time <= 18:
        return 'Good evening'
    else:
        return 'Good night'

# Home View
@login_required
def home(request):
    if request.user.is_staff:
        return staff_home(request)

    # Fetch reports submitted by the logged-in user
    user_reports = UserCrimeReport.objects.filter(user=request.user)

    return render(request, 'usr_home_pg.html', {
        'username': request.user.username,
        'tm': part_of_day(),
        'user_reports': user_reports,  # Pass reports to the template
    })


# Staff Home (Admin View)
@login_required
def staff_home(request):
    # Fetch crime reports from the database
    if not request.user.is_staff:
        return redirect('/')
    
    crime_reports = UserCrimeReport.objects.all()

    # Statistics calculation
    total_crimes = crime_reports.count()
    pending_reports = crime_reports.filter(status="Pending").count()
    under_investigation = crime_reports.filter(status="In Progress").count()
    resolved_cases = crime_reports.filter(status="Resolved").count()

    context = {
        "crime_reports": crime_reports,
        "total_crimes": total_crimes,
        "pending_reports": pending_reports,
        "under_investigation": under_investigation,
        "resolved_cases": resolved_cases,
    }

    return render(request, "admin_home.html", context)

from .forms import CrimeReportForm

# Crime Reporting Page
@login_required
def crime_reporting(request):
    if request.method == 'POST':
        form = CrimeReportForm(request.POST)
        if form.is_valid():
            crime_report = form.save(commit=False)
            crime_report.user = request.user  # Assign the logged-in user
            crime_report.status = 'Pending'  # Default status
            crime_report.save()
            messages.success(request, "Crime report submitted successfully!")
            return redirect('/report-crime')
        else:
            print(form.errors)  # 🔴 Debugging: Print errors to console
            messages.error(request, "All fields are required!")

    form = CrimeReportForm()
    return render(request, 'reporting.html', {'form': form})



# View Crime Report
@login_required
def view_report(request, report_id):
    report = get_object_or_404(UserCrimeReport, id=report_id)
    return render(request, 'view_report.html', {'report': report,'isSuperUser':request.user.is_staff})

# Update Crime Report
@login_required
def update_report(request, report_id):
    if not request.user.is_staff:
        return redirect('/')
    report = get_object_or_404(UserCrimeReport, id=report_id)

    if request.method == 'POST':
        report.status = request.POST.get('status', report.status)
        report.admin_notes = request.POST.get('adminNotes', report.admin_notes)
        report.save()
        messages.success(request, "Report updated successfully!")
        return redirect('admin_dashboard')

    return render(request, 'update_status.html', {'report': report})

# Logout
@login_required
def logout_user(request):
    auth_logout(request)
    return redirect(reverse('login'))

# Login View (Renamed to Avoid Conflict)
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Incorrect username or password')
            return redirect(reverse('login'))
    
    if request.user.is_authenticated:
        return redirect('/')
    
    return render(request, 'login.html')

# Sign Up (Register)
def sign_up(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('firstname', '').strip()
        last_name = request.POST.get('lastname', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        if not (email and first_name and last_name and username and password and confirm_password):
            messages.error(request, "All fields are required!")
            return redirect(reverse('register')) 

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect(reverse('register'))

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken!")
            return redirect(reverse('register'))

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already used!")
            return redirect(reverse('register'))

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect(reverse('login'))

    if request.user.is_authenticated:
        return redirect('/')

    return render(request, 'signin.html')

# Test View
def test_view(request):
    return render(request, 'welcome.html')
