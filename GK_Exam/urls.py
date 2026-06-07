from django.contrib import admin
from django.urls import path
from registration import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('toggle-payment/<int:student_id>/', views.toggle_payment, name='toggle_payment'),
    path('admit-card/<int:student_id>/', views.download_admit_card, name='download_admit_card'),
    path('admissions/', views.admissions, name='admissions'),
    path('admission-success/', views.admission_success, name='admission_success'),
    path('toggle-admission-status/<int:app_id>/', views.toggle_admission_status, name='toggle_admission_status'),
    path('toggle-admission-payment/<int:app_id>/', views.toggle_admission_payment, name='toggle_admission_payment'),
    path('contact/', views.contact, name='contact'),
    path('contact-success/', views.contact_success, name='contact_success'),
    path('toggle-message-status/<int:msg_id>/', views.toggle_message_status, name='toggle_message_status'),
    path('courses/', views.courses, name='courses'),
    path('student-signup/', views.student_signup, name='student_signup'),
    path('student-login/', views.student_login, name='student_login'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student-logout/', views.student_logout, name='student_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)