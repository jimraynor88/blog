#!/usr/bin/env python3
"""
Script para generar la tienda desde archivos Markdown.
Genera dos archivos:
- products.json: con los datos de los productos (lo usará el JavaScript de tu web).
- tienda.html: la página completa de la tienda.
"""
import os
import json
import frontmatter

# Configuración
PRODUCTOS_DIR = "productos"  # Carpeta donde guardas los .md de tus productos
SALIDA_JSON = "docs/products.json"  # Archivo JSON para el catálogo

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

def main():
    productos = leer_productos()
    # Filtramos solo los productos activos (status: active)
    productos_activos = [p for p in productos if p.get('status') == 'active']
    
    # Guardamos la lista en un archivo JSON
    with open(SALIDA_JSON, 'w', encoding='utf-8') as f:
        json.dump(productos_activos, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(productos_activos)} productos exportados a {SALIDA_JSON}")

if __name__ == "__main__":
    main()
