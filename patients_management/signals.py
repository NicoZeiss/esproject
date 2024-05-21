from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_migrate, post_save

from . import settings
from .models import Patient, Doctor


@receiver(post_migrate)
def test(sender, **kwargs):
    if sender.name == 'patients_management':
        doctor_group, doctor_created = Group.objects.get_or_create(name=settings.DOCTOR_GROUP_NAME)
        patient_group, patient_created = Group.objects.get_or_create(name=settings.PATIENT_GROUP_NAME)

        if doctor_created:
            patient_content_type = ContentType.objects.get_for_model(Patient, False)
            patient_permissions = Permission.objects.filter(content_type=patient_content_type)
            for permission in patient_permissions:
                doctor_group.permissions.add(permission)

        if patient_created:
            pass


@receiver(post_save, sender=Patient)
def add_patient_to_group(sender, instance, created, **kwargs):
    if created and instance.role == Patient.Role.PATIENT:
        patient_group = Group.objects.get(name=settings.PATIENT_GROUP_NAME)
        instance.groups.add(patient_group)
        instance.save()


@receiver(post_save, sender=Doctor)
def add_doctor_to_group(sender, instance, created, **kwargs):
    if created and instance.role == Patient.Role.DOCTOR:
        doctor_group = Group.objects.get(name=settings.DOCTOR_GROUP_NAME)
        instance.groups.add(doctor_group)
        instance.save()
