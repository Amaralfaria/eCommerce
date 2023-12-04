from django.http import JsonResponse
from .models import Produto
from .serializers import *
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework import  mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django.db import transaction



class ProdutoViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated, ] 
    serializer_class = ProdutoSerializer
    queryset = Produto.objects.all()

    def get(self, request):
        produtos = Produto.objects.all()

        nomeProduto = request.query_params.get('nomeProduto',None)
        precoMaximo = request.query_params.get('precoMaximo',None)
        precoMinimo = request.query_params.get('precoMinimo',None)
        # fornecedorProduto = request.query_params.get('fornecedor',None)
        raio = request.query_params.get('raio',None)

        if nomeProduto:
            produtos = produtos.filter(Q(nome__icontains=nomeProduto))
        if precoMaximo:
            print(precoMaximo)
            produtos = produtos.filter(Q(preco__lte=precoMaximo))
        if precoMinimo:
            produtos = produtos.filter(Q(preco__gte=precoMinimo))


        serializer = ProdutoSerializer(produtos, many=True)
        return JsonResponse({"produtos":serializer.data})
    
    def post(self, request):
        serializer = ProdutoSerializer(data=request.data)
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
    

class UsuarioViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny,]
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return JsonResponse({"Usuarios": serializer.data})
    

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

    def get(self, request):
        fornecedores = Fornecedor.objects.all()
        serializer = FornecedorSerializer(fornecedores, many=True)
        return JsonResponse({"fornecedores": serializer.data})
    

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
        serializer = FornecedorSerializer(data=request.data)
        if serializer.is_valid():
            fornecedor = serializer.save()
            fornecedor.fornecedor_user = request.user

            return Response(dict(request.data), status=status.HTTP_201_CREATED)




        
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
    

class ClienteViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ] 
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()
        
    def get(self,request):
        usuarios = Cliente.objects.all()
        serializer = ClienteSerializer(usuarios, many=True)
        return JsonResponse({"usuarios": serializer.data})
    
    
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
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            cliente = serializer.save()
            cliente.cliente_user = request.user

            return Response(dict(request.data), status=status.HTTP_201_CREATED)
        
        
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
    



    

class AvaliacaoViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ] 
    serializer_class = AvaliacaoSerializer
    queryset = Avaliacao.objects.all()
        
    def get(self,request):
        print(request.user.id)
        avaliacoes = Avaliacao.objects.all()
        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return JsonResponse({"avaliacoes": serializer.data})
    
    def post(self,request):
        serializer = AvaliacaoSerializer(data=request.data)
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
    permission_classes = [IsAuthenticated, ] 
    serializer_class = RelatorioSerializer
    queryset = Relatorio.objects.all()
        
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







