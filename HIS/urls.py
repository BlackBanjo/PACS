from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prijava', views.prijava, name='prijava'),
    path('pacientForm', views.pacientForm, name='pacientForm'),
    path('uvodna', views.uvod, name='uvod'),
    path('seznamPacientov', views.seznamPacient, name='seznam_pacientov'),
    path('pacient/<int:pk>/', views.pacientPodrobnost, name='pacient'),
    path('pregledForm/<int:pk>/', views.pregledForm, name='pregledForm'),
    path('pregledSprememba/<int:pk>/', views.pregledSpremeni, name='pregledSpremeni'),
    path('pregledIzbrisi/<int:pk>/', views.pregledIzbrisi, name='pregledIzbrisi'),
    path('seznamPregledov', views.seznamPregled, name='seznam_pregledov'),
    path('pregled/<int:pk>/', views.pregledPodrobnost, name='pregled'),

    # user auth urls
    path('HIS/auth/', views.auth_view),
    path(r'^logout/$', views.logout, name='odjava'),
    path(r'^loggedin/$', views.loggedin),
]

admin.site.index_title = "Admin"
admin.site.site_title = "Admin"