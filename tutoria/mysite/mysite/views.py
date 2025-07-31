
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
# Django
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Dominio de la plataforma de tutorías (definido en clases.py)
# Si este archivo (views.py) y clases.py están en la MISMA app:
from .clases import (
    SesionTutoria,
    Usuario,
    Estudiante,
    Tutor,
    Cola,
    ArbolBinarioBusqueda,
    PlataformaTutorias,
)


def index(request):
    #resp = lista.obtener()
    return render(request,"index.html")
    #return HttpResponse("Hola mundo")
    #return render(request,"index.html",{"lista":lista.obtener()})

def login(request):
    return render(request,"login.html")

def buscar_dulce(request):
    return render(request,"buscar_dulce.html")

def home(request):
    return render(request,"home.html")

def recomendacion(request):
    return render(request,"recomendacion.html")

def iniciar(request):
    libUser = LibUser()
    email = request.POST['email']
    password = request.POST['password']
    resp = libUser.login(email, password)
    if(resp):

        return redirect("/home")
    else: 
        return redirect("/login")
    


########

def dulce(request):
    return render(request,"dulce.html")

def create_dulce(request):
    return render(request,"create_dulce.html")

def insert_dulce(request):
    id = request.POST['id']
    nombre = request.POST['nombre']
    marca = request.POST['marca']
    descripcion = request.POST['descripcion']
    precio = request.POST['precio']
    cantidad = request.POST['cantidad']
    libDulce = LibDulce()
    resp = libDulce.create(id, nombre, marca, descripcion, precio, cantidad)
    if(resp):
        return redirect("/dulce")
    else:
        return redirect("/dulce/crear")


def edit_dulce(request):
    id = request.POST['id']
    libDulce = LibDulce()
    dulce = libDulce.get_dulce_by_id(id)
    return render(request,"edit_dulce.html",{'dulce':dulce})

def update_dulce(request):
    id = request.POST['id']
    nombre = request.POST['nombre']
    marca = request.POST['marca']
    descripcion = request.POST['descripcion']
    precio = request.POST['precio']
    cantidad = request.POST['cantidad']
    libDulce = LibDulce()
    resp = libDulce.edit_dulce(id, nombre, marca, descripcion, precio, cantidad)
    if(resp):
        return redirect("/dulce")
    else:
        return redirect("/dulce/edit?id="+id)
    
def remove_dulce(request):
    id = request.GET['id']
    libDulce = LibDulce()
    dulce = libDulce.get_dulce_by_id(id)
    return render(request,"remove_dulce.html",{'dulce':dulce})

def delete_dulce(request):
    id = request.POST['id']
    libDulce = LibDulce()
    resp = libDulce.eliminar(id)
    if(resp):
        return redirect("/dulce")
    else:
        return redirect("/dulce/remove?id="+id)
    
def dulce(request):
    libDulce = LibDulce()
    lista = libDulce.get_producto()
    return render(request,"dulce.html",{"lista":lista})

def comprar_dulce(request):
    dulce_id = request.GET.get('id')
    lib_dulce = LibDulce()

    if lib_dulce.comprar_dulce(dulce_id):
        return redirect('/buscar_dulce')
    else:
        return render(request, 'error.html', {'mensaje': 'No hay suficiente stock o dulce no encontrado.'})


def dulce_list(request):
    dulces = dulce.objects.all()
    low_stock = [d for d in dulces if d.cantidad <= d.stock_minimo]
    critical_stock = [d for d in low_stock if d.cantidad <= d.stock_minimo * 0.3]
    
    return render(request, 'dulce.html', {
        'dulces': dulces,
        'low_stock': low_stock,
        'critical_stock': critical_stock
    })

####################################

def resenia(request):
    return render(request,"resenia.html")

def create_resenia(request):
    return render(request,"create_resenia.html")

def insert_resenia(request):
    id = request.POST['id']
    descripcion = request.POST['descripcion']
    libResenia = LibResenia()
    resp = libResenia.create(id, descripcion)
    if(resp):
        return redirect("/resenia")
    else:
        return redirect("/resenia/crear")


def edit_resenia(request):
    id = request.POST['id']
    libResenia = LibResenia()
    resenia = libResenia.get_resenia_by_id(id)
    return render(request,"edit_resenia.html",{'resenia':resenia})

def update_resenia(request):
    id = request.POST['id']
    descripcion = request.POST['descripcion']
    libResenia = LibResenia()
    resp = libResenia.edit_resenia(id, descripcion)
    if(resp):
        return redirect("/resenia")
    else:
        return redirect("/resenia/edit?id="+id)
    
def remove_resenia(request):
    id = request.GET['id']
    libResenia = LibResenia()
    resenia = libResenia.get_resenia_by_id(id)
    return render(request,"remove_resenia.html",{'resenia':resenia})

