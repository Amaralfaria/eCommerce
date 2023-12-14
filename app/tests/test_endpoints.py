import pytest
import json
from app.models import *
from django.test import TestCase, Client
from rest_framework.test import APIClient, APITestCase
from app.tests.factories import *

pytestmark = pytest.mark.django_db

class TestUsuarioEndpoints(APITestCase):
    def setUp(self):
        self.api_client = APIClient
        self.usuario_factory = UsuarioFactory
        self.endpoint = '/usuarios/'
        self.fornecedor = ForncedorFactory()
        self.cliente = ClienteFactory()
        
        Usuario.objects.filter(pk=self.cliente.cliente_user.id).update(is_cliente=True,is_fornecedor=False)
        Usuario.objects.filter(pk=self.fornecedor.fornecedor_user.id).update(is_cliente=False,is_fornecedor=True)


        self.cliente.cliente_user.set_password('password')
        self.cliente.cliente_user.save()
        self.fornecedor.fornecedor_user.set_password('password')
        self.fornecedor.fornecedor_user.save()

        self.usuarioCliente = Client()
        self.usuarioFornecedor = Client()

        self.usuarioCliente.login(username=self.cliente.cliente_user.username, password='password')

        self.usuarioFornecedor.login(username=self.fornecedor.fornecedor_user.username, password='password')



    def test_usuario_get(self):
        self.usuario_factory.create_batch(4)

        response = self.api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)['Usuarios']) == 6 # 4 + 2 do setup

    def test_tipo_usuario(self):
        endpoint_completa = '/usuario/tipo/'

        responseCliente = self.usuarioCliente.get(endpoint_completa)
        responseFornecedor = self.usuarioFornecedor.get(endpoint_completa)

        assert responseCliente.status_code == 200
        assert responseFornecedor.status_code == 200





    def test_usuario_post(self):
        novo_cliente = {
                    "username": "cliente",
                    "email": "cliente@gmail.com",
                    "password": "cliente",
                    "telefone": "9999999",
                    "is_cliente": True,
                    "is_fornecedor": False
        }
        
        response = self.api_client().post(self.endpoint,data=json.dumps(novo_cliente), content_type='application/json')
        obj_novo_cliente = Usuario.objects.get(pk=response.json()['id'])

        assert response.status_code == 201
        assert obj_novo_cliente.username == 'cliente'

    def test_usuario_get_specific(self):
        self.usuario_factory()
        endpoint_id = self.endpoint + f'{1}'
        obj_usuario = Usuario.objects.get(pk=1)
        
        response = self.api_client().get(endpoint_id)

        assert response.status_code == 200
        assert obj_usuario.id == response.json()['id']

    def test_usuario_put(self):
        self.usuario_factory()
        endpoint_id = self.endpoint + f'{1}'
        update_usuario = {
            "telefone": "77777777"
        }

        response = self.api_client().put(endpoint_id,data=json.dumps(update_usuario),content_type='application/json')

        assert response.status_code == 200
        assert Usuario.objects.get(pk=1).telefone == '77777777'

    def test_usuario_delete(self):
        self.usuario_factory()
        endpoint_id = self.endpoint + f'{1}'

        response = self.api_client().delete(endpoint_id)

        try:
            usuario = Usuario.objects.get(pk=1)
        except Usuario.DoesNotExist:
            usuario = None

        assert response.status_code == 204
        assert usuario == None

        


