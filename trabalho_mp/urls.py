"""
URL configuration for trabalho_mp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView
from app.views import index, criar_usuario, produto_especifico, login_view, criar_fornecedor, criar_produto,produtos_comprados, home, chat, conversas_fornecedores

urlpatterns = [
    path('admin/', admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/docs/",SpectacularSwaggerView.as_view(url_name="schema")),

    #produtos
    path("produtos/",views.ProdutoViewSet.as_view({"get":"get","post":"post"}), name="produtos"),
    path("produtos/<int:id>", views.ProdutoViewSet.as_view({"get":"get_specific","put":"put","delete":"delete"})),

    #categorias
    path('categorias/', views.CategoriaViewSet.as_view({"get":"get"})),
    path('categorias/<int:id>', views.CategoriaViewSet.as_view({"get":"get_specific"})),

    #Compras
    path("cliente/compras/", views.CompraViewSet.as_view({"get":"get_cliente_compras","post":"post"})),
    path("cliente/compras/<int:id>", views.CompraViewSet.as_view({"get":"get_specific","delete":"delete"})),


    #usuarios
    path("usuarios/", views.UsuarioViewSet.as_view({"get":"get","post":"post"}), name="usuarios"),
    path('usuarios/<int:id>', views.UsuarioViewSet.as_view({"get":"get_specific","put":"put","delete":"delete"})),
    path('logout/', views.UsuarioViewSet.as_view({"get":"logout_user"})),

    #fornecedores
    path('fornecedores/', views.FornecedorViewSet.as_view({"get":"get","post":"post"})),
    path('fornecedores/<int:id>', views.FornecedorViewSet.as_view({"get":"get_specific","put":"put","delete":"delete"})),

    #feiras
    path('feira/', views.FeiraViewSet.as_view({"get":"get"})),

    #Mensagens
    path('mensagens/<int:user2>', views.MensagemViewSet.as_view({"get":"get_msg_cliente_fornecedor"})),
    path('mensagens/', views.MensagemViewSet.as_view({"post":"post"})),
    path('mensagens_fornecedor/', views.MensagemViewSet.as_view({"get":"get_diferentes_usuarios_chat"})),

    #avaliacoes
    path('avaliacoes_produto/<int:id>', views.AvaliacaoViewSet.as_view({"get":"get"})),
    path('avaliacoes/<int:id>', views.AvaliacaoViewSet.as_view({"get":"get_specific","put":"put","delete":"delete"})),
    path('avaliacoes/', views.AvaliacaoViewSet.as_view({"post":"post","get":"get_all"})),

    #relatorios
    # path('relatorios/', views.RelatorioViewSet.as_view({"get":"get","post":"post"})),
    # path('relatorios/<int:id>', views.RelatorioViewSet.as_view({"get":"get_specific","put":"put","delete":"delete"})),
    # path('relatorios/', views.RelatorioViewSet.as_view({"get":"get","post":"post"})),


    #Clientes
    path('cliente/', views.ClienteViewSet.as_view({"get":"get","post":"post"})),
    path('cliente/<int:id>', views.ClienteViewSet.as_view({"get":"get_specific","put":"put","delete":"delete"})),

    #tokens
    # path('usuarios/login/refresh', TokenRefreshView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/verify', TokenVerifyView.as_view(), name="token_verify"),
    path('token/refresh', TokenRefreshView.as_view(), name="token_refresh"),

    #templates
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('criar_usuario/', criar_usuario,name='cadastro'),
    path('visualizar_produto/<int:id>',produto_especifico, name='visualização de produto unico'),
    path('login/', login_view, name='login'),
    path('criar_fornecedor/',criar_fornecedor, name='criar fornecedor'),
    path('criar_produto/',criar_produto, name='criar produto'),
    path('produtos_comprados/',produtos_comprados, name='criar produto'),
    path('chat/<int:id>',chat, name='chat privado'),
    path('conversas/',conversas_fornecedores, name='conversas de um fornecedor'),
]
