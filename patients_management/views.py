import requests
from django import forms
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Patient


@login_required(login_url='/login/')
def index(request):
    context = {
        'patients': Patient.objects.all()
    }

    return render(
        request,
        f"patients_management/pages/index/index.html",
        context
    )


def patient_details(request):
    return render(request, 'patients_management/pages/index/contents/patient_details.html')


def patient_consultations(request):
    return render(request, 'patients_management/pages/index/contents/patient_consultations.html')


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['username', 'password', 'first_name', 'last_name', 'street', 'zip_code', 'city']
        widgets = {
            'street': forms.HiddenInput(),
            'zip_code': forms.HiddenInput(),
            'city': forms.HiddenInput(),
        }


def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            user = Patient.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                street=form.cleaned_data['street'],
                zip_code=form.cleaned_data['zip_code'],
                city=form.cleaned_data['city'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data.get('email', None),
            )
            login(request, user)
            return redirect('index')
    else:
        form = PatientForm()
    return render(
        request,
        'patients_management/pages/patient_form.html',
        {'form': form}
    )


def address_autocomplete(request):
    query = request.GET.get('q', '')
    if query:
        response = requests.get(f'https://api-adresse.data.gouv.fr/search/?q={query}')
        addresses = response.json()
        results = [{
            'id': item['properties']['id'],
            'text': item['properties']['label'],
            'street': item['properties'].get('name', ''),
            'zip_code': item['properties'].get('postcode', ''),
            'city': item['properties'].get('city', ''),
        } for item in addresses.get('features', [])]
    else:
        results = []
    return JsonResponse({'results': results})
