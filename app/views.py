from django.http import JsonResponse
from .models import Produto
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET','POST'])
def lista_produtos(request):

    if request.method == 'GET':
        produtos = Produto.objects.all()
        serializer = ProdutoSerializer(produtos, many=True)
        return JsonResponse({"produtos":serializer.data})
    elif request.method == 'POST':
        serializer = ProdutoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','DELETE'])
def produto_by_id(request, id):

    try:
        produto = Produto.objects.get(pk=id)
    except Produto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProdutoSerializer(produto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        produto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def lista_usuarios(request):

    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return JsonResponse({"usuarios": serializer.data})
    elif request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def usuario_by_id(request, id):

    try:
        usuario = Usuario.objects.get(pk=id)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def login_request(request):
    if request.method == 'POST':
        try:
            userEmail = request.data["email"]
            userPassword = request.data["password"]
            usuario = Usuario.objects.get(email=userEmail, password=userPassword)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(status=status.HTTP_200_OK)



    
@api_view(['GET', 'POST'])
def lista_fornecedores(request):

    if request.method == 'GET':
        fornecedores = Fornecedor.objects.all()
        serializer = FornecedorSerializer(fornecedores, many=True)
        return JsonResponse({"fornecedores": serializer.data})
    elif request.method == 'POST':
        serializer = FornecedorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def fornecedor_by_id(request, id):

    try:
        fornecedor = Fornecedor.objects.get(pk=id)
    except Fornecedor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FornecedorSerializer(fornecedor)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = FornecedorSerializer(fornecedor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        fornecedor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def lista_avaliacoes(request):

    if request.method == 'GET':
        avaliacoes = Avaliacao.objects.all()
        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return JsonResponse({"avaliacoes": serializer.data})
    elif request.method == 'POST':
        serializer = AvaliacaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def avaliacao_by_id(request, id):

    try:
        avaliacao = Avaliacao.objects.get(pk=id)
    except Avaliacao.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AvaliacaoSerializer(avaliacao)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = AvaliacaoSerializer(avaliacao, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        avaliacao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def lista_relatorios(request):

    if request.method == 'GET':
        relatorios = Relatorio.objects.all()
        serializer = RelatorioSerializer(relatorios, many=True)
        return JsonResponse({"relatorios": serializer.data})
    elif request.method == 'POST':
        serializer = RelatorioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def relatorio_by_id(request, id):

    try:
        relatorio = Relatorio.objects.get(pk=id)
    except Relatorio.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = RelatorioSerializer(relatorio)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RelatorioSerializer(relatorio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        relatorio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

