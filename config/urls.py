from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from patients_management.views import register, register_patient, register_doctor, address_autocomplete, index, \
    patient_details, patient_consultations, doctor_patients, doctor_consultations


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='patients_management/pages/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('register/', register, name='register'),
    path('register-doctor/', register_doctor, name='register_doctor'),
    path('register-patient/', register_patient, name='register_patient'),
    path('address_autocomplete/', address_autocomplete, name='address_autocomplete'),

    path('patient/details/', patient_details, name='patient_details'),
    path('patient/consultations/', patient_consultations, name='patient_consultations'),

    path('doctor/patients/', doctor_patients, name='doctor_patients'),
    path('doctor/consultations/', doctor_consultations, name='doctor_consultations'),
]
