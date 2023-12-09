from django.http import JsonResponse
from .models import Produto
from .serializers import *
from rest_framework.response import Response
from django.db.models import Q, F
from rest_framework import status
from rest_framework import  mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from datetime import date
from drf_spectacular.utils import extend_schema
from .utils import haversine





class ProdutoViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ] 
    serializer_class = ProdutoSerializer
    queryset = Produto.objects.all()


    @extend_schema(description='Faz uma query de todos os produtos e faz uma filtragem baseada nos parametros baseados pela URL. Parametros: nomeProduto,precoMaximo,precoMinimo,raio, latitude e longitude do cliente')
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
            produtos = produtos.filter(haversine(lat1=latitudeCliente,lon1=longitudeCliente,lat2=F('fornecedor__latitude'),lon2=F('fornecedor__longitude')) <= raio)

        if feira:
            produtos = produtos.filter(Q(fornecedor__feira=int(feira)))
        if fornecedorProduto:
            produtos = produtos.filter(Q(fornecedor__nome_do_negocio__icontains=fornecedorProduto))
        if nomeProduto:
            produtos = produtos.filter(Q(nome__icontains=nomeProduto))
        if precoMaximo:
            precoMaximo = float(precoMaximo)
            produtos = produtos.filter(Q(preco__lte=precoMaximo))
        if precoMinimo:
            precoMinimo = float(precoMinimo)
            produtos = produtos.filter(Q(preco__gte=precoMinimo))


        serializer = ProdutoSerializer(produtos, many=True)
        return JsonResponse({"produtos":serializer.data})
    

    @extend_schema(description='Cria um produto, é necessario estar logado com o usuario do fornecedor que está adicionando o produto. Não é necesario incluir o campo do fornecedor, ele será obtido pela autenticação')
    def post(self, request):
        data = request.data
        data["fornecedor"] = Fornecedor.objects.get(fornecedor_user=request.user).id
        serializer = ProdutoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
    
    def get_specific(self, request, id):
        try:
            produto = Produto.objects.get(pk=id)
        except Produto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)
    
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

    @extend_schema(description='Retorna todas as categorias registradas. Feita para utilizar no cadastro dos produtos')
    def get(self,request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return JsonResponse({"categorias":serializer.data})



class CompraViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = CompraSerializer
    queryset = Compra.objects.all()

    @extend_schema(description='Retorna as compras do cliente logado. Não preencher o campo cliente, ele será puxado do usuario autenticado')
    def get_cliente_compras(self, request):
        try:
            cliente = Cliente.objects.get(cliente_user=request.user)
        except Cliente.DoesNotExist:
            return Response("Usuario logado não é cliente", status=status.HTTP_403_FORBIDDEN)
        
        compras = Compra.objects.filter(cliente=cliente)
        serializer = CompraSerializer(compras, many=True)

        return JsonResponse({"Compras":serializer.data}, status=status.HTTP_200_OK)

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
        
    def get_specific(self,request,id):
        try:
            compra = Compra.objects.get(pk=id)
        except Compra.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CompraSerializer(compra)
        return Response(serializer.data)

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


    @extend_schema(description='Retorna todos os usuarios do banco de dados')
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return JsonResponse({"Usuarios": serializer.data})
    
    @extend_schema(description='Cria um usuario o qual devera ser cliente ou fornecedor')
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def get_specific(self, request, id):
        try:
            usuario = Usuario.objects.get(pk=id)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    
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

    @extend_schema(description='Retorna todos os fornecedores do banco de dados')
    def get(self, request):
        fornecedores = Fornecedor.objects.all()
        serializer = FornecedorSerializer(fornecedores, many=True)
        return JsonResponse({"fornecedores": serializer.data})
    
    @extend_schema(description='Para criar um fornecedor é necessario estar logado com um usuario do tipo is_fornecedor para ele ser associado ao novo forncedor. Não é necessario incluir o campo fornecedor_user')
    def post(self, request):
        # serializer = FornecedorSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # fields_usuario = ['username','email','telefone','password']
        # fields_fornecedor = ['nome_do_negocio', 'endereco', 'latitude', 'longitude']

        # dict_usuario = {key: value for key, value in request.data.items() if key in fields_usuario}

        # dict_fornecedor = {key: value for key, value in request.data.items() if key in fields_fornecedor}

        # dict_usuario['is_cliente'] = True

        # serializer_usuario = UsuarioSerializer(data=dict_usuario)
        # serializer_fornecedor = FornecedorSerializer(data=dict_fornecedor)
        # if serializer_usuario.is_valid() and serializer_fornecedor.is_valid():
        #     user = serializer_usuario.save()
        #     fornecedor = serializer_fornecedor.save()
        #     fornecedor.fornecedor_user = user

        #     return Response(dict(request.data), status=status.HTTP_201_CREATED)
        data = request.data
        data["fornecedor_user"] = request.user.id
        
        serializer = FornecedorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)




    
    def get_specific(self, request, id):
        try:
            fornecedor = Fornecedor.objects.get(pk=id)
        except Fornecedor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = FornecedorSerializer(fornecedor)
        return Response(serializer.data)
    
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


    @extend_schema(description='Retorna todas as feiras cadastradas no sistema juntamente com seu ID. Feita para usar no cadastro de um Forncedor')
    def get(self, request):
        feiras = Feira.objects.all()
        serializer = FeiraSerializer(feiras, many=True)
        return JsonResponse({"feiras":serializer.data})
    

class ClienteViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ] 
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()
        

    @extend_schema(description='Retorna todos os clientes do banco de dados')
    def get(self,request):
        usuarios = Cliente.objects.all()
        serializer = ClienteSerializer(usuarios, many=True)
        return JsonResponse({"usuarios": serializer.data})
    
    @extend_schema(description='Para criar um cliente é necessario estar logado com um usuario do tipo is_cliente para ele ser associado ao novo cliente. Não é necessario incluir o campo cliente_user, ele irá ser preenchido com o usuario do tipo cliente autenticado')
    def post(self,request):

        # fields_usuario = ['username','email','telefone','password']
        # fields_cliente = ['preferencias_de_busca']

        # dict_usuario = {key: value for key, value in request.data.items() if key in fields_usuario}

        # dict_cliente = {key: value for key, value in request.data.items() if key in fields_cliente}

        # dict_usuario['is_cliente'] = True

        # serializer_usuario = UsuarioSerializer(data=dict_usuario)
        # serializer_cliente = ClienteSerializer(data=dict_cliente)
        # if serializer_usuario.is_valid() and serializer_cliente.is_valid():
        #     user = serializer_usuario.save()
        #     client = serializer_cliente.save()
        #     client.cliente_user = user

        #     return Response(dict(request.data), status=status.HTTP_201_CREATED)
        data = request.data
        data["cliente_user"] = request.user.id
        serializer = ClienteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
    def get_specific(self,request, id):
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)
    
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
    
    def delete(self,request, id):
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    


class MensagemViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = MensagemSerializer
    queryset = Mensagem.objects.all()


    @extend_schema(description='Retorna todas as mensagens entre user1 e user2. Retorna de maneira ordenada')
    def get_msg_cliente_fornecedor(self,request,user1,user2):
        mensagens = Mensagem.objects.filter((Q(destinatario=user1) & Q(remetente=user2)) | (Q(destinatario=user2) & Q(remetente=user1))).order_by('data_envio')

        for msg in mensagens:
            print(msg.__dict__)

        serializer = MensagemSerializer(mensagens, many=True)

        

        return JsonResponse({"mensagens": serializer.data})
    
    @extend_schema(description='Cria uma nova mensagem. O remetente será o usuario autenticado e o destinatario será o id de um Usuario')
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
        

    @extend_schema(description='retorna todas as avaliações do banco de dados. Filtragem baseada em produto ainda não feita')
    def get(self,request):
        print(request.user.id)
        avaliacoes = Avaliacao.objects.all()
        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return JsonResponse({"avaliacoes": serializer.data})
    

    @extend_schema(description='Cria nova avaliação. Para usar deve estar autenticado com um cliente para preencher o campo cliente. Não é necessario preencher o campo cliente')
    def post(self,request):
        data = request.data
        data["cliente"] = Cliente.objects.get(cliente_user=request.user).id
        serializer = AvaliacaoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        


        
    def get_specific(self,request, id):
        try:
            avaliacao = Avaliacao.objects.get(pk=id)
        except Avaliacao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        serializer = AvaliacaoSerializer(avaliacao)
        return Response(serializer.data)
    

    
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
    
    def delete(self,request, id):
        try:
            avaliacao = Avaliacao.objects.get(pk=id)
        except Avaliacao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        avaliacao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RelatorioViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny, ] 
    serializer_class = RelatorioSerializer
    queryset = Relatorio.objects.all()
        

    @extend_schema(description='Retorna todos os relatorios do banco de dados')
    def get(self,request):
        print(request.user.id)
        relatorios = Relatorio.objects.all()
        serializer = RelatorioSerializer(relatorios, many=True)
        return JsonResponse({"relatorios": serializer.data})
    
    def post(self,request):
        serializer = RelatorioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        


        
    def get_specific(self,request, id):
        try:
            relatorio = Relatorio.objects.get(pk=id)
        except Relatorio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        serializer = RelatorioSerializer(relatorio)
        return Response(serializer.data)
    
    def put(self,request, id):
        try:
            relatorio = Relatorio.objects.get(pk=id)
        except Relatorio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RelatorioSerializer(relatorio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request, id):
        try:
            relatorio = Relatorio.objects.get(pk=id)
        except Relatorio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        relatorio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







