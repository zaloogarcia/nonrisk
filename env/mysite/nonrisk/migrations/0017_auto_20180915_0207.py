# Generated by Django 2.1 on 2018-09-15 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nonrisk', '0016_auto_20180915_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='pacient',
            name='acv',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pacient',
            name='acv_ait',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pacient',
            name='diabetes',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pacient',
            name='diabetes_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pacient',
            name='diabetes_type',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pacient',
            name='dislipidemia',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pacient',
            name='dislipidemia_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pacient',
            name='dislipidemia_type',
            field=models.CharField(blank=True, choices=[('I', 'I'), ('IIa', 'IIa'), ('IIb', 'IIb'), ('III', 'III'), ('IV', 'IV'), ('V', 'V')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='pacient',
            name='enfvp',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pacient',
            name='fecvt',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pacient',
            name='hyper',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pacient',
            name='hyper_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pacient',
            name='hyper_type',
            field=models.CharField(blank=True, choices=[('Primaria', 'Primaria'), ('Secundaria', 'Secundaria')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='pacient',
            name='iam',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pacient',
            name='irc',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pacient',
            name='irc_type',
            field=models.CharField(blank=True, choices=[('G1', 'G1'), ('G2', 'G2'), ('G3a', 'G3a'), ('G3b', 'G3b'), ('G4', 'G4'), ('G5', 'G5')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='pacient',
            name='revasc',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
