from django.shortcuts import render

def criar_usuario(request):
    return render(request, 'criar_usuario.html')