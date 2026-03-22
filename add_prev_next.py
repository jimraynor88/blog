#!/usr/bin/env python3
import os
import sys
from bs4 import BeautifulSoup
import re

def natural_sort_key(s):
    """Clave de ordenación natural (numérica) para nombres de archivo."""
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', s)]

def main():
    if len(sys.argv) > 1:
        site_dir = sys.argv[1]
    else:
        site_dir = "site"

    if not os.path.isdir(site_dir):
        print(f"Error: el directorio '{site_dir}' no existe.")
        sys.exit(1)

    # Recorremos todas las carpetas dentro de site_dir
    for root, dirs, files in os.walk(site_dir):
        # Buscamos subcarpetas que contengan un archivo index.html
        subdirs = [d for d in dirs if os.path.exists(os.path.join(root, d, 'index.html'))]
        if len(subdirs) <= 1:
            continue   # No hay suficientes páginas para añadir enlaces

        # Ordenamos las subcarpetas de forma natural
        subdirs.sort(key=natural_sort_key)

        # Creamos una lista con las rutas completas de cada index.html
        page_paths = []
        for sub in subdirs:
            page_paths.append(os.path.join(root, sub, 'index.html'))

        # Para cada página que no sea índice de la carpeta padre, añadimos enlaces
        for idx, full_path in enumerate(page_paths):
            # Determinar si esta página es un índice de sección (por ejemplo, la raíz de una sección)
            # En Material, el índice de una sección suele estar en root/index.html
            # Aquí asumimos que no queremos enlaces en la página index.html de la carpeta padre
            # Comprobamos si el archivo actual es el index.html de la carpeta raíz de la sección
            parent_path = os.path.dirname(full_path)
            if os.path.basename(parent_path) == '' or parent_path == root:
                # Esto es el índice de la sección, saltamos
                continue

            # Calculamos rutas relativas
            base_dir = os.path.dirname(full_path)
            prev_path = page_paths[idx-1] if idx > 0 else None
            next_path = page_paths[idx+1] if idx < len(page_paths)-1 else None

            if prev_path is None and next_path is None:
                continue

            # Leer el HTML
            with open(full_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            content_div = soup.find('div', class_='md-content')
            if not content_div:
                continue

            # Construir enlaces
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

            content_div.append(BeautifulSoup(nav_html, 'html.parser'))

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

            print(f"Actualizado: {full_path}")

if __name__ == '__main__':
    main()
