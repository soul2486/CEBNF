# Generated by Django 4.2.6 on 2023-10-31 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eleves',
            name='statut',
            field=models.BooleanField(default=False),
        ),
    ]
