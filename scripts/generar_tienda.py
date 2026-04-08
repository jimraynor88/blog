#!/usr/bin/env python3
"""
Generador de tienda estática con dos opciones de índice:
- Tarjetas (grid responsivo)
- Tabla simple
"""
import os
import re
import frontmatter

PRODUCTOS_DIR = "productos"
OUTPUT_DIR = "docs/tienda"

def limpiar_texto(texto, max_len=150):
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
        productos.append({
            "slug": slug,
            "title": post.get('title', 'Sin título'),
            "price": post.get('price', '0'),
            "currency": post.get('currency', 'EUR'),
            "image": post.get('image', ''),
            "kofi_link": post.get('kofi_link', '#'),
            "status": post.get('status', 'draft'),
            "description": post.content,
        })
    return productos

def generar_indice_tarjetas(productos):
    """Opción A: Tarjetas responsivas con imagen, título y descripción."""
    activos = [p for p in productos if p['status'] == 'active']
    if not activos:
        print("⚠️ No hay productos activos para el índice de tarjetas.")
        return

    contenido = """---
title: Tienda (Tarjetas)
description: Todos mis productos y servicios
---

# Tienda

<div class="productos-grid">
"""
    for p in activos:
        desc_corta = limpiar_texto(p['description'], 120)
        imagen_html = f'<img src="{p["image"]}" alt="{p["title"]}" class="producto-imagen">' if p['image'] else ''
        contenido += f"""
  <a href="/tienda/{p['slug']}/" class="producto-card">
    {imagen_html}
    <div class="producto-card-info">
      <h3 class="producto-card-titulo">{p['title']}</h3>
      <p class="producto-card-desc">{desc_corta}</p>
    </div>
  </a>
"""
    contenido += """</div>

<style>
.productos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}
.producto-card {
    display: block;
    text-decoration: none;
    color: inherit;
    border: 1px solid var(--md-default-fg-color--lighter);
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    background: var(--md-default-bg-color);
}
.producto-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
.producto-imagen {
    width: 100%;
    height: 160px;
    object-fit: cover;
    background-color: #f0f0f0;
}
.producto-card-info {
    padding: 1rem;
}
.producto-card-titulo {
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
    font-weight: 500;
}
.producto-card-desc {
    font-size: 0.9rem;
    color: var(--md-default-fg-color--light);
    margin: 0;
}
</style>
"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "index-tarjetas.md"), "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"✅ Índice de tarjetas generado en {OUTPUT_DIR}/index-tarjetas.md")

def generar_indice_tabla(productos):
    """Opción B: Tabla simple con imagen pequeña, título y descripción."""
    activos = [p for p in productos if p['status'] == 'active']
    if not activos:
        print("⚠️ No hay productos activos para el índice de tabla.")
        return

    contenido = """---
title: Tienda (Tabla)
description: Todos mis productos y servicios
---

# Tienda

<div class="productos-tabla">
"""
    for p in activos:
        desc_corta = limpiar_texto(p['description'], 100)
        imagen_html = f'<img src="{p["image"]}" alt="{p["title"]}" class="producto-tabla-imagen">' if p['image'] else ''
        contenido += f"""
  <a href="/tienda/{p['slug']}/" class="producto-tabla-fila">
    <div class="producto-tabla-celda-imagen">{imagen_html}</div>
    <div class="producto-tabla-celda-info">
      <h3 class="producto-tabla-titulo">{p['title']}</h3>
      <p class="producto-tabla-desc">{desc_corta}</p>
    </div>
  </a>
"""
    contenido += """</div>

<style>
.productos-tabla {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 2rem;
}
.producto-tabla-fila {
    display: flex;
    align-items: center;
    gap: 1rem;
    text-decoration: none;
    color: inherit;
    padding: 0.75rem;
    border: 1px solid var(--md-default-fg-color--lighter);
    border-radius: 8px;
    transition: background 0.2s;
}
.producto-tabla-fila:hover {
    background: var(--md-default-fg-color--lightest);
}
.producto-tabla-celda-imagen {
    flex-shrink: 0;
    width: 60px;
    height: 60px;
}
.producto-tabla-imagen {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 6px;
}
.producto-tabla-celda-info {
    flex: 1;
}
.producto-tabla-titulo {
    margin: 0 0 0.25rem 0;
    font-size: 1.1rem;
    font-weight: 500;
}
.producto-tabla-desc {
    margin: 0;
    font-size: 0.85rem;
    color: var(--md-default-fg-color--light);
}
</style>
"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "index-tabla.md"), "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"✅ Índice de tabla generado en {OUTPUT_DIR}/index-tabla.md")

def generar_detalles(productos):
    """Genera página de detalle para cada producto, incluyendo imagen."""
    activos = [p for p in productos if p['status'] == 'active']
    for p in activos:
        imagen_html = f'<img src="{p["image"]}" alt="{p["title"]}" class="producto-detalle-imagen">' if p['image'] else ''
        contenido = f"""---
title: {p['title']}
description: {limpiar_texto(p['description'], 160)}
---

# {p['title']}

<div class="producto-detalle">

<div class="producto-detalle-info">
  {imagen_html}
  <p class="producto-precio">{p['price']} {p['currency']}</p>
  <a href="{p['kofi_link']}" class="producto-boton" target="_blank" rel="noopener noreferrer">Comprar</a>
</div>

<div class="producto-detalle-descripcion">
{p['description']}
</div>

</div>

<style>
.producto-detalle {{
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}}
.producto-detalle-info {{
    flex: 1;
    min-width: 200px;
}}
.producto-detalle-imagen {{
    width: 100%;
    max-width: 300px;
    height: auto;
    border-radius: 8px;
    margin-bottom: 1rem;
}}
.producto-precio {{
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--md-primary-fg-color);
}}
.producto-boton {{
    display: inline-block;
    background-color: var(--md-primary-fg-color);
    color: var(--md-primary-bg-color);
    padding: 0.7rem 1.5rem;
    text-decoration: none;
    border-radius: 4px;
    margin-top: 1rem;
}}
.producto-boton:hover {{
    background-color: var(--md-accent-fg-color);
}}
.producto-detalle-descripcion {{
    flex: 2;
}}
</style>
"""
        out_file = os.path.join(OUTPUT_DIR, f"{p['slug']}.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"✅ Página de detalle: {out_file}")

def main():
    productos = leer_productos()
    generar_indice_tarjetas(productos)   # Opción A
    generar_indice_tabla(productos)      # Opción B
    generar_detalles(productos)

if __name__ == "__main__":
    main()
