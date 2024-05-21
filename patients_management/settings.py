from django.conf import settings


DOCTOR_GROUP_NAME = getattr(settings, 'DOCTOR_GROUP_NAME', 'Docteurs')
PATIENT_GROUP_NAME = getattr(settings, 'PATIENT_GROUP_NAME', 'Patients')
