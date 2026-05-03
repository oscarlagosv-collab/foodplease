from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Local, Categoria, Sucursal, ProductoMenu, Carrito, ItemCarrito


def principal(request):
    categorias = Categoria.objects.filter(activo=True)

    return render(request, 'principal.html', {
        'categorias': categorias
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
    return render(request, 'registro.html')

def detalle_local(request, local_id):
    local = get_object_or_404(Local, id=local_id, activo=True)
    sucursales = Sucursal.objects.filter(local=local, activo=True)

    return render(request, 'detalle_local.html', {
        'local': local,
        'sucursales': sucursales
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