class TestClienteEndpoints(APITestCase):
    def setUp(self):
        self.endpoint = '/cliente/'
        self.cliente_factory = ClienteFactory
        self.client = Client()
        self.api_client = APIClient
        self.usuario_factory = UsuarioFactory

        


    # cliente_factory = ClienteFactory()  # Substitua pelo seu código de criação de cliente
    # api_client = APIClient()

    def test_usuario_get(self):
        self.cliente_factory.create_batch(4)
        Usuario.objects.update(is_cliente=True,is_fornecedor=False)

        response = self.api_client().get(self.endpoint)
            

        assert response.status_code == 200
        assert len(json.loads(response.content)['usuarios']) == 4

    def test_usuario_post(self):
        usuario = self.usuario_factory()
        Usuario.objects.update(is_cliente=True,is_fornecedor=False)
        usuario.set_password('password')
        usuario.save()

        self.client.login(username=usuario.username,password='password')

        novo_cliente = {
            "preferencias_de_busca": None
        }

        
        response = self.client.post(self.endpoint,data=json.dumps(novo_cliente), content_type='application/json')
        # obj_novo_cliente = Usuario.objects.get(pk=response.json()['id'])

        assert response.status_code == 201

    def test_client_get_specific(self):
        cliente = self.cliente_factory()
        endpoint_id = self.endpoint + f'{cliente.id}'
        
        response = self.client.get(endpoint_id)

        assert response.status_code == 200
        assert cliente.id == response.json()['id']

    def test_usuario_put(self):
        cliente = self.cliente_factory()
        Usuario.objects.update(is_cliente=True,is_fornecedor=False)
        cliente.cliente_user.set_password('password')
        cliente.cliente_user.save()
        endpoint_id = self.endpoint + f'{cliente.id}'
        update_cliente = {
            "preferencias_de_busca": {
                "p1":"tudo"
            }
        }

        self.client.login(username=cliente.cliente_user.username,password='password')
        response = self.client.put(endpoint_id,data=json.dumps(update_cliente),content_type='application/json')

        assert response.status_code == 200
        assert Cliente.objects.get(pk=cliente.id).preferencias_de_busca == {
            "p1": "tudo"
        }

    def test_usuario_delete(self):
        cliente = self.cliente_factory()
        Usuario.objects.update(is_cliente=True,is_fornecedor=False)
        cliente.cliente_user.set_password('password')
        cliente.cliente_user.save()
        endpoint_id = self.endpoint + f'{cliente.id}'

        self.client.login(username=cliente.cliente_user.username,password='password')
        response = self.client.delete(endpoint_id)

        try:
            cliente = Cliente.objects.get(pk=cliente.id)
        except Cliente.DoesNotExist:
            cliente = None

        assert response.status_code == 204
        assert cliente == None


    

class TestFornecedorEndpoints(APITestCase):
    def setUp(self):
        self.endpoint = '/fornecedores/'
        self.fornecedor_factory = ForncedorFactory
        self.client = APIClient()
        self.usuario_factory = UsuarioFactory

    def test_fornecedor_post(self):
        fornecedor = self.fornecedor_factory()
        usuario = UsuarioFactory()
        fornecedor.fornecedor_user = usuario
        Usuario.objects.update(is_cliente=False, is_fornecedor=True)
        usuario.set_password('password')
        usuario.save()

        self.client.login(username=usuario.username, password='password')

        novo_fornecedor = {
            "nome_do_negocio": "biju teste",
            "endereco": "rua",
            "latitude": 50,
            "longitude": 50,
            "feira": FeiraFactory().id,
        }

        response = self.client.post(self.endpoint, data=json.dumps(novo_fornecedor), content_type='application/json')

        assert response.status_code == 201


    def test_fornecedor_get(self):
        self.fornecedor_factory.create_batch(4)
        Usuario.objects.update(is_cliente=False, is_fornecedor=True)

        response = self.client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)['fornecedores']) == 4


    def test_fornecedor_get_specific(self):
        fornecedor = self.fornecedor_factory()
        endpoint_id = self.endpoint + f'{fornecedor.id}'

        response = self.client.get(endpoint_id)

        assert response.status_code == 200
        assert fornecedor.id == response.json()['id']

    def test_fornecedor_put(self):
        fornecedor = self.fornecedor_factory()
        Usuario.objects.update(is_cliente=False, is_fornecedor=True)
        fornecedor.fornecedor_user.set_password('password')
        fornecedor.fornecedor_user.save()
        endpoint_id = self.endpoint + f'{fornecedor.id}'
        update_fornecedor = {
            "nome_do_negocio": "bijuterias sp"
        }

        self.client.login(username=fornecedor.fornecedor_user.username, password='password')
        response = self.client.put(endpoint_id, data=json.dumps(update_fornecedor), content_type='application/json')

        assert response.status_code == 200
        assert Fornecedor.objects.get(pk=fornecedor.id).nome_do_negocio == "bijuterias sp"

    def test_fornecedor_delete(self):
        fornecedor = self.fornecedor_factory()
        Usuario.objects.update(is_cliente=False, is_fornecedor=True)
        fornecedor.fornecedor_user.set_password('password')
        fornecedor.fornecedor_user.save()
        endpoint_id = self.endpoint + f'{fornecedor.id}'

        self.client.login(username=fornecedor.fornecedor_user.username, password='password')
        response = self.client.delete(endpoint_id)

        try:
            fornecedor = Fornecedor.objects.get(pk=fornecedor.id)
        except Fornecedor.DoesNotExist:
            fornecedor = None

        assert response.status_code == 204
        assert fornecedor is None

