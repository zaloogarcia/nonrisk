from django.urls import path

from . import views

urlpatterns = [
    path('pacient/<int:pacient_id>', views.pacient_view, name='pacient_view'),
    path('', views.pacients_view, name='pacients_view'),
    path('search/pacient', views.pacient_search, name= 'pacient_search'),
    path('add/pacient', views.pacient_add, name='pacient_add'),
    path('pacient/<int:pacient_id>/edit', views.pacient_edit, name='pacient_edit'),
    path('pacient/<int:pacient_id>/delete', views.pacient_delete, name='pacient_delete'),
    path('pacient/<int:pacient_id>/add', views.study_add, name='study_add'),
    path('pacient/<int:pacient_id>/<int:studies_id>', views.study_view, name='study_view'),
    path('pacient/<int:pacient_id>/<int:studies_id>/pdf', views.export_pdf, name='export_pdf'),
    path('pacient/<int:pacient_id>/<int:studies_id>/edit', views.study_edit, name='study_edit'),
    path('pacient/<int:pacient_id>/<int:studies_id>/delete', views.study_delete, name='study_delete'),
]

