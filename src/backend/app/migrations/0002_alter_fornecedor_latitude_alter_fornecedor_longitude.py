# Generated by Django 4.2.7 on 2023-11-22 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fornecedor',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=10),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=10),
        ),
    ]