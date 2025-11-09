from django.db import models
from django.contrib.auth.models import User



# -------------------
# Patient Model
# -------------------
# accounts/models.py

class Patient(models.Model):


    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    GENDER_CHOICES = [('M','Male'), ('F','Female'), ('O','Other')]
    id = models.AutoField(primary_key=True)
    name    = models.CharField(max_length=100, default="Unknown")
    age     = models.PositiveIntegerField()
    gender  = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    contact = models.CharField(max_length=15, blank=True)
    bed = models.OneToOneField("Bed", on_delete=models.SET_NULL, null=True, blank=True)
    assigned_doctor = models.ForeignKey("Doctor", on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')
    def __str__(self):
        return f"{self.name} (#{self.id})"

    class Meta:
        ordering = ['id']              # <- ascending (1,2,3…)
        verbose_name = "Patient"
        verbose_name_plural = "Patients"



# -------------------
# Doctor Model
# -------------------
class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"


# -------------------
# Appointment Model
# -------------------
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default="Scheduled")
    description = models.TextField()

    def __str__(self):
        return f"{self.patient.name} → {self.doctor.name} on {self.date.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"


# -------------------
# IV Bag Monitoring
# -------------------
class IVBag(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    level = models.IntegerField()  # percentage (0-100)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.name} - {self.level}%"

    class Meta:
        verbose_name = "IV Bag Monitor"
        verbose_name_plural = "IV Bag Monitors"


# -------------------
# Bed Management
# -------------------
class Bed(models.Model):
    bed_number = models.CharField(max_length=10, unique=True)
    is_occupied = models.BooleanField(default=False)
    

    def __str__(self):
            return f"Bed {self.bed_number} ({'Occupied' if self.is_occupied else 'Free'})"

    class Meta:
        verbose_name = "Hospital Bed"
        verbose_name_plural = "Hospital Beds"


# -------------------
# Patient Reports
# -------------------
class Report(models.Model):
    patient_name = models.CharField(max_length=200, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    report_type = models.CharField(max_length=100, choices=[
        ('Blood Test', 'Blood Test'),
        ('X-Ray', 'X-Ray'),
        ('Discharge Summary', 'Discharge Summary'),
        ('Prescription', 'Prescription'),
        ('Other', 'Other')])
    report_image = models.ImageField(upload_to='reports/', blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_type} - {self.patient.name}"

class ReportFile(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='reports/')
    file_type = models.CharField(max_length=50, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.report.patient.name}"
    