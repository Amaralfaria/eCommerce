# Generated by Django 4.2.7 on 2023-11-22 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_fornecedor_latitude_alter_fornecedor_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fornecedor',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
    ]
