#!/usr/bin/env python3
import os
import sys
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from pathlib import Path

def main():
    if len(sys.argv) > 1:
        site_dir = sys.argv[1]
    else:
        site_dir = "site"

    sitemap_path = os.path.join(site_dir, "sitemap.xml")
    if not os.path.isfile(sitemap_path):
        print("Error: sitemap.xml not found. Build might not have generated it.")
        sys.exit(1)

    # Parsear sitemap
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [elem.text for elem in root.findall('.//ns:loc', ns)]
    
    # Mapear URL a ruta de archivo HTML en el disco
    page_paths = []
    for url in urls:
        # Extraer la ruta relativa desde site_dir
        # Ej: https://jim88.pp.ua/Astrologia/Carta_Natal/casa_01/ -> casa_01/index.html
        # O mejor, usamos la ruta real en disco
        path = url.replace("https://jim88.pp.ua", "").lstrip("/")
        if path.endswith("/"):
            path = path + "index.html"
        else:
            # Si no termina en /, asumimos que es un archivo .html
            path = path + ".html" if not path.endswith(".html") else path
        full_path = os.path.join(site_dir, path)
        if os.path.isfile(full_path):
            page_paths.append(full_path)

    # Generar enlaces para cada página (excepto la primera y última)
    for idx, full_path in enumerate(page_paths):
        prev_path = page_paths[idx-1] if idx > 0 else None
        next_path = page_paths[idx+1] if idx < len(page_paths)-1 else None

        if prev_path is None and next_path is None:
            continue

        # Leer el HTML
        with open(full_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Buscar el contenedor del contenido principal
        content_div = soup.find('div', class_='md-content')
        if not content_div:
            continue

        # Construir los enlaces con rutas relativas
        base_dir = os.path.dirname(full_path)

        nav_html = '<div class="prev-next-nav" style="display: flex; justify-content: space-between; margin-top: 2rem;">'
        if prev_path:
            rel_prev = os.path.relpath(prev_path, base_dir)
            nav_html += f'<a href="{rel_prev}" class="prev">&larr; Anterior</a>'
        else:
            nav_html += '<span></span>'
        if next_path:
            rel_next = os.path.relpath(next_path, base_dir)
            nav_html += f'<a href="{rel_next}" class="next">Siguiente &rarr;</a>'
        nav_html += '</div>'

        # Insertar después del contenido principal
        content_div.append(BeautifulSoup(nav_html, 'html.parser'))

        # Guardar el HTML modificado
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print(f"Actualizado: {full_path}")

if __name__ == '__main__':
    main()
