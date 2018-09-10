from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pacient_id>/', views.pacient_view, name='pacient_view'),
    path('pacientes', views.pacients_view, name='pacients_view'),
]