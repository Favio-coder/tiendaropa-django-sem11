from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Prenda


class PrendaModelTest(TestCase):
    """Pruebas del modelo Prenda."""

    def setUp(self):
        self.prenda = Prenda.objects.create(
            nombre='Polo Alpaca',
            categoria='Polos',
            talla='M',
            color='Azul',
            precio='45.00',
            stock=10,
            descripcion='Polo de alpaca para el frío.',
            disponible=True,
        )

    def test_crear_prenda(self):
        """Verifica que se crea una prenda correctamente."""
        self.assertEqual(self.prenda.nombre, 'Polo Alpaca')
        self.assertEqual(self.prenda.categoria, 'Polos')
        self.assertEqual(str(self.prenda.precio), '45.00')
        self.assertEqual(self.prenda.stock, 10)
        self.assertTrue(self.prenda.disponible)

    def test_str_prenda(self):
        """Verifica el método __str__ del modelo."""
        esperado = 'Polo Alpaca (Polos) - M - Azul'
        self.assertEqual(str(self.prenda), esperado)

    def test_queryset_disponibles(self):
        """Verifica el método disponibles() del QuerySet."""
        Prenda.objects.create(
            nombre='Pantalón Jean',
            categoria='Pantalones',
            talla='32',
            color='Azul',
            precio='89.90',
            stock=5,
            disponible=False,
        )
        disponibles = Prenda.objects.disponibles()
        self.assertEqual(disponibles.count(), 1)
        self.assertEqual(disponibles.first(), self.prenda)

    def test_queryset_por_categoria(self):
        """Verifica el método por_categoria() del QuerySet."""
        polos = Prenda.objects.por_categoria('Polos')
        self.assertEqual(polos.count(), 1)
        self.assertEqual(polos.first().nombre, 'Polo Alpaca')

    def test_queryset_stock_bajo(self):
        """Verifica el método stock_bajo() del QuerySet."""
        Prenda.objects.create(
            nombre='Pantalón Chino',
            categoria='Pantalones',
            talla='30',
            color='Caqui',
            precio='70.00',
            stock=1,
            disponible=True,
        )
        bajo = Prenda.objects.stock_bajo(limite=5)
        self.assertEqual(bajo.count(), 1)

    def test_queryset_buscar(self):
        """Verifica el método buscar() del QuerySet."""
        resultados = Prenda.objects.buscar('alpaca')
        self.assertEqual(resultados.count(), 1)
        self.assertEqual(resultados.first().nombre, 'Polo Alpaca')


class PrendaRutasTest(TestCase):
    """Pruebas de rutas y vistas."""

    def setUp(self):
        self.prenda = Prenda.objects.create(
            nombre='Casaca Andina',
            categoria='Casacas',
            talla='L',
            color='Gris',
            precio='135.00',
            stock=15,
            descripcion='Casaca abrigada para Huancayo.',
            disponible=True,
        )

    def test_home_url(self):
        """Verifica que la ruta / responde con 200."""
        response = self.client.get(reverse('prendas:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tienda')

    def test_catalogo_url(self):
        """Verifica que la ruta /catalogo/ responde con 200."""
        response = self.client.get(reverse('prendas:catalogo'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Catálogo')

    def test_detalle_url(self):
        """Verifica que la ruta /prenda/<pk>/ responde con 200."""
        response = self.client.get(reverse('prendas:detalle', args=[self.prenda.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Casaca Andina')

    def test_catalogo_filtro_categoria(self):
        """Verifica el filtrado por categoría en el catálogo."""
        response = self.client.get(
            reverse('prendas:catalogo') + '?categoria=Casacas'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Casaca Andina')

    def test_catalogo_busqueda(self):
        """Verifica la búsqueda por nombre en el catálogo."""
        response = self.client.get(reverse('prendas:catalogo') + '?q=Casaca')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Casaca Andina')

    def test_detalle_prenda_inexistente(self):
        """Verifica que una prenda inexistente devuelve 404."""
        response = self.client.get(reverse('prendas:detalle', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_admin_registro(self):
        """Verifica que Prenda está registrada en el admin."""
        from django.contrib.admin import site
        self.assertIn(Prenda, site._registry)
