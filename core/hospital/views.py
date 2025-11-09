from django.shortcuts import render

def home(request):
    return render(request, "hospital/home.html")

def patient(request):
    patient_data = {
        "name": "John Doe",
        "age": 30,
        "history": "Diabetes",
        "diagnosis": "Hypertension",
        "treatment": "Medication + Lifestyle Changes"
    }
    return render(request, "hospital/patient.html", {"patient": patient_data})

def doctor(request):
    doctors_data = [
        {"name": "Dr. Smith", "specialty": "Cardiology"},
        {"name": "Dr. Jane", "specialty": "Neurology"}
    ]
    return render(request, "hospital/doctor.html", {"doctors": doctors_data})

def admin_portal(request):
    return render(request, "hospital/admin.html")
