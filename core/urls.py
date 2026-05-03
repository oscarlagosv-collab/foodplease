from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='principal'),
    path('principal/', views.principal, name='principal'),
    path('locales/', views.locales, name='locales'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('login/', views.login_view, name='login'),
    path('carrito/', views.carrito, name='carrito'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('categoria/<int:categoria_id>/', views.locales_por_categoria, name='locales_por_categoria'),
    path('local/<int:local_id>/', views.detalle_local, name='detalle_local'),
    path('sucursal/<int:sucursal_id>/', views.detalle_sucursal, name='detalle_sucursal'),
    path('agregar-carrito/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/aumentar/<int:producto_id>/', views.aumentar_carrito, name='aumentar_carrito'),
    path('carrito/disminuir/<int:producto_id>/', views.disminuir_carrito, name='disminuir_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_carrito, name='eliminar_carrito'),
]