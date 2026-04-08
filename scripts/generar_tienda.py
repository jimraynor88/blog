#!/usr/bin/env python3
"""
Script para generar la tienda desde archivos Markdown.
Genera dos archivos:
- docs/products.json: con los datos de los productos (lo usará el JavaScript de tu web).
- docs/tienda/index.md: la página principal de la tienda.
"""
import os
import json
import frontmatter
from datetime import datetime

# Configuración
PRODUCTOS_DIR = "productos"  # Carpeta donde guardas los .md de tus productos
SALIDA_JSON = "docs/products.json"
SALIDA_TIENDA_INDEX = "docs/tienda/index.md" # Nueva ruta para la página estática

def leer_productos():
    """Lee todos los archivos .md de la carpeta productos y extrae los datos."""
    productos = []
    for filename in os.listdir(PRODUCTOS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(PRODUCTOS_DIR, filename)
            try:
                # Carga el archivo .md, separando el front matter (---) del contenido
                post = frontmatter.load(filepath)
                # Añade los datos del producto a una lista
                productos.append({
                    "title": post.get('title'),
                    "price": post.get('price'),
                    "currency": post.get('currency'),
                    "image": post.get('image'),
                    "kofi_link": post.get('kofi_link'),
                    "status": post.get('status'),
                    "description": post.content,
                    "slug": filename.replace(".md", "") # Identificador único
                })
            except Exception as e:
                print(f"Error procesando {filename}: {e}")
    return productos

def generar_pagina_tienda(productos):
    """Genera la página estática de la tienda (docs/tienda/index.md) con todos los productos."""
    # Filtramos solo los productos activos (status: active)
    productos_activos = [p for p in productos if p.get('status') == 'active']
    if not productos_activos:
        print("⚠️ No se encontraron productos activos. No se generará la página de la tienda.")
        return

    # Crear el contenido de la página en formato Markdown
    contenido = """---
title: Tienda
description: Adquiere mis servicios y productos
---

# Tienda

Aquí puedes ver todos los productos y servicios que ofrezco.

"""
    for p in productos_activos:
        # Añadir cada producto como un bloque en la página
        contenido += f"""
<div class="producto-tarjeta">
    <div class="producto-info">
        <h3 class="producto-titulo">{p['title']}</h3>
        <div class="producto-descripcion">{p['description']}</div>
        <p class="producto-precio">{p['price']} {p['currency']}</p>
        <a href="{p['kofi_link']}" class="producto-boton" target="_blank" rel="noopener noreferrer">Comprar</a>
    </div>
</div>
"""
    # Asegurar que el directorio de salida existe
    os.makedirs(os.path.dirname(SALIDA_TIENDA_INDEX), exist_ok=True)
    with open(SALIDA_TIENDA_INDEX, 'w', encoding='utf-8') as f:
        f.write(contenido)

    print(f"✅ Página de tienda generada en {SALIDA_TIENDA_INDEX}")

def main():
    productos = leer_productos()
    # Filtramos solo los productos activos (status: active)
    productos_activos = [p for p in productos if p.get('status') == 'active']
    
    # 1. Guardamos la lista en un archivo JSON
    with open(SALIDA_JSON, 'w', encoding='utf-8') as f:
        json.dump(productos_activos, f, indent=2, ensure_ascii=False)
    print(f"✅ {len(productos_activos)} productos exportados a {SALIDA_JSON}")

    # 2. Generamos la página estática de la tienda
    generar_pagina_tienda(productos_activos)

if __name__ == "__main__":
    main()
