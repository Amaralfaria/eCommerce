from django.http import JsonResponse
from .models import Produto
from .serializers import *
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework import  mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.utils import get_jwt_tokens



class AutenticacaoViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = AutenticacaoSerializer
    queryset = Usuario.objects.all()

    def post(self,request):
        try:
            userEmail = request.data["email"]
            userPassword = request.data["password"]
            usuario = Usuario.objects.get(email=userEmail, password=userPassword)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


        return JsonResponse(get_jwt_tokens(usuario))
        
        return Response(status=status.HTTP_200_OK)



class ProdutoViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ] 
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
    




class FornecedorViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ] 
    serializer_class = FornecedorSerializer
    queryset = Fornecedor.objects.all()

    def get(self, request):
        fornecedores = Fornecedor.objects.all()
        serializer = FornecedorSerializer(fornecedores, many=True)
        return JsonResponse({"fornecedores": serializer.data})
    
    def post(self, request):
        serializer = FornecedorSerializer(data=request.data)
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
    

class UsuarioViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ] 
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()
        
    def get(self,request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return JsonResponse({"usuarios": serializer.data})
    
    def post(self,request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def get_specific(self,request, id):
        try:
            usuario = Usuario.objects.get(pk=id)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    
    def put(self,request, id):
        try:
            usuario = Usuario.objects.get(pk=id)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, id):
        try:
            usuario = Usuario.objects.get(pk=id)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)     
    



    

class AvaliacaoViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ] 
    serializer_class = AvaliacaoSerializer
    queryset = Avaliacao.objects.all()
        
    def get(self,request):
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







