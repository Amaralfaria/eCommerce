from django.http import JsonResponse
from .models import Produto
from .serializers import *
from rest_framework.response import Response
from django.db.models import Q, F, ExpressionWrapper, fields
from rest_framework import status
from rest_framework import  mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from datetime import date
from drf_spectacular.utils import extend_schema
from django.db.models.functions import ACos, Cos, Radians, Sin
from django.shortcuts import render




class ProdutoViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ] 
    serializer_class = ProdutoSerializer
    queryset = Produto.objects.all()


    '''
    /***************************************************************************
    *Função: API que retorna lista de produtos
    *Descrição: 
        Faz uma query de todos os produtos e faz uma filtragem baseada nos parametros baseados pela URL. Parametros: nomeProduto,precoMaximo,precoMinimo, raio, banca, feira,latitude e longitude do cliente. Para retornar a distancia devem ser fornecido raio, latitude e longitude do cliente. Exemplo: http://127.0.0.1:8000/produtos/?raio=14&latitudeCliente=50.1&longitudeCliente=50.1

    * Parametros
        request - objeto de HttpRequest

    * Valor retornado
        Retorna um JsonResponse com todos os produtos que atendiam as condicoes passadas pela URL. Caso seja um metodo POST e o objeto tenha sido criado, retorna uma Response com status 201_CREATED junto com os dados do novo produto

    * Assertica de entrada
        request.method == 'GET'
    ***************************************************************************/ 
'''

    @extend_schema(description='Faz uma query de todos os produtos e faz uma filtragem baseada nos parametros baseados pela URL. Parametros: nomeProduto,precoMaximo,precoMinimo, raio, banca, feira,latitude e longitude do cliente. Para retornar a distancia devem ser fornecido raio, latitude e longitude do cliente. Exemplo: http://127.0.0.1:8000/produtos/?raio=14&latitudeCliente=50.1&longitudeCliente=50.1')
    def get(self, request):
        produtos = Produto.objects.all()

        nomeProduto = request.query_params.get('nomeProduto',None)
        precoMaximo = request.query_params.get('precoMaximo',None)
        precoMinimo = request.query_params.get('precoMinimo',None)
        fornecedorProduto = request.query_params.get('banca',None)
        feira = request.query_params.get('feira',None)
        raio = request.query_params.get('raio',None)
        latitudeCliente = request.query_params.get('latitudeCliente',None)
        longitudeCliente = request.query_params.get('longitudeCliente',None)

        if raio and latitudeCliente and longitudeCliente:
            raio = float(raio)
            latitudeCliente = float(latitudeCliente)
            longitudeCliente = float(longitudeCliente)

            produtos = Produto.objects.annotate(
                distancia=ExpressionWrapper(
                    ACos(
                        Cos(Radians(latitudeCliente)) * Cos(Radians(F('fornecedor__latitude'))) * Cos(Radians(F('fornecedor__longitude')) - Radians(longitudeCliente)) +
                        Sin(Radians(latitudeCliente)) * Sin(Radians(F('fornecedor__latitude')))
                    ) * 6371,  # Raio da Terra em quilômetros
                    output_field=fields.FloatField()
                )
            ).filter(distancia__lte=raio)

        if feira:
            produtos = produtos.filter(Q(fornecedor__feira=int(feira)))
        if fornecedorProduto:
            produtos = produtos.filter(Q(fornecedor__nome_do_negocio__icontains=fornecedorProduto))

        if nomeProduto:
            produtos = produtos.filter(Q(nome__icontains=nomeProduto))
        if precoMaximo:
            print(precoMaximo)
            produtos = produtos.filter(Q(preco__lte=precoMaximo))
        if precoMinimo:
            produtos = produtos.filter(Q(preco__gte=precoMinimo))


        serialized = list(produtos.values())

        for produto in serialized:
            produto["fornecedor"] = produto.pop("fornecedor_id")



        # serializer = ProdutoSerializer(produtos, many=True)
        

        # return JsonResponse({"produtos":serializer.data})
        return JsonResponse({"produtos":serialized})
    
    '''
    /***************************************************************************
    *Função: API que criar um novo produto
    *Descrição: 
        Recebe uma requisição HTTP. É criado um novo objeto no banco de dados a partir das informações        passadas, sendo elas, nome, descricao, preco e id da categoria. O usuario autenticado é um fornecedor e será associado ao produto.

    * Parametros
        request - objeto de HttpRequest

    * Valor retornado
        Caso o objeto tenha sido criado, retorna uma Response com status 201_CREATED junto com os dados do novo produto

    * Assertica de entrada
        request.method == 'POST'
        all(campo in request.data for campo in["nome","descricao","preco","categoria","fornecedor"])
        request.user.is_authenticated
        request.user.is_fornecedor
    ***************************************************************************/ 
    '''
         
    @extend_schema(description='É criado um novo produto no banco de dados a partir das informações        passadas, sendo elas, nome, descricao, preco e id da categoria. O usuario autenticado é um fornecedor e será associado ao produto.')
    def post(self, request):
        data = request.data
        data["fornecedor"] = Fornecedor.objects.get(fornecedor_user=request.user).id
        serializer = ProdutoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
    '''
    /***************************************************************************
    *Função: API que retorna um produto pelo ID
    *Descrição: 
        Retorna um unico produto a partir de id passada na URL

    * Parametros
        request - objeto de HttpRequest
        id - id do produto desejado

    * Valor retornado
        Retorna uma Response com o produto em questão caso seja encontrado com status 200. Caso não encontre retona uma response com status 404

    * Assertica de entrada
        request.method == 'GET'
        type(id) == int
    ***************************************************************************/ 
    '''
    @extend_schema(description='Retorna um unico produto a partir de id passada na URL')
    def get_specific(self, request, id):
        try:
            produto = Produto.objects.get(pk=id)
        except Produto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)
    

    '''
    /***************************************************************************
    *Função: API atualiza um produto pelo ID
    *Descrição: 
        Atualiza produto com base no ID passado na URL

    * Parametros
        request - objeto de HttpRequest
        id - id do produto desejado

    * Valor retornado
        Retorna uma Response com o produto atualizado em questão caso seja encontrado com status 200. Caso não encontre retona uma response com status 404

    * Assertica de entrada
        request.method == 'PUT'
        type(id) == int
        request.user.is_authenticated
    ***************************************************************************/ 
    '''
    @extend_schema(description='Atualiza produto com base no ID passado na URL')
    def put(self, request, id):
        try:
            produto = Produto.objects.get(pk=id)
        except Produto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProdutoSerializer(produto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    '''
    /***************************************************************************
    *Função: API que deleta produto pelo ID
    *Descrição: 
        Deleta produto com base no ID passado na URL

    * Parametros
        request - objeto de HttpRequest
        id - id do produto desejado

    * Valor retornado
        Retorna uma Response status 204 caso o produto tenha sido encontrado e deletado. Caso não encontre retona uma response com status 404

    * Assertica de entrada
        request.method == 'DELETE'
        type(id) == int
        request.user.is_authenticated
    ***************************************************************************/ 
    '''
    @extend_schema(description='Deleta produto com base no ID passado na URL')
    def delete(self, request, id):
        try:
            produto = Produto.objects.get(pk=id)
        except Produto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        produto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoriaViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()

    '''
    /***************************************************************************
    *Função: API que retorna lista de categorias
    *Descrição: 
        Será feita uma query que retornará todas as categorias disponíveis.

    * Parâmetros
        request - objeto de HttpRequest

    * Valor retornado
        Retorna um JsonResponse com todas as categorias com status 200.

    * Assertiva de entrada
        request.method == 'GET'
    ***************************************************************************/
    '''
    @extend_schema(description='Retorna todas as categorias registradas. Feita para utilizar no cadastro dos produtos')
    def get(self,request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return JsonResponse({"categorias":serializer.data})
    
    def get_specific(self, request, id):
        categoria = Categoria.objects.get(pk=id)
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)


class CompraViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CompraSerializer
    queryset = Compra.objects.all()


    '''
    /***************************************************************************
    *Função: API que retorna lista de compras
    *Descrição: 
        Será feita uma query que retornará todas as compras do cliente logado.

    * Parâmetros
        request - objeto de HttpRequest

    * Valor retornado
        Retorna um JsonResponse com todas as compras com status 200.

    * Assertiva de entrada
        request.method == 'GET'
        request.user.is_authenticated
        request.user.is_cliente
    ***************************************************************************/
    '''
    @extend_schema(description='Retorna as compras do cliente logado. Não preencher o campo cliente, ele será puxado do usuario autenticado')
    def get_cliente_compras(self, request):
        try:
            cliente = Cliente.objects.get(cliente_user=request.user)
        except Cliente.DoesNotExist:
            return Response("Usuario logado não é cliente", status=status.HTTP_403_FORBIDDEN)
        
        compras = Compra.objects.filter(cliente=cliente)
        serializer = CompraSerializer(compras, many=True)

        return JsonResponse({"Compras":serializer.data}, status=status.HTTP_200_OK)


    '''
    /***************************************************************************
    *Função: API que cria uma nova compra
    *Descrição: 
        Recebe uma requisição HTTP. É criada uma nova compra no banco de dados a partir das informações passadas, incluindo lista de produto e data compra. O usuario deve estar autenticado para que a compra seja associada a ele

    * Parâmetros
        request - objeto de HttpRequest

    * Valor retornado
        Caso a compra tenha sido criada, retorna uma Response com status 201_CREATED junto com os dados da nova compra.

    * Assertiva de entrada
        request.method == 'POST'
        all(campo in request.data for campo in ['produtos', 'data_compra'])
        request.user.is_authenticated
        request.user.is_cliente
    ***************************************************************************/
    '''
    @extend_schema(description='Realiza uma nova compra no perfil do cliente logado. Não precisa preencher o campo cliente, ele será puxado do usuario autenticado')
    def post(self, request):
        try:
            cliente = Cliente.objects.get(cliente_user=request.user)
        except Cliente.DoesNotExist:
            return Response("Usuario logado não é cliente", status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        data["cliente"] = cliente.id
        data["data_compra"] = date.today()
        serializer = CompraSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        

    '''
    /***************************************************************************
    *Função: API que retorna uma compra pelo ID
    *Descrição: 
        Retorna uma única compra a partir do ID passado na URL.

    * Parâmetros
        request - objeto de HttpRequest
        id - ID da compra desejada

    * Valor retornado
        Retorna uma Response com a compra em questão caso seja encontrada com status 200. Caso não encontre, retorna uma response com status 404.

    * Assertiva de entrada
        request.method == 'GET'
        type(id) == int
    ***************************************************************************/
    '''
    @extend_schema(description='Retorna uma única compra a partir do ID passado na URL.')
    def get_specific(self,request,id):
        try:
            compra = Compra.objects.get(pk=id)
        except Compra.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CompraSerializer(compra)
        return Response(serializer.data)
    '''
    /***************************************************************************
    *Função: API que deleta uma compra pelo ID
    *Descrição: 
        Deleta uma compra com base no ID passado na URL.

    * Parâmetros
        request - objeto de HttpRequest
        id - ID da compra desejada

    * Valor retornado
        Retorna uma Response status 204 caso a compra tenha sido encontrada e deletada. Caso não encontre, retorna uma response com status 404.

    * Assertiva de entrada
        request.method == 'DELETE'
        type(id) == int
        request.user.is_authenticated
    ***************************************************************************/
    '''
    @extend_schema(description='Deleta uma compra com base no ID passado na URL. Usuario deve estar autenticado')
    def delete(self,request,id):
        try:
            compra = Compra.objects.get(pk=id)
        except Compra.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        compra.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UsuarioViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny,]
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()


    '''
    /***************************************************************************
    *Função: API que retorna lista de usuarios
    *Descrição: 
        Será         feita uma query a qual retornara todos os usuarios.

    * Parametros
        request - objeto de HttpRequest

    * Valor retornado
        Retorna um JsonResponse com todos os usuarios com status 200.

    * Assertiva de entrada
        request.method == 'GET'
    ***************************************************************************/ 
    '''

    @extend_schema(description='Retorna todos os usuarios do banco de dados')
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return JsonResponse({"Usuarios": serializer.data})
    
    '''
    /***************************************************************************
    *Função: API que criar um novo usuario
    *Descrição: 
        Recebe uma requisição HTTP. É criado um novo objeto no banco de dados a partir das informações        passadas, sendo elas, username, email, password, telefone, is_cliente, is_fornecedor.

    * Parametros
        request - objeto de HttpRequest

    * Valor retornado
        Caso o objeto tenha sido criado, retorna uma Response com status 201_CREATED junto com os dados do novo usuario

    * Assertica de entrada
        request.method == 'POST'
        all(campo in request.data for campo in['username', 'email', 'password', 'telefone','is_cliente','is_fornecedor'])
    '''
    
    @extend_schema(description='Cria um usuario o qual devera ser cliente ou fornecedor')
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Errores de Serialização:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    '''
    /***************************************************************************
    *Função: API que retorna um usuario pelo ID
    *Descrição: 
        Retorna um unico usuario a partir de id passada na URL

    * Parametros
        request - objeto de HttpRequest
        id - id do usuario desejado

    * Valor retornado
        Retorna uma Response com o usuario em questão caso seja encontrado com status 200. Caso não encontre retona uma response com status 404

    * Assertica de entrada
        request.method == 'GET'
        type(id) == int
    ***************************************************************************/ 
    '''
    @extend_schema(description='Retorna um unico usuario a partir de id passada na URL')
    def get_specific(self, request, id):
        try:
            usuario = Usuario.objects.get(pk=id)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    

    '''
    /***************************************************************************
    *Função: API atualiza um usuario pelo ID
    *Descrição: 
        Atualiza usuario com base no ID passado na URL

    * Parametros
        request - objeto de HttpRequest
        id - id do usuario desejado

    * Valor retornado
        Retorna uma Response com o usuariio atualizado em questão caso seja encontrado com status 200. Caso não encontre retona uma response com status 404

    * Assertica de entrada
        request.method == 'PUT'
        type(id) == int
    ***************************************************************************/ 
'''
    @extend_schema(description='Atualiza usuario com base no ID passado na URL')
    def put(self, request, id):
        try:
            usuario = Usuario.objects.get(pk=id)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    '''
    /***************************************************************************
    *Função: API que deleta usuario pelo ID
    *Descrição: 
        Deleta usuario com base no ID passado na URL

    * Parametros
        request - objeto de HttpRequest
        id - id do usuario desejado

    * Valor retornado
        Retorna uma Response status 204 caso o usuario tenha sido encontrado e deletado. Caso não encontre retona uma response com status 404

    * Assertica de entrada
        request.method == 'DELETE'
        type(id) == int
    ***************************************************************************/ 
    '''
    @extend_schema(description='Deleta usuario com base no ID passado na URL')
    def delete(self, request, id):
        try:
            usuario = Usuario.objects.get(pk=id)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FornecedorViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ] 
    serializer_class = FornecedorSerializer
    queryset = Fornecedor.objects.all()


    '''
    /***************************************************************************
    *Função: API que retorna lista de fornecedores
    *Descrição: 
        Será         feita uma query a qual retornara todos os fornecedores.

    * Parametros
        request - objeto de HttpRequest

    * Valor retornado
        Retorna um JsonResponse com todos os fornecedores com status 200.

    * Assertiva de entrada
        request.method == 'GET'
    ***************************************************************************/ 
    '''
    @extend_schema(description='Retorna todos os fornecedores do banco de dados')
    def get(self, request):
        fornecedores = Fornecedor.objects.all()
        serializer = FornecedorSerializer(fornecedores, many=True)
        return JsonResponse({"fornecedores": serializer.data})
    

    '''
    /***************************************************************************
    *Função: API que criar um novo fornecedor
    *Descrição: 
        Recebe uma requisição HTTP. É criado um novo objeto no banco de dados a partir das informações        passadas, sendo elas, 'nome_do_negocio', 'endereco', 'latitude', 'longitude', 'feira'. Deve ter um usuario is_fornecedor logado para que ele seja associado ao novo fornecedor.

    * Parametros
        request - objeto de HttpRequest

    * Valor retornado
        Caso o objeto tenha sido criado, retorna uma Response com status 201_CREATED junto com os dados do novo fornecedor

    * Assertica de entrada
        request.method == 'POST'
        all(campo in request.data for campo in['nome_do_negocio', 'endereco', 'latitude', 'longitude', 'feira'])
        request.user.is_authenticated
        request.user.is_fornecedor
    '''
    @extend_schema(description='É criado um novo objeto no banco de dados a partir das informações        passadas, sendo elas, nome_do_negocio, endereco, latitude, longitude, feira. Deve ter um usuario is_fornecedor logado para que ele seja associado ao novo fornecedor')
    def post(self, request):
        data = request.data
        data["fornecedor_user"] = request.user.id
        print(data["fornecedor_user"])
        serializer = FornecedorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)




    '''
    /***************************************************************************
    *Função: API que retorna um fornecedor pelo ID
    *Descrição: 
        Retorna um unico fornecedor a partir de id passada na URL

    * Parametros
        request - objeto de HttpRequest
        id - id do fornecedor desejado

    * Valor retornado
        Retorna uma Response com o fornecedor em questão caso seja encontrado com status 200. Caso não encontre retona uma response com status 404

    * Assertica de entrada
        request.method == 'GET'
        type(id) == int
    ***************************************************************************/ 
    '''
    @extend_schema(description='Retorna um unico fornecedor a partir de id passada na URL')
    def get_specific(self, request, id):
        try:
            fornecedor = Fornecedor.objects.get(pk=id)
        except Fornecedor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = FornecedorSerializer(fornecedor)
        return Response(serializer.data)
    

    '''
    /***************************************************************************
    *Função: API atualiza um fornecedor pelo ID
    *Descrição: 
        Atualiza fornecedor com base no ID passado na URL

    * Parametros
        request - objeto de HttpRequest
        id - id do fornecedor desejado

    * Valor retornado
        Retorna uma Response com o fornecedor atualizado em questão caso seja encontrado com status 200. Caso não encontre retona uma response com status 404

    * Assertica de entrada
        request.method == 'PUT'
        type(id) == int
        request.user.is_authenticated
    ***************************************************************************/ 
    '''
    @extend_schema(description='Atualiza fornecedor com base no ID passado na URL')
    def put(self, request, id):
        try:
            fornecedor = Fornecedor.objects.get(pk=id)
        except Fornecedor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = FornecedorSerializer(fornecedor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    '''
    /***************************************************************************
    *Função: API que deleta fornecedor pelo ID
    *Descrição: 
        Deleta fornecedor com base no ID passado na URL

    * Parametros
        request - objeto de HttpRequest
        id - id do usuario desejado

    * Valor retornado
        Retorna uma Response status 204 caso o usuario tenha sido encontrado e deletado. Caso não encontre retona uma response com status 404

    * Assertica de entrada
        request.method == 'DELETE'
        type(id) == int
        request.user.is_authenticated
    ***************************************************************************/ 
    '''
    @extend_schema(description='Deleta fornecedor com base no ID passado na URL')
    def delete(self, request, id):
        try:
            fornecedor = Fornecedor.objects.get(pk=id)
        except Fornecedor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        fornecedor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class FeiraViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny, ] 
    serializer_class = FeiraSerializer
    queryset = Feira.objects.all()

    '''
    /***************************************************************************
    *Função: API que retorna lista de feiras
    *Descrição: 
        Será feita uma query que retornará todas as feiras disponíveis.

    * Parâmetros
        request - objeto de HttpRequest

    * Valor retornado
        Retorna um JsonResponse com todas as feiras com status 200.

    * Assertiva de entrada
        request.method == 'GET'
    ***************************************************************************/
    '''
    @extend_schema(description='Retorna todas as feiras cadastradas no sistema juntamente com seu ID. Feita para usar no cadastro de um Forncedor')
    def get(self, request):
        feiras = Feira.objects.all()
        serializer = FeiraSerializer(feiras, many=True)
        return JsonResponse({"feiras":serializer.data})
    

class ClienteViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ] 
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()
        
    '''
    /***************************************************************************
    * Função: API que retorna lista de clientes
    * Descrição:
        Realiza uma query para retornar todos os clientes.

    * Parâmetros
        request - objeto de HttpRequest

    * Valor retornado
        Retorna um JsonResponse com todos os clientes com status 200.

    * Assertiva de entrada
        request.method == 'GET'
    ***************************************************************************/
    '''
    @extend_schema(description='Retorna todos os clientes do banco de dados')
    def get(self,request):
        usuarios = Cliente.objects.all()
        serializer = ClienteSerializer(usuarios, many=True)
        return JsonResponse({"usuarios": serializer.data})
    
    '''
    /***************************************************************************
    * Função: API que cria um novo cliente
    * Descrição:
        Recebe uma requisição HTTP. Cria um novo objeto no banco de dados com as informações passadas, incluindo 'nome', 'email' e 'telefone'. 
        O usuário logado deve ser do tipo cliente para ser associado ao novo cliente.

    * Parâmetros
        request - objeto de HttpRequest

    * Valor retornado
        Caso o objeto tenha sido criado, retorna uma Response com status 201_CREATED junto com os dados do novo cliente.

    * Assertiva de entrada
        request.method == 'POST'
        all(campo in request.data for campo in ['nome', 'email', 'telefone'])
        request.user.is_authenticated and request.user.is_cliente
    ***************************************************************************/
    '''
    @extend_schema(description='Cria um novo cliente no banco de dados com as informações passadas, incluindo nome, email e telefone. O usuário logado deve ser do tipo cliente para ser associado ao novo cliente')
    def post(self,request):
        data = request.data
        data["cliente_user"] = request.user.id
        serializer = ClienteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    '''
    /***************************************************************************
    * Função: API que retorna um cliente pelo ID
    * Descrição:
        Retorna um único cliente com base no ID passado na URL.

    * Parâmetros
        request - objeto de HttpRequest
        id - id do cliente desejado

    * Valor retornado
        Retorna uma Response com o cliente em questão caso seja encontrado com status 200. 
        Caso não encontre, retorna uma response com status 404.

    * Assertiva de entrada
        request.method == 'GET'
        type(id) == int
    ***************************************************************************/
    '''
    @extend_schema(description='Retorna um único cliente com base no ID passado na URL.')
    def get_specific(self,request, id):
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)
    
    '''
    /***************************************************************************
    * Função: API que atualiza um cliente pelo ID
    * Descrição:
        Atualiza o cliente com base no ID passado na URL.

    * Parâmetros
        request - objeto de HttpRequest
        id - id do cliente desejado

    * Valor retornado
        Retorna uma Response com o cliente atualizado em questão caso seja encontrado com status 200. 
        Caso não encontre, retorna uma response com status 404.

    * Assertiva de entrada
        request.method == 'PUT'
        type(id) == int
        request.user.is_authenticated
    ***************************************************************************/
    '''

    @extend_schema(description='Atualiza o cliente com base no ID passado na URL. O usuario deve estar logado')
    def put(self,request, id):
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ClienteSerializer(cliente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    '''
    /***************************************************************************
    * Função: API que deleta um cliente pelo ID
    * Descrição:
        Deleta o cliente com base no ID passado na URL.

    * Parâmetros
        request - objeto de HttpRequest
        id - id do cliente desejado

    * Valor retornado
        Retorna uma Response status 204 caso o cliente tenha sido encontrado e deletado. 
        Caso não encontre, retorna uma response com status 404.

    * Assertiva de entrada
        request.method == 'DELETE'
        type(id) == int
        request.user.is_authenticated
    ***************************************************************************/
    '''
    @extend_schema(description='Deleta o cliente com base no ID passado na URL. O usuario deve estar logado')
    def delete(self,request, id):
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    


class MensagemViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = MensagemSerializer
    queryset = Mensagem.objects.all()

    '''
    /***************************************************************************
    *Função: API que retorna lista de mensagens
    *Descrição: 
        Será feita uma query que retornará todas as mensagens entre dois usuarios.

    * Parâmetros
        request - objeto de HttpRequest
        user1 - id do usuario 1
        user2 - id do usuario 2

    * Valor retornado
        Retorna um JsonResponse com todas as mensagens entre os usuarios com status 200.

    * Assertiva de entrada
        request.method == 'GET'
    ***************************************************************************/
    '''
    @extend_schema(description='Será feita uma query que retornará todas as mensagens entre dois usuarios. Retorna de maneira ordenada')
    def get_msg_cliente_fornecedor(self,request,user2):
        user1 = request.user.id

        print('usuarios',user1, user2)

        mensagens = Mensagem.objects.filter((Q(destinatario_id=user1) & Q(remetente_id=user2)) | (Q(destinatario_id=user2) & Q(remetente_id=user1))).order_by('data_envio')

        print("a")

        m = Mensagem.objects.all()

        for mm in m:
            print(mm.__dict__)

        for mensagem in mensagens:
            print(mensagem.__dict__)

        # for msg in mensagens:
        #     print(msg.__dict__)

        serializer = MensagemSerializer(mensagens, many=True)

        

        return JsonResponse({"mensagens": serializer.data})
    
    '''
    /***************************************************************************
    *Função: API que criar uma nova mensagem
    *Descrição: 
        Recebe uma requisição HTTP. É criada uma nova mensagem no banco de dados a partir das informações passadas, incluindo 'destinatario', 'conteudo' e 'data_envio'. O usuario devera estar autenticado para que ele seja o remetente da mensagem no banco de dados

    * Parâmetros
        request - objeto de HttpRequest

    * Valor retornado
        Caso a mensagem tenha sido criada, retorna uma Response com status 201_CREATED junto com os dados da nova mensagem.

    * Assertiva de entrada
        request.method == 'POST'
        all(campo in request.data for campo in ['destinatario', 'conteudo', 'data_envio'])
        request.user.is_authenticated
    ***************************************************************************/
    '''
    @extend_schema(description='É criada uma nova mensagem no banco de dados a partir das informações passadas, incluindo destinatario, conteudo e data_envio. O usuario devera estar autenticado para que ele seja o remetente da mensagem no banco de dados')
    def post(self,request):
        # data = request.data
        # data["remetente"] = request.user.id
        serializer = MensagemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)


class AvaliacaoViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ] 
    serializer_class = AvaliacaoSerializer
    queryset = Avaliacao.objects.all()
        

    '''
    /***************************************************************************
    *Função: API que retorna lista de avaliações
    *Descrição: 
        Será feita uma query que retornará todas as avaliações.

    * Parâmetros
        request - objeto de HttpRequest

    * Valor retornado
        Retorna um JsonResponse com todas as avaliações com status 200.

    * Assertiva de entrada
        request.method == 'GET'
    ***************************************************************************/
    '''

    @extend_schema(description='retorna todas as avaliações de um produto do banco de dados')

    def get_all(self,request):
        avaliacoes = Avaliacao.objects.all()
        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return JsonResponse({"avaliacoes": serializer.data})


    def get(self,request, id):
        # print(request.user.id)
        avaliacoes = Avaliacao.objects.filter(produto=id)
        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return JsonResponse({"avaliacoes": serializer.data})
    

    '''
    /***************************************************************************
    *Função: API que criar uma nova avaliação
    *Descrição: 
        Recebe uma requisição HTTP. É criada uma nova avaliação no banco de dados a partir das informações passadas, incluindo 'produto' ,'nota' e 'comentario'. É necessario estar autenticado para que a nova avaliação seja associada ao usuario

    * Parâmetros
        request - objeto de HttpRequest

    * Valor retornado
        Caso a avaliação tenha sido criada, retorna uma Response com status 201_CREATED junto com os dados da nova avaliação.

    * Assertiva de entrada
        request.method == 'POST'
        all(campo in request.data for campo in ['produto', 'nota','comentario'])
        request.user.is_authenticated
        request.user.is_cliente
    ***************************************************************************/
    '''

    @extend_schema(description='É criada uma nova avaliação no banco de dados a partir das informações passadas, incluindo produto ,nota e comentario. É necessario estar autenticado para que a nova avaliação seja associada ao usuario')
    def post(self,request):
        data = request.data
        data["cliente"] = Cliente.objects.get(cliente_user=request.user).id
        serializer = AvaliacaoSerializer(data=data)
        if serializer.is_valid():
            ava = serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

    '''
    /***************************************************************************
    *Função: API que retorna uma avaliação pelo ID
    *Descrição: 
        Retorna uma única avaliação a partir do ID passado na URL.

    * Parâmetros
        request - objeto de HttpRequest
        id - ID da avaliação desejada

    * Valor retornado
        Retorna uma Response com a avaliação em questão caso seja encontrada com status 200. Caso não encontre, retorna uma response com status 404.

    * Assertiva de entrada
        request.method == 'GET'
        type(id) == int
    ***************************************************************************/
    '''
    @extend_schema(description='Retorna uma única avaliação a partir do ID passado na URL.')
    def get_specific(self,request, id):
        try:
            avaliacao = Avaliacao.objects.get(pk=id)
        except Avaliacao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        serializer = AvaliacaoSerializer(avaliacao)
        return Response(serializer.data)
    
    '''
    /***************************************************************************
    *Função: API atualiza uma avaliação pelo ID
    *Descrição: 
        Atualiza uma avaliação com base no ID passado na URL.

    * Parâmetros
        request - objeto de HttpRequest
        id - ID da avaliação desejada

    * Valor retornado
        Retorna uma Response com a avaliação atualizada em questão caso seja encontrada com status 200. Caso não encontre, retorna uma response com status 404.

    * Assertiva de entrada
        request.method == 'PUT'
        type(id) == int
        request.user.is_authenticated
    ***************************************************************************/
    '''
    @extend_schema(description='Atualiza uma avaliação com base no ID passado na URL. O usuario deve estar logado')
    def put(self,request, id):
        try:
            avaliacao = Avaliacao.objects.get(pk=id)
        except Avaliacao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AvaliacaoSerializer(avaliacao, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    '''
    /***************************************************************************
    *Função: API que deleta uma avaliação pelo ID
    *Descrição: 
        Deleta uma avaliação com base no ID passado na URL.

    * Parâmetros
        request - objeto de HttpRequest
        id - ID da avaliação desejada

    * Valor retornado
        Retorna uma Response status 204 caso a avaliação tenha sido encontrada e deletada. Caso não encontre, retorna uma response com status 404.

    * Assertiva de entrada
        request.method == 'DELETE'
        type(id) == int
        request.user.is_authenticated
    ***************************************************************************/
    '''
    @extend_schema(description='Deleta uma avaliação com base no ID passado na URL. O usuario deve estar logado')
    def delete(self,request, id):
        try:
            avaliacao = Avaliacao.objects.get(pk=id)
        except Avaliacao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        avaliacao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class RelatorioViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
#     permission_classes = [AllowAny, ] 
#     serializer_class = RelatorioSerializer
#     queryset = Relatorio.objects.all()
        

#     @extend_schema(description='Retorna todos os relatorios do banco de dados')
#     def get(self,request):
#         # print(request.user.id)
#         relatorios = Relatorio.objects.all()
#         serializer = RelatorioSerializer(relatorios, many=True)
#         return JsonResponse({"relatorios": serializer.data})
    
#     def post(self,request):
#         serializer = RelatorioSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        


        
#     def get_specific(self,request, id):
#         try:
#             relatorio = Relatorio.objects.get(pk=id)
#         except Relatorio.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
    
#         serializer = RelatorioSerializer(relatorio)
#         return Response(serializer.data)
    
#     def put(self,request, id):
#         try:
#             relatorio = Relatorio.objects.get(pk=id)
#         except Relatorio.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         serializer = RelatorioSerializer(relatorio, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request, id):
#         try:
#             relatorio = Relatorio.objects.get(pk=id)
#         except Relatorio.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         relatorio.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request,'home.html')


def chat(request, id):
    context = {
        "id": id
    }
    return render(request,'chat.html',context)

def criar_usuario(request):
    return render(request, 'criarUsuario.html')

def login_view(request):
    return render(request,'login.html')

def produto_especifico(request, id):
    context = {
        "id": id
    }
    return render(request, 'produto.html', context)

def criar_fornecedor(request):
    return render(request,'criarFornecedor.html')

def criar_produto(request):
    return render(request,'cadastro_produto.html')

def produtos_comprados(request):
    return render(request,'produtos_comprados.html')