class TestProdutoEndpoints(APITestCase):
    def setUp(self):
        self.endpoint = '/produtos/'
        self.produto_factory = ProdutoFactory
        self.usuario_factory = UsuarioFactory
        self.client = APIClient()

        # Crie um usuário para autenticação nos testes
        self.fornecedor = ForncedorFactory()

        Usuario.objects.update(is_cliente=False, is_fornecedor=True)
        self.fornecedor.fornecedor_user.set_password('password')
        self.fornecedor.fornecedor_user.save()

        self.client.login(username=self.fornecedor.fornecedor_user.username, password='password')

    def test_produto_get(self):
        self.produto_factory.create_batch(4)

        response = self.client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)['produtos']) == 4

    def test_produto_post(self):
        novo_produto = {
            "nome": "Produto Teste",
            "descricao": "teste",
            "preco": 50.0,
            "categoria": CategoriaFactory().id,
        }
        

        response = self.client.post(self.endpoint, data=json.dumps(novo_produto), content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_produto_get_specific(self):
        produto = self.produto_factory()

        endpoint_id = f'{self.endpoint}{produto.id}'
        response = self.client.get(endpoint_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], produto.id)


    def test_produto_put(self):
        produto = self.produto_factory()
        endpoint_id = f'{self.endpoint}{produto.id}'

        update_produto = {
            "preco": 1000.0
        }

        response = self.client.put(endpoint_id, data=json.dumps(update_produto), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Produto.objects.get(pk=produto.id).preco, 1000)

    def test_produto_delete(self):
        produto = self.produto_factory()
        endpoint_id = f'{self.endpoint}{produto.id}'

        response = self.client.delete(endpoint_id)

        with self.assertRaises(Produto.DoesNotExist):
            Produto.objects.get(pk=produto.id)

        self.assertEqual(response.status_code, 204)





class TestCompraEndpoints(APITestCase):
    def setUp(self):
        self.endpoint = '/cliente/compras/'
        self.compra_factory = CompraFactory
        self.usuario_factory = UsuarioFactory
        self.client = APIClient()

        # Crie um usuário para autenticação nos testes
        self.cliente = ClienteFactory()
        Usuario.objects.update(is_cliente=True, is_fornecedor=False)
        self.cliente.cliente_user.set_password('password')
        self.cliente.cliente_user.save()

        self.client.login(username=self.cliente.cliente_user.username, password='password')

    def test_compra_get(self):
        self.compra_factory.create_batch(4, produtos=[ProdutoFactory()])

        Compra.objects.update(cliente=self.cliente)

        self.compra_factory.create_batch(4)

        response = self.client.get(self.endpoint)

        self.assertEqual(response.status_code, 200)
        assert response.status_code == 200
        assert len(json.loads(response.content)['Compras']) == 4


    def test_compra_post(self):
        novo_compra = {
            "data_compra": "2023-12-10",
            "produtos": [
                ProdutoFactory().id
            ]
        }

        response = self.client.post(self.endpoint, data=json.dumps(novo_compra), content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_compra_get_specific(self):
        compra = self.compra_factory()

        endpoint_id = f'{self.endpoint}{compra.id}'
        response = self.client.get(endpoint_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], compra.id)

    # def test_compra_put(self):
    #     compra = self.compra_factory(produtos=[ProdutoFactory()])
    #     endpoint_id = f'/cliente/compras/{compra.id}'

    #     update_compra = {
    #         "data_compra": "2023-12-12",
    #     }

    #     response = self.client.put(endpoint_id, data=json.dumps(update_compra), content_type='application/json')

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Compra.objects.get(pk=compra.id).data_compra, "2023-12-12")

    def test_compra_delete(self):
        compra = self.compra_factory(produtos=[ProdutoFactory()])
        endpoint_id = f'/cliente/compras/{compra.id}'

        response = self.client.delete(endpoint_id)

        with self.assertRaises(Compra.DoesNotExist):
            Compra.objects.get(pk=compra.id)

        self.assertEqual(response.status_code, 204)


