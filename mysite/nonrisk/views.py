from django.core import serializers
import re
import math
import base64
import tkinter
import io
from io import *
import PIL
from PIL import Image
import matplotlib
matplotlib.use('Agg')
from matplotlib import pylab
from pylab import *
from django.http import *
from nonrisk.forms import *
import xhtml2pdf.pisa as pisa
from nonrisk.models import *
from datetime import date
from datetime import datetime
from django.template import loader
from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.db import IntegrityError
from django.views.generic import View
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from dateutil.relativedelta import relativedelta
from django.template.loader import get_template
from django.template.defaulttags import register
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.files.images import ImageFile

# NEED TO INSTALL: - PILLOW
#                  - PDFKIT
#                  - REPORTLAB
#                  - xhtml2pdf
#                  - matplotlib
#                  -sudo apt-get install python3-tk
#                  -django-cleanup


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def ageFromDate(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

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
            last_studies_date = studies_list.filter(pacient_id= pacient.id).order_by('date').last()
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

@login_required
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

@login_required
def pacient_view(request,pacient_id): 
    try:
        pacient = Pacient.objects.filter(id=pacient_id).values()[:1].get()
        studies_list = Studies.objects.filter(pacient_id = pacient_id) #List of pacient's studies
        context = {'pacient':pacient, 'studies_list':studies_list,}
    except Pacient.DoesNotExist:
        raise Http404("Pacient does not exist")
    return render(request, 'pacient.html', context)

@login_required
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
                race = request.POST.get('race'),
                arterial_age = 0,
                
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

@login_required
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
            arterial_age = pacient.arterial_age,
            
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

@login_required
def pacient_delete(request, pacient_id):
        Pacient.objects.filter(id=pacient_id).delete()

        pacients_list = Pacient.objects.all()
        context = {'pacients_list': pacients_list,}
        return redirect('pacients_view')

@login_required
def study_view(request, pacient_id, studies_id):
    try:
        study = Studies.objects.filter(id=studies_id) [:1].get()
        pacient = Pacient.objects.filter(id=pacient_id) [:1].get()
        context = {'pacient': pacient,'study':study}
    except Studies.DoesNotExist:
        raise Http404("Study does not exist")
    return render(request, 'study.html', context)

@login_required
def study_add(request, pacient_id):
    pacient = Pacient.objects.filter(id=pacient_id).get()

    if request.method == 'POST':

        #Patient photo
        image_data = request.POST.get('image_data')
        image_data = re.sub("^data:image/png;base64,", "", image_data)
        image_data = base64.b64decode(image_data)
        image_data = BytesIO(image_data)
        im = Image.open(image_data)
        filename = 'Arterias-'+ str(pacient.id) + '-' + str(request.POST.get('date')) + '.png'
        tempfile = im
        tempfile_io = BytesIO()
        tempfile.save(tempfile_io, format=im.format)

        # Graphic chart
        leftarea = request.POST.get('areaizquierda')
        rightarea = request.POST.get('areaderecha')
        totalarea = float(leftarea) + float(rightarea)
        age = ageFromDate(pacient.date_of_birth)

        xlabel('Edad')
        ylabel('Area total de Ateroclerosis(mm²)')
        title('Promedio de Area de Placa por Edad/Sexo')

        # Prevencion primaria
        # Women
        if (pacient.iam or pacient.acv or pacient.revasc or pacient.enfvp or pacient.acv_ait):
            plt.plot(age, totalarea, 'ro', label='Usted')
            plt.plot([30,  38.0, 43, 48, 53, 58, 63, 68, 73, 78],
                     [10, 18, 25, 36, 45, 75, 100, 108, 130, 160],
                     color='grey', marker='o',linestyle='None', label='Mujeres')
            # Men
            plt.plot([36, 40, 45, 50, 55, 60,  65,   70, 75,  80],
                     [15, 20, 40, 55, 90, 125, 160, 190, 210, 248],
                     'ko', label='Hombres')
            plt.legend(loc='best')
            plt.axis([25, 85, -5, 260])

        # Prevencion secundaria
        else:
            plt.plot(age, totalarea, 'ro', label='Usted')
            plt.plot([28.63,  38.0,   43.0,   48.0,   53.0,   58.0,    63.0,    68.0,    73.0,    77.0],
                     [2.4561, 2.4561, 2.8070, 2.8070, 4.9123, 11.9298, 15.4386, 22.1053, 32.2807, 41.4035],
                     color='grey', marker='o',linestyle='None', label='Mujeres')
            # Men
            plt.plot([36,     40,     45,     50,     55,      60,      65,      70,      75,      79],
                     [2.4561, 2.8070, 5.6140, 9.8246, 14.7368, 18.2456, 29.4737, 39.2982, 44.5614, 78.2456],
                     'ko', label='Hombres')           
            plt.legend(loc='best')
            plt.axis([25, 85, -5, 80])


        # Store Chart in a string buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        figure = ImageFile(buffer)
        figurename = 'Grafico-'+ str(pacient.id) + '-' + str(request.POST.get('date')) + '.png'

        # Closes chart plot
        plt.clf()

        # Arterial Age update and Renal filter Update
        scr = float(request.POST.get('creat'))
        renalFilter = 0
        if pacient.sex == 'M' :
            arterialAge = round(((math.log(totalarea/5.4175))/0.0426))
            
            if pacient.race == 'B': #Black
                renalFilter = 141 * (min((scr/ 0.9), 1)**(-0.411))* (max(scr/0.9, 1)**(-1.209))* (0.993 ** float(age)) * 1.159
            elif pacient.race == 'W': #White
                renalFilter = 141 * (min((scr/ 0.9), 1)**(-0.411))* (max(scr/0.9, 1)**(-1.209))* (0.993 ** float(age))

        elif pacient.sex == 'F':
            arterialAge = round(((math.log(totalarea/4.1942))/0.0392),4)
            if pacient.race == 'B':
                renalFilter = 141 * (min((scr/ 0.7), 1)**(-0.329))* (max(scr/0.9, 1)**(-1.209))* (0.993 ** float(age)) *1.018 * 1.159
            elif pacient.race == 'W':
                renalFilter = 141 * (min((scr/ 0.9), 1)**(-0.329))* (max(scr/0.9, 1)**(-1.209))* (0.993 ** float(age)) * 1.018 

        Pacient.objects.filter(id=pacient_id).update(arterial_age= arterialAge)


        new_study = Studies.objects.create(
            pacient=pacient,
            date= request.POST.get('date'),
            doctor=request.POST.get('doctor'),
            
            weight=request.POST.get('weight'),
            height=request.POST.get('height'),
            tas=request.POST.get('tas'),
            tad=request.POST.get('tad'),
            pulse=request.POST.get('pulse'),
            renal_filter= round(renalFilter),

            chol_level=None if request.POST.get('chol_level') == '' else request.POST.get('chol_level'),
            hdl_level=None if request.POST.get('hdl_level') == '' else request.POST.get('hdl_level'),
            ldl_level=None if request.POST.get('ldl_level') == '' else request.POST.get('ldl_level'),
            tri_level=None if request.POST.get('tri_level') == '' else request.POST.get('tri_level'),

            glucemia=request.POST.get('glucemia'),
            hba1c=request.POST.get('hba1c'),
            ac_uric=request.POST.get('ac_uric'),
            creat=request.POST.get('creat'),
            tsh=request.POST.get('tsh'),
            pcr=request.POST.get('pcr'),

            comments= None if request.POST.get('comments') == '' else request.POST.get('comments'),
        )
        new_study.photo.save(filename, ContentFile(tempfile_io.getvalue()) , save = True) #save the photo
        new_study.graphic.save(figurename, ContentFile(buffer.getvalue()) , save = True) #save the photo

        
        return redirect('study_view', pacient.id, new_study.id)
    else:
        pacient = Pacient.objects.filter(id=pacient_id).get()
        context = {'pacient': pacient}
        return render(request,'study_add.html', context)

@login_required
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
            doctor=request.POST.get('doctor'),
            
            weight=request.POST.get('weight'),
            height=request.POST.get('height'),
            tas=request.POST.get('tas'),
            tad=request.POST.get('tad'),
            pulse=request.POST.get('pulse'),

            chol_level=None if request.POST.get('chol_level') == '' else request.POST.get('chol_level'),
            hdl_level=None if request.POST.get('hdl_level') == '' else request.POST.get('hdl_level'),
            ldl_level=None if request.POST.get('ldl_level') == '' else request.POST.get('ldl_level'),
            tri_level=None if request.POST.get('tri_level') == '' else request.POST.get('tri_level'),

            glucemia=request.POST.get('glucemia'),
            hba1c=request.POST.get('hba1c'),
            ac_uric=request.POST.get('ac_uric'),
            creat=request.POST.get('creat'),
            tsh=request.POST.get('tsh'),
            pcr=request.POST.get('pcr'),

            comments=None if request.POST.get('comments') == 'None' else request.POST.get('comments'),
        )
        
        return render(request, 'study.html', context)

