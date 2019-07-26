from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone

# Create your models here.

class Kraj(models.Model):
    id = models.AutoField(primary_key=True)
    mesto = models.CharField(max_length=100, default='')
    postnaStevilka = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        ime = str(self.mesto) + " " + str(self.postnaStevilka)
        return ime

class Pacient(models.Model):
    ime = models.CharField(max_length=100)
    priimek = models.CharField(max_length=100)
    SPOL = (
        ('M', 'Moški'),
        ('Ž', 'Ženska'),
    )
    spol = models.CharField(max_length=1, choices=SPOL, default='M')
    rojstniDatum = models.DateField()
    emso = models.PositiveIntegerField()
    ulica = models.CharField(max_length=200, default='')
    id = models.AutoField(primary_key=True)
    mesto = models.ForeignKey(Kraj, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        ime = str(self.ime) + ' ' + str(self.priimek) + ', ' + str(self.emso)
        return ime

class Naprava(models.Model):
    id = models.AutoField(primary_key=True)
    naziv = models.CharField(max_length=100)
    kratica = models.CharField(max_length=25, default='')

    def __str__(self):
        if self.kratica == '':
            return self.naziv
        return self.kratica

class DelTelesa(models.Model):
    id = models.AutoField(primary_key=True)
    naziv = models.CharField(max_length=100)

    def __str__(self):
        return self.naziv

class Slikanje(models.Model):
    id = models.AutoField(primary_key=True)
    #naprava = models.ForeignKey(Naprava, on_delete=models.CASCADE, blank=True, null=True)
    #delTelesa = models.ForeignKey(DelTelesa, on_delete=models.CASCADE, blank=True, null=True)
    opis = models.CharField(max_length=500, default ='')
    SPS_koda = models.PositiveIntegerField(null=True)
    koda = models.CharField(max_length=10, default='')

    def __str__(self):
        ime = str(self.koda) + ' ' + str(self.opis)
        return ime

class Pregled(models.Model):
    id = models.AutoField(primary_key=True)
    pacient = models.ForeignKey(Pacient, on_delete=models.CASCADE, blank=True, null=True)
    tipSlikanja = models.ManyToManyField(Slikanje, blank=True, null=True)
    datumNastanka = models.DateField(auto_now=True)
