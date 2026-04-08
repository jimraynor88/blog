#!/usr/bin/env python3
"""
Genera la tienda estática:
- docs/tienda/index.md (índice con tarjetas)
- docs/tienda/<slug>.md (página de detalle de cada producto)
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

def generar_indice(productos):
    """Genera docs/tienda/index.md con tarjetas responsivas."""
    activos = [p for p in productos if p['status'] == 'active']
    if not activos:
        print("⚠️ No hay productos activos.")
        return

    contenido = """---
title: Tienda
description: Todos mis productos y servicios
---

# Tienda

<div class="productos-grid">
"""
    for p in activos:
        # Descripción corta (primeros 150 caracteres sin saltos)
        desc_corta = limpiar_texto(p['description'], 150)
        imagen_html = f'<img src="{p["image"]}" alt="{p["title"]}" class="producto-imagen">' if p['image'] else ''
        contenido += f"""
  <div class="producto-card">
    <a href="/tienda/{p['slug']}/" class="producto-link">
      {imagen_html}
      <div class="producto-card-info">
        <h3 class="producto-card-titulo">{p['title']}</h3>
        <p class="producto-card-desc">{desc_corta}</p>
      </div>
    </a>
  </div>
"""
    contenido += """</div>

<style>
.productos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}
.producto-card {
    border: 1px solid var(--md-default-fg-color--lighter);
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    background: var(--md-default-bg-color);
}
.producto-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.producto-link {
    text-decoration: none;
    color: inherit;
    display: block;
}
.producto-imagen {
    width: 100%;
    height: 180px;
    object-fit: cover;
}
.producto-card-info {
    padding: 1rem;
}
.producto-card-titulo {
    margin-top: 0;
    font-size: 1.2rem;
    font-weight: 500;
}
.producto-card-desc {
    font-size: 0.9rem;
    color: var(--md-default-fg-color--light);
}
</style>
"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"✅ Índice generado en {OUTPUT_DIR}/index.md")

def generar_detalles(productos):
    """Genera una página por cada producto activo."""
    activos = [p for p in productos if p['status'] == 'active']
    for p in activos:
        contenido = f"""---
title: {p['title']}
description: {limpiar_texto(p['description'], 160)}
---

# {p['title']}

<div class="producto-detalle">

<div class="producto-detalle-info">
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
    generar_indice(productos)
    generar_detalles(productos)

if __name__ == "__main__":
    main()