@login_required
def study_delete(request, studies_id, pacient_id):
    study = Studies.objects.filter(id=studies_id).delete()
    studies = Studies.objects.filter(pacient=pacient_id)
    context = {'studies': studies}
    return redirect('pacient_view', pacient_id)

@login_required
def export_pdf(request, pacient_id, studies_id):
    template = get_template('pdf.html')
    pacient = Pacient.objects.filter(id = pacient_id) [:1].get()
    studies = Studies.objects.filter(id = studies_id) [:1].get()

    if pacient.smoke:
        years = relativedelta(pacient.smoke_quit, pacient.smoke_duration).years
        print(years)
    else:
        years = 0
    # Patient drawing
    with open(str(studies.photo.path), "rb") as image_file:
        encoded = base64.b64encode(image_file.read())
    encoded= encoded.decode()
    url_photo = 'data:image/png;base64,{}'.format(encoded)

    # Patient chart
    with open(str(studies.graphic.path), "rb") as image_file:
        encoded2 = base64.b64encode(image_file.read())
    encoded2 = encoded2.decode()
    url_graphic = 'data:image/png;base64,{}'.format(encoded2)


    context = {'pacient':pacient, 'studies':studies, 'photo': url_photo,
               'graphic': url_graphic, 'smoke_years': years}

    html = template.render(context)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        response = HttpResponse(response.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Estudio.pdf'
        return response
    else:
        return HttpResponse("Error Rendering PDF", status=400)


