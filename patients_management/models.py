from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class UserAccount(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"

    base_role = Role.ADMIN

    role = models.CharField(max_length=10, choices=Role.choices)
    street = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.role = self.base_role
        return super().save(*args, **kwargs)


class PatientManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Patient.base_role)


class Patient(UserAccount):
    base_role = UserAccount.Role.PATIENT

    objects = PatientManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_superuser = False
        self.is_staff = False
        return super().save(*args, **kwargs)


class DoctorManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Doctor.base_role)


class Doctor(UserAccount):
    base_role = UserAccount.Role.DOCTOR

    objects = PatientManager()

    def save(self, *args, **kwargs):
        self.is_superuser = False
        self.is_staff = True
        return super().save(*args, **kwargs)

    class Meta:
        proxy = True
