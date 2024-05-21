import requests
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator

from django.http import JsonResponse
from django.urls import resolve
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import PatientForm, DoctorForm, CustomAuthenticationForm
from .models import UserAccount, Patient, Doctor


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def index(request):
    if request.user.is_authenticated:
        if request.user.role == UserAccount.Role.DOCTOR:
            return redirect('doctor_consultations')
        elif request.user.role == UserAccount.Role.PATIENT:
            return redirect('patient_consultations')
    return redirect('login')


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'patients_management/pages/login.html'


@login_required(login_url='/login/')
def patient_details(request):
    current_view = resolve(request.path_info).url_name
    return render(
        request,
        'patients_management/pages/patient/patient_details.html',
        {'current_view': current_view}
    )


@login_required(login_url='/login/')
def patient_consultations(request):
    current_view = resolve(request.path_info).url_name
    return render(
        request,
        'patients_management/pages/patient/patient_consultations.html',
        {'current_view': current_view}
    )


@login_required(login_url='/login/')
def doctor_consultations(request):
    current_view = resolve(request.path_info).url_name
    return render(
        request,
        'patients_management/pages/doctor/doctor_consultations.html',
        {'current_view': current_view}
    )


@login_required(login_url='/login/')
def doctor_list_patients(request):
    current_view = resolve(request.path_info).url_name
    patients = Patient.objects.all().order_by('username')
    paginator = Paginator(patients, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'patients_management/pages/doctor/doctor_patients.html',
        {'page_obj': page_obj, 'current_view': current_view}
    )


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
            print(form.cleaned_data)
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