def delete_resenia(request):
    id = request.POST['id']
    libResenia = LibResenia()
    resp = libResenia.eliminar(id)
    if(resp):
        return redirect("/resenia")
    else:
        return redirect("/resenia/remove?id="+id)
    
def resenia(request):
    libResenia = LibResenia()
    lista = libResenia.get_resenia()

    return render(request,"resenia.html",{"lista":lista})

###########################################3

def favorito(request):
    return render(request,"favorito.html")

def create_favorito(request):
    return render(request,"create_favorito.html")

def insert_favorito(request):
    id = request.POST['id']
    nombre = request.POST['nombre']
    marca = request.POST['marca']
    precio = request.POST['precio']
    publico = request.POST['publico']
    fecha = request.POST['fecha']
    libFavorito = LibFavorito()
    resp = libFavorito.create(id, nombre, marca, precio, publico, fecha)
    if(resp):
        return redirect("/favorito")
    else:
        return redirect("/favorito/crear")


def edit_favorito(request):
    id = request.POST['id']
    libFavorito = LibFavorito()
    favorito = libFavorito.get_favorito_by_id(id)
    return render(request,"edit_favorito.html",{'favorito':favorito})

def update_favorito(request):
    id = request.POST['id']
    nombre = request.POST['nombre']
    marca = request.POST['marca']
    precio = request.POST['precio']
    publico = request.POST['publico']
    fecha = request.POST['fecha']
    libFavorito = LibFavorito()
    resp = libFavorito.edit_favorito(id, nombre, marca, precio, publico, fecha)
    if(resp):
        return redirect("/favorito")
    else:
        return redirect("/favorito/edit?id="+id)
    
def remove_favorito(request):
    id = request.GET['id']
    libFavorito = LibFavorito()
    favorito = libFavorito.get_favorito_by_id(id)
    return render(request,"remove_favorito.html",{'favorito':favorito})

def delete_favorito(request):
    id = request.POST['id']
    libFavorito = LibFavorito()
    resp = libFavorito.eliminar(id)
    if(resp):
        return redirect("/favorito")
    else:
        return redirect("/favorito/remove?id="+id)
    
def favorito(request):
    libFavorito = LibFavorito()
    lista = libFavorito.get_favorito()

    return render(request,"favorito.html",{"lista":lista})

##########################################################


######### Vistas para Proveedor ##########

def proveedor(request):
    libProveedor = LibProveedor()
    proveedores = libProveedor.get_proveedores()
    return render(request, "proveedor.html", {'proveedores': proveedores})

def create_proveedor(request):
    return render(request, "create_proveedor.html")

