# Generated by Django 2.2 on 2018-09-28 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nonrisk', '0024_auto_20180927_0336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studies',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='Studies photo'),
        ),
    ]
