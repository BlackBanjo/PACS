# Generated by Django 2.2 on 2019-07-26 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HIS', '0009_auto_20190725_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kraj',
            name='postnaStevilka',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
