from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context, Template
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
import datetime

from hl7apy import core
from hl7 import client

from .form import *
from .models import *
from .filters import *

global nazivOrganizacije
global naslovAE_Strani
global port_Strani
global IP_Server
global port_Server
global naslovAE_Server
global hl7_remove
nazivOrganizacije = "bolnica"
naslovAE_Strani = "RIS"
port_Strani = 2000
IP_Server = "localhost"
port_Server = 8080
naslovAE_Server = "PACS"

global pregled_odstrani
pregled_odstrani = ""


def zacniHL7():
    hl = core.Message("ORM_O01")
    hl.msh.msh_4 = nazivOrganizacije
    hl.msh.msh_9 = "ORM^O01"
    hl.msh.msh_10 = "168715"
    hl.msh.msh_11 = "P"
    return hl

def posljiSporocilo(sporocilo):
    with (client.MLLPClient(IP_Server, port_Server)) as nov:
        nov.send_message(sporocilo)
        nov.close()
    return

def index(request):
    template_name = 'indeks.html'
    def get(self, request, redirect_authenticated_user):   #DELA OK za prijavljene
        if request.user:
            # If a user is logged in, redirect them to a page informing them of such
            return render(request, template_name)
    return render(request, template_name)


def uvod(request):
    template_name = 'osnova.html'
    return render(request, template_name)


def pacientForm(request):
    template_name = 'pacientForm.html'
    if request.method == "POST":
        form = PacientForm(request.POST)
        if form.is_valid():
            pacient = form.save(commit=False)
            pacient.save()
            return redirect('/seznamPacientov')
    else:
        form = PacientForm()
    return render(request, template_name, {'form': form})


def pacientPodrobnost(request, pk):
    pacient = get_object_or_404(Pacient, id=pk)
    return render(request, 'pacientPodrobnost.html', {'pacient': pacient})


def seznamPacient(request):
    template_name = 'seznamPacientov.html'
    seznam = Pacient.objects.all()
    pacient_filter = PacientFilter(request.GET, queryset=seznam)
    context = dict({'pacient_seznam': pacient_filter})
    return render(request, template_name, context)


def seznamPregled(request):
    template_name = 'seznamPregledov.html'
    seznam = Pregled.objects.filter()
    seznam_filter = PregledFilter(request.GET, queryset=seznam)
    context = dict({'pregled_seznam': seznam_filter})
    return render(request, template_name, context)


def pregledForm(request, pk):
    template_name = 'pregledForm.html'
    if request.method == "POST":
        dobi_pacienta = get_object_or_404(Pacient, id=pk)
        form = PregledForm(request.POST)
        if form.is_valid():
            pregled = form.save(commit=True)
            pregled.pregledDatum = timezone.now()
            pregled.pacient = dobi_pacienta

            #dodaj novo
            hl_sporocilo = zacniHL7()
            hl_sporocilo.add_group("ORM_O01_ORDER")
            hl_sporocilo.ORM_O01_ORDER.ORC.orc_1 = "NW"
            hl_sporocilo.ORM_O01_ORDER.ORC.orc_2 = "ORD-" + str(pregled.id)
            hl_sporocilo.ORM_O01_ORDER.ORC.orc_3 = "ORD-" + str(pregled.id)

            hl_sporocilo.add_group("ORM_O01_PATIENT")
            hl_sporocilo.ORM_O01_PATIENT.pid.pid_3 = str(dobi_pacienta.id)
            hl_sporocilo.ORM_O01_PATIENT.pid.pid_5 = dobi_pacienta.priimek + '^' + dobi_pacienta.ime
            hl_sporocilo.ORM_O01_PATIENT.pid.pid_6 = str(dobi_pacienta.rojstniDatum.year) + str(dobi_pacienta.rojstniDatum.month) + str(dobi_pacienta.rojstniDatum.day)
            hl_sporocilo.ORM_O01_PATIENT.pid.pid_8 = dobi_pacienta.spol

            for slikanje in pregled.tipSlikanja.all():
                obr = core.Segment('OBR')
                obr.obr_4 = slikanje.koda
                obr.obr_39 = slikanje.opis
                hl_sporocilo.add(obr)

            posljiSporocilo(hl_sporocilo)
            pregled.save()

            return redirect('/seznamPregledov')
    else:
        form = PregledForm()
    return render(request, template_name, {'form': form})


