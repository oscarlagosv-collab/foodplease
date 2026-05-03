from django.db import models


REGIONES = [
    ('RM', 'Región Metropolitana'),
    ('V', 'Valparaíso'),
    ('VI', 'O’Higgins'),
    ('VII', 'Maule'),
    ('VIII', 'Biobío'),
    ('IX', 'La Araucanía'),
]

COMUNAS = [
    ('Santiago', 'Santiago'),
    ('Providencia', 'Providencia'),
    ('Maipú', 'Maipú'),
    ('Puente Alto', 'Puente Alto'),
    ('Valparaíso', 'Valparaíso'),
    ('Viña del Mar', 'Viña del Mar'),
    ('Rancagua', 'Rancagua'),
    ('Talca', 'Talca'),
    ('Concepción', 'Concepción'),
    ('Temuco', 'Temuco'),
]


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Local(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='locales')
    imagen = models.ImageField(upload_to='locales/', blank=True, null=True)
    descripcion = models.TextField(blank=True)
    calificacion = models.DecimalField(max_digits=2, decimal_places=1, default=4.5)
    tiempo_entrega = models.CharField(max_length=50, default="25-35 min")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Sucursal(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='sucursales')
    nombre = models.CharField(max_length=100)
    region = models.CharField(max_length=50, choices=REGIONES, default='RM')
    comuna = models.CharField(max_length=100, choices=COMUNAS, default='Santiago')
    direccion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.local.nombre} - {self.nombre}"


class ProductoMenu(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.sucursal}"
    
from django.contrib.auth.models import User

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(ProductoMenu, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return self.producto.nombre