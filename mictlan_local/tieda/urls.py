from re import template
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('home/', views.home, name='home'),
    path('clientes/', views.clientes, name='clientes'),
    path('verpedidos/', views.verpedidos, name='verpedidos'),
    path('eliminar-cliente/<id>', views.eliminar_cliente, name='eliminar_cliente'),
    path('eliminar-pedido/<id>/', views.eliminar_pedido, name='eliminar_pedido'),
    path('actualizar-pedido/<id>/', views.actualizar_pedido, name='actualizar_pedido'),
    path('eliminar-lista/<id>/', views.eliminar_lista, name='eliminar_lista'),
    path('', LoginView.as_view(template_name='paginas/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='paginas/logout.html'), name='logout'),
]