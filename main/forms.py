from django import forms
from .models import UserCrimeReport
from .models import EvidencePhoto

class CrimeReportForm(forms.ModelForm):
    class Meta:
        model = UserCrimeReport
        fields = ['typeofCrime', 'description']  # Ensure fields match model
        widgets = {
            'typeofCrime': forms.Select(choices=[
                ('Violent crime', 'Violent crime'),
                ('Kidnapping', 'Kidnapping'),
                ('Theft', 'Theft'),
                ('Sexual assault', 'Sexual assault'),
                ('Drug offences', 'Drug offences'),
                ('Fraud', 'Fraud'),
                ('Other', 'Other')
            ], attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long.")
        return description


class EvidencePhotoForm(forms.ModelForm):
    class Meta:
        model = EvidencePhoto
        fields = ['image']
