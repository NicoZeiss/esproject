from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from faker import Faker

from patients_management.models import Patient


class Command(BaseCommand):
    help = 'Create 5000 Patients'

    def handle(self, *args, **kwargs):
        fake = Faker()
        patients = []
        password = make_password("Password1@")

        for _ in range(5000):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{fake.user_name()}_{get_random_string(3)}"
            email = f"{username}@example.com"
            street = fake.street_address()
            zip_code = fake.zipcode()
            city = fake.city()
            patient = Patient(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                street=street,
                zip_code=zip_code,
                city=city,
                role='PATIENT'
            )
            patients.append(patient)

        Patient.objects.bulk_create(patients)
        self.stdout.write(self.style.SUCCESS('Successfully created 5000 Patients'))
