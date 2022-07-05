from http.client import PRECONDITION_FAILED
from django.db import models
from datetime import datetime, date

class PedidoCompleto(models.Model):
    fecha = models.CharField(max_length=30)
    id_pedido = models.IntegerField()
    nombre_pedido = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()
    descripcion = models.CharField(max_length=50)
    montextra = models.IntegerField()
    subtotal = models.IntegerField()
    total = models.IntegerField()
    calle = models.CharField(max_length=50)
    colonia = models.CharField(max_length=50)
    entrecalles = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    def __str__(self):
        pedidostr = str(self.id_pedido)
        cantidadstr = str(self.cantidad)
        cadena = pedidostr +"/"+ self.nombre_pedido +"/"+ cantidadstr +"/"+ self.calle
        return cadena

class Cliente(models.Model):
    telefono = models.CharField(max_length=50)
    calle = models.CharField(max_length=50)
    colonia = models.CharField(max_length=50)
    entrecalles = models.CharField(max_length=50)

    def __str__(self):
        cadena = self.telefono + "/" + self.calle
        return cadena

class PedidoIncompleto(models.Model):
    id_pedido = models.IntegerField()
    nombre = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()
    descripcion = models.CharField(max_length=50)
    montoextra = models.IntegerField()
    subtotal = models.IntegerField()
    total = models.IntegerField()
