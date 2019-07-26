from django.contrib.auth.models import User
from .models import *
import django_filters


class PacientFilter(django_filters.FilterSet):
    class Meta:
        model = Pacient
        fields = ['ime', 'priimek', 'spol', 'rojstniDatum', 'emso', 'ulica', 'mesto']


class PregledFilter(django_filters.FilterSet):
    class Meta:
        model = Pregled
        fields = ['pacient__ime', 'pacient__priimek']