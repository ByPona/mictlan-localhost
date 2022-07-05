from multiprocessing import context
from re import T
from ssl import AlertDescription
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls import is_valid_path
from .forms import AgregarPedido
from .models import PedidoCompleto, Cliente
from datetime import datetime
from django.contrib import messages
from django.urls import reverse_lazy

class Pedido(object):
    def __init__(self, columna, num_pedido, producto, cantidad, precio_unitario, prodextra, montoextra, total, totaltotales):
        self.columna = columna
        self.num_pedido = num_pedido
        self.producto = producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.prodextra = prodextra
        self.montoextra = montoextra
        self.total = total
        self.totaltotales = totaltotales


    def __str__(self):
        return "Objeto = %s %s %s %s %s" % (self.num_pedido, self.producto, self.cantidad, self.prodextra, self.montoextra)


pedidos = []
globals()['id_num_pedido'] = 1

def home(request):
    
    if request.user.is_authenticated:
        pass
    else:
        return redirect('login')

    telefono_exist = ""
    fechaobj = str(datetime.today().strftime('%d/%m/%Y')) 
    pedidoscompletos = PedidoCompleto.objects.filter(fecha__exact=fechaobj).order_by("id_pedido")
    
    if request.method == 'POST':

        if 'id_pedido' in request.POST:
            num_pedido = request.POST['id_pedido']
        else:
            num_pedido = False

        if 'prod' in request.POST:
            producto = request.POST['prod']
        else:
            producto = False

        if 'cantidad' in request.POST:
            cantidad = request.POST['cantidad']
        else:
            cantidad = False

        if 'prodextra' in request.POST:
            prodextra = request.POST['prodextra']
        else:
            prodextra = False

        if 'montextra' in request.POST:
            montextra = request.POST['montextra']
        else:
            montextra = False

        if 'dom' in request.POST:
            calleynum = request.POST['dom']
        else:
            calleynum = False

        if 'col' in request.POST:
            col = request.POST['col']
        else:
            col = False

        if 'entre_calles' in request.POST:
            entrecalles = request.POST['entre_calles']
        else:
            entrecalles = False

        if 'tel' in request.POST:
            telefono = request.POST['tel']
        else:
            telefono = False

        #Atrapa siempre el numero de pedido para que no se necesite voler a poner
        if(len(pedidos)>0):
            num_pedido = pedidos[0].num_pedido
            
        #Valida el codigo de producto
        if(num_pedido!="" and producto!="" and cantidad!=""):
            if (producto == "cla"):
                producto = "Clasica"
                precio_unitario = 85
            elif (producto == "xoc"):
                producto = "Xochipilli"
                precio_unitario = 85
            elif (producto == "jag"):
                precio_unitario = 90
                producto = "Jaguar"
            elif (producto == "que"):
                precio_unitario = 90
                producto = "Quetzal"
            elif (producto == "cha"):
                precio_unitario = 90
                producto = "Chamuco"
            elif (producto == "tla"):
                precio_unitario = 95
                producto = "Tlaloc"
            elif (producto == "mal"):
                precio_unitario = 95
                producto = "Malinche"
            elif (producto == "moc"):
                precio_unitario = 125
                producto = "Moctezuma"
            elif (producto == "pm"):
                precio_unitario = 50
                producto = "Papas Mictlan"
            elif (producto == "gue"):
                precio_unitario = 40
                producto = "Gueritos"
            elif (producto == "fra"):
                precio_unitario = 35
                producto = "Francesas"
            elif (producto == "gaj"):
                precio_unitario = 40
                producto = "Gajo"
            elif (producto == "ac"):
                precio_unitario = 35
                producto = "Aros Cebolla"
            else:
                return render(request, 'paginas/home.html', {"pedidos":pedidos, "pedidoscompletos":pedidoscompletos, 'id_num_pedido':globals()['id_num_pedido'], "telefono_exist":telefono_exist})

            #Atrapa excepcion de cantidad = string
            if(cantidad.isalpha()==True):
                return render(request, 'paginas/home.html', {"pedidos":pedidos, "pedidoscompletos":pedidoscompletos, 'id_num_pedido':globals()['id_num_pedido'], "telefono_exist":telefono_exist})
            
            total = int(precio_unitario)*int(cantidad)

            #Evalua excepcion de que montoextra sea vacio o string
            try:
                montextra = eval(montextra)
            except:
                montextra = 0

            total = total+int(montextra)

            #Asignamos columna
            if(len(pedidos)>0):
                columna = int(pedidos[-1].columna)+1
            else:
                columna = 1
            
            totaltotales = 0

            #Sacamos el total de totales recorriendo la lista y añadiendo 
            if(len(pedidos)>0):
                for n in pedidos:
                    totaltotales = totaltotales + n.total 
                totaltotales = totaltotales + total
            else:
                totaltotales = total
            
            if(num_pedido.isalpha()==True):
                num_pedido = globals()['id_num_pedido']

            #Creamos el objeto
            
            pedido = Pedido(columna, num_pedido, producto, cantidad, precio_unitario, prodextra, montextra, total, totaltotales)
            pedidos.append(pedido)
            print("entro aqui")
            for n in pedidos:
                print(n)

        #Revisa que el cliente no este registrado en dado casi de que sea asi lo registra en la base de datos y de igual manera hace el pedido, en dado caso de que no haya productos en la lista no hace nada, pero si se pueden registrar clientes de esta manera
        elif(calleynum!="" and col!="" and telefono!="" and entrecalles!=""):
            if(telefono.isalpha()==True):
                return render(request, 'paginas/home.html', {"pedidos":pedidos, "pedidoscompletos":pedidoscompletos, 'id_num_pedido':globals()['id_num_pedido'], "telefono_exist":telefono_exist})
            if(len(Cliente.objects.filter(telefono__exact=telefono))==0):
                Cliente.objects.create(telefono = telefono, calle = calleynum, colonia = col, entrecalles = entrecalles)

            if(len(pedidos)>0):
                for n in pedidos:
                    PedidoCompleto.objects.create(fecha = fechaobj, id_pedido= n.num_pedido, nombre_pedido=n.producto, cantidad = n.cantidad, precio_unitario = n.precio_unitario, descripcion = n.prodextra, montextra = n.montoextra, subtotal = n.total, total = n.totaltotales, calle = calleynum, colonia = col, entrecalles = entrecalles, telefono = telefono, estado = 'NoEnviado')
                pedidos.clear()
                globals()['id_num_pedido'] = globals()['id_num_pedido'] + 1
                
            else:
                return render(request, 'paginas/home.html', {"pedidos":pedidos, "pedidoscompletos":pedidoscompletos, 'id_num_pedido':globals()['id_num_pedido'], "telefono_exist":telefono_exist})
        
        #Caso por si el usuario recoge el pedido en la sucursal
        elif(telefono!="" and calleynum.lower() == "aqui" and col!=""):
            for n in pedidos:
                PedidoCompleto.objects.create(fecha = fechaobj, id_pedido= n.num_pedido, nombre_pedido=n.producto, cantidad = n.cantidad, precio_unitario = n.precio_unitario, descripcion = n.prodextra, montextra = n.montoextra, subtotal = n.total, total = n.totaltotales, calle = calleynum, colonia = col, entrecalles = "", telefono = telefono, estado = 'NoEnviado')
            pedidos.clear()
            globals()['id_num_pedido'] = globals()['id_num_pedido'] + 1

        #Revisa si ya existe el cliente y si es asi añade el pedido si hay productos
        elif(telefono!=""):
            if(len(Cliente.objects.filter(telefono__exact=telefono))>0):
                telefono_exist = "Cliente Ya Registrado"
                if(len(pedidos)>0):
                    cliente = Cliente.objects.filter(telefono__exact=telefono).get()
                    for n in pedidos:
                        PedidoCompleto.objects.create(fecha = fechaobj, id_pedido = n.num_pedido, nombre_pedido = n.producto, cantidad = n.cantidad, precio_unitario = n.precio_unitario, descripcion = n.prodextra, montextra = n.montoextra, subtotal = n.total, total = n.totaltotales, calle = cliente.calle, colonia = cliente.colonia, entrecalles = cliente.entrecalles, telefono = cliente.telefono, estado = "NoEnviado")
                    pedidos.clear()
                    globals()['id_num_pedido'] = globals()['id_num_pedido'] + 1
            else:
                telefono_exist = "Cliente No Registrado"
        
        #Restablece el numero de pedido de la vista (home.html)
        elif(num_pedido == "rest"):
            if cantidad=="":
                cantidad = 1
            globals()['id_num_pedido'] = int(cantidad)

        #Si no se cumple ningun caso regresa la vista (home.html)
        else:
            return render(request, 'paginas/home.html', {"pedidos":pedidos, "pedidoscompletos":pedidoscompletos, 'id_num_pedido':globals()['id_num_pedido'], "telefono_exist":telefono_exist})

    return render(request, 'paginas/home.html', {"pedidos":pedidos, "pedidoscompletos":pedidoscompletos, 'id_num_pedido':globals()['id_num_pedido'], "telefono_exist":telefono_exist})

