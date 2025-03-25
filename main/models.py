from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserCrimeReport(models.Model):
    CRIME_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Investigation', 'Under Investigation'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null values for existing data
    typeofCrime = models.CharField(max_length=100, verbose_name="Type of Crime")
    description = models.TextField(verbose_name="Crime Description", default="No description provided.")  
    location = models.CharField(max_length=255, default="Unknown Location", verbose_name="Crime Location")
    date = models.DateTimeField(default=timezone.now, verbose_name="Reported Date")  
    status = models.CharField(max_length=20, choices=CRIME_STATUS_CHOICES, default='Pending', verbose_name="Report Status")
    admin_notes = models.TextField(blank=True, null=True, verbose_name="Admin Notes")

    def __str__(self):
        return f"Report {self.id} - {self.typeofCrime} - {self.status}"
