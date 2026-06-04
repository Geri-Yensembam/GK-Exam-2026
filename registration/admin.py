from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'college', 'subject', 'payment_status', 'registration_date']
    list_editable = ['payment_status']
    list_filter = ['payment_status', 'year_of_study', 'gender', 'subject']
    search_fields = ['full_name', 'email', 'college']