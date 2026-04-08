#!/usr/bin/env python3
"""
Generador de tienda estilo lista (como el blog)
- docs/tienda/index.md: listado de productos
- docs/tienda/<slug>.md: página de detalle de cada producto
"""
import os
import re
import frontmatter
from collections import defaultdict

PRODUCTOS_DIR = "productos"
OUTPUT_DIR = "docs/tienda"

def limpiar_texto(texto, max_len=200):
    """Elimina saltos de línea extra y acorta a max_len caracteres."""
    texto = re.sub(r'\n+', ' ', texto).strip()
    if len(texto) > max_len:
        return texto[:max_len] + "..."
    return texto

def leer_productos():
    productos = []
    for filename in os.listdir(PRODUCTOS_DIR):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(PRODUCTOS_DIR, filename)
        post = frontmatter.load(filepath)
        slug = filename.replace(".md", "")
        tags = post.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        productos.append({
            "slug": slug,
            "title": post.get('title', 'Sin título'),
            "price": post.get('price', '0'),
            "currency": post.get('currency', 'EUR'),
            "image": post.get('image', ''),
            "kofi_link": post.get('kofi_link', '#'),
            "status": post.get('status', 'draft'),
            "description": post.content,
            "tags": tags,
        })
    return productos

def write_index(productos):
    """Genera docs/tienda/index.md con listado estilo blog."""
    activos = [p for p in productos if p['status'] == 'active']
    if not activos:
        print("⚠️ No hay productos activos. No se genera índice.")
        return

    content = """# Tienda

Lista de productos disponibles:

"""
    for p in activos:
        desc_corta = limpiar_texto(p['description'], 150)
        content += f"## [{p['title']}](/tienda/{p['slug']}/)\n\n"
        content += f"{desc_corta}\n\n"
        if p['tags']:
            content += "**Etiquetas:** "
            tag_links = []
            for tag in p['tags']:
                # Para etiquetas, podrías generar un enlace a /tienda/tags/<tag>/ si implementas esa página
                # De momento solo mostramos el nombre sin enlace
                tag_links.append(f"`{tag}`")
            content += " ".join(tag_links) + "\n\n"
        content += "---\n\n"
    with open(os.path.join(OUTPUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Índice de tienda generado en {OUTPUT_DIR}/index.md")

def write_detail(productos):
    """Genera página de detalle para cada producto activo."""
    activos = [p for p in productos if p['status'] == 'active']
    for p in activos:
        imagen_html = f'<img src="{p["image"]}" alt="{p["title"]}" style="max-width: 100%; height: auto; border-radius: 8px; margin-bottom: 1rem;">' if p['image'] else ''
        content = f"""---
title: {p['title']}
---

# {p['title']}

<div style="display: flex; flex-wrap: wrap; gap: 2rem;">
  <div style="flex: 1; min-width: 200px;">
    {imagen_html}
    <p style="font-size: 1.5rem; font-weight: bold; color: var(--md-primary-fg-color);">{p['price']} {p['currency']}</p>
    <a href="{p['kofi_link']}" target="_blank" rel="noopener noreferrer" style="display: inline-block; background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); padding: 0.6rem 1.2rem; text-decoration: none; border-radius: 4px;">Comprar</a>
  </div>
  <div style="flex: 2;">
    {p['description']}
  </div>
</div>
"""
        out_file = os.path.join(OUTPUT_DIR, f"{p['slug']}.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"✅ {len(activos)} páginas de detalle generadas")

def main():
    productos = leer_productos()
    # Filtrar solo activos para el índice y detalles
    activos = [p for p in productos if p['status'] == 'active']
    if not activos:
        print("No hay productos activos. No se genera nada.")
        return
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    write_index(activos)
    write_detail(activos)

if __name__ == "__main__":
    main()
