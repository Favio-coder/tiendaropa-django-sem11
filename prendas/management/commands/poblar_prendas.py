from django.core.management.base import BaseCommand
from django.db import transaction

from prendas.models import Prenda


class Command(BaseCommand):
    help = 'Pobla la base de datos con prendas de una tienda de ropa de Huancayo.'

    PRENDAS = [
        {
            'nombre': 'Polo Piqué Alpaca',
            'categoria': 'Polos',
            'talla': 'M',
            'color': 'Azul marino',
            'precio': '45.00',
            'stock': 25,
            'descripcion': 'Polo de piqué con fibra de alpaca, ideal para el clima de Huancayo.',
            'disponible': True,
        },
        {
            'nombre': 'Polo Sport Huancayo',
            'categoria': 'Polos',
            'talla': 'L',
            'color': 'Rojo',
            'precio': '38.50',
            'stock': 18,
            'descripcion': 'Polo deportivo con logo bordado de la ciudad de Huancayo.',
            'disponible': True,
        },
        {
            'nombre': 'Pantalón Jean Andino',
            'categoria': 'Pantalones',
            'talla': '32',
            'color': 'Azul',
            'precio': '89.90',
            'stock': 12,
            'descripcion': 'Pantalón jean resistente, estilo andino, talla 32.',
            'disponible': True,
        },
        {
            'nombre': 'Pantalón de Vestir',
            'categoria': 'Pantalones',
            'talla': '34',
            'color': 'Negro',
            'precio': '75.00',
            'stock': 3,
            'descripcion': 'Pantalón formal para oficina y eventos.',
            'disponible': True,
        },
        {
            'nombre': 'Vestido Verano Huancayo',
            'categoria': 'Vestidos',
            'talla': 'S',
            'color': 'Floral',
            'precio': '110.00',
            'stock': 8,
            'descripcion': 'Vestido ligero para la temporada de verano en Huancayo.',
            'disponible': True,
        },
        {
            'nombre': 'Vestido Evening',
            'categoria': 'Vestidos',
            'talla': 'M',
            'color': 'Negro',
            'precio': '145.00',
            'stock': 2,
            'descripcion': 'Vestido elegante para eventos nocturnos.',
            'disponible': True,
        },
        {
            'nombre': 'Casaca Andina',
            'categoria': 'Casacas',
            'talla': 'L',
            'color': 'Gris',
            'precio': '135.00',
            'stock': 15,
            'descripcion': 'Casaca abrigada para el frío de la sierra de Huancayo.',
            'disponible': True,
        },
        {
            'nombre': 'Casaca Impermeable',
            'categoria': 'Casacas',
            'talla': 'XL',
            'color': 'Verde',
            'precio': '120.00',
            'stock': 1,
            'descripcion': 'Casaca impermeable para días de lluvia en la región.',
            'disponible': True,
        },
        {
            'nombre': 'Bufanda de Alpaca',
            'categoria': 'Accesorios',
            'talla': 'Única',
            'color': 'Beige',
            'precio': '55.00',
            'stock': 30,
            'descripcion': 'Bufanda artesanal de alpaca bebé, hecha en Huancayo.',
            'disponible': True,
        },
        {
            'nombre': 'Gorro Andino',
            'categoria': 'Accesorios',
            'talla': 'Única',
            'color': 'Multicolor',
            'precio': '30.00',
            'stock': 40,
            'descripcion': 'Gorro andino con orejeras, diseño tradicional.',
            'disponible': True,
        },
        {
            'nombre': 'Polo Básico Blanco',
            'categoria': 'Polos',
            'talla': 'S',
            'color': 'Blanco',
            'precio': '35.00',
            'stock': 0,
            'descripcion': 'Polo básico de algodón, color blanco, talla S.',
            'disponible': False,
        },
        {
            'nombre': 'Pantalón Chino',
            'categoria': 'Pantalones',
            'talla': '30',
            'color': 'Caqui',
            'precio': '70.00',
            'stock': 7,
            'descripcion': 'Pantalón chino casual, color caqui, talla 30.',
            'disponible': True,
        },
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        contador = 0
        for datos in self.PRENDAS:
            obj, creado = Prenda.objects.update_or_create(
                nombre=datos['nombre'],
                talla=datos['talla'],
                color=datos['color'],
                defaults=datos,
            )
            if creado:
                contador += 1
        self.stdout.write(
            self.style.SUCCESS(
                f'Se insertaron {contador} prendas nuevas. Total: {Prenda.objects.count()} prendas.'
            )
        )
