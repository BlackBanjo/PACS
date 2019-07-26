from django import forms
from django.contrib import admin

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'

class SlikanjeInput(forms.CheckboxSelectMultiple):
    input_type = 'checkBox'

class PacientForm(forms.ModelForm):

    class Meta:
        model = Pacient
        fields = ['ime', 'priimek', 'spol', 'rojstniDatum', 'emso', 'ulica', 'mesto']
        labels = {
            'rojstniDatum': ('Datum rojstva'),
        }
        widgets = {
            'rojstniDatum': DateInput()
        }


class PregledForm(forms.ModelForm):

    class Meta:
        model = Pregled
        fields = ['tipSlikanja']
        labels = {
            'tipSlikanja': ('Tip Slikanja'),
        }
        widgets = {
            'tipSlikanja': SlikanjeInput()
        }