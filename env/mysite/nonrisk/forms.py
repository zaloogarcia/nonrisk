from django import forms
from .models import *

class PacientForm(forms.ModelForm):

	class Meta:
		model = Pacient
		fields = ('id', 'name','name_second','name_last','sex','address','phone',
			'date_of_birth' ,'medical_details' ,'smoke','smoke_quantity' ,'smoke_duration',
			'smoke_quit' , 'diabetes','diabetes_type','diabetes_date', 'hyper','hyper_type',
			'hyper_date', 'dislipidemia','dislipidemia_type','dislipidemia_date','irc',
			'irc_type', 'iam','acv','revasc','enfvp','acv_ait','fecvt')


class StudiesForm(forms.ModelForm):

	class Meta:
		model = Studies
		fields = ('pacient','id','date','weight','height','tas','tad','pulse',
			'diabetes_chol_level','diabetes_hdl_level' ,'diabetes_ldl_level',
			'diabetes_tri_level' ,'glucemia','hba1c','ac_uric','creat','tsh',
			'pcr','comments')