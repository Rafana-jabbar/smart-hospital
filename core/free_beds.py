import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import Bed, Patient

# Find all beds that are marked as occupied but have no patient assigned
occupied_beds = Bed.objects.filter(is_occupied=True)
beds_freed = 0

for bed in occupied_beds:
    # Check if a patient is actually in this bed
    patient_in_bed = Patient.objects.filter(bed=bed).first()
    if not patient_in_bed:
        bed.is_occupied = False
        bed.save()
        beds_freed += 1
        print(f"Bed {bed.bed_number} has been marked as free.")

if beds_freed == 0:
    print("No beds needed to be freed.")
else:
    print(f"\nFinished. Freed up {beds_freed} bed(s).")
