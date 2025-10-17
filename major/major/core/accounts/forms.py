from django import forms
from .models import Report  # import your model

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields =  ['patient_name', 'report_type', 'diagnosis', 'report_image' ]