def pregledSpremeni(request, pk):
    global pregled_odstrani
    template_name = 'pregledForm.html'
    pregled = get_object_or_404(Pregled, id=pk)

    print(pregled.id)
    if request.method == "POST":
        form = PregledForm(request.POST, instance=pregled)
        if form.is_valid():
            pregled = form.save(commit=True)
            pregled.pregledDatum = timezone.now()
            dobi_pacienta = pregled.pacient

            #izbrisi staro
            hl_sporocilo = zacniHL7()
            hl_sporocilo.add_group("ORM_O01_ORDER")
            hl_sporocilo.ORM_O01_ORDER.ORC.orc_1 = "CA"
            hl_sporocilo.ORM_O01_ORDER.ORC.orc_2 = "ORD-" + str(pregled_odstrani.id)
            hl_sporocilo.ORM_O01_ORDER.ORC.orc_3 = "ORD-" + str(pregled_odstrani.id)

            hl_sporocilo.add_group("ORM_O01_PATIENT")
            hl_sporocilo.ORM_O01_PATIENT.pid.pid_3 = str(dobi_pacienta.id)
            hl_sporocilo.ORM_O01_PATIENT.pid.pid_5 = dobi_pacienta.priimek + '^' + dobi_pacienta.ime
            hl_sporocilo.ORM_O01_PATIENT.pid.pid_6 = str(dobi_pacienta.rojstniDatum.year) + str(dobi_pacienta.rojstniDatum.month) + str(dobi_pacienta.rojstniDatum.day)
            hl_sporocilo.ORM_O01_PATIENT.pid.pid_8 = dobi_pacienta.spol

            for slikanje in pregled_odstrani.tipSlikanja.all():
                obr = core.Segment('OBR')
                obr.obr_4 = slikanje.koda
                obr.obr_39 = slikanje.opis
                hl_sporocilo.add(obr)

            posljiSporocilo(hl_sporocilo)
            #print(hl_sporocilo.to_er7().replace('\r','\n'))

            #dodaj novo
            hl_sporocilo = zacniHL7()
            hl_sporocilo.add_group("ORM_O01_ORDER")
            hl_sporocilo.ORM_O01_ORDER.ORC.orc_1 = "NW"
            hl_sporocilo.ORM_O01_ORDER.ORC.orc_2 = "ORD-" + str(pregled.id)
            hl_sporocilo.ORM_O01_ORDER.ORC.orc_3 = "ORD-" + str(pregled.id)

            hl_sporocilo.add_group("ORM_O01_PATIENT")
            hl_sporocilo.ORM_O01_PATIENT.pid.pid_3 = str(dobi_pacienta.id)
            hl_sporocilo.ORM_O01_PATIENT.pid.pid_5 = dobi_pacienta.priimek + '^' + dobi_pacienta.ime
            hl_sporocilo.ORM_O01_PATIENT.pid.pid_6 = str(dobi_pacienta.rojstniDatum.year) + str(dobi_pacienta.rojstniDatum.month) + str(dobi_pacienta.rojstniDatum.day)
            hl_sporocilo.ORM_O01_PATIENT.pid.pid_8 = dobi_pacienta.spol

            for slikanje in pregled.tipSlikanja.all():
                obr = core.Segment('OBR')
                obr.obr_4 = slikanje.koda
                obr.obr_39 = slikanje.opis
                hl_sporocilo.add(obr)

            posljiSporocilo(hl_sporocilo)
            #print(hl_sporocilo.to_er7().replace('\r','\n'))
            pregled.save()

            return redirect('/seznamPregledov')
    else:
        form = PregledForm(instance=pregled)
        pregled_odstrani = pregled
    return render(request, template_name, {'form': form})


def pregledIzbrisi(request, pk):
    template_name = 'izbrisano.html'
    pregled = get_object_or_404(Pregled, id=pk)
    dobi_pacienta = pregled.pacient

    #izbrisi
    hl_sporocilo = zacniHL7()
    hl_sporocilo.add_group("ORM_O01_ORDER")
    hl_sporocilo.ORM_O01_ORDER.ORC.orc_1 = "NW"
    hl_sporocilo.ORM_O01_ORDER.ORC.orc_2 = "ORD-" + str(pregled.id)
    hl_sporocilo.ORM_O01_ORDER.ORC.orc_3 = "ORD-" + str(pregled.id)

    hl_sporocilo.add_group("ORM_O01_PATIENT")
    hl_sporocilo.ORM_O01_PATIENT.pid.pid_3 = str(dobi_pacienta.id)
    hl_sporocilo.ORM_O01_PATIENT.pid.pid_5 = dobi_pacienta.priimek + '^' + dobi_pacienta.ime
    hl_sporocilo.ORM_O01_PATIENT.pid.pid_6 = str(dobi_pacienta.rojstniDatum.year) + str(
        dobi_pacienta.rojstniDatum.month) + str(dobi_pacienta.rojstniDatum.day)
    hl_sporocilo.ORM_O01_PATIENT.pid.pid_8 = dobi_pacienta.spol

    for slikanje in pregled.tipSlikanja.all():
        obr = core.Segment('OBR')
        obr.obr_4 = slikanje.koda
        obr.obr_39 = slikanje.opis
        hl_sporocilo.add(obr)

    posljiSporocilo(hl_sporocilo)
    #print(hl_sporocilo.to_er7().replace('\r','\n'))

    pregled.delete()

    return render(request, template_name)


def pregledPodrobnost(request, pk):
    pregled = get_object_or_404(Pregled, id=pk)
    return render(request, 'pregledPodrobnost.html', {'pregled': pregled})


def prijava(request):
    return render(request, 'prijava.html')


#login
def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    #inactive_user = User.objects.filter(email=username)
    #if not inactive_user:
    #   messages.info(request, 'Prijava ni bila uspešna. Poskusite ponovno.')
    #    return HttpResponseRedirect('/')

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/uvodna')
    else:
       messages.info(request, 'Prijava ni bila uspešna. Poskusite ponovno.')
       return HttpResponseRedirect('/')


# odjava
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


#je prijavljen
def loggedin(request):

    return render_to_response('ps/prijavljen.html',
                              {'full_name':request.user.username})