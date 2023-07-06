from django.shortcuts import render
from .models import *
from django.contrib.auth.views import logout_then_login
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect
import requests

# Create your views here.
def home(request):
    productos =  Producto.objects.all() 
    context={'productos':productos}
    if request.session.get("modificado",None):
        context["modificado"]= True
        del request.session["modificado"]
    suscrito(request,context)
    print(context)
    return render(request, 'core/index.html',context,)

def carrito(request):
     context={}
     carro = request.session.get("carro", [])
     suscrito(request,context)
     context["carrito"]=carrito
     return render(request, 'core/carrito.html',{"carro":request.session.get("carro", [])})

def comprar(request):
    carro = request.session.get("carro", [])
    total = 0
    for c in carro:
        total += c[5]
    
    suscrito = False  
    if request.user.is_authenticated:  
        email = request.user.email
        resp = requests.get(f"http://127.0.0.1:8000/api/suscrito/{email}")
        suscrito = resp.json()["suscrito"]

    descuento = 0
    if suscrito:
        descuento = round(total * 0.05)   

    total -= descuento

    venta = Venta()
    venta.cliente = request.user
    venta.total = total
    venta.save()

    for c in carro:
        detalle = Detalle()
        detalle.venta = venta
        detalle.producto = Producto.objects.get(id=c[0])
        detalle.cantidad = c[4]
        detalle.precio = c[3]
        detalle.total = c[5]
        detalle.save()

    for c in carro:
        producto_id = c[0]
        cantidad = c[4]
        producto = Producto.objects.get(id=producto_id)
        producto.stock -= cantidad
        producto.save()

    request.session["carro"] = []
    return redirect(to="carrito")


def delete(request, id):
    carro = request.session.get("carro", [])
    for item in carro:
        if item[0] == id:
            if item[4] > 1:
                item[4] -= 1
                item[5] = item[3] * item[4]
                break
            else:
                carro.remove(item)
    request.session["carro"] = carro
    return redirect (to="carrito")


def addtocar(request, id):
    producto = Producto.objects.get(id=id)
    carro = request.session.get("carro", [])

    for item in carro:
        if item[0] == id:
            item[4] += 1
            item[5] = item[3] * item[4]
            break
        item[5] = item[3] * item[4]
    else:
        carro.append([id, producto.descripcion, producto.imagen, producto.precio, 1, producto.precio])
    request.session["carro"] = carro
    return redirect(to="home")

def carrito(request):
    carro = request.session.get("carro", [])
    total = 0
    
    for i in carro:
        total += i[3] * i[4]
    suscrito = False  
    if request.user.is_authenticated: 
        email = request.user.email
        resp = requests.get(f"http://127.0.0.1:8000/api/suscrito/{email}")
        suscrito = resp.json()["suscrito"]
    descuento = 0
    if suscrito:
        descuento = round(total * 0.05) 
    total -= descuento
    
    return render(request, 'core/carrito.html', {"carro": carro, 'total': total})

def limpiar(request):
    request.session.flush()
    return redirect(to="home")

    

def suscrito( request, context):
    if request.user.is_authenticated:
        email= request.user.email
        resp = requests.get(f"http://127.0.0.1:8000/api/suscrito/{email}")
        context["suscrito"]= resp.json()["suscrito"]

def suscribir( request):
    context= {}
    if request.method== "POST":
        if request.user.is_authenticated:
            resp = requests.get(f"http://127.0.0.1:8000/api/suscribir/{request.user.email}")
            context["mensaje"] = resp.json()["mensaje"]
            suscrito(request,context)
        return render(request,'core/suscribir.html',context)
    else:
         suscrito(request,context)
         return render(request,'core/suscribir.html',context)
       
    
    



def login(request):
    return render(request, 'core/login.html')

def logout(request):
    return logout_then_login(request, login_url="login")

def registro(request):
    if request.method == "POST":
        form = Registro(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:        
        form = Registro()
    return render(request, 'core/registro.html', {'form':form})


def seguimientoPedido(request):
    return render(request, 'core/seguimientoPedido.html')

def tablaproducto(request):
    return render(request, 'core/tablaproducto.html')

def tablaUsuario(request):
    return render(request, 'core/tablaUsuario.html')

def historial(request):
    context ={}
    suscrito(request,context)
    if not request.user.is_authenticated:
        return redirect(to="login")
    compras = Venta.objects.filter(cliente=request.user)
    return render(request, 'core/historial.html', {"compras":compras})