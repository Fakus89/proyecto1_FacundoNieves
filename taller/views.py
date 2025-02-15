
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import BusquedaAuto, FormCliente, FormAuto, FormProblema, BusquedaNombre, BusquedaAuto, BusquedaInconveniente, CreacionDeUsuario,EdicionUsuario
from .models import Auto, Cliente, Problema
from django.views.generic import ListView, DetailView
from django.contrib.auth import login as log, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MiAvatarUser

@login_required
def taller(request):
    return render(request,"taller/taller1.html", {"user_avatar_url":buscar_url_avatar(request.user)})

@login_required
def form_cliente(request):

    if request.method == "POST":
        clientex= FormCliente(request.POST)
        if clientex.is_valid():
            datocliente=clientex.cleaned_data
            nuevo_cliente= Cliente(nombre=datocliente["nombre"],apellido=datocliente["apellido"],telefono=datocliente["telefono"],email=datocliente["email"])
            nuevo_cliente.save()
            return render(request, "taller/auto_n.html",{"nuevo_cliente":nuevo_cliente,"user_avatar_url":buscar_url_avatar(request.user)})
    clientex= FormCliente()
    return render(request, "taller/cliente.html",{"clientex": clientex,"user_avatar_url":buscar_url_avatar(request.user)})

@login_required
def form_auto(request):

    if request.method == "POST":
        autox= FormAuto(request.POST)
        if autox.is_valid():
            datoauto=autox.cleaned_data
            nuevo_auto= Auto(marca=datoauto["marca"],modelo=datoauto["modelo"],patente=datoauto["patente"])
            nuevo_auto.save()     
            return render(request, "taller/arreglos.html",{"nuevo_auto":nuevo_auto,"user_avatar_url":buscar_url_avatar(request.user)})
    autox= FormAuto()
    return render(request, "taller/auto_n.html",{"autox": autox})

@login_required
def form_problemas(request):

    if request.method == "POST":
        problemax= FormProblema(request.POST)
        if problemax.is_valid():
            datoproblema=problemax.cleaned_data
            nuevo_problema= Problema(inconveniente=datoproblema["inconveniente"])
            nuevo_problema.save()   
            return render(request, "taller/lista_clientes.html",{"nuevo_problema":nuevo_problema,"user_avatar_url":buscar_url_avatar(request.user)})
    problemax= FormProblema
    return render(request, "taller/arreglos.html",{"problemax": problemax,"user_avatar_url":buscar_url_avatar(request.user)})

##########################################-----busquedas---------########################################

@login_required
def busqueda_nombre(request):
    nombre_buscado=[]
    dato1=request.GET.get("partial_nombre")
    if dato1 is not None:
        nombre_buscado=Cliente.objects.filter(nombre__icontains=dato1)
    buscador1= BusquedaNombre()
    return render(request, "taller/busqueda_cliente.html", {"buscador1":buscador1,"nombre_buscado":nombre_buscado,"user_avatar_url":buscar_url_avatar(request.user)})


@login_required
def busqueda_patente(request):
    patente_buscado=[]
    dato2=request.GET.get("partial_patente")
    if dato2 is not None:
        patente_buscado=Auto.objects.filter(patente__icontains=dato2)
    buscador2=BusquedaAuto()
    return render(request, "taller/busqueda_auto.html", {"buscador2":buscador2,"patente_buscado":patente_buscado,"user_avatar_url":buscar_url_avatar(request.user)})

@login_required
def busqueda_inconveniente(request):
    inconveniente_buscado=[]
    dato3=request.GET.get("partial_inconveniente")
    if dato3 is not None:
        inconveniente_buscado=Problema.objects.filter(inconveniente__icontains=dato3)
    buscador3=BusquedaInconveniente()
    return render(request, "taller/busqueda_inconveniente.html",{"buscador3":buscador3,"inconveniente_buscado":inconveniente_buscado,"user_avatar_url":buscar_url_avatar(request.user)})


            ######################-----------CRUD-----------##########################

#lista de clientes

@login_required
def lista_clientes(request):
    lista_de_clientes=Cliente.objects.all()
    return render(request,"taller/lista_clientes.html",{"lista_de_clientes":lista_de_clientes,"user_avatar_url":buscar_url_avatar(request.user)})

