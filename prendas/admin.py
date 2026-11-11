from django.contrib import admin

from .models import Prenda


@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'talla', 'color', 'precio', 'stock', 'disponible', 'fecha_ingreso')
    list_filter = ('categoria', 'disponible', 'fecha_ingreso')
    search_fields = ('nombre', 'descripcion', 'color')
    list_editable = ('disponible', 'stock')
    list_per_page = 20
    ordering = ('-fecha_ingreso',)
