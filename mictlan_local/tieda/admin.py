from django.contrib import admin
from .models import PedidoCompleto, Cliente, PedidoIncompleto

admin.site.register(PedidoCompleto)
admin.site.register(Cliente)
admin.site.register(PedidoIncompleto)