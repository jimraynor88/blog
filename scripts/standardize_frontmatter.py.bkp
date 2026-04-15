#!/usr/bin/env python3
"""
Script para estandarizar frontmatter en archivos .md.
No elimina información, solo añade campos faltantes.
"""
import os
import re
import frontmatter
from pathlib import Path

DOCS_DIR = "docs"

# Reglas por ruta: (regex, campos_obligatorios, campos_opcionales_con_default)
RULES = [
    (r"blog/posts/.*\.md", 
     {"title": "", "date": "", "tags": []},
     {"author": "Jim Raynor", "draft": False}),
    (r"tienda/.*\.md",
     {"title": "", "price": "", "currency": "EUR", "kofi_link": "", "status": "active"},
     {"image": "", "tags": []}),
    (r"Astrologia/Carta_Natal/Casas/Casa_\d+\.md",
     {"title": "", "alias": ""},
     {"tags": ["astrología", "casa natal"]}),
    (r".*\.md",  # default
     {"title": ""},
     {"author": "Jim Raynor", "tags": []}),
]

def get_defaults(filepath):
    """Devuelve (campos_obligatorios, campos_opcionales) para la ruta dada"""
    for pattern, required, optional in RULES:
        if re.search(pattern, filepath):
            return required.copy(), optional.copy()
    # fallback
    return {"title": ""}, {}

def update_frontmatter(filepath):
    """Actualiza el frontmatter del archivo añadiendo campos faltantes"""
    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    original_content = post.content
    metadata = post.metadata

    required, optional = get_defaults(filepath)
    changed = False

    # Añadir campos obligatorios si no existen
    for key, default_value in required.items():
        if key not in metadata:
            metadata[key] = default_value
            changed = True
            print(f"  + Añadido campo '{key}' con valor '{default_value}'")

    # Añadir campos opcionales con valor por defecto
    for key, default_value in optional.items():
        if key not in metadata:
            metadata[key] = default_value
            changed = True
            print(f"  + Añadido campo opcional '{key}' con valor '{default_value}'")

    if changed:
        new_post = frontmatter.Post(original_content, **metadata)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(new_post))
        print(f"✅ Actualizado: {filepath}")
    else:
        print(f"⏩ Sin cambios: {filepath}")

def main():
    for root, dirs, files in os.walk(DOCS_DIR):
        # Ignorar carpetas especiales
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('site', 'overrides')]
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, DOCS_DIR)
                print(f"Procesando {rel_path}...")
                update_frontmatter(full_path)

if __name__ == "__main__":
    main()
