import re, math, base64, tkinter, matplotlib, io
from io import *
from PIL import Image
matplotlib.use('Agg')
from matplotlib import pylab
from pylab import *
from django.http import *
from .models import *
from .forms import *
import xhtml2pdf.pisa as pisa
from datetime import date, datetime
from django.template import loader
from weasyprint import HTML, CSS
from reportlab.pdfgen import canvas
from django.http import FileResponse, HttpResponse
from django.db import IntegrityError
from django.views.generic import View
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from dateutil.relativedelta import relativedelta
from django.template.loader import get_template
from django.template.defaulttags import register
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile

# NEED TO INSTALL: - PILLOW
#                  - PDFKIT
#                  - REPORTLAB
#                  - xhtml2pdf
#                  - matplotlib
#                  -sudo apt-get install python3-tk
#                  -sudo apt-get install libcairo2-dev
#                  -django-cleanup
#                  -weasyprint


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
def companies_view(request):
    companies_list = Company.objects.all()
    patient_list = Patient.objects.all()

    ammount_patients = 0
    ammount_patients_dict = {}
    for company in companies_list:
        ammount_patients = patient_list.filter(company_id = company.id).count()
        ammount_patients_dict.update({company.id : ammount_patients})
        ammount_patients = 0
    context = {'companies_list':companies_list, 'ammount_patients':ammount_patients_dict}
    return render(request, 'companies.html', context)

@login_required
def company_add(request):
    if request.method == 'POST':
        new_company = Company.objects.create(
            name = request.POST.get('name'))
        new_company.logo=request.FILES['logo']
        new_company.save()

        return redirect('company_view', new_company.id)
    elif request.method == 'GET':
        return(render(request, 'company_add.html'))

@login_required
def company_edit(request, company_id):
    company = Company.objects.filter(id=company_id).values() [:1].get()
    
    if request.method == 'GET':
        context = {'company': company}
        return(render(request, 'company_edit.html',context))
    
    if request.method == 'POST':
        company = Company.objects.filter(id=company_id).get()
        company.name = request.POST.get('name')
        company.save()
        return redirect('company_view', company.id)
            
@login_required
def company_search(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        companies_list = Company.objects.all()

        if RepresentsInt(data): 
            companies_list = list(Company.object.filter(id=data))
        else:  
            companies_list = list(Company.objects.filter(name__startswith=data))
        context = { 'companies_list': companies_list}            
        return render(request, 'company_search.html', context)

# Terminar company_view
@login_required
def company_view(request, company_id):
    company = Company.objects.filter(id=company_id) [:1].get()
    patients_list = Patient.objects.filter(company=company)
    studies_list = Studies.objects.all()
    
    ammount_studies = 0
    ammount_studies_dict = {}
    last_studies_date_dict = {}
    last_studies_date = ''
    for patient in patients_list:
        ammount_studies = studies_list.filter(patient_id= patient.id).count()
        if ammount_studies > 0:
            last_studies_date = studies_list.filter(patient_id= patient.id).order_by('date').last()
            last_studies_date = str(last_studies_date.date)
        else:
            ammount_studies = 0
            last_studies_date = ''    
     
        last_studies_date_dict.update({patient.id : last_studies_date})
        ammount_studies_dict.update({patient.id : ammount_studies})
        last_studies_date = ''
        ammount_studies = 0

    context = {'patients_list': patients_list, 'ammount_studies': ammount_studies_dict,
     'last_studies_date': last_studies_date_dict, 'company':company}
    return render(request,'company.html',context)

@login_required
def company_delete(request, company_id):
        Company.objects.filter(id=company_id).delete()

        return redirect('companies_view')

@login_required
def patient_search(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        studies_list = Studies.objects.all()

        ammount_studies = 0
        ammount_studies_dict = {}
        last_studies_date_dict = {}
        last_studies_date = ''

        if RepresentsInt(data): patient_list = list(Patient.objects.filter(id = data))
        else:
            patient_list = list(Patient.objects.filter(name__startswith= data))
            patient_list.extend(list(Patient.objects.filter(name_last__startswith= data)))

        for patient in patient_list:
            ammount_studies = studies_list.filter(patient_id = patient.id).count()
            if ammount_studies > 0:
                last_studies_date = studies_list.filter(patient_id= patient.id).order_by('date').first()
                last_studies_date = str(last_studies_date.date)
            else:
                ammount_studies = 0
                last_studies_date = ''
            last_studies_date_dict.update({patient.id : last_studies_date})
            ammount_studies_dict.update({patient.id : ammount_studies})
            last_studies_date = ''
            ammount_studies = 0
        context = {'patient_list': patient_list,'ammount_studies': ammount_studies_dict,
            'last_studies_date': last_studies_date_dict}
        return render(request, 'patient_search.html', context)

@login_required
def patient_view(request,company_id, patient_id): 
    try:
        company = Company.objects.filter(id=company_id).values() [:1].get()
        patient = Patient.objects.filter(id=patient_id).values()[:1].get()
        studies_list = Studies.objects.filter(patient_id = patient_id) #List of patient's studies
        context = {'company': company, 'patient':patient, 'studies_list':studies_list,}
    except Patient.DoesNotExist:
        raise Http404("Patient does not exist")
    return render(request, 'patient.html', context)

@login_required
def patient_add(request, company_id):
    company = Company.objects.filter(id=company_id).get()
    try:
        if request.method == 'POST':
            new_patient = Patient.objects.create(
                company = company,
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

            return redirect('patient_view', company.id, new_patient.id)
        elif request.method == 'GET':
            context = {'company' : company}
            return(render(request, 'patient_add.html', context
                ))
    except IntegrityError:
        return HttpResponse("Patient with the same ID exist")

@login_required
def patient_edit(request, company_id, patient_id):
    try:
        patient = Patient.objects.filter(id=patient_id).values()[:1].get()
        company = Company.objects.filter(id=company_id).values()[:1].get()
    except Patient.DoesNotExist:
        raise Http404("Patient does not exist")

    if request.method == "GET":
        context = {'patient':patient, 'company':company}
        return render(request,'patient_edit.html', context)
    
    elif request.method == "POST":
        # print(request.POST.get('id'), patient.id)
        patient = Patient.objects.filter(id=patient_id).get()

        patient.id                = request.POST.get('id')
        patient.name              = request.POST.get('name')
        patient.name_second       = request.POST.get('name_second')
        patient.name_last         = request.POST.get('name_last')
        patient.sex               = request.POST.get('sex')
        patient.address           = request.POST.get('address')
        patient.phone             = request.POST.get('phone')
        patient.date_of_birth     = request.POST.get('date_of_birth')
        patient.medical_details   = request.POST.get('medical_details')
        patient.smoke             = request.POST.get('smoke')        == 'on'
        patient.diabetes          = request.POST.get('diabetes')     == 'on'
        patient.hyper             = request.POST.get('hyper')        == 'on'
        patient.dislipidemia      = request.POST.get('dislipidemia') == 'on'
        patient.irc               = request.POST.get('irc')          == 'on'
        patient.iam               = request.POST.get('iam')          == 'on'
        patient.acv               = request.POST.get('acv')          == 'on'
        patient.revasc            = request.POST.get('revasc')       == 'on'
        patient.enfvp             = request.POST.get('enfvp')        == 'on'
        patient.acv_ait           = request.POST.get('acv_ait')      == 'on'
        patient.fecvt             = request.POST.get('fecvt')        == 'on'
        patient.smoke_quantity    = None if request.POST.get('smoke_quantity')    == '' else request.POST.get('smoke_quantity')
        patient.smoke_duration    = None if request.POST.get('smoke_duration')    == '' else request.POST.get('smoke_duration')
        patient.smoke_quit        = None if request.POST.get('smoke_quit')        == '' else request.POST.get('smoke_quit')
        patient.diabetes_type     = None if request.POST.get('diabetes_type')     == '' else request.POST.get('diabetes_type')
        patient.diabetes_date     = None if request.POST.get('diabetes_date')     == '' else request.POST.get('diabetes_date')
        patient.hyper_type        = None if request.POST.get('hyper_type')        == '' else request.POST.get('hyper_type')
        patient.hyper_date        = None if request.POST.get('hyper_date')        == '' else request.POST.get('hyper_date')
        patient.irc_type          = None if request.POST.get('irc_type')          == '' else request.POST.get('irc_type')
        patient.dislipidemia_type = None if request.POST.get('dislipidemia_type') == '' else request.POST.get('dislipidemia_type')
        patient.dislipidemia_date = None if request.POST.get('dislipidemia_date') == '' else request.POST.get('dislipidemia_date')
        patient.save()
        return redirect('patient_view', company_id, patient_id)

@login_required
def patient_delete(request, company_id, patient_id):
        Patient.objects.filter(id=patient_id).delete()

        return redirect('company_view', company_id)

@login_required
def study_view(request, company_id, patient_id, studies_id):
    try:
        study = Studies.objects.filter(id=studies_id)[:1].get()
        patient = Patient.objects.filter(id=patient_id)[:1].get()
        company = Company.objects.filter(id=company_id)[:1].get()
        context = {'company':company,'patient': patient,'study':study}
    except Studies.DoesNotExist:
        raise Http404("Study does not exist")
    return render(request, 'study.html', context)

@login_required
def study_add(request, company_id, patient_id):
    company = Company.objects.filter(id=company_id).get()
    patient = Patient.objects.filter(id=patient_id).get()

    if request.method == 'POST':

        #Patient photo
        image_data = request.POST.get('image_data')
        image_data = re.sub("^data:image/png;base64,", "", image_data)
        image_data = base64.b64decode(image_data)
        image_data = BytesIO(image_data)
        im = Image.open(image_data)
        filename = 'Arterias-'+ str(patient.id) + '-' + str(request.POST.get('date')) + '.png'
        tempfile = im
        tempfile_io = BytesIO()
        tempfile.save(tempfile_io, format=im.format)

        # Graphic chart
        leftarea = request.POST.get('areaizquierda')
        rightarea = request.POST.get('areaderecha')
        totalarea = float(leftarea) + float(rightarea)
        age = ageFromDate(patient.date_of_birth)

        xlabel('Edad')
        ylabel('Area total de Ateroclerosis(mm²)')
        title('Promedio de Area de Placa por Edad/Sexo')

        # Prevencion primaria
        # Women
        if (patient.iam or patient.acv or patient.revasc or patient.enfvp or patient.acv_ait):
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
        figurename = 'Grafico-'+ str(patient.id) + '-' + str(request.POST.get('date')) + '.png'

        # Closes chart plot
        plt.clf()

        # Arterial Age update and Renal filter Update
        scr = float(request.POST.get('creat'))
        renalFilter = 0
        if patient.sex == 'M' :
            arterialAge = round(((math.log(totalarea/5.4175))/0.0426))
            
            if patient.race == 'B': #Black
                renalFilter = 141 * (min((scr/ 0.9), 1)**(-0.411))* (max(scr/0.9, 1)**(-1.209))* (0.993 ** float(age)) * 1.159
            elif patient.race == 'W': #White
                renalFilter = 141 * (min((scr/ 0.9), 1)**(-0.411))* (max(scr/0.9, 1)**(-1.209))* (0.993 ** float(age))

        elif patient.sex == 'F':
            arterialAge = round(((math.log(totalarea/4.1942))/0.0392),4)
            if patient.race == 'B':
                renalFilter = 141 * (min((scr/ 0.7), 1)**(-0.329))* (max(scr/0.9, 1)**(-1.209))* (0.993 ** float(age)) *1.018 * 1.159
            elif patient.race == 'W':
                renalFilter = 141 * (min((scr/ 0.9), 1)**(-0.329))* (max(scr/0.9, 1)**(-1.209))* (0.993 ** float(age)) * 1.018 

        Patient.objects.filter(id=patient_id).update(arterial_age= arterialAge)


        new_study = Studies.objects.create(
            patient=patient,
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
        print(filename)
        new_study.photo.save(filename, ContentFile(tempfile_io.getvalue()) , save = True) #save the photo
        new_study.graphic.save(figurename, ContentFile(buffer.getvalue()) , save = True) #save the photo

        
        return redirect('study_view', company.id, patient.id, new_study.id)
    else:
        company = Company.objects.filter(id=company_id).get()
        patient = Patient.objects.filter(id=patient_id).get()
        context = {'company':company, 'patient': patient}
        return render(request,'study_add.html', context)

@login_required
def study_edit(request, company_id, patient_id, studies_id):
    try:
        company    = Company.objects.filter(id=company_id)[:1].get()
        patient    = Patient.objects.filter(id=patient_id)
        study_list = Studies.objects.filter(patient=patient_id)
        study      = Studies.objects.filter(id=studies_id).get()
        patient    = patient.get()
        context    = {'company':company,'patient':patient ,'study':study}

    except Studies.DoesNotExist:
        raise Http404("Study does not exist")

    if request.method == "GET":
        print(context)
        return render(request,'study_edit.html', context)
    
    elif request.method == "POST":
        study.date      = request.POST.get('date')
        study.doctor    = request.POST.get('doctor')     
        study.weight    = request.POST.get('weight')
        study.height    = request.POST.get('height')
        study.tas       = request.POST.get('tas')
        study.tad       = request.POST.get('tad')
        study.pulse     = request.POST.get('pulse')
        study.glucemia  = request.POST.get('glucemia')
        study.hba1c     = request.POST.get('hba1c')
        study.ac_uric   = request.POST.get('ac_uric')
        study.creat     = request.POST.get('creat')
        study.tsh       = request.POST.get('tsh')
        study.pcr       = request.POST.get('pcr')
        study.chol_level= None if request.POST.get('chol_level') == '' else request.POST.get('chol_level')
        study.hdl_level = None if request.POST.get('hdl_level')  == '' else request.POST.get('hdl_level')
        study.ldl_level = None if request.POST.get('ldl_level')  == '' else request.POST.get('ldl_level')
        study.tri_level = None if request.POST.get('tri_level')  == '' else request.POST.get('tri_level')
        study.comments  = None if request.POST.get('comments')   == 'None' else request.POST.get('comments')
        study.save()
        return render(request, 'study.html', context)

@login_required
def study_delete(request, company_id, studies_id, patient_id):
    study = Studies.objects.filter(id=studies_id).delete()
    studies = Studies.objects.filter(patient=patient_id)
    context = {'studies': studies}
    return redirect('patient_view', company_id, patient_id)

@login_required
def export_pdf(request, company_id, patient_id, studies_id):
    template = get_template('pdf2.html')
    company = Company.objects.filter(id=company_id)[:1].get()
    patient = Patient.objects.filter(id = patient_id) [:1].get()
    studies = Studies.objects.filter(id = studies_id) [:1].get()

    if patient.smoke:
        years = relativedelta(patient.smoke_quit, patient.smoke_duration).years
    else:
        years = 0

    # Company logo
    with open(str(company.logo.path), "rb") as image_file:
        encoded1 = base64.b64encode(image_file.read())
    encoded1 = encoded1.decode()
    url_logo = 'data:image/png;base64,{}'.format(encoded1)

    # Patient drawing
    with open(str(studies.photo.path), "rb") as image_file:
        encoded2 = base64.b64encode(image_file.read())
    encoded2= encoded2.decode()
    url_photo = 'data:image/png;base64,{}'.format(encoded2)

    # Patient chart
    with open(str(studies.graphic.path), "rb") as image_file:
        encoded3 = base64.b64encode(image_file.read())
    encoded3 = encoded3.decode()
    url_graphic = 'data:image/png;base64,{}'.format(encoded3)


    context = {'patient':patient, 'studies':studies, 'photo': url_photo,
               'graphic': url_graphic,'logo': url_logo, 'smoke_years': years}

    html = template.render(context)
    # response = BytesIO()
    # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    pdf = HTML(string=html).write_pdf(presentational_hints=True)
    # if not pdf.err:
        # response = HttpResponse(response.get_value(), content_type='application/pdf')
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Estudio.pdf'
    return response
    # else:
        # return HttpResponse("Error Rendering PDF", status=400)


