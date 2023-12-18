from pytest_factoryboy import register
from rest_framework.test import APIClient
import pytest
from .factories import *

register(UsuarioFactory)
register(ClienteFactory)
register(ForncedorFactory)
register(ProdutoFactory)
register(CompraFactory)
register(AvaliacaoFactory)
register(MensagemFactory)
register(FeiraFactory)
register(CategoriaFactory)

@pytest.fixture
def api_client():
    return APIClient