from django.apps import AppConfig


class PatientsManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'patients_management'

    def ready(self) -> None:
        import patients_management.signals
