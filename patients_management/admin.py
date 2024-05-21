from django.contrib import admin
from .models import UserAccount, Patient


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['username']


class PatientAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_name', 'first_name', 'email']


admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Patient, PatientAdmin)
