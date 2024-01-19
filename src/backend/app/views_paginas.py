from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, "home.html")


def chat(request, id):
    context = {"id": id}
    return render(request, "chat.html", context)


def criar_usuario(request):
    return render(request, "criarUsuario.html")


def login_view(request):
    return render(request, "login.html")


def produto_especifico(request, id):
    context = {"id": id}
    return render(request, "produto.html", context)


def criar_fornecedor(request):
    return render(request, "criarFornecedor.html")


def criar_produto(request):
    return render(request, "cadastro_produto.html")


def produtos_comprados(request):
    return render(request, "produtos_comprados.html")


def conversas_fornecedores(request):
    return render(request, "conversas_fornecedor.html")
