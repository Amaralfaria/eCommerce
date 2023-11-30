from rest_framework import serializers
from .models import *

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ['id','nome_do_negocio', 'endereco', 'detalhes_de_contato', 'latitude', 'longitude']
        read_only_fields = ['id']

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id','username', 'first_name', 'last_name', 'email', 'password','is_active', 'is_staff', 'is_superuser', 'date_joined',
    'groups', 'user_permissions',
                  'preferencias_de_busca', 'informacoes_de_contato']
        read_only_fields = ['id']

        extra_kwargs = {
            'is_active': {'required': False},
            'is_staff': {'required': False},
            'is_superuser': {'required': False},
            'date_joined': {'required': False},
            'groups': {'required': False},
            'user_permissions': {'required': False}
        }


        

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id','nome', 'descricao', 'preco', 'categoria', 'fornecedor']
        read_only_fields = ['id']

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ['id','usuario', 'produto', 'nota', 'comentario']
        read_only_fields = ['id']


class RelatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relatorio
        fields = ['id','dados_de_uso']
        read_only_fields = ['id']

class AutenticacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['email', 'password']
        read_only_fields = ['email','password']
    