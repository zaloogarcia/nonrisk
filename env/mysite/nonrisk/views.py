import re
import base64
import io
from io import *
from PIL import Image
from django.http import *
from nonrisk.forms import *
from nonrisk.models import *
from datetime import datetime
from django.template import loader
from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.db import IntegrityError
from django.views.generic import View
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.files.base import ContentFile

# NEED TO INSTALL PILLOW
# NEED TO INSTALL PDFKIT

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

@register.filter
def get_item(dictionary, key): return dictionary.get(key)

@login_required
def pacients_view(request):
    pacients_list = Pacient.objects.all()
    studies_list = Studies.objects.all()
    
    ammount_studies = 0
    ammount_studies_dict = {}
    last_studies_date_dict = {}
    last_studies_date = ''
    for pacient in pacients_list:
        ammount_studies = studies_list.filter(pacient_id= pacient.id).count()
        if ammount_studies > 0:
            last_studies_date = studies_list.filter(pacient_id= pacient.id).order_by('date').first()
            last_studies_date = str(last_studies_date.date)
        else:
            ammount_studies = 0
            last_studies_date = ''    
     
        last_studies_date_dict.update({pacient.id : last_studies_date})
        ammount_studies_dict.update({pacient.id : ammount_studies})
        last_studies_date = ''
        ammount_studies = 0

    context = {'pacients_list': pacients_list, 'ammount_studies': ammount_studies_dict,
     'last_studies_date': last_studies_date_dict}
    return render(request,'pacients.html',context)

def pacient_search(request):
    print(request.method)
    if request.method == 'POST':
        data = request.POST.get('data')
        print(data)
        studies_list = Studies.objects.all()

        ammount_studies = 0
        ammount_studies_dict = {}
        last_studies_date_dict = {}
        last_studies_date = ''

        if RepresentsInt(data): pacient_list = list(Pacient.objects.filter(id = data))
        else:
            pacient_list = list(Pacient.objects.filter(name__startswith= data))
            pacient_list.extend(list(Pacient.objects.filter(name_last__startswith= data)))

        for pacient in pacient_list:
            ammount_studies = studies_list.filter(pacient_id = pacient.id).count()
            if ammount_studies > 0:
                last_studies_date = studies_list.filter(pacient_id= pacient.id).order_by('date').first()
                last_studies_date = str(last_studies_date.date)
            else:
                ammount_studies = 0
                last_studies_date = ''
            last_studies_date_dict.update({pacient.id : last_studies_date})
            ammount_studies_dict.update({pacient.id : ammount_studies})
            last_studies_date = ''
            ammount_studies = 0
        context = {'pacient_list': pacient_list,'ammount_studies': ammount_studies_dict,
            'last_studies_date': last_studies_date_dict}
        print (context)
        return render(request, 'pacient_search.html', context)


def pacient_view(request,pacient_id): 
    try:
        pacient = Pacient.objects.filter(id=pacient_id).values()[:1].get()
        studies_list = Studies.objects.filter(pacient_id = pacient_id) #List of pacient's studies
        context = {'pacient':pacient, 'studies_list':studies_list,}
    except Pacient.DoesNotExist:
        raise Http404("Pacient does not exist")
    return render(request, 'pacient.html', context)


def pacient_add(request):
    try:
        if request.method == 'POST':
            new_pacient = Pacient.objects.create(
                id = request.POST.get('id'),
                name = request.POST.get('name'),
                name_second= request.POST.get('name_second'),
                name_last= request.POST.get('name_last'),
                sex= request.POST.get('sex'),
                address= request.POST.get('address'),
                phone= request.POST.get('phone'),
                date_of_birth= request.POST.get('date_of_birth'),
                medical_details= request.POST.get('medical_details'),
                
                smoke= request.POST.get('smoke') == 'on',
                smoke_quantity= None if request.POST.get('smoke_quantity') == '' else request.POST.get('smoke_quantity'),
                smoke_duration= None if request.POST.get('smoke_duration') == '' else request.POST.get('smoke_duration'),
                smoke_quit= None if request.POST.get('smoke_quit') == '' else request.POST.get('smoke_quit'),

                
                diabetes = request.POST.get('diabetes') == 'on',
                diabetes_type= None if request.POST.get('diabetes_type') == '' else request.POST.get('diabetes_type'),
                diabetes_date= None if request.POST.get('diabetes_date') == '' else request.POST.get('diabetes_date'),

                hyper = request.POST.get('hyper') =='on',
                hyper_type= None if request.POST.get('hyper_type') == '' else request.POST.get('hyper_type'),
                hyper_date= None if request.POST.get('hyper_date') == '' else request.POST.get('hyper_date'),

                dislipidemia = request.POST.get('dislipidemia') == 'on',
                dislipidemia_type= None if request.POST.get('dislipidemia_type') == '' else request.POST.get('dislipidemia_type'),
                dislipidemia_date= None if request.POST.get('dislipidemia_date') == '' else request.POST.get('dislipidemia_date'),
                
                irc = request.POST.get('irc') == 'on',
                irc_type= None if request.POST.get('irc_type') == '' else request.POST.get('irc_type'),

                iam = request.POST.get('iam') == 'on',
                acv = request.POST.get('acv') == 'on',
                revasc = request.POST.get('revasc') == 'on',
                enfvp = request.POST.get('enfvp') == 'on',
                acv_ait = request.POST.get('acv_ait') == 'on',
                fecvt = request.POST.get('fecvt') == 'on',
            )

            return redirect('pacient_view', new_pacient.id)
        elif request.method == 'GET':
            return(render(request, 'pacient_add.html'))
    except IntegrityError:
        return HttpResponse("Pacient with the same ID exist")


def pacient_edit(request, pacient_id):
    try:
        pacient = Pacient.objects.filter(id=pacient_id).get()
        print(pacient.smoke)
    except Pacient.DoesNotExist:
        raise Http404("Pacient does not exist")

    if request.method == "GET":
        context = model_to_dict(pacient)
        print(context)
        return render(request,'pacient_edit.html', context)
    
    elif request.method == "POST":
        new_pacient = Pacient.objects.create(
            id = request.POST.get('id'),
            name = request.POST.get('name'),
            name_second= request.POST.get('name_second'),
            name_last= request.POST.get('name_last'),
            sex= request.POST.get('sex'),
            address= request.POST.get('address'),
            phone= request.POST.get('phone'),
            date_of_birth= request.POST.get('date_of_birth'),
            medical_details= request.POST.get('medical_details'),
            
            smoke= request.POST.get('smoke') == 'on',
            smoke_quantity= None if request.POST.get('smoke_quantity') == '' else request.POST.get('smoke_quantity'),
            smoke_duration= None if request.POST.get('smoke_duration') == '' else request.POST.get('smoke_duration'),
            smoke_quit= None if request.POST.get('smoke_quit') == '' else request.POST.get('smoke_quit'),

            
            diabetes = request.POST.get('diabetes') == 'on',
            diabetes_type= None if request.POST.get('diabetes_type') == '' else request.POST.get('diabetes_type'),
            diabetes_date= None if request.POST.get('diabetes_date') == '' else request.POST.get('diabetes_date'),

            hyper = request.POST.get('hyper') =='on',
            hyper_type= None if request.POST.get('hyper_type') == '' else request.POST.get('hyper_type'),
            hyper_date= None if request.POST.get('hyper_date') == '' else request.POST.get('hyper_date'),

            dislipidemia = request.POST.get('dislipidemia') == 'on',
            dislipidemia_type= None if request.POST.get('dislipidemia_type') == '' else request.POST.get('dislipidemia_type'),
            dislipidemia_date= None if request.POST.get('dislipidemia_date') == '' else request.POST.get('dislipidemia_date'),
            
            irc = request.POST.get('irc') == 'on',
            irc_type= None if request.POST.get('irc_type') == '' else request.POST.get('irc_type'),

            iam = request.POST.get('iam') == 'on',
            acv = request.POST.get('acv') == 'on',
            revasc = request.POST.get('revasc') == 'on',
            enfvp = request.POST.get('enfvp') == 'on',
            acv_ait = request.POST.get('acv_ait') == 'on',
            fecvt = request.POST.get('fecvt') == 'on',
        )
        
        return render(request, 'pacient.html', model_to_dict(pacient))


def pacient_delete(request, pacient_id):
        Pacient.objects.filter(id=pacient_id).delete()

        pacients_list = Pacient.objects.all()
        context = {'pacients_list': pacients_list,}
        return redirect('pacients_view')


def study_view(request, pacient_id, studies_id):
    try:
        study = Studies.objects.filter(id=studies_id) [:1].get()
        pacient = Pacient.objects.filter(id=pacient_id) [:1].get()
        context = {'pacient': pacient,'study':study}
    except Studies.DoesNotExist:
        raise Http404("Study does not exist")
    return render(request, 'study.html', context)

def study_add(request, pacient_id):
    pacient = Pacient.objects.filter(id=pacient_id).get()

    if request.method == 'POST':

        #Patient photo
        image_data = request.POST.get('image_data')
        image_data = re.sub("^data:image/png;base64,", "", image_data)
        image_data = base64.b64decode(image_data)
        image_data = BytesIO(image_data)
        im = Image.open(image_data)
        filename = str(pacient) + str(request.POST.get('date')) + '.png'
        tempfile = im
        tempfile_io = BytesIO()
        tempfile.save(tempfile_io, format=im.format)


        new_study = Studies.objects.create(
            pacient=pacient,
            date= request.POST.get('date'),
            
            weight=request.POST.get('weight'),
            height=request.POST.get('height'),
            tas=request.POST.get('tas'),
            tad=request.POST.get('tad'),
            pulse=request.POST.get('pulse'),

            diabetes_chol_level=None if request.POST.get('diabetes_chol_level') == '' else request.POST.get('diabetes_chol_level'),
            diabetes_hdl_level=None if request.POST.get('diabetes_hdl_level') == '' else request.POST.get('diabetes_hdl_level'),
            diabetes_ldl_level=None if request.POST.get('diabetes_ldl_level') == '' else request.POST.get('diabetes_ldl_level'),
            diabetes_tri_level=None if request.POST.get('diabetes_tri_level') == '' else request.POST.get('diabetes_tri_level'),

            glucemia=request.POST.get('glucemia'),
            hba1c=request.POST.get('hba1c'),
            ac_uric=request.POST.get('ac_uric'),
            creat=request.POST.get('creat'),
            tsh=request.POST.get('tsh'),
            pcr=request.POST.get('pcr'),

            comments= None if request.POST.get('comments') == '' else request.POST.get('comments'),
        )
        new_study.photo.save(filename, ContentFile(tempfile_io.getvalue()) , save = True) #save the photo
        
        return redirect('study_view', pacient.id, new_study.id)
    else:
        pacient = Pacient.objects.filter(id=pacient_id).get()
        context = {'pacient': pacient}
        return render(request,'study_add.html', context)

def study_edit(request, pacient_id, studies_id):
    try:
        pacient = Pacient.objects.filter(id=pacient_id)
        study_list = Studies.objects.filter(pacient=pacient_id)
        study = Studies.objects.filter(id=studies_id).get()
        pacient = pacient.get()
        context = {'pacient':pacient ,'study':study}
        print(study)
    except Studies.DoesNotExist:
        raise Http404("Study does not exist")

    if request.method == "GET":
        print(context)
        return render(request,'study_edit.html', context)
    
    elif request.method == "POST":
        new_study = Studies.objects.create(
            pacient=pacient,
            date= request.POST.get('date'),
            
            weight=request.POST.get('weight'),
            height=request.POST.get('height'),
            tas=request.POST.get('tas'),
            tad=request.POST.get('tad'),
            pulse=request.POST.get('pulse'),

            diabetes_chol_level=None if request.POST.get('diabetes_chol_level') == '' else request.POST.get('diabetes_chol_level'),
            diabetes_hdl_level=None if request.POST.get('diabetes_hdl_level') == '' else request.POST.get('diabetes_hdl_level'),
            diabetes_ldl_level=None if request.POST.get('diabetes_ldl_level') == '' else request.POST.get('diabetes_ldl_level'),
            diabetes_tri_level=None if request.POST.get('diabetes_tri_level') == '' else request.POST.get('diabetes_tri_level'),

            glucemia=request.POST.get('glucemia'),
            hba1c=request.POST.get('hba1c'),
            ac_uric=request.POST.get('ac_uric'),
            creat=request.POST.get('creat'),
            tsh=request.POST.get('tsh'),
            pcr=request.POST.get('pcr'),

            comments=None if request.POST.get('comments') == 'None' else request.POST.get('comments'),
        )
        
        return render(request, 'study.html', context)

def study_delete(request, studies_id, pacient_id):
    study = Studies.objects.filter(id=studies_id).delete()
    studies = Studies.objects.filter(pacient=pacient_id)
    context = {'studies': studies}
    return redirect('pacient_view', pacient_id)

def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    p.drawString(100, 100, 'Hello world.')
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

