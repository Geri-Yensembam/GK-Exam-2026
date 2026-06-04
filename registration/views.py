from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .forms import StudentRegistrationForm
from .models import Student

def landing(request):
    return render(request, 'registration/landing.html')

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def success(request):
    return render(request, 'registration/success.html')

@staff_member_required(login_url='/admin/login/')
def dashboard(request):
    students = Student.objects.all().order_by('-registration_date')
    total = students.count()
    return render(request, 'registration/dashboard.html', {
        'students': students,
        'total': total,
    })