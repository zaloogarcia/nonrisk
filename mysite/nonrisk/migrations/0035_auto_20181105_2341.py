# Generated by Django 2.1 on 2018-11-05 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nonrisk', '0034_auto_20181102_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacient',
            name='arterial_age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studies',
            name='renal_filter',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
