from django import forms
from .models import Student
from .models import Student, AdmissionApplication
from django.forms.widgets import DateInput

class StudentRegistrationForm(forms.ModelForm):
    
    YEAR_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
    ]
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    SUBJECT_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Mathematics', 'Mathematics'),
        ('Physics', 'Physics'),
    ]

    year_of_study = forms.ChoiceField(choices=YEAR_CHOICES)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    class Meta:
        model = Student
        fields = [
            'full_name',
            'email', 
            'phone',
            'college',
            'department',
            'year_of_study',
            'gender',
            'subject',
        ]

class AdmissionApplicationForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
    )
    class Meta:
        model = AdmissionApplication
        fields = ['full_name', 'email', 'phone', 'date_of_birth', 
                  'program', 'tenth_percentage', 'twelfth_percentage', 
                  'entrance_score', 'address']