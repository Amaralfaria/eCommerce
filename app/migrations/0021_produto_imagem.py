# Generated by Django 4.2.7 on 2023-12-11 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_remove_fornecedor_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='imagens_produtos/'),
        ),
    ]
