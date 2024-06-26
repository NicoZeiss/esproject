from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Patient, Doctor, Consultation


class PatientForm(forms.ModelForm):
    class Meta:
        input_classes = 'w-full py-2 px-4'
        model = Patient
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'street', 'zip_code', 'city']
        widgets = {
            'username': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Nom d\'utilisateur'}),
            'password': forms.PasswordInput(attrs={'class': input_classes, 'placeholder': 'Mot de passe'}),
            'first_name': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Nom'}),
            'email': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Email'}),
            'street': forms.HiddenInput(),
            'zip_code': forms.HiddenInput(),
            'city': forms.HiddenInput(),
        }


class ModifyPatientForm(forms.ModelForm):
    class Meta:
        input_classes = 'w-full py-2 px-4'
        model = Patient
        fields = ['username', 'first_name', 'last_name', 'email', 'street', 'zip_code', 'city']
        widgets = {
            'username': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Nom d\'utilisateur'}),
            'first_name': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Nom'}),
            'email': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Email'}),
            'street': forms.HiddenInput(),
            'zip_code': forms.HiddenInput(),
            'city': forms.HiddenInput(),
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        input_classes = 'w-full py-2 px-4'
        model = Doctor
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Nom d\'utilisateur'}),
            'password': forms.PasswordInput(attrs={'class': input_classes, 'placeholder': 'Mot de passe'}),
            'first_name': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Nom'}),
            'email': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Email'}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    input_classes = 'w-full py-2 px-4'
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': input_classes,
            'placeholder': 'Nom d\'utilisateur',
        }
    ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': input_classes,
                'placeholder': 'Mot de passe',
            }
        )
    )


class ConsultationForm(forms.ModelForm):
    class Meta:
        input_classes = 'w-full py-2 px-4'
        model = Consultation
        fields = ['patient', 'description', 'date', 'consultation_type']
        widgets = {
            'date': forms.DateTimeInput(
                attrs={'class': input_classes, 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'description': forms.Textarea(attrs={'class': input_classes, 'placeholder': 'Description'}),
            'consultation_type': forms.Select(attrs={'class': input_classes, 'placeholder': 'Type'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.order_by('last_name', 'first_name')
        self.fields['date'].input_formats = ['%Y-%m-%dT%H:%M']
