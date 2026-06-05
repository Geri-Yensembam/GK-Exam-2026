from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import StudentRegistrationForm
from .models import Student
from .utils import generate_admit_card

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

@staff_member_required(login_url='/admin/login/')
def toggle_payment(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.payment_status = not student.payment_status
    student.save()

    if student.payment_status:
        # Generate PDF
        pdf_buffer = generate_admit_card(student)
        
        # Create email with attachment
        from django.core.mail import EmailMessage
        email = EmailMessage(
            subject='GK Exam 2026 - Admit Card',
            body=f"""
Dear {student.full_name},

Your payment has been verified successfully!
Please find your admit card attached to this email.

Exam Details:
- Date: 15th June 2026
- Center: Sunshine Academy, Pune
- Time: 10:00 AM
- Subject: {student.subject}

Please bring the printed admit card and a valid photo ID to the examination center.

Best regards,
GK Exam 2026 Team
Sunshine Academy, Pune
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[student.email],
        )
        # Attach PDF
        filename = f"AdmitCard_{student.full_name.replace(' ', '_')}.pdf"
        email.attach(filename, pdf_buffer.read(), 'application/pdf')
        email.send(fail_silently=False)

    return redirect('dashboard')

@staff_member_required(login_url='/admin/login/')
def download_admit_card(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    buffer = generate_admit_card(student)
    filename = f"AdmitCard_{student.full_name.replace(' ', '_')}.pdf"
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response