import requests

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import PatientForm, DoctorForm
from .models import Patient, Doctor


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


@login_required(login_url='/login/')
def index(request):
    return render(request, f"patients_management/pages/index/index.html")


@login_required(login_url='/login/')
def patient_details(request):
    return render(request, 'patients_management/pages/index/contents/patient_details.html')


@login_required(login_url='/login/')
def patient_consultations(request):
    return render(request, 'patients_management/pages/index/contents/patient_consultations.html')


@login_required(login_url='/login/')
def doctor_patients(request):
    return render(request, 'patients_management/pages/index/contents/doctor_patients.html')


@login_required(login_url='/login/')
def doctor_consultations(request):
    return render(request, 'patients_management/pages/index/contents/doctor_consultations.html')


@unauthenticated_user
def register(request):
    return render(
        request,
        'patients_management/pages/register/register.html'
    )


@unauthenticated_user
def register_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            user = Doctor.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data.get('email', None),
            )
            login(request, user)
            return redirect('index')
    else:
        form = DoctorForm()
    return render(
        request,
        'patients_management/pages/register/register_doctor.html',
        {'form': form}
    )


@unauthenticated_user
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
        'patients_management/pages/register/register_patient.html',
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
