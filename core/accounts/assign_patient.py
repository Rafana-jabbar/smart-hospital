import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()
from accounts.models import Patient, Doctor

# Assign every patient to the first doctor
doctor = Doctor.objects.first()
if not doctor:
    print("No doctors found! Please create a doctor using Django admin.")
else:
    count = 0
    for p in Patient.objects.all():
        p.assigned_doctor = doctor
        p.save()
        print(f"Assigned {p.name} to {doctor.name}")
        count += 1
    if count == 0:
        print("No patients found.")
    else:
        print("Done assigning patients!")