from django.db import models


class PrendaQuerySet(models.QuerySet):
    """QuerySet personalizado para el modelo Prenda."""

    def disponibles(self):
        """Devuelve solo las prendas disponibles."""
        return self.filter(disponible=True)

    def por_categoria(self, categoria):
        """Filtra prendas por una categoría dada."""
        return self.filter(categoria=categoria)

    def stock_bajo(self, limite=5):
        """Devuelve prendas con stock menor o igual al límite indicado."""
        return self.filter(stock__lte=limite)

    def buscar(self, termino):
        """Busca prendas por nombre o descripción (búsqueda insensible a mayúsculas)."""
        return self.filter(
            models.Q(nombre__icontains=termino)
            | models.Q(descripcion__icontains=termino)
        )


class Prenda(models.Model):
    """Modelo que representa una prenda de vestir."""

    CATEGORIAS = [
        ('Polos', 'Polos'),
        ('Pantalones', 'Pantalones'),
        ('Vestidos', 'Vestidos'),
        ('Casacas', 'Casacas'),
        ('Accesorios', 'Accesorios'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        verbose_name='Categoría',
    )
    talla = models.CharField(max_length=10, verbose_name='Talla')
    color = models.CharField(max_length=50, verbose_name='Color')
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio',
    )
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name='Fecha de ingreso')
    disponible = models.BooleanField(default=True, verbose_name='Disponible')

    objects = PrendaQuerySet.as_manager()

    class Meta:
        ordering = ['-fecha_ingreso']
        verbose_name = 'Prenda'
        verbose_name_plural = 'Prendas'

    def __str__(self):
        return f'{self.nombre} ({self.categoria}) - {self.talla} - {self.color}'
