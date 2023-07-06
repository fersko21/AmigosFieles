from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', home, name="home"),
    path("login", LoginView.as_view(template_name="core/login.html"), name="login"), 
    path('logout', logout, name="logout"),
    path('addtocar/<id>',addtocar, name="addtocar"),
    path('registro',registro,name="registro"),
    path('delete/<id>',delete, name="delete"),
    path('limpiar',limpiar, name="limpiar"),
    path('carrito',carrito, name="carrito"),
    path("comprar", comprar, name="comprar"),
    path('seguimientoPedido',seguimientoPedido, name="seguimientoPedido"),
    path('tablaproducto',tablaproducto,name="tablaproducto"),
    path('tablaUsuario',tablaUsuario, name="tablaUsuario"),
    path("historial", historial, name="historial"),
    path("suscribir", suscribir, name="suscribir"),
    

]
