#!/usr/bin/env python3
"""
Genera un archivo index.md en cada carpeta de docs/ que no tenga uno,
listando los archivos .md y subcarpetas (excluyendo índices existentes).
No requiere plugins de MkDocs, escribe directamente en el sistema de archivos.
"""
import os
from pathlib import Path

DOCS_DIR = "docs"
IGNORE_DIRS = [".git", ".github", "overrides", "site", "scripts", "productos"]
IGNORE_FILES = [".pages", "README.md", "CNAME", "license", "yaml", "SUMMARY.md"]
MARKDOWN_EXTS = (".md", ".markdown")

def get_title_from_markdown(file_path):
    """Extrae el título del primer encabezado (# Título) o del nombre del archivo."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('# '):
                    return line[2:].strip()
    except:
        pass
    return file_path.stem.replace('_', ' ').title()

def generate_index_for_folder(folder_path):
    """Crea o actualiza index.md dentro de la carpeta."""
    items = []  # (icono, enlace, descripción)
    for child in sorted(folder_path.iterdir()):
        if child.name in IGNORE_FILES or child.name.startswith('.'):
            continue
        if child.is_dir() and child.name not in IGNORE_DIRS:
            # Subcarpeta: enlazar a su índice
            title = child.name.replace('_', ' ').title()
            items.append(('📁', f"[{title}]({child.name}/)", ''))
        elif child.suffix in MARKDOWN_EXTS and child.name != "index.md":
            title = get_title_from_markdown(child)
            items.append(('📄', f"[{title}]({child.name})", ''))
    if not items:
        return False

    folder_title = folder_path.name.replace('_', ' ').title()
    index_content = f"# {folder_title}\n\n"
    index_content += "| Icono | Página |\n"
    index_content += "|-------|--------|\n"
    for icon, link, _ in items:
        index_content += f"| {icon} | {link} |\n"

    index_path = folder_path / "index.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"✅ Generado/actualizado: {index_path}")
    return True

def main():
    base_path = Path(DOCS_DIR)
    if not base_path.exists():
        print(f"Error: No se encuentra la carpeta '{DOCS_DIR}'.")
        return

    # Generar índices para todas las carpetas
    count = 0
    for current_dir in sorted(base_path.rglob("*")):
        if current_dir.is_dir() and current_dir.name not in IGNORE_DIRS:
            if generate_index_for_folder(current_dir):
                count += 1
    print(f"Proceso completado. {count} índices generados/actualizados.")

if __name__ == "__main__":
    main()
