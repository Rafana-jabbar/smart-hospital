from django import forms
from django.contrib.auth.models import User, Group
from accounts.models import Patient, Doctor, Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'description']


