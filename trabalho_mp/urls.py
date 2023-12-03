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





urlpatterns = [
    path('admin/', admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/docs/",SpectacularSwaggerView.as_view(url_name="schema")),

    #produtos
    path("produtos/",views.ProdutoViewSet.as_view({"get":"get","post":"post"}), name="produtos"),
    path("produtos/<int:id>", views.ProdutoViewSet.as_view({"get":"get_specific","put":"put","delete":"delete"})),

    #usuarios
    path("usuarios/", views.UsuarioViewSet.as_view({"get":"get","post":"post"}), name="usuarios"),
    path('usuarios/<int:id>', views.UsuarioViewSet.as_view({"get":"get_specific","put":"put","delete":"delete"})),

    #fornecedores
    path('fornecedores/', views.FornecedorViewSet.as_view({"get":"get","post":"post"})),
    path('fornecedores/<int:id>', views.FornecedorViewSet.as_view({"get":"get_specific","put":"put","delete":"delete"})),

    #avaliacoes
    path('avaliacoes/', views.AvaliacaoViewSet.as_view({"get":"get","post":"post"})),
    path('avaliacoes/<int:id>', views.AvaliacaoViewSet.as_view({"get":"get_specific","put":"put","delete":"delete"})),

    #relatorios
    path('relatorios/', views.RelatorioViewSet.as_view({"get":"get","post":"post"})),
    path('relatorios/<int:id>', views.RelatorioViewSet.as_view({"get":"get_specific","put":"put","delete":"delete"})),

    #Clientes
    path('cliente/', views.ClienteViewSet.as_view({"get":"get","post":"post"})),
    path('cliente/<int:id>', views.ClienteViewSet.as_view({"get":"get_specific","put":"put","delete":"delete"})),

    #tokens
    # path('usuarios/login/refresh', TokenRefreshView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/verify', TokenVerifyView.as_view(), name="token_verify"),
    path('token/refresh', TokenRefreshView.as_view(), name="token_refresh"),
]
