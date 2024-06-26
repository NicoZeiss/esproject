from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone


class UserAccount(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"

    base_role = Role.ADMIN

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(max_length=10, choices=Role.choices)
    street = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.last_name and self.first_name:
            return f"{self.last_name.upper()} {self.first_name.capitalize()}"
        return self.username.capitalize()

    @property
    def full_name(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        self.role = self.base_role
        return super().save(*args, **kwargs)

    @property
    def address(self):
        if self.street and self.zip_code and self.city:
            return f"{self.street}, {self.zip_code} {self.city.upper()}"
        return None


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


class Consultation(models.Model):
    class ConsultationType(models.TextChoices):
        VISIT = "VISIT", "Visite"
        AFTERCARE = "AFTERCARE", "Suivi"
        SURGERY = "SURGERY", "Opération"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_consultations')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_consultations')
    consultation_type = models.CharField(
        max_length=10,
        choices=ConsultationType.choices,
        default=ConsultationType.VISIT
    )
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        assert self.patient.role == Patient.base_role, "'patient' should be a PATIENT role"
        assert self.doctor.role == Doctor.base_role, "'doctor' should be a DOCTOR role"
        return super().save(*args, **kwargs)

    @property
    def verbose_type(self):
        for choice in self.ConsultationType.choices:
            if choice[0] == self.consultation_type:
                return choice[1]

    @property
    def is_outdated(self):
        return self.date < timezone.now()
