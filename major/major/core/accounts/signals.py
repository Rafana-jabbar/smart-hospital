from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User, Group
from .models import Patient, Bed, Doctor
from django.dispatch import receiver


@receiver(pre_save, sender=Patient)
def free_old_bed(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_patient = Patient.objects.get(pk=instance.pk)
            if old_patient.bed and old_patient.bed != instance.bed:
                old_patient.bed.is_occupied = False
                old_patient.bed.save()
        except Patient.DoesNotExist:
            pass


@receiver(post_save, sender=Patient)
def occupy_new_bed(sender, instance, **kwargs):
    if instance.bed:
        instance.bed.is_occupied = True
        instance.bed.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create groups if they don't exist
        patient_group, created = Group.objects.get_or_create(name='Patient')
        doctor_group, created = Group.objects.get_or_create(name='Doctor')
        admin_group, created = Group.objects.get_or_create(name='Admin')

        # For simplicity, let's assume new users are patients by default
        # In a real application, you'd have a registration form where the user selects their role
        instance.groups.add(patient_group)
        Patient.objects.create(user=instance, name=instance.username, age=0, contact='')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'patient'):
        instance.patient.save()
    elif hasattr(instance, 'doctor'):
        instance.doctor.save()
