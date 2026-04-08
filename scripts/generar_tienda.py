#!/usr/bin/env python3
"""
Generador de tienda estática con dos opciones de índice (corregido).
"""
import os
import re
import frontmatter

PRODUCTOS_DIR = "productos"
OUTPUT_DIR = "docs/tienda"

def limpiar_texto(texto, max_len=150):
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
    activos = [p for p in productos if p['status'] == 'active']
    if not activos:
        return

    contenido = """---
title: Tienda (Tarjetas)
---

<div id="tienda-tarjetas">
"""
    for p in activos:
        desc_corta = limpiar_texto(p['description'], 120)
        imagen_html = f'<img src="{p["image"]}" alt="{p["title"]}">' if p['image'] else ''
        contenido += f"""
  <a href="/tienda/{p['slug']}/" class="tarjeta-item">
    <div class="tarjeta-imagen">{imagen_html}</div>
    <div class="tarjeta-info">
      <h3>{p['title']}</h3>
      <p>{desc_corta}</p>
    </div>
  </a>
"""
    contenido += """
</div>

<style>
#tienda-tarjetas {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}
#tienda-tarjetas .tarjeta-item {
    display: block !important;
    text-decoration: none !important;
    border: 1px solid var(--md-default-fg-color--lighter);
    border-radius: 8px;
    overflow: hidden;
    background: var(--md-default-bg-color);
    transition: transform 0.2s, box-shadow 0.2s;
}
#tienda-tarjetas .tarjeta-item:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.1);
}
#tienda-tarjetas .tarjeta-imagen {
    width: 100%;
    height: 160px;
    overflow: hidden;
}
#tienda-tarjetas .tarjeta-imagen img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}
#tienda-tarjetas .tarjeta-info {
    padding: 0.8rem;
}
#tienda-tarjetas .tarjeta-info h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
    font-weight: 500;
}
#tienda-tarjetas .tarjeta-info p {
    margin: 0;
    font-size: 0.85rem;
    color: var(--md-default-fg-color--light);
}
</style>
"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "index-tarjetas.md"), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("✅ índice de tarjetas generado")

def generar_indice_tabla(productos):
    activos = [p for p in productos if p['status'] == 'active']
    if not activos:
        return

    contenido = """---
title: Tienda (Lista)
---

<div id="tienda-lista">
"""
    for p in activos:
        desc_corta = limpiar_texto(p['description'], 100)
        imagen_html = f'<img src="{p["image"]}" alt="{p["title"]}">' if p['image'] else ''
        contenido += f"""
  <a href="/tienda/{p['slug']}/" class="lista-item">
    <div class="lista-imagen">{imagen_html}</div>
    <div class="lista-info">
      <h3>{p['title']}</h3>
      <p>{desc_corta}</p>
    </div>
  </a>
"""
    contenido += """
</div>

<style>
#tienda-lista {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin: 2rem 0;
}
#tienda-lista .lista-item {
    display: flex !important;
    align-items: center;
    gap: 1rem;
    text-decoration: none !important;
    border: 1px solid var(--md-default-fg-color--lighter);
    border-radius: 8px;
    padding: 0.5rem;
    background: var(--md-default-bg-color);
    transition: background 0.2s;
}
#tienda-lista .lista-item:hover {
    background: var(--md-default-fg-color--lightest);
}
#tienda-lista .lista-imagen {
    flex-shrink: 0;
    width: 60px;
    height: 60px;
}
#tienda-lista .lista-imagen img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 4px;
    display: block;
}
#tienda-lista .lista-info {
    flex: 1;
}
#tienda-lista .lista-info h3 {
    margin: 0 0 0.2rem 0;
    font-size: 1rem;
    font-weight: 500;
}
#tienda-lista .lista-info p {
    margin: 0;
    font-size: 0.8rem;
    color: var(--md-default-fg-color--light);
}
</style>
"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "index-tabla.md"), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("✅ índice de tabla generado")

def generar_detalles(productos):
    activos = [p for p in productos if p['status'] == 'active']
    for p in activos:
        imagen_html = f'<img src="{p["image"]}" alt="{p["title"]}" class="detalle-imagen">' if p['image'] else ''
        contenido = f"""---
title: {p['title']}
---

# {p['title']}

<div id="producto-detalle">
  <div class="detalle-info">
    {imagen_html}
    <p class="detalle-precio">{p['price']} {p['currency']}</p>
    <a href="{p['kofi_link']}" class="detalle-boton" target="_blank">Comprar</a>
  </div>
  <div class="detalle-descripcion">
    {p['description']}
  </div>
</div>

<style>
#producto-detalle {{
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}}
.detalle-info {{
    flex: 1;
    min-width: 200px;
}}
.detalle-imagen {{
    width: 100%;
    max-width: 280px;
    height: auto;
    border-radius: 8px;
    margin-bottom: 1rem;
    display: block;
}}
.detalle-precio {{
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--md-primary-fg-color);
}}
.detalle-boton {{
    display: inline-block;
    background-color: var(--md-primary-fg-color);
    color: var(--md-primary-bg-color);
    padding: 0.6rem 1.2rem;
    text-decoration: none;
    border-radius: 4px;
    margin-top: 1rem;
}}
.detalle-boton:hover {{
    background-color: var(--md-accent-fg-color);
}}
.detalle-descripcion {{
    flex: 2;
}}
</style>
"""
        out_file = os.path.join(OUTPUT_DIR, f"{p['slug']}.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(contenido)
    print(f"✅ {len(activos)} páginas de detalle generadas")

def main():
    productos = leer_productos()
    generar_indice_tarjetas(productos)
    generar_indice_tabla(productos)
    generar_detalles(productos)

if __name__ == "__main__":
    main()
