from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-dashboard/', views.staff_home, name='admin_dashboard'),
    path('report-crime/', views.crime_reporting, name='report_crime'),
    path('view-report/<int:report_id>/', views.view_report, name='view_report'),
    path('update-report/<int:report_id>/', views.update_report, name='update_report'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.user_login, name='login'),
    path('register/', views.sign_up, name='register'),
    path('view-profile/', views.profile_view, name='profile_view'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

]
