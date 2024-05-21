from django import forms

from .models import Patient, Doctor


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'street', 'zip_code', 'city']
        widgets = {
            'street': forms.HiddenInput(),
            'zip_code': forms.HiddenInput(),
            'city': forms.HiddenInput(),
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
