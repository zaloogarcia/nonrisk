from django.contrib import admin

from .models import Company, Patient, Studies

admin.site.register(Company)
admin.site.register(Patient)
admin.site.register(Studies)