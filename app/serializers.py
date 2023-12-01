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
        fields = ['id','username', 'email', 'password',
                  'telefone', 'telefone']
        read_only_fields = ['id']


    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user


        

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
    