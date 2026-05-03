from .models import Carrito


def carrito_contador(request):
    cantidad = 0

    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(
            usuario=request.user,
            finalizado=False
        ).first()

        if carrito:
            cantidad = sum(item.cantidad for item in carrito.items.all())

    else:
        carrito_sesion = request.session.get('carrito', {})
        cantidad = sum(carrito_sesion.values())

    return {
        'cantidad_carrito': cantidad
    }