def insert_proveedor(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        direccion = request.POST.get("direccion")
        telefono = request.POST.get("telefono")
        libProveedor = LibProveedor()
        if libProveedor.create(id, nombre, email, direccion, telefono):
            return redirect('/proveedor')
        else:
            return redirect('/proveedor/crear')
    return redirect('/proveedor')


def edit_proveedor(request, id):  # Aquí 'id' se pasa desde la URL
    libProveedor = LibProveedor()

    if request.method == 'GET':
        proveedor = libProveedor.get_proveedor_by_id(id)  # Usar 'id' directamente
        return render(request, "edit_proveedor.html", {'proveedor': proveedor})

    elif request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']

        resp = libProveedor.edit_proveedor(id, nombre, email, direccion, telefono)

        if resp:
            return redirect("/proveedor")
        else:
            return redirect(f"/proveedor/edit/{id}")  # Cambiar a URL correcta



def update_proveedor(request):
        id = request.POST.get('id')
        nombre = request.POST['nombre']
        email = request.POST['email']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        libProveedor = LibProveedor()
        resp = libProveedor.edit_proveedor(id, nombre, email, direccion, telefono)
        if resp:
            return redirect("/proveedor")
        else:
            return redirect(f"/proveedor/edit/{id}/") 

def remove_proveedor(request):
    id = request.GET.get('id')
    libProveedor = LibProveedor()
    proveedor = libProveedor.get_proveedor_by_id(id)
    return render(request, "remove_proveedor.html", {'proveedor': proveedor})
    if resp:
            return redirect("/proveedor")
    else:
            return redirect(f"/proveedor/remove/{id}/")
    


def delete_proveedor(request):
    if request.method == 'POST':  # Solo procesar si es un POST
        id = request.POST.get('id')  # Obtener el ID desde el formulario
        libProveedor = LibProveedor()
        resp = libProveedor.eliminar(id)  # Llamar al método para eliminar

        if resp:
            return redirect("/proveedor")
        else:
            return redirect(f"/proveedor/remove?id={id}")
    return redirect("/proveedor")


    
def registro(request):
    return render(request,"registro.html")

def create_registro(request):
    return render(request,"create_registro.html")

def insert_registro(request):
    email = request.POST['email']
    password = request.POST['password']
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    libUser = LibUser()
    resp = libUser.create(email, password, nombre, apellido)
    if(resp):
        return redirect("/registro")
    else:
        return redirect("/registro/crear")


def edit_registro(request):
    email = request.POST['email']
    libUser = LibUser()
    registro = libUser.get_user_by_email(email)
    return render(request,"edit_registro.html",{'registro':registro})

def update_registro(request):
    email = request.POST['email']
    password = request.POST['password']
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    libUser = LibUser()
    resp = libUser.edit_user(email, password, nombre, apellido)
    if(resp):
        return redirect("/registro")
    else:
        return redirect("/registro/edit?email="+email)
    
def remove_registro(request):
    email = request.GET['email']
    libUser = LibUser()
    registro = libUser.get_user_by_email(email)
    return render(request,"remove_registro.html",{'registro':registro})

def delete_registro(request):
    email = request.POST['email']
    libUser = LibUser()
    resp = libUser.eliminar(email)
    if(resp):
        return redirect("/registro")
    else:
        return redirect("/registro/remove?email="+email)
    
def registro(request):
    libUser = LibUser()
    lista = libUser.get_users()
    return render(request,"registro.html",{"lista":lista})


def promocion(request):
    return render(request,"promocion.html")

def promocion(request):
    libPromocion = LibPromocion()
    promociones = libPromocion.get_promociones()  # Asegúrate que este método exista en LibPromocion
    return render(request, "promocion.html", {'promociones': promociones})

def create_promocion(request):
    return render(request,"create_promocion.html")

def edit_promocion(request, id):
    libPromocion = LibPromocion()
    
    # Obtener la promoción a editar
    promocion = libPromocion.get_by_id(id)  # Asegúrate que exista este método

    if request.method == "POST":
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        descuento = request.POST['descuento']
        fechainicio = request.POST['fecha_inicio']
        fechafinal = request.POST['fecha_final']

        # Actualizar promoción
        actualizado = libPromocion.update(id, codigo, nombre, descripcion, descuento, fechainicio, fechafinal)

        if actualizado:
            return redirect("/promocion")
        else:
            return render(request, "edit_promocion.html", {'promocion': promocion, 'error': 'No se pudo actualizar'})
    
    return render(request, "edit_promocion.html", {'promocion': promocion})


def insert_promocion(request):
    if request.method == "POST":
        codigo = request.POST['codigo']
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        descuento = request.POST['descuento']
        fechainicio = request.POST['fecha_inicio']
        fechafinal = request.POST['fecha_final']

        libPromocion = LibPromocion()
        resp = libPromocion.create(codigo, nombre, descripcion, descuento, fechainicio, fechafinal)

        if resp:
            return redirect("/promocion")
        else:
            return redirect("/promocion/crear")

def update_promocion(request):
    id = request.POST['id']
    nombre = request.POST['nombre']
    descripcion = request.POST['descripcion']
    descuento = request.POST['descuento']
    fecha_inicio = request.POST['fecha_inicio']
    fecha_fin = request.POST['fecha_fin']

    libPromocion = LibPromocion()
    resp = libPromocion.edit_promocion(id, nombre, descripcion, descuento, fecha_inicio, fecha_fin)
    
    if resp:
        return redirect("/promocion")
    else:
        return redirect(f"/promocion/edit?id={id}")

def remove_promocion(request):
    id = request.GET['id']

    libPromocion = LibPromocion()
    resp = libPromocion.delete_promocion(id)

    return redirect("/promocion")

def delete_promocion(request):
    id = request.POST['id']
    libPromocion = LibPromocion()
    resp = libPromocion.eliminar(id)
    if resp:
        return redirect("/promocion")
    else:
        return redirect(f"/promocion/remove?id={id}")








################################ 

def buscar_dulce(request):
    lib_dulce = LibDulce()
    dulces = []
    nombre = request.GET.get('nombre', None)
    if nombre:
        dulces = lib_dulce.search_by_name(nombre)
    marca = request.GET.get('marca', None)
    if marca:
        dulces = lib_dulce.search_by_marca(marca)
    return render(request, 'buscar_dulce.html', {'lista': dulces})

######################################

def lista_deseo(request):
    # Obtener la lista de deseos de la sesión
    lista_deseos = request.session.get('lista_deseos', {})

    # Convertir la lista de deseos en un formato adecuado para pasar a la plantilla
    productos = [
        {
            'id': key,
            'nombre': item['nombre'],
            'descripcion': item['descripcion'],
            'precio': item['precio'],
            'imagen_url': item['imagen_url'],
        }
        for key, item in lista_deseos.items()
    ]

    return render(request, 'lista_deseo.html', {'productos': productos})
