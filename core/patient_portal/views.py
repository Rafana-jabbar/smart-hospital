from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import FileResponse, HttpResponseForbidden
from django.utils import timezone
from accounts.models import Patient, Doctor, IVBag, Report, Appointment
from .forms import AppointmentForm


def _is_patient(user):
    return user.is_authenticated and user.groups.filter(name='Patient').exists()


def patient_login(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        name = request.POST.get('name')

        if not patient_id or not name:
            return render(request, 'patient_portal/login.html', {'error': 'Please provide both Patient ID and Name.'})

        user = authenticate(request, patient_id=patient_id, name=name)
        
        if user is not None:
            if _is_patient(user):
                login(request, user)
                return redirect('patient_portal:dashboard')
            else:
                # This case is a safeguard for if a non-patient user is somehow returned
                return render(request, 'patient_portal/login.html', {'error': 'Authentication failed.'})
        else:
            return render(request, 'patient_portal/login.html', {'error': 'Invalid Patient ID or Name.'})
        
    return render(request, 'patient_portal/login.html')


@login_required
def patient_logout(request):
    logout(request)
    return redirect('patient_portal:login')


@login_required
def dashboard(request):
    if not _is_patient(request.user):
        return HttpResponseForbidden('Forbidden')
    patient = get_object_or_404(Patient, user=request.user)
    assigned_doctor = getattr(patient, 'assigned_doctor', None)
    bed = getattr(patient, 'bed', None)
    iv_status = IVBag.objects.filter(patient=patient).order_by('-last_updated').first()
    reports = Report.objects.filter(patient=patient).order_by('-created_at')
    appointments = Appointment.objects.filter(patient=patient).order_by('-date')[:10]
    form = AppointmentForm()
    return render(request, 'patient_portal/dashboard.html', {
        'patient': patient,
        'assigned_doctor': assigned_doctor,
        'bed': bed,
        'iv_status': iv_status,
        'reports': reports,
        'appointments': appointments,
        'form': form,
    })


@login_required
def download_report(request, report_id):
    if not _is_patient(request.user):
        return HttpResponseForbidden('Forbidden')
    patient = get_object_or_404(Patient, user=request.user)
    report = get_object_or_404(Report, id=report_id, patient=patient)
    if report.report_image:
        return FileResponse(report.report_image.open('rb'))
    file_obj = report.files.first()
    if file_obj:
        return FileResponse(file_obj.file.open('rb'))
    return redirect('patient_portal:dashboard')


@login_required
def book_appointment(request):
    if not _is_patient(request.user):
        return HttpResponseForbidden('Forbidden')
    patient = get_object_or_404(Patient, user=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.patient = patient
            appt.status = 'Pending'
            if appt.date and appt.date.tzinfo is None:
                appt.date = timezone.make_aware(appt.date)
            appt.save()
    return redirect('patient_portal:dashboard')


@login_required
def appointment_history(request):
    if not _is_patient(request.user):
        return HttpResponseForbidden('Forbidden')
    patient = get_object_or_404(Patient, user=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('-date')
    return render(request, 'patient_portal/appointments.html', {'appointments': appointments})


