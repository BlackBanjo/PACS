# Generated by Django 2.2 on 2019-07-23 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HIS', '0007_auto_20190723_1704'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pregled',
            old_name='pregledDatum',
            new_name='datumNastanka',
        ),
    ]