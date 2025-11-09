from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Report, Patient, IVBag
from .forms import ReportForm
from .iv_module import get_iv_level




# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='Patient').exists():
                    return redirect('patient')
                elif user.groups.filter(name='Doctor').exists():
                    return redirect('doctor')
                elif user.groups.filter(name='Admin').exists():
                    return redirect('admin')
                else:
                    return redirect('home') # Default redirect for users with no specific role
            else:
                # Invalid login
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def patient_reports(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    reports = patient.reports.all()  
    return render(request, 'reports/patient_reports.html', {'patient': patient, 'reports': reports})

def add_report(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.patient = patient
            report.doctor = getattr(request.user, 'doctor', None)
            report.save()
            return redirect('patient_reports', patient_id=patient.id)
    else:
        form = ReportForm()
    return render(request, 'reports/add_report.html', {'form': form, 'patient': patient})  
  

def report_upload(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('report_upload')  # reload the page after upload
    else:
        form = ReportForm()
    
    reports = Report.objects.all()
    return render(request, 'accounts/report_upload.html', {'form': form})

def reports_by_patient(request, name):
    reports = Report.objects.filter(patient_name__iexact=name)
    return render(request, 'accounts/patient_reports.html', {'name': name, 'reports': reports})

def iv_dashboard(request):
    for iv in IVBag.objects.all():
        if iv.level > 0:
            iv.level -= random.randint(5, 15)
            iv.save()
    iv_bags = IVBag.objects.select_related('patient').all()
    return render(request, 'iv/dashboard.html', {'iv_bags': iv_bags})    
