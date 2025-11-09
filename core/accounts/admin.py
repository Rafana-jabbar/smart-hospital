from django.contrib import admin
from .models import Doctor, Patient, Appointment, IVBag, Bed, Report, ReportFile
from django.utils.html import format_html
from django.urls import reverse
   

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age','delete_link', )   # Columns to display
    search_fields = ('name',)               # Search bar
    list_filter = ('age',)                            # Side filter
    exclude = ['user']

    def delete_link(self, obj):
        url = reverse("admin:accounts_patient_delete", args=[obj.id])
        return format_html('<a href="{}" style="color:red;">Delete</a>', url)

    delete_link.short_description = "Delete"

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialization')
    search_fields = ('name', 'specialization')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'date', 'time')
    search_fields = ('patient__name', 'doctor__name')
    list_filter = ('date', 'doctor')   # filter by date & doctor


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('id', 'bed_number', 'is_occupied')
    list_filter = ('is_occupied',)


@admin.register(IVBag)
class IVBagAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'level')
    list_filter = ('level',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'created_at', 'diagnosis', 'doctor', 'report_type')
    search_fields = ('patient__name', 'diagnosis')
    list_filter = ('created_at',)


