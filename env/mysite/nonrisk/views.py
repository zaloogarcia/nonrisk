from django.http import HttpResponse
from nonrisk.models import *
from django.template import loader
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Hello, world.")

@login_required
def pacients_view(request):
	pacients_list = Pacient.objects.all()
	context = {'pacients_list': pacients_list,}
	# for x in range (0,len(pacients_list)):
	# 	response = response + (' El paciente es  %s' % pacients_list[x].name)
	return render(request,'pacients.html',context)

def pacient_view(request,pacient_id):
	try:
		pacient = Pacient.objects.filter(id=pacient_id)[:1].get()
	except Pacient.DoesNotExist:
		raise Http404("Pacient does not exist")
	return HttpResponse('el nombre del pibe es %s' % pacient.name)
