#!/usr/bin/env python3
"""
Script para añadir enlaces "anterior / siguiente" a las páginas generadas por MkDocs.
Solo se añaden en carpetas donde haya más de un archivo HTML.
"""

import os
import sys
from bs4 import BeautifulSoup
from pathlib import Path

def natural_sort_key(s):
    """Clave de ordenación natural (numérica) para nombres de archivo."""
    import re
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', s)]

def main():
    # Directorio de salida de MkDocs (se pasa como argumento o se usa el predeterminado)
    if len(sys.argv) > 1:
        site_dir = sys.argv[1]
    else:
        site_dir = "site"

    if not os.path.isdir(site_dir):
        print(f"Error: el directorio '{site_dir}' no existe.")
        sys.exit(1)

    # Recorremos todas las carpetas dentro de site_dir
    for root, dirs, files in os.walk(site_dir):
        # Buscamos archivos .html en la carpeta actual
        html_files = [f for f in files if f.endswith('.html') and f != 'index.html']
        if len(html_files) <= 1:
            continue   # No hay suficientes páginas para añadir enlaces

        # Ordenamos los archivos de forma natural (para que 10 vaya después de 9)
        html_files.sort(key=natural_sort_key)

        # Creamos un diccionario con la ruta completa y el orden
        page_list = []
        for fname in html_files:
            full_path = os.path.join(root, fname)
            page_list.append((fname, full_path))

        # Añadimos el enlace anterior/siguiente a cada página
        for idx, (fname, full_path) in enumerate(page_list):
            prev_fname = page_list[idx-1][0] if idx > 0 else None
            next_fname = page_list[idx+1][0] if idx < len(page_list)-1 else None

            if prev_fname is None and next_fname is None:
                continue

            # Leer el HTML
            with open(full_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            # Buscar el contenedor del contenido principal (podemos insertar después del artículo)
            # En Material, el contenido está en <div class="md-content">
            content_div = soup.find('div', class_='md-content')
            if not content_div:
                continue

            # Construir los enlaces
            nav_html = '<div class="prev-next-nav" style="display: flex; justify-content: space-between; margin-top: 2rem;">'
            if prev_fname:
                nav_html += f'<a href="{prev_fname}" class="prev">&larr; Anterior</a>'
            else:
                nav_html += '<span></span>'
            if next_fname:
                nav_html += f'<a href="{next_fname}" class="next">Siguiente &rarr;</a>'
            nav_html += '</div>'

            # Insertar después del contenido principal
            content_div.append(BeautifulSoup(nav_html, 'html.parser'))

            # Guardar el HTML modificado
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

            print(f"Actualizado: {full_path}")

if __name__ == '__main__':
    main()
