from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .forms import StudentRegistrationForm, AdmissionApplicationForm
from .models import Student, AdmissionApplication, ContactMessage, StudentAccount
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


def courses(request):
    return render(request, 'registration/courses.html')


def admissions(request):
    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admission_success')
    else:
        form = AdmissionApplicationForm()
    return render(request, 'registration/admissions.html', {'form': form})


def admission_success(request):
    return render(request, 'registration/admission_success.html')


def contact(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if full_name and email and message:
            ContactMessage.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            return redirect('contact_success')
    return render(request, 'registration/contact.html')


def contact_success(request):
    return render(request, 'registration/contact_success.html')


@staff_member_required(login_url='/admin/login/')
def dashboard(request):
    students = Student.objects.all().order_by('-registration_date')
    admissions = AdmissionApplication.objects.all().order_by('-applied_date')
    messages = ContactMessage.objects.all().order_by('-received_on')
    total_students = students.count()
    total_admissions = admissions.count()
    unread_messages = messages.filter(status='Unread').count()
    return render(request, 'registration/dashboard.html', {
        'students': students,
        'total': total_students,
        'admissions': admissions,
        'total_admissions': total_admissions,
        'messages': messages,
        'unread_messages': unread_messages,
    })


@staff_member_required(login_url='/admin/login/')
def toggle_payment(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.payment_status = not student.payment_status
    student.save()

    if student.payment_status:
        if not student.roll_number:
            last_roll = Student.objects.filter(
                roll_number__isnull=False
            ).exclude(roll_number='').order_by('roll_number').last()
            if last_roll and last_roll.roll_number:
                last_num = int(last_roll.roll_number)
                new_roll = str(last_num + 1)
            else:
                new_roll = "4601"
            student.roll_number = new_roll
            student.save()

        pdf_buffer = generate_admit_card(student)
        email = EmailMessage(
            subject='Chekla College of Engineering - GK Exam 2026 Admit Card',
            body=f"""
Dear {student.full_name},

Your payment has been verified successfully!
Your Roll Number is: {student.roll_number}

Please find your admit card attached to this email.

Exam Details:
- Date: 15th June 2026
- Center: Chekla College of Engineering
- Time: 10:00 AM
- Subject: {student.subject}

Please bring the printed admit card and a valid photo ID.

Best regards,
Chekla College of Engineering
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[student.email],
        )
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


@staff_member_required(login_url='/admin/login/')
def toggle_admission_status(request, app_id):
    app = get_object_or_404(AdmissionApplication, id=app_id)
    status_cycle = ['Pending', 'Reviewing', 'Accepted', 'Rejected']
    current_index = status_cycle.index(app.status)
    app.status = status_cycle[(current_index + 1) % len(status_cycle)]
    app.save()
    return redirect('dashboard')


@staff_member_required(login_url='/admin/login/')
def toggle_admission_payment(request, app_id):
    app = get_object_or_404(AdmissionApplication, id=app_id)
    app.payment_status = not app.payment_status
    app.save()

    if app.payment_status:
        if not app.prn_number:
            last_app = AdmissionApplication.objects.filter(
                prn_number__startswith='CHE-2026-'
            ).exclude(prn_number='').order_by('prn_number').last()
            if last_app and last_app.prn_number:
                last_num = int(last_app.prn_number.split('-')[2])
                new_prn = f"CHE-2026-{str(last_num + 1).zfill(3)}"
            else:
                new_prn = "CHE-2026-001"
            app.prn_number = new_prn
            app.save()

        send_mail(
            subject='Chekla College of Engineering - Admission Confirmed & PRN Number',
            message=f"""
Dear {app.full_name},

Congratulations! Your admission to Chekla College of Engineering has been confirmed.

Your PRN Number: {app.prn_number}
Program: {app.program}

Create your student account at:
http://127.0.0.1:8000/student-signup/

Steps:
1. Go to http://127.0.0.1:8000/student-signup/
2. Enter PRN: {app.prn_number}
3. Create a password
4. Login to view your profile

For queries: cheklacoe@gmail.com

Best regards,
Chekla College of Engineering
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[app.email],
            fail_silently=False,
        )

    return redirect('dashboard')


@staff_member_required(login_url='/admin/login/')
def toggle_message_status(request, msg_id):
    msg = get_object_or_404(ContactMessage, id=msg_id)
    status_cycle = ['Unread', 'Read', 'Replied']
    current_index = status_cycle.index(msg.status)
    msg.status = status_cycle[(current_index + 1) % len(status_cycle)]
    msg.save()
    return redirect('dashboard')


def student_signup(request):
    error = None
    if request.method == 'POST':
        prn = request.POST.get('prn_number').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            error = "Passwords don't match!"
        else:
            try:
                admission = AdmissionApplication.objects.get(prn_number=prn)
                if hasattr(admission, 'studentaccount'):
                    error = "Account already exists for this PRN!"
                else:
                    import hashlib
                    hashed = hashlib.sha256(password.encode()).hexdigest()
                    StudentAccount.objects.create(
                        admission=admission,
                        prn_number=prn,
                        password=hashed
                    )
                    request.session['student_prn'] = prn
                    request.session['student_name'] = admission.full_name
                    return redirect('student_dashboard')
            except AdmissionApplication.DoesNotExist:
                error = "Invalid PRN number! Please check your email."

    return render(request, 'registration/student_signup.html', {'error': error})


def student_login(request):
    error = None
    if request.method == 'POST':
        prn = request.POST.get('prn_number').strip()
        password = request.POST.get('password')
        try:
            import hashlib
            hashed = hashlib.sha256(password.encode()).hexdigest()
            account = StudentAccount.objects.get(prn_number=prn, password=hashed)
            request.session['student_prn'] = prn
            request.session['student_name'] = account.admission.full_name
            from django.utils import timezone
            account.last_login = timezone.now()
            account.save()
            return redirect('student_dashboard')
        except StudentAccount.DoesNotExist:
            error = "Invalid PRN or password!"

    return render(request, 'registration/student_login.html', {'error': error})


def student_dashboard(request):
    if not request.session.get('student_prn'):
        return redirect('student_login')
    prn = request.session['student_prn']
    account = StudentAccount.objects.get(prn_number=prn)
    admission = account.admission
    exam = None
    try:
        exam = Student.objects.get(email=admission.email)
    except Student.DoesNotExist:
        pass
    return render(request, 'registration/student_dashboard.html', {
        'account': account,
        'admission': admission,
        'exam': exam,
    })


def student_logout(request):
    request.session.flush()
    return redirect('student_login')