#metodo para buscar los clientes segun su numero de telefono, en dado caso de no buscar nada aparecen todo
def clientes(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('login')
        
    cliente = Cliente.objects.all()
    
    if request.method == 'POST':

        if 'buscar_cliente' in request.POST:
            buscar_cliente = request.POST['buscar_cliente']
        else:
            buscar_cliente = False
        
        if(buscar_cliente!=""):
            cliente = Cliente.objects.filter(telefono__exact=buscar_cliente)

    return render(request, 'paginas/clientes.html',{"cliente":cliente}) 

#Actualizamos pedido para mandarlo como enviado, utilizamos id para mandar parametro
def actualizar_pedido(request, id):
    updater = get_object_or_404(PedidoCompleto, id = id)
    if(updater.estado=="NoEnviado"):
        PedidoCompleto.objects.filter(id__exact=id).update(estado="Enviado")
    else:
        PedidoCompleto.objects.filter(id__exact=id).update(estado="NoEnviado")
    return redirect(to='home')

#Funcion eliminar cliente, mismo metodo de arriba
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id = id)
    cliente.delete()
    return redirect(to="clientes")

#Ver pedidos ordenados por fecha y id, igual se puede buscar pedido
def verpedidos(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('login')

    pedidos_ver = PedidoCompleto.objects.order_by("fecha").order_by("id")

    if request.method == 'POST':

        if 'buscar_pedido' in request.POST:
            buscar_pedido = request.POST['buscar_pedido']
        else:
            buscar_pedido = False

        if(buscar_pedido!=""):
            pedidos_ver = PedidoCompleto.objects.filter(fecha__exact=buscar_pedido).order_by("id_pedido")

    return render(request, 'paginas/verpedidos.html',{"pedidos_ver":pedidos_ver})

#Funcion eliminar pedido, mismo metodo que eliminar cliente
def eliminar_pedido(request, id):
    totalaux = 0
    pedido = get_object_or_404(PedidoCompleto, id = id)
    idaux = pedido.id_pedido
    pedido.delete()
    pedidosacttotal = PedidoCompleto.objects.filter(id_pedido__exact=idaux)
    for n in pedidosacttotal:
        print(n.subtotal)
        totalaux = totalaux + int(n.subtotal)
    PedidoCompleto.objects.filter(id_pedido__exact=idaux).update(total=totalaux)
    return redirect(to="verpedidos")

#Funcion eliminar lista de pedido, sacamos de la lista 
def eliminar_lista(request, id):
    for x in range(0,len(pedidos)):
        print(type(pedidos[x].columna))
        print(type(id))
        if(pedidos[x].columna == int(id)):
            pedidos.pop(x)
            break

    if(len(pedidos)>0):
        totalupdate = 0

        for n in pedidos:
            totalupdate = totalupdate + n.total

        for n in pedidos:
            n.totaltotales = totalupdate

    return redirect(to="home")
