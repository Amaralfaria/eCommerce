from django.test import TestCase
from app.models import Usuario, Fornecedor, Produto, Avaliacao
from django.core.exceptions import ValidationError
import json

class UsuarioTestCase(TestCase):
    def test_usuario_valido(self):
        usuario = Usuario(username="usuario_teste", email="teste@teste.com", password = "senha123",informacoes_de_contato="1234567890")
        usuario.full_clean()

    def test_usuario_invalido(self):
        usuario = Usuario(username="usuario_teste", email="teste@teste.com", password = "",informacoes_de_contato="1234")
        with self.assertRaises(ValidationError):
            usuario.full_clean()


class FornecedorTestCase(TestCase):
    def test_fornecedor_valido(self):
        fornecedor = Fornecedor(
            nome_do_negocio="Negocio Teste",
            endereco="Rua Teste, 123",
            detalhes_de_contato="teste@teste.com",
            latitude='40.288484',  # Valor válido para latitude
            longitude='-74.006098'  # Valor válido para longitude
        )
        fornecedor.full_clean()  # Isso deve passar sem erros

    def test_fornecedor_invalido(self):
        # Teste com campos obrigatórios faltando
        fornecedor = Fornecedor(
            nome_do_negocio="", 
            endereco="", 
            detalhes_de_contato="Sem e-mail",
            latitude=91,  # Valor fora do intervalo válido
            longitude=181  # Valor fora do intervalo válido
        )
        with self.assertRaises(ValidationError):
            fornecedor.full_clean()


class ProdutoTestCase(TestCase):
    def setUp(self):
        # Criar um objeto Fornecedor com valores para latitude e longitude
        self.fornecedor = Fornecedor.objects.create(
            nome_do_negocio="Negocio Teste",
            endereco="Rua Teste, 123",
            detalhes_de_contato="Email: teste@teste.com",
            latitude=40.7128,  # Exemplo de latitude
            longitude=-74.0060  # Exemplo de longitude
        )

        # Agora, criar um objeto Produto usando o Fornecedor criado
        self.produto = Produto.objects.create(
            nome="Produto Teste",
            descricao="Descrição longa suficiente",
            preco=10.00,
            categoria="Categoria Teste",
            fornecedor=self.fornecedor
        )

    def test_produto_valido(self):
        produto = Produto(nome="Produto Teste", descricao="Descrição do produto teste", preco=10.00, categoria="Categoria Teste", fornecedor=self.fornecedor)
        produto.full_clean()

    def test_produto_invalido(self):
        produto = Produto(nome="", descricao="Curta", preco=-10.00, categoria="", fornecedor=self.fornecedor)
        with self.assertRaises(ValidationError):
            produto.full_clean()


class AvaliacaoTestCase(TestCase):
    def setUp(self):
        # Criar um objeto Fornecedor com valores para latitude e longitude
        self.fornecedor = Fornecedor.objects.create(
            nome_do_negocio="Negocio Teste",
            endereco="Rua Teste, 123",
            detalhes_de_contato="teste@teste.com",
            latitude=40.7128,  # Valor válido para latitude
            longitude=-74.0060  # Valor válido para longitude
        )

        # Criar um objeto Usuario
        self.usuario = Usuario.objects.create(username="usuario_teste", email="teste@teste.com")

        # Criar um objeto Produto usando o Fornecedor criado
        self.produto = Produto.objects.create(
            nome="Produto Teste",
            descricao="Descrição longa suficiente",
            preco=10.00,
            categoria="Categoria Teste",
            fornecedor=self.fornecedor
        )

    def test_avaliacao_valida(self):
        # Teste para uma avaliação válida
        avaliacao = Avaliacao(usuario=self.usuario, produto=self.produto, nota=5, comentario="Comentário longo o suficiente")
        avaliacao.full_clean()  # Isso deve passar sem erros

    def test_avaliacao_invalida(self):
        # Teste para uma avaliação inválida
        avaliacao = Avaliacao(usuario=self.usuario, produto=self.produto, nota=0, comentario="Curto")
        with self.assertRaises(ValidationError):
            avaliacao.full_clean()








