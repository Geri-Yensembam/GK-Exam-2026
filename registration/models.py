from django.db import models

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    college = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    year_of_study = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    subject = models.CharField(max_length=50)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    roll_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.full_name