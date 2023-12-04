from django.contrib import admin
from .models import Usuario, Fornecedor, Produto, Avaliacao,Cliente 

# registrando modelos

admin.site.register(Usuario)
admin.site.register(Fornecedor)
admin.site.register(Produto)
admin.site.register(Avaliacao)
admin.site.register(Cliente)
