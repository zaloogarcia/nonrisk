from django.urls import path

from . import views

urlpatterns = [
    # Companies level
    path('', views.companies_view, name='companies_view'),
    path('add/company', views.company_add, name='company_add'),
    path('search/company', views.company_search, name= 'company_search'),
    path('search/patient', views.patient_search, name= 'patient_search'),
    # Company level 
    path('<int:company_id>/edit', views.company_edit, name='company_edit'),
    path('<int:company_id>/delete', views.company_delete, name='company_delete'),
    path('<int:company_id>/patients', views.company_view, name='company_view'),
    path('<int:company_id>/add-patient', views.patient_add, name='patient_add'),
    # Patient level
    path('<int:company_id>/<int:patient_id>', views.patient_view, name='patient_view'),
    path('<int:company_id>/<int:patient_id>/edit', views.patient_edit, name='patient_edit'),
    path('<int:company_id>/<int:patient_id>/delete', views.patient_delete, name='patient_delete'),
    path('<int:company_id>/<int:patient_id>/add', views.study_add, name='study_add'),
    # Study level
    path('<int:company_id>/<int:patient_id>/<int:studies_id>', views.study_view, name='study_view'),
    path('<int:company_id>/<int:patient_id>/<int:studies_id>/pdf', views.export_pdf, name='export_pdf'),
    path('<int:company_id>/<int:patient_id>/<int:studies_id>/edit', views.study_edit, name='study_edit'),
    path('<int:company_id>/<int:patient_id>/<int:studies_id>/delete', views.study_delete, name='study_delete'),
]

