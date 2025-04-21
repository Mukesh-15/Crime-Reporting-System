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

    PRIORITY_CHOICES = [
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Medium'),
        (4, 'High'),
        (5, 'Critical'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    typeofCrime = models.CharField(max_length=100, verbose_name="Type of Crime")
    description = models.TextField(verbose_name="Crime Description", default="No description provided.")  
    location = models.CharField(max_length=255, default="Unknown Location", verbose_name="Crime Location")
    latitude = models.CharField(max_length=255, default="0", verbose_name="Latitude")
    longititude = models.CharField(max_length=255, default="0", verbose_name="Longitude")
    date = models.DateTimeField(default=timezone.now, verbose_name="Reported Date")
    submitted_at = models.DateTimeField(default=timezone.now, verbose_name="Submitted At")
    status = models.CharField(max_length=20, choices=CRIME_STATUS_CHOICES, default='Pending', verbose_name="Report Status")
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, verbose_name="Priority Level")
    admin_notes = models.TextField(blank=True, null=True, verbose_name="Admin Notes")

    def __str__(self):
        return f"Report {self.id} - {self.typeofCrime} - {self.status}"
    


class EvidencePhoto(models.Model):
    report = models.ForeignKey(UserCrimeReport, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='evidence_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for Report {self.report.id}"
