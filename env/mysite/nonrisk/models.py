from __future__ import unicode_literals
from django.db import models
import datetime
from django.contrib.auth.models import User

class Pacient(models.Model):
    id = models.AutoField(primary_key=True)

    MALE = 'M'
    FEMALE = 'F'
    SEX_OPTIONS = ((MALE, 'Male'), (FEMALE, 'Female'))

    name = models.CharField(max_length=50, null=False, blank=False)
    name_second = models.CharField(max_length=50, null=False, blank=True)
    name_last = models.CharField(max_length=50, null=False, blank=False)
    sex = models.CharField(max_length=1, choices=SEX_OPTIONS)
    address = models.CharField(max_length=175, null=False, blank=False)
    phone = models.IntegerField()
    date_of_birth = models.DateField()
    medical_details = models.CharField(max_length=300)

    smoke = models.BooleanField()
    smoke_quantity = models.IntegerField(blank=True)
    smoke_duration = models.DateField(blank=True)
    smoke_quit = models.DateField(blank=True)

    diabetes = models.BooleanField()
    diabetes_type = models.IntegerField(blank=True)
    diabetes_chol_level = models.IntegerField(blank=True) #Chol Level
    diabetes_hdl_level = models.IntegerField(blank=True)  #TRI Level
    diabetes_ldl_level = models.IntegerField(blank=True)  #HDL Level
    diabetes_tri_level = models.IntegerField(blank=True)  #LDL Level

    def __str__(self):
        return self.name

class Studies(models.Model):
    pacient = models.ForeignKey(Pacient, on_delete=models.CASCADE)

    date = models.DateField()
    SYMPTOMATIC = 'SYM'
    ASYMPTOMATIC = 'ASY'
    TERRITORY_OPTIONS = ((SYMPTOMATIC, 'Symptomatic'),
     (ASYMPTOMATIC, 'ASYMPTOMATIC'))

    territory = models.CharField(max_length=3, choices=TERRITORY_OPTIONS)

    carotid_1 = models.BooleanField()  # Unilateral motor and sensory deficit
    carotid_2 = models.BooleanField()  # Tinlgin or numbness on one side
    carotid_3 = models.BooleanField()  # Aphasia
    carotid_4 = models.BooleanField()  # Monocular disturbances (Amarosis fugax)

    vertebrobasilar_1 = models.BooleanField()  # Bilateral motor and sensory deficits
    vertebrobasilar_2 = models.BooleanField()  # Vertigo(a pinning sensation)
    vertebrobasilar_3 = models.BooleanField()  # Ataxia (Unsteadiness)
    vertebrobasilar_4 = models.BooleanField()  # Binocular visual field defects
    vertebrobasilar_5 = models.BooleanField()  # Drop attacks
    vertebrobasilar_6 = models.BooleanField()  # Diplopia

    nonspecific_1 = models.BooleanField() # Light-headedness
    nonspecific_2 = models.BooleanField() # Syncope
    nonspecific_3 = models.BooleanField() # Headache
    nonspecific_4 = models.BooleanField() # Confusion

    comments = models.CharField(max_length=300, null=False, blank=False)

    def __str__(self):
        return self.date
