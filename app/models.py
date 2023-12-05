from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re
import json


class Usuario(AbstractUser):
    is_cliente = models.BooleanField(default=False)
    is_fornecedor = models.BooleanField(default=False)
    telefone = models.TextField()
    
        
    

class Cliente(models.Model):
    # Adicionando campos extras
    cliente_user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='cliente_user', null=True)
    preferencias_de_busca = models.JSONField(null=True, blank=True)
    


    # Alterações para evitar conflitos de relacionamento
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="usuario_groups",  
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="usuario_user_permissions",  
        related_query_name="usuario",
    )

    def clean(self):
        # super().clean()
        pass

        # Validar se o telefone está presente nas informações de contato
        # padrao_telefone = re.compile(r'(\(\d{2}\)\s?)?\d{6}-?\d{4}\b')
        # if not padrao_telefone.search(self.informacoes_de_contato):
        #     raise ValidationError({'informacoes_de_contato': 'Informações de contato devem incluir um número de telefone válido no formato 1234567890, (12) 34567890 ou 123456-7890.'})

        # if self.preferencias_de_busca:
        #     try:
        #         preferencias = json.loads(self.preferencias_de_busca)
                
        #         if 'distancia_maxima' not in preferencias:
        #             raise ValidationError({'preferencias_de_busca': 'Distância máxima é obrigatória nas preferências de busca.'})
        #     except json.JSONDecodeError:
        #         raise ValidationError({'preferencias_de_busca': 'Formato JSON inválido.'})

    def __str__(self):
        return self.credentials


class Fornecedor(models.Model):
    fornecedor_user = models.OneToOneField(Usuario, related_name='forncedor_user', on_delete=models.CASCADE)
    nome_do_negocio = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def clean(self):
        # Validação da latitude
        if self.latitude is not None and (self.latitude < -90 or self.latitude > 90):
            raise ValidationError({'latitude': 'Latitude deve estar entre -90 e 90.'})

        # Validação da longitude
        if self.longitude is not None and (self.longitude < -180 or self.longitude > 180):
            raise ValidationError({'longitude': 'Longitude deve estar entre -180 e 180.'})
        
        # Validação do nome do negócio
        if not self.nome_do_negocio.strip():
            raise ValidationError({'nome_do_negocio': 'O nome do negócio não pode ser vazio.'})

        # Validação do endereço
        if not self.endereco.strip():
            raise ValidationError({'endereco': 'O endereço não pode ser vazio.'})

        # Validação dos detalhes de contato
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self.detalhes_de_contato):
            raise ValidationError({'detalhes_de_contato': 'Detalhes de contato devem incluir um e-mail válido.'})
        
        # Validação da latitude
        if self.latitude is None or (self.latitude < -90 or self.latitude > 90):
            raise ValidationError({'latitude': 'Latitude é obrigatória e deve estar entre -90 e 90.'})

        # Validação da longitude
        if self.longitude is None or (self.longitude < -180 or self.longitude > 180):
            raise ValidationError({'longitude': 'Longitude é obrigatória e deve estar entre -180 e 180.'})

    def __str__(self):
        return self.nome_do_negocio


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=255)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='produtos')

    def clean(self):
        # Validação do nome
        if not self.nome.strip():
            raise ValidationError({'nome': 'O nome do produto não pode ser vazio.'})

        # Validação da descrição
        if len(self.descricao) < 10:  # exemplo: exigir pelo menos 10 caracteres
            raise ValidationError({'descricao': 'A descrição deve ter pelo menos 10 caracteres.'})

        # Validação do preço
        if self.preco <= 0:
            raise ValidationError({'preco': 'O preço deve ser positivo.'})

        # Validação da categoria
        if not self.categoria.strip():
            raise ValidationError({'categoria': 'A categoria não pode ser vazia.'})

    def __str__(self):
        return self.nome


class Avaliacao(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='avaliacoes')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField()
    comentario = models.TextField()

    def clean(self):
        # Validação da nota
        if not (1 <= self.nota <= 5):
            raise ValidationError({'nota': 'A nota deve estar entre 1 e 5.'})

        # Validação do comentário
        if len(self.comentario) < 20:  # exemplo: exigir pelo menos 20 caracteres
            raise ValidationError({'comentario': 'O comentário deve ter pelo menos 20 caracteres.'})

    def __str__(self):
        return f"Avaliação de {self.usuario.username} para {self.produto.nome}"


class Relatorio(models.Model):
    dados_de_uso = models.JSONField()

    def clean(self):
        # Verifica se 'dados_de_uso' não está vazio
        if not self.dados_de_uso:
            raise ValidationError({'dados_de_uso': 'Dados de uso não podem estar vazios.'})

        # Aqui você pode adicionar outras validações necessárias

    def __str__(self):
        return f"Relatório {self.id}"


