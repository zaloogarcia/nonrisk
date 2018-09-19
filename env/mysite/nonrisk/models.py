from __future__ import unicode_literals
from django.db import models
import datetime
from django.contrib.auth.models import User

class Pacient(models.Model):
    id = models.IntegerField(primary_key=True) #DNI

    MALE = 'M'
    FEMALE = 'F'
    SEX_OPTIONS = ((MALE, 'Male'), (FEMALE, 'Female'))

    name = models.CharField(max_length=50, null=False, blank=False)
    name_second = models.CharField(max_length=50, null=True, blank=True)
    name_last = models.CharField(max_length=50, null=False, blank=False)
    sex = models.CharField(max_length=1, choices=SEX_OPTIONS)
    address = models.CharField(max_length=175, null=False, blank=False)
    phone = models.IntegerField()
    date_of_birth = models.DateField()
    medical_details = models.CharField(max_length=300)

    smoke = models.BooleanField()
    smoke_quantity = models.IntegerField(null=True, blank=True)
    smoke_duration = models.DateField(null=True, blank=True)
    smoke_quit = models.DateField(null=True, blank=True)

    diabetes = models.BooleanField()
    diabetes_type = models.IntegerField(null=True, blank=True)
    diabetes_date = models.DateField(null=True, blank=True)

    PRIMARY = 'Primaria'
    SECONDARY = 'Secundaria'
    HYPER_OPTIONS = ((PRIMARY, 'Primaria'),(SECONDARY, 'Secundaria'))
    hyper = models.BooleanField()
    hyper_type = models.CharField(null=True, max_length=10,choices=HYPER_OPTIONS, blank=True)
    hyper_date = models.DateField(null=True, blank=True)

    I = 'I'
    IIA = 'IIa'
    IIB = 'IIb'
    III = 'III'
    IV = 'IV'
    V = 'V'
    DISLIPIDEMIA_OPTIONS = ((I,'I'),(IIA, 'IIa'),(IIB,'IIb'),(III,'III'),
        (IV, 'IV'),(V,'V'))
    dislipidemia = models.BooleanField()
    dislipidemia_type = models.CharField(null=True, max_length=10,
                                         choices=DISLIPIDEMIA_OPTIONS, blank=True)
    dislipidemia_date = models.DateField(null=True, blank=True)
    
    G1 ='G1'
    G2 ='G2'
    G3A='G3a'
    G3B='G3b'
    G4 ='G4'
    G5 ='G5'
    IRC_OPTIONS = ((G1,'G1'),(G2,'G2'),(G3A,'G3a'),(G3B,'G3b'),(G4,'G4'),(G5,'G5'))
    irc = models.BooleanField()
    irc_type = models.CharField(null=True,blank=True, choices=IRC_OPTIONS, max_length=3)

    iam = models.BooleanField()
    acv = models.BooleanField()
    revasc = models.BooleanField()
    enfvp = models.BooleanField()
    acv_ait= models.BooleanField()
    fecvt = models.BooleanField()

    def __str__(self):
        return self.name

class Studies(models.Model):
    pacient = models.ForeignKey(Pacient, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    date = models.DateField()

    weight = models.IntegerField() #in kg
    height  = models.IntegerField() #in cm
    tas = models.IntegerField()
    tad = models.IntegerField()
    pulse = models.IntegerField()

    diabetes_chol_level = models.IntegerField(null=True,blank=True) #Chol Level
    diabetes_hdl_level = models.IntegerField(null=True,blank=True)  #TRI Level
    diabetes_ldl_level = models.IntegerField(null=True,blank=True)  #HDL Level
    diabetes_tri_level = models.IntegerField(null=True,blank=True)  #LDL Level
    
    glucemia  = models.IntegerField()
    hba1c = models.IntegerField()
    ac_uric = models.IntegerField()
    creat = models.IntegerField()
    tsh = models.IntegerField()
    pcr = models.IntegerField()

    comments = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        name = str(self.id)
        return name
