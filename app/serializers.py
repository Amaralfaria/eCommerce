from rest_framework import serializers
from .models import *

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ['nome_do_negocio', 'endereco', 'latitude', 'longitude']
        # read_only_fields = ['id']

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password',
                  'telefone','is_cliente','is_fornecedor']
        # read_only_fields = ['id']


    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['preferencias_de_busca']
        # read_only_fields = ['id']

        

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'categoria', 'fornecedor']
        # read_only_fields = ['id']

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ['usuario', 'produto', 'nota', 'comentario']
        # read_only_fields = ['id']


class RelatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relatorio
        fields = ['dados_de_uso']
        # read_only_fields = ['id']

class AutenticacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['email', 'password']
        read_only_fields = ['email','password']
    