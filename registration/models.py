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

class AdmissionApplication(models.Model):
    PROGRAM_CHOICES = [
        ('B.E. Computer Engineering', 'B.E. Computer Engineering'),
        ('B.E. Electrical Engineering', 'B.E. Electrical Engineering'),
        ('B.E. Mechanical Engineering', 'B.E. Mechanical Engineering'),
        ('B.E. Civil Engineering', 'B.E. Civil Engineering'),
        ('B.E. Electronics & Telecom', 'B.E. Electronics & Telecom'),
        ('B.E. Chemical Engineering', 'B.E. Chemical Engineering'),
        ('M.E. Computer Engineering', 'M.E. Computer Engineering'),
        ('M.E. Mechanical Engineering', 'M.E. Mechanical Engineering'),
        ('M.E. Electrical Engineering', 'M.E. Electrical Engineering'),
        ('M.E. Electronics & Telecom', 'M.E. Electronics & Telecom'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewing', 'Reviewing'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    program = models.CharField(max_length=100, choices=PROGRAM_CHOICES)
    tenth_percentage = models.FloatField()
    twelfth_percentage = models.FloatField()
    entrance_score = models.FloatField(blank=True, null=True)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.BooleanField(default=False)
    prn_number = models.CharField(max_length=20, blank=True)
    applied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class SemesterMarksheet(models.Model):
    SEMESTER_CHOICES = [
        ('Semester 1', 'Semester 1'),
        ('Semester 2', 'Semester 2'),
        ('Semester 3', 'Semester 3'),
        ('Semester 4', 'Semester 4'),
        ('Semester 5', 'Semester 5'),
        ('Semester 6', 'Semester 6'),
        ('Semester 7', 'Semester 7'),
        ('Semester 8', 'Semester 8'),
    ]

    student = models.ForeignKey(AdmissionApplication, on_delete=models.CASCADE, related_name='marksheets')
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    marksheet = models.FileField(upload_to='marksheets/')
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.semester}"

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('Unread', 'Unread'),
        ('Read', 'Read'),
        ('Replied', 'Replied'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Unread')
    received_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"
    
class StudentAccount(models.Model):
    admission = models.OneToOneField(AdmissionApplication, on_delete=models.CASCADE)
    prn_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.prn_number