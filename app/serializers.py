from rest_framework import serializers

from .models import *
from PIL import Image
import base64
import io



class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = [
            "id",
            "nome_do_negocio",
            "endereco",
            "latitude",
            "longitude",
            "fornecedor_user",
            "feira",
        ]
        read_only_fields = ["id"]


class FeiraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feira
        fields = "__all__"
        read_only_fields = ["id"]


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "email",
            "password",
            "telefone",
            "is_cliente",
            "is_fornecedor",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = Usuario.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            telefone=validated_data["telefone"],
            is_cliente=validated_data["is_cliente"],
            is_fornecedor=validated_data["is_fornecedor"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "preferencias_de_busca", "cliente_user"]
        read_only_fields = ["id"]


class MensagemSerializer(serializers.ModelSerializer):
    destinatario_id = serializers.IntegerField(
        write_only=True, label="ID do Destinatário"
    )
    remetente = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        write_only=True,
        label="ID do Remetente",
    )

    destinatario_username = serializers.ReadOnlyField(
        source="destinatario.username", read_only=True
    )
    remetente_username = serializers.ReadOnlyField(
        source="remetente.username", read_only=True
    )

    class Meta:
        model = Mensagem
        fields = [
            "id",
            "destinatario_id",
            "remetente",
            "conteudo",
            "data_envio",
            "destinatario_username",
            "remetente_username",
        ]

    # class Meta:
    #     model = Mensagem
    #     fields = ['id', 'remetente', 'destinatario', 'conteudo', 'data_envio']


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id','nome', 'descricao', 'preco', 'categoria', 'fornecedor','imagem']
        read_only_fields = ['id']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
        read_only_fields = ["id"]


class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = "__all__"
        read_only_fields = ["id"]


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ["id", "cliente", "produto", "nota", "comentario"]
        read_only_fields = ["id"]


# class RelatorioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Relatorio
#         fields = ['id','dados_de_uso']
#         read_only_fields = ['id']

# class AutenticacaoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Usuario
#         fields = ['email', 'password']
#         read_only_fields = ['email','password']
