# Generated by Django 4.2.7 on 2023-12-09 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_mensagem_data_envio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensagem',
            name='data_envio',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]