#actualizar cliente

@login_required
def actualizar_cliente(request, id):
    cliente=Cliente.objects.get(id=id)

    if request.method == "POST": 
        clientex= FormCliente(request.POST)
        if clientex.is_valid():
            datocliente=clientex.cleaned_data
            cliente.nombre=datocliente["nombre"]
            cliente.apellido=datocliente["apellido"]
            cliente.telefono=datocliente["telefono"]
            cliente.email=datocliente["email"]
            cliente.save()
            return redirect("lista_clientes")
    clientex= FormCliente()
    return render(request, "taller/actualizar_cliente.html",{"clientex": clientex, "cliente":cliente,"user_avatar_url":buscar_url_avatar(request.user)})

#Borrar cliente
@login_required
def borrar_cliente(request, id):
    cliente=Cliente.objects.get(id=id)
    cliente.delete()
    return redirect("lista_clientes")

#CRUD en BV
class ClienteDetalle(LoginRequiredMixin,DetailView):
    model= Cliente
    template_name="taller/datos_cliente.html"
    
class ListaAuto(LoginRequiredMixin,ListView):
    model= Auto
    template_name="taller/listas_autos.html"


class ListaArreglo(LoginRequiredMixin,ListView):
    model= Problema
    template_name="taller/listas_problemas.html"



#########################################----------loging registrar logout----------------###############################3


def login(request):
    

    if request.method =="POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username=form.cleaned_data["username"] 
            password=form.cleaned_data["password"]
            user=authenticate(username=username,password=password)

            if user is not None:
                log(request, user)
                return render(request,"taller/taller1.html",{"mensaje":"Login correcto","user_avatar_url":buscar_url_avatar(request.user)})
            else:
                return render(request,"taller/login.html",{"form":form, "mensaje":"reintentar"})

        else:
            return render(request,"taller/login.html",{"form":form, "mensaje":"Datos incorrectos"})
    else:
        form = AuthenticationForm()
        return render(request,"taller/login.html",{"form":form, "mensaje": "Bienvenidos"})

    #log
    #authenticate


#################################-----------Creación y edicion de Usuario------------------#####################################

###---#creación
@login_required
def registrar(request):
    
    if request.method == "POST":
        usuario=CreacionDeUsuario(request.POST)

        if usuario.is_valid():
            user= usuario.cleaned_data["username"]
            usuario.save()
            return render(request,"taller/taller1.html",{"mensaje": f"El usuario {{user}},fue creado correctamente, por favor vuelva a loguearse ","user_avatar_url":buscar_url_avatar(request.user)})
        else:
            return render(request, "taller/registrar.html",{"usuario":usuario, "mensaje": "Intente nuevamente"})

    form=CreacionDeUsuario()
    return render(request, "taller/registrar.html",{"form":form, "mensaje": ""})


###---edicion
@login_required
def editar_usuario(request):
    mensaje=""
    request.user

    if request.method == "POST":
        form=EdicionUsuario(request.POST)
        
        if form.is_valid():
          
            data=form.cleaned_data
            request.user.first_name=data.get("first_name","")
            request.user.last_name=data.get("last_name","")
            request.user.email=data.get("email")

            if data.get("password1") == data.get("password2") and len(data.get("password1")) >8:
                request.user.set_password(data.get("password1"))
            else:
                mensaje="Intente nuevamente"
         
            request.user.save()
            return render(request,"taller/taller1.html",{"mensaje":"Se edito correctamente","user_avatar_url":buscar_url_avatar(request.user)})
        else: 
            return render(request, "taller/editar_usuario.html",{"form":form, "mensaje": "Intente nuevamente"})
            
    form=EdicionUsuario(
        initial={
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "username": request.user.username
        })
    return render(request, "taller/editar_usuario.html",{"form":form, "mensaje": ""})

###---Avatar
def buscar_url_avatar(user):
    return MiAvatarUser.objects.filter(user=user)[0].img.url

##########################################-------para mas adelante-------########################################

def about(request):
    return HttpResponse ('''
                            <h1> Pagina en construcción </h1>
                          ''')

def contact(request):
    return HttpResponse ('''
                            <h1> Pagina en construcción </h1>
                          ''')


