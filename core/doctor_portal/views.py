from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.utils import timezone
from functools import wraps
from accounts.models import Doctor, Patient, Appointment, Report
from .forms import NoteForm


DOCTOR_SESSION_KEY = 'doctor_id'


def get_current_doctor(request):
    doctor_id = request.session.get(DOCTOR_SESSION_KEY)
    if not doctor_id:
        return None
    try:
        return Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return None


def doctor_login_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        doctor = get_current_doctor(request)
        if doctor is None:
            return redirect('doctor_portal:login')
        request.current_doctor = doctor
        return view_func(request, *args, **kwargs)
    return _wrapped


def doctor_login(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        name = request.POST.get('name')
        if not doctor_id or not name:
            return render(request, 'doctor_portal/login.html', {'error': 'Please provide both Doctor ID and Name.'})
        try:
            doctor = Doctor.objects.get(id=doctor_id, name__iexact=name)
            request.session[DOCTOR_SESSION_KEY] = doctor.id
            return redirect('doctor_portal:dashboard')
        except Doctor.DoesNotExist:
            return render(request, 'doctor_portal/login.html', {'error': 'Invalid Doctor ID or Name.'})
    return render(request, 'doctor_portal/login.html')


def doctor_logout(request):
    request.session.pop(DOCTOR_SESSION_KEY, None)
    try:
        request.session.flush()
    except Exception:
        pass
    return redirect('doctor_portal:login')


@doctor_login_required
def dashboard(request):
    doctor = request.current_doctor
    patients = Patient.objects.filter(assigned_doctor=doctor).order_by('name')
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date')
    recent_reports = Report.objects.filter(doctor=doctor).order_by('-created_at')[:10]
    return render(request, 'doctor_portal/dashboard.html', {
        'doctor': doctor,
        'patients': patients,
        'appointments': appointments,
        'recent_reports': recent_reports,
    })


@doctor_login_required
def patient_detail(request, patient_id):
    doctor = request.current_doctor
    patient = get_object_or_404(Patient, id=patient_id)
    # Enforce that the patient is assigned to the logged-in doctor
    if patient.assigned_doctor_id != doctor.id:
        return HttpResponseForbidden('Forbidden')
    reports = Report.objects.filter(patient=patient).order_by('-created_at')
    form = NoteForm()
    return render(request, 'doctor_portal/patient_detail.html', {
        'patient': patient,
        'reports': reports,
        'form': form,
    })


@doctor_login_required
def approve_appointment(request, appointment_id):
    doctor = request.current_doctor
    appt = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    appt.status = 'Approved'
    appt.save()
    return redirect('doctor_portal:dashboard')


@doctor_login_required
def reject_appointment(request, appointment_id):
    doctor = request.current_doctor
    appt = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    appt.status = 'Rejected'
    appt.save()
    return redirect('doctor_portal:dashboard')


@doctor_login_required
def add_note(request, patient_id):
    doctor = request.current_doctor
    patient = get_object_or_404(Patient, id=patient_id)
    if patient.assigned_doctor_id != doctor.id:
        return HttpResponseForbidden('Forbidden')
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.patient = patient
            report.doctor = doctor
            report.save()
            return redirect('doctor_portal:patient_detail', patient_id=patient.id)
    return redirect('doctor_portal:dashboard')


