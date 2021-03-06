from django import forms
from .models import *

class CompanyForm(forms.ModelForm):
	model = Company
	fields = ('name')
	logo = forms.FileField(label='Seleccione un Archivo')

class PatientForm(forms.ModelForm):

	class Meta:
		model = Patient
		fields = ('id', 'name','name_second','name_last','sex','address','phone', 'arterial_age',
			'date_of_birth' ,'medical_details' ,'smoke','smoke_quantity' ,'smoke_duration',
			'smoke_quit' , 'diabetes','diabetes_type','diabetes_date', 'hyper','hyper_type',
			'hyper_date', 'dislipidemia','dislipidemia_type','dislipidemia_date','irc',
			'irc_type', 'iam','acv','revasc','enfvp','acv_ait','fecvt', 'race')


class StudiesForm(forms.ModelForm):

	class Meta:
		model = Studies
		fields = ('patient','id','date','weight','height','tas','tad','pulse',
			'chol_level','hdl_level' ,'ldl_level',
			'tri_level' ,'glucemia','hba1c','ac_uric','creat','tsh',
			'pcr','comments', 'renal_filter')