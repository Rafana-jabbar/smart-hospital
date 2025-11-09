from django import forms
from accounts.models import Report


class NoteForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_type', 'diagnosis', 'notes']


