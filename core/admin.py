from django.contrib import admin
from .models import Local, Sucursal, ProductoMenu, Categoria, PerfilCliente

class SucursalInline(admin.TabularInline):
    model = Sucursal
    extra = 1


class ProductoMenuInline(admin.TabularInline):
    model = ProductoMenu
    extra = 1


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'activo')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre',)
    inlines = [SucursalInline]


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'local', 'region', 'comuna', 'direccion', 'activo')
    list_filter = ('region', 'comuna', 'activo')
    search_fields = ('nombre', 'local__nombre', 'direccion')
    inlines = [ProductoMenuInline]

    class Media:
        js = ('js/admin_comunas.js',)


@admin.register(ProductoMenu)
class ProductoMenuAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sucursal', 'precio', 'disponible')
    list_filter = ('disponible', 'sucursal__local')
    search_fields = ('nombre', 'descripcion', 'sucursal__nombre')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)

class AdminCustom(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

@admin.register(PerfilCliente)
class PerfilClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__email', 'telefono')