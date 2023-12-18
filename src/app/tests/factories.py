import factory

from app.models import *


class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario

    username = factory.Sequence(lambda n: "usuario_%d" % n)
    email = factory.Sequence(lambda n: "usuario_%d@gmail.com" % n)
    password = "password"
    telefone = "99999999"
    is_cliente = factory.Faker("boolean")
    is_fornecedor = not is_cliente


class ClienteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cliente

    preferencias_de_busca = None
    cliente_user = factory.SubFactory(UsuarioFactory)


class FeiraFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feira

    nome = factory.Faker("text", max_nb_chars=50)


class ForncedorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Fornecedor

    feira = factory.SubFactory(FeiraFactory)
    fornecedor_user = factory.SubFactory(UsuarioFactory)
    nome_do_negocio = factory.Faker("text", max_nb_chars=50)
    endereco = factory.Faker("text", max_nb_chars=50)
    latitude = factory.Faker("random_int", min=0, max=180)
    longitude = factory.Faker("random_int", min=0, max=180)


class CategoriaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Categoria

    nome = factory.Faker("text", max_nb_chars=50)


class ProdutoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Produto

    nome = factory.Faker("text", max_nb_chars=50)
    descricao = factory.Faker("text", max_nb_chars=200)
    preco = factory.Faker("random_int", min=0, max=2000)
    categoria = factory.SubFactory(CategoriaFactory)
    fornecedor = factory.SubFactory(ForncedorFactory)


class CompraFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Compra

    cliente = factory.SubFactory(ClienteFactory)
    data_compra = factory.Faker("date_this_decade")

    # Use o método SubFactory para criar produtos associados
    # produtos = factory.SubFactory(ProdutoFactory)

    @factory.post_generation
    def produtos(self, create, extracted, **kwargs):
        if not create:
            # A chamada foi feita para um método de construção, não para criar um objeto.
            return

        if extracted:
            # Adiciona os produtos fornecidos ao objeto Compra
            for produto in extracted:
                self.produtos.add(produto)


class AvaliacaoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Avaliacao

    cliente = factory.SubFactory(ClienteFactory)
    produto = factory.SubFactory(ProdutoFactory)
    nota = factory.Faker("random_int", min=1, max=5)
    comentario = factory.Faker("text", max_nb_chars=50)


class MensagemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mensagem

    destinatario = factory.SubFactory(UsuarioFactory)
    remetente = factory.SubFactory(UsuarioFactory)
    conteudo = factory.Faker("text", max_nb_chars=200)
    data_envio = factory.Faker("date_this_decade")
