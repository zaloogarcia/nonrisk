# Generated by Django 2.1 on 2018-09-14 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nonrisk', '0011_auto_20180914_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacient',
            name='diabetes_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pacient',
            name='dislipidemia_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pacient',
            name='hyper_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pacient',
            name='smoke_duration',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pacient',
            name='smoke_quit',
            field=models.DateField(blank=True, null=True),
        ),
    ]
