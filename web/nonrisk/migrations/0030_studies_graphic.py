# Generated by Django 2.1 on 2018-10-18 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nonrisk', '0029_auto_20181014_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='studies',
            name='graphic',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Graphic photo'),
        ),
    ]