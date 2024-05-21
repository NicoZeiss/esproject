from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from patients_management.views import register_patient, address_autocomplete, index, patient_details, \
    patient_consultations


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='patients_management/pages/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register-patient/', register_patient, name='register_patient'),
    path('address_autocomplete/', address_autocomplete, name='address_autocomplete'),

    path('patient/details/', patient_details, name='patient_details'),
    path('patient/consultations/', patient_consultations, name='patient_consultations'),
]
