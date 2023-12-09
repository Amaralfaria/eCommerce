from django.contrib import admin
from .models import Usuario, Fornecedor, Produto, Avaliacao,Cliente ,Compra, Mensagem, Categoria, Feira

# registrando modelos

admin.site.register(Usuario)
admin.site.register(Fornecedor)
admin.site.register(Produto)
admin.site.register(Avaliacao)
admin.site.register(Cliente)
admin.site.register(Compra)
admin.site.register(Mensagem)
admin.site.register(Categoria)
admin.site.register(Feira)
