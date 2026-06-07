from django.contrib import admin
from .models import Student, AdmissionApplication, ContactMessage, StudentAccount, SemesterMarksheet

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'college', 'subject', 'payment_status', 'registration_date']
    list_editable = ['payment_status']
    list_filter = ['payment_status', 'year_of_study', 'gender', 'subject']
    search_fields = ['full_name', 'email', 'college']

class SemesterMarksheetInline(admin.TabularInline):
    model = SemesterMarksheet
    extra = 1

@admin.register(AdmissionApplication)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'program', 'status', 'payment_status', 'applied_date']
    list_editable = ['status', 'payment_status']
    list_filter = ['status', 'payment_status', 'program']
    search_fields = ['full_name', 'email']
    inlines = [SemesterMarksheetInline]

@admin.register(SemesterMarksheet)
class SemesterMarksheetAdmin(admin.ModelAdmin):
    list_display = ['student', 'semester', 'uploaded_on']
    list_filter = ['semester']
    search_fields = ['student__full_name']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject', 'status', 'received_on']
    list_editable = ['status']
    list_filter = ['status']
    search_fields = ['full_name', 'email', 'subject']

@admin.register(StudentAccount)
class StudentAccountAdmin(admin.ModelAdmin):
    list_display = ['prn_number', 'admission', 'created_at', 'last_login']
    search_fields = ['prn_number']