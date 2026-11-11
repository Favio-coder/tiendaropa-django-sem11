"""Script para tomar capturas de pantalla del proyecto."""

import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from playwright.sync_api import sync_playwright

CAPTURAS_DIR = Path("capturas")
CAPTURAS_DIR.mkdir(exist_ok=True)


def cmd_output_to_image(command, output_path, title="Comando"):
    """Ejecuta un comando y guarda su salida como imagen PNG."""
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    output = result.stdout
    if result.stderr:
        output += "\n" + result.stderr

    # Renderizar texto como imagen
    lines = output.splitlines()
    font_size = 16
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    # Calcular dimensiones
    max_width = 0
    for line in lines:
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        if w > max_width:
            max_width = w

    line_height = font_size + 4
    width = max_width + 40
    height = len(lines) * line_height + 40

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Título
    draw.text((20, 10), title, fill="black", font=font)

    y = 40
    for line in lines:
        draw.text((20, y), line, fill="black", font=font)
        y += line_height

    img.save(output_path)
    print(f"Guardado: {output_path}")


def web_screenshot(url, output_path, wait_selector=None):
    """Toma una captura de una página web."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(url, wait_until="networkidle")
        if wait_selector:
            page.wait_for_selector(wait_selector, timeout=5000)
        page.screenshot(path=str(output_path), full_page=True)
        browser.close()
    print(f"Guardado: {output_path}")


def main():
    # 01_check.png
    cmd_output_to_image(
        ".venv\\Scripts\\python manage.py check",
        CAPTURAS_DIR / "01_check.png",
        "python manage.py check"
    )

    # 02_migraciones.png
    cmd_output_to_image(
        ".venv\\Scripts\\python manage.py migrate",
        CAPTURAS_DIR / "02_migraciones.png",
        "python manage.py migrate"
    )

    # 03_datos.png
    cmd_output_to_image(
        ".venv\\Scripts\\python manage.py poblar_prendas",
        CAPTURAS_DIR / "03_datos.png",
        "python manage.py poblar_prendas"
    )

    # 04_pruebas.png
    cmd_output_to_image(
        ".venv\\Scripts\\python manage.py test prendas",
        CAPTURAS_DIR / "04_pruebas.png",
        "python manage.py test prendas"
    )

    # Capturas web
    base_url = "http://127.0.0.1:8000"

    # 05_inicio.png
    web_screenshot(f"{base_url}/", CAPTURAS_DIR / "05_inicio.png")

    # 06_catalogo.png
    web_screenshot(f"{base_url}/catalogo/", CAPTURAS_DIR / "06_catalogo.png")

    # 07_filtro_categoria.png
    web_screenshot(f"{base_url}/catalogo/?categoria=Polos", CAPTURAS_DIR / "07_filtro_categoria.png")

    # 08_busqueda.png
    web_screenshot(f"{base_url}/catalogo/?q=casaca", CAPTURAS_DIR / "08_busqueda.png")

    # 09_detalle.png (prenda pk=1)
    web_screenshot(f"{base_url}/prenda/1/", CAPTURAS_DIR / "09_detalle.png")

    # 10_admin.png (necesita login - solo captura la página de login)
    web_screenshot(f"{base_url}/admin/", CAPTURAS_DIR / "10_admin.png")

    print("\nTodas las capturas se han guardado en capturas/")


if __name__ == "__main__":
    main()
