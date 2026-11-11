# Tienda de Ropa - Catálogo de Prendas

Aplicación web de catálogo para una tienda de ropa desarrollada con **Django 5.2**, **Python** y **SQLite**.

## Requisitos

- Python 3.10+
- Django 5.2

## Instalación

1. Clonar o descargar el proyecto.
2. Crear y activar el entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Linux/Mac
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Aplicar migraciones:

```bash
python manage.py migrate
```

5. Poblar la base de datos con prendas de ejemplo:

```bash
python manage.py poblar_prendas
```

6. Crear un superusuario para el panel admin:

```bash
python manage.py createsuperuser
```

7. Ejecutar el servidor:

```bash
python manage.py runserver
```

8. Abrir en el navegador: http://127.0.0.1:8000/

## Rutas

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/` | `home()` | Página de inicio |
| `/catalogo/` | `PrendaListView` | Catálogo de prendas (ListView) |
| `/prenda/<int:pk>/` | `PrendaDetailView` | Detalle de una prenda (DetailView) |
| `/admin/` | Admin | Panel de administración de Django |

El catálogo acepta parámetros de consulta:
- `?categoria=Polos` — filtra por categoría
- `?q=casaca` — busca por nombre o descripción

## Pruebas

Ejecutar las pruebas de la aplicación `prendas`:

```bash
python manage.py test prendas
```

Verificar la configuración del proyecto:

```bash
python manage.py check
```

## Estructura MTV

- **Modelo** (`prendas/models.py`): `Prenda` con campos nombre, categoria, talla, color, precio, stock, descripcion, fecha_ingreso, disponible y `PrendaQuerySet` con métodos `disponibles()`, `por_categoria()`, `stock_bajo()` y `buscar()`.
- **Vistas** (`prendas/views.py`): `home()` (función), `PrendaListView` (ListView) y `PrendaDetailView` (DetailView).
- **Plantillas** (`prendas/templates/prendas/`): `base.html`, `home.html`, `catalogo.html`, `detalle.html` con herencia y bloques.