class TestAvaliacaoEndpoints(APITestCase):
    def setUp(self):
        self.endpoint = '/avaliacoes/'
        self.usuario_factory = UsuarioFactory
        self.avaliacao_factory = AvaliacaoFactory
        self.client = APIClient()

        # Crie um usuário para autenticação nos testes
        self.cliente = ClienteFactory()
        Usuario.objects.update(is_cliente=True, is_fornecedor=False)
        self.cliente.cliente_user.set_password('password')
        self.cliente.cliente_user.save()

        self.client.login(username=self.cliente.cliente_user.username, password='password')

    def test_avaliacao_get(self):
        self.avaliacao_factory.create_batch(4)
        Avaliacao.objects.update(cliente=self.cliente)

        # self.compra_factory.create_batch(4)

        response = self.client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)['avaliacoes']) == 4

    def test_avaliacao_produto(self):
        self.avaliacao_factory.create_batch(4)
        produto = ProdutoFactory()
        endpoint_completo = f'/avaliacoes_produto/{produto.id}'
        Avaliacao.objects.update(produto=produto)


        self.avaliacao_factory.create_batch(4)

        response = self.client.get(endpoint_completo)

        assert response.status_code == 200
        assert len(json.loads(response.content)['avaliacoes']) == 4


    


    def test_avaliacao_post(self):
        nova_avaliacao = {
            "produto": ProdutoFactory().id,
            "nota": 5,
            "comentario": "bom"
        }

        response = self.client.post(self.endpoint, data=json.dumps(nova_avaliacao), content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_avaliacao_get_specific(self):
        avaliacao = self.avaliacao_factory()

        endpoint_id = f'{self.endpoint}{avaliacao.id}'
        response = self.client.get(endpoint_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], avaliacao.id)

    def test_avaliacao_put(self):
        avaliacao = self.avaliacao_factory()
        endpoint_id = f'/avaliacoes/{avaliacao.id}'

        update_avaliacao = {
            "nota": 4,
        }

        response = self.client.put(endpoint_id, data=json.dumps(update_avaliacao), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Avaliacao.objects.get(pk=avaliacao.id).nota, 4)

    def test_avaliacao_delete(self):
        avaliacao = self.avaliacao_factory()
        endpoint_id = f'/avaliacoes/{avaliacao.id}'

        response = self.client.delete(endpoint_id)

        with self.assertRaises(Avaliacao.DoesNotExist):
            Avaliacao.objects.get(pk=avaliacao.id)

        self.assertEqual(response.status_code, 204)


        

class TestMensagemEndpoints(APITestCase):
    def setUp(self):
        self.endpoint = '/mensagens/'
        self.mensagem_factory = MensagemFactory
        self.client = APIClient()
        self.fornecedorCliente = Client()

        # Crie um usuário para autenticação nos testes
        self.cliente = ClienteFactory()
        Usuario.objects.update(is_cliente=True, is_fornecedor=False)
        self.cliente.cliente_user.set_password('password')
        self.cliente.cliente_user.save()
        self.client.login(username=self.cliente.cliente_user.username, password='password')

        self.fornecedor = ForncedorFactory()
        Usuario.objects.filter(pk=self.fornecedor.fornecedor_user.id).update(is_cliente=False, is_fornecedor=True)
        self.fornecedor.fornecedor_user.set_password('password')
        self.fornecedor.fornecedor_user.save()
        self.fornecedorCliente.login(username=self.fornecedor.fornecedor_user.username,password='password')
        

    def test_mensagem_get(self):
        # user1 = UsuarioFactory()
        # user2 = UsuarioFactory()

        mensagem = MensagemFactory()
        Mensagem.objects.update(remetente_id=self.cliente.cliente_user.id)
        MensagemFactory()

        endpoint_id = f'/mensagens/{mensagem.destinatario.id}'
        
        response = self.client.get(endpoint_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['mensagens']), 1)

    def test_get_diferentes_usuarios_chat(self):
        self.mensagem_factory.create_batch(4)
        endpoint_completo = '/mensagens_fornecedor/'
        
        Mensagem.objects.update(destinatario_id=self.fornecedor.fornecedor_user.id, remetente_id=self.cliente.cliente_user.id)
        
        msg1 = self.mensagem_factory()

        Mensagem.objects.filter(pk=msg1.id).update(remetente_id=self.fornecedor.fornecedor_user.id, destinatario_id=self.cliente.cliente_user.id)

        msg2 = self.mensagem_factory()
        Mensagem.objects.filter(pk=msg2.id).update(remetente_id=ClienteFactory().cliente_user.id, destinatario_id=self.cliente.cliente_user.id)

        response = self.fornecedorCliente.get(endpoint_completo)

        assert response.status_code == 200


    def test_mensagem_post(self):
        nova_mensagem = {
            "destinatario_id": UsuarioFactory().id,
            "conteudo": "chato"
        }

        response = self.client.post(self.endpoint, data=json.dumps(nova_mensagem), content_type='application/json')

        self.assertEqual(response.status_code, 201)

    
class TestCategoriaEndpoints(APITestCase):
    def setUp(self):
        self.endpoint = '/categorias/'
        self.categoria_factory = CategoriaFactory
        self.client = APIClient()


    def test_feira_get(self):
        # Crie algumas instâncias de feira para testar o método GET
        self.categoria_factory.create_batch(4)

        response = self.client.get(self.endpoint)

        self.assertEqual(response.status_code, 200)
        assert len(json.loads(response.content)['categorias']) == 4