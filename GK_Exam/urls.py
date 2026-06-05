from django.contrib import admin
from django.urls import path
from registration import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('toggle-payment/<int:student_id>/', views.toggle_payment, name='toggle_payment'),
    path('admit-card/<int:student_id>/', views.download_admit_card, name='download_admit_card'),
]