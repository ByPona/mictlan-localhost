from code import interact
from mailbox import NoSuchMailboxError
from django import forms

class AgregarPedido(forms.Form):
    num_pedido = forms.IntegerField()
    producto = forms.CharField()
    cantidad = forms.IntegerField()
    producto_extra = forms.CharField()
    monto_extra = forms.IntegerField()

    calleynum = forms.CharField()
    colonia = forms.CharField()
    entrecalles = forms.CharField()
    telefono = forms.CharField()

