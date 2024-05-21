from django.urls import path

from patients_management.views import register, register_patient, register_doctor, address_autocomplete, index, \
    patient_details, patient_consultations, doctor_list_patients, doctor_consultations


urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('register-doctor/', register_doctor, name='register_doctor'),
    path('register-patient/', register_patient, name='register_patient'),
    path('address_autocomplete/', address_autocomplete, name='address_autocomplete'),

    path('patient/details/', patient_details, name='patient_details'),
    path('patient/consultations/', patient_consultations, name='patient_consultations'),

    path('doctor/patients/', doctor_list_patients, name='doctor_list_patients'),
    path('doctor/consultations/', doctor_consultations, name='doctor_consultations'),
]