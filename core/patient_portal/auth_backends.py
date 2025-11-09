from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from accounts.models import Patient

class PatientIdNameAuthBackend(BaseBackend):
    def authenticate(self, request, patient_id=None, name=None):
        """
        Authenticates a patient by their ID and case-insensitive name.
        """
        try:
            # Use a case-insensitive lookup for the name
            patient = Patient.objects.get(id=patient_id, name__iexact=name)
            # If the patient is found, return their associated user account
            return patient.user
        except Patient.DoesNotExist:
            # No patient found with this ID and name
            return None

    def get_user(self, user_id):
        """
        Required method for the Django authentication framework.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
