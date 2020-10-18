# Generated by Django 3.1.2 on 2020-10-13 17:59

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('climbguide', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='pitches',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
