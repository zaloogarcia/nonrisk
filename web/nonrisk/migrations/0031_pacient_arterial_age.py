# Generated by Django 2.1 on 2018-10-19 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nonrisk', '0030_studies_graphic'),
    ]

    operations = [
        migrations.AddField(
            model_name='pacient',
            name='arterial_age',
            field=models.FloatField(blank=True, null=True),
        ),
    ]