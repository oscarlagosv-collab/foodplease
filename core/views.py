from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Local, Categoria, Sucursal, ProductoMenu, Carrito, ItemCarrito, PerfilCliente, CalificacionLocal
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg

def principal(request):

    comuna = request.GET.get("comuna")

    categorias = Categoria.objects.filter(activo=True)

    if comuna:
        locales = Local.objects.filter(
            sucursales__comuna__icontains=comuna,
            activo=True
        ).distinct()
    else:
        locales = Local.objects.filter(activo=True)

    return render(request, "principal.html", {
        "categorias": categorias,
        "locales": locales,
        "comuna": comuna
    })

def locales(request):
    locales = Local.objects.filter(activo=True)

    return render(request, 'locales.html', {
        'locales': locales
    })

def locales_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id, activo=True)
    locales = Local.objects.filter(categoria=categoria, activo=True)

    return render(request, 'locales_por_categoria.html', {
        'categoria': categoria,
        'locales': locales
    })

def nosotros(request):
    return render(request, 'nosotros.html')


def carrito(request):
    items = []
    total = 0

    if request.user.is_authenticated:
        carrito_usuario = Carrito.objects.filter(
            usuario=request.user,
            finalizado=False
        ).first()

        if carrito_usuario:
            for item in carrito_usuario.items.all():
                subtotal = item.subtotal()
                total += subtotal
                items.append({
                    'producto': item.producto,
                    'cantidad': item.cantidad,
                    'subtotal': subtotal
                })

    else:
        carrito_sesion = request.session.get('carrito', {})

        for producto_id, cantidad in carrito_sesion.items():
            producto = ProductoMenu.objects.get(id=producto_id)
            subtotal = producto.precio * cantidad
            total += subtotal

            items.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })

    return render(request, 'carrito.html', {
        'items': items,
        'total': total
    })


def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('principal')
        else:
            error = "Usuario o contraseña incorrectos"

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('principal')


def registro(request):
    if request.method == "POST":
        nombre_completo = request.POST.get("nombre_completo")
        username = request.POST.get("username")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("registro")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return redirect("registro")

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return redirect("registro")

        partes_nombre = nombre_completo.split(" ", 1)
        first_name = partes_nombre[0]
        last_name = partes_nombre[1] if len(partes_nombre) > 1 else ""

        usuario = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        PerfilCliente.objects.create(
            usuario=usuario,
            telefono=telefono
        )

        messages.success(request, "Usuario creado correctamente. Ahora puedes iniciar sesión.")
        return redirect("login")

    return render(request, "registro.html")

def detalle_local(request, local_id):
    local = get_object_or_404(Local, id=local_id, activo=True)
    sucursales = Sucursal.objects.filter(local=local, activo=True)

    promedio = local.calificaciones.aggregate(
        promedio=Avg("estrellas")
    )["promedio"] or 0

    mi_calificacion = 0

    if request.user.is_authenticated:
        calificacion = CalificacionLocal.objects.filter(
            local=local,
            usuario=request.user
        ).first()

        if calificacion:
            mi_calificacion = calificacion.estrellas

    return render(request, 'detalle_local.html', {
        'local': local,
        'sucursales': sucursales,
        'promedio': round(promedio, 1),
        'mi_calificacion': mi_calificacion
    })

def detalle_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, activo=True)
    productos = ProductoMenu.objects.filter(sucursal=sucursal, disponible=True)

    return render(request, 'detalle_sucursal.html', {
        'sucursal': sucursal,
        'productos': productos
    })

def agregar_carrito(request, producto_id):
    producto = get_object_or_404(ProductoMenu, id=producto_id, disponible=True)

    if request.user.is_authenticated:
        carrito, creado = Carrito.objects.get_or_create(
            usuario=request.user,
            finalizado=False
        )

        item, creado = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto
        )

        if not creado:
            item.cantidad += 1
            item.save()

    else:
        carrito = request.session.get('carrito', {})

        producto_id_str = str(producto.id)

        if producto_id_str in carrito:
            carrito[producto_id_str] += 1
        else:
            carrito[producto_id_str] = 1

        request.session['carrito'] = carrito
        request.session.modified = True

    return redirect(request.META.get('HTTP_REFERER', 'principal'))

def aumentar_carrito(request, producto_id):
    producto = get_object_or_404(ProductoMenu, id=producto_id)

    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user, finalizado=False).first()
        item = ItemCarrito.objects.filter(carrito=carrito, producto=producto).first()

        if item:
            item.cantidad += 1
            item.save()
    else:
        carrito = request.session.get('carrito', {})
        producto_id = str(producto_id)
        carrito[producto_id] = carrito.get(producto_id, 0) + 1
        request.session['carrito'] = carrito
        request.session.modified = True

    return redirect('carrito')


def disminuir_carrito(request, producto_id):
    producto = get_object_or_404(ProductoMenu, id=producto_id)

    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user, finalizado=False).first()
        item = ItemCarrito.objects.filter(carrito=carrito, producto=producto).first()

        if item:
            item.cantidad -= 1

            if item.cantidad <= 0:
                item.delete()
            else:
                item.save()
    else:
        carrito = request.session.get('carrito', {})
        producto_id = str(producto_id)

        if producto_id in carrito:
            carrito[producto_id] -= 1

            if carrito[producto_id] <= 0:
                del carrito[producto_id]

        request.session['carrito'] = carrito
        request.session.modified = True

    return redirect('carrito')


def eliminar_carrito(request, producto_id):
    producto = get_object_or_404(ProductoMenu, id=producto_id)

    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user, finalizado=False).first()
        ItemCarrito.objects.filter(carrito=carrito, producto=producto).delete()
    else:
        carrito = request.session.get('carrito', {})
        producto_id = str(producto_id)

        if producto_id in carrito:
            del carrito[producto_id]

        request.session['carrito'] = carrito
        request.session.modified = True

    return redirect('carrito')

def seleccionar_direccion(request):
    return render(request, "seleccionar_direccion.html")

@login_required
def mis_datos(request):
    perfil, creado = PerfilCliente.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        user = request.user

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")

        nueva_password = request.POST.get("password")

        if nueva_password:
            user.set_password(nueva_password)
            update_session_auth_hash(request, user)

        user.save()

        perfil.telefono = request.POST.get("telefono")
        perfil.save()

        return redirect("mis_datos")

    return render(request, "mis_datos.html", {
        "perfil": perfil
    })


@login_required
def eliminar_usuario(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect("seleccionar_direccion")

    return redirect("mis_datos")

@login_required
def calificar_local(request, local_id):
    if request.method == "POST":
        estrellas = int(request.POST.get("estrellas", 0))

        if estrellas < 1 or estrellas > 5:
            return JsonResponse({"ok": False, "error": "Calificación inválida"})

        local = get_object_or_404(Local, id=local_id, activo=True)

        CalificacionLocal.objects.update_or_create(
            local=local,
            usuario=request.user,
            defaults={"estrellas": estrellas}
        )

        promedio = local.calificaciones.aggregate(
            promedio=Avg("estrellas")
        )["promedio"]

        return JsonResponse({
            "ok": True,
            "promedio": round(promedio, 1)
        })

    return JsonResponse({"ok": False, "error": "Método no permitido"})

def categorias_movil(request):
    categorias = Categoria.objects.filter(activo=True)

    return render(request, 'categorias_movil.html', {
        'categorias': categorias
    })