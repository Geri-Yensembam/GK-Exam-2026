from django import forms
from .models import Student

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
        ('English', 'English'),
        ('Maths', 'Maths'),
        ('Computer Science', 'Computer Science'),
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