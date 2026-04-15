#!/usr/bin/env python3
"""
Genera dinámicamente:
- SUMMARY.md: navegación completa del sitio (para literate-nav)
- index.md para carpetas (sobrescribe los existentes)
Lee el frontmatter (title, description, tags) y asigna iconos temáticos.
"""
import os
from pathlib import Path
import frontmatter
import mkdocs_gen_files

DOCS_DIR = "docs"
IGNORE_DIRS = [".git", ".github", "overrides", "site", "scripts", "productos"]
IGNORE_FILES = [".pages", "README.md", "CNAME", "license", "yaml"]
MARKDOWN_EXTS = (".md", ".markdown")

# Mapa de iconos por palabra clave (se buscarán en la ruta, título, tags)
# Puedes añadir más entradas o modificar los iconos (emojis o códigos HTML)
THEME_ICONS = {
    "astrologia": "🔮",
    "carta_natal": "🌟",
    "casas": "🏠",
    "perfiles": "👤",
    "conditio_vitae": "📜",
    "blog": "📝",
    "seguridad": "🔒",
    "pgp": "🔑",
    "contacto": "📧",
    "tienda": "🛒",
    "cursos": "📚",
    "zona-privada": "🔐",
    "acceso-exclusivo": "⭐",
    "privado": "🚫",
    "admin": "👑",
    "invitados": "👥",
}

def get_icon_for_path(path_str, title, tags):
    """Devuelve un icono según la ruta, título o etiquetas."""
    path_lower = path_str.lower()
    for keyword, icon in THEME_ICONS.items():
        if keyword in path_lower or keyword in title.lower():
            return icon
    if tags:
        for tag in tags:
            tag_lower = tag.lower()
            for keyword, icon in THEME_ICONS.items():
                if keyword in tag_lower:
                    return icon
    # Icono por defecto según tipo de contenido
    if "index" in path_str:
        return "📄"
    return "📌"

def get_title_description_tags(file_path):
    """Extrae título, descripción y tags del frontmatter.
       Si no hay descripción, toma los primeros 150 caracteres del contenido."""
    try:
        post = frontmatter.load(file_path)
        title = post.get('title', file_path.stem.replace('_', ' ').title())
        description = post.get('description', '')
        tags = post.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        # Si no hay descripción, usar un extracto del contenido
        if not description and post.content:
            # Eliminar saltos de línea excesivos y tomar primeros 150 caracteres
            raw = ' '.join(post.content.split())
            description = raw[:150] + ('...' if len(raw) > 150 else '')
        return title, description, tags
    except Exception:
        return file_path.stem.replace('_', ' ').title(), '', []

def generate_summary_and_indexes():
    """Recorre docs/ y genera SUMMARY.md e index.md dinámicos."""
    nav_lines = []
    base_path = Path(DOCS_DIR)
    
    def process_dir(current_dir, indent_level=0, relative_path=""):
        nonlocal nav_lines
        items = []  # lista de (title, url, typ, icon, description)
        children = sorted(current_dir.iterdir())
        for child in children:
            if child.name in IGNORE_FILES or child.name.startswith('.'):
                continue
            if child.is_dir() and child.name not in IGNORE_DIRS:
                # Procesar subdirectorio recursivamente
                sub_result = process_dir(child, indent_level + 1, f"{relative_path}/{child.name}")
                if sub_result:
                    # Intentar obtener título del índice del subdirectorio (si existe)
                    idx_path = child / "index.md"
                    if idx_path.exists():
                        title, _, _ = get_title_description_tags(idx_path)
                    else:
                        title = child.name.replace('_', ' ').title()
                    icon = get_icon_for_path(str(child), title, [])
                    items.append((title, f"{relative_path}/{child.name}/", 'dir', icon, ''))
            elif child.suffix in MARKDOWN_EXTS and child.name != "index.md":
                title, desc, tags = get_title_description_tags(child)
                url = f"{relative_path}/{child.stem}"
                icon = get_icon_for_path(str(child), title, tags)
                items.append((title, url, 'file', icon, desc))
        
        if not items:
            return None
        
        # Generar el índice de esta carpeta (index.md)
        folder_title = current_dir.name.replace('_', ' ').title()
        index_content = f"# {folder_title}\n\n"
        index_content += "| Icono | Página | Descripción |\n"
        index_content += "|-------|--------|-------------|\n"
        for title, url, typ, icon, desc in items:
            # Asegurar que la URL termina con / para carpetas (ya lo tiene)
            link = f"[{title}]({url}/)" if typ == 'dir' else f"[{title}]({url})"
            # Limitar descripción a 100 caracteres para la tabla
            short_desc = desc[:100] + ('...' if len(desc) > 100 else '')
            index_content += f"| {icon} | {link} | {short_desc} |\n"
        
        # Escribir index.md (sobrescribe cualquier existente)
        out_path = current_dir.relative_to(base_path) / "index.md"
        with mkdocs_gen_files.open(out_path, 'w') as f:
            f.write(index_content)
        
        # Añadir entrada en la navegación (SUMMARY.md)
        indent = "  " * indent_level
        section_title = folder_title
        nav_lines.append(f"{indent}* [{section_title}]({relative_path}/)")
        for title, url, typ, icon, _ in items:
            if typ == 'dir':
                nav_lines.append(f"{indent}  * {icon} [{title}]({url}/)")
            else:
                nav_lines.append(f"{indent}  * {icon} [{title}]({url})")
        return True
    
    # Procesar la raíz
    root_path = base_path
    # Página de inicio
    if (root_path / "index.md").exists():
        title, desc, tags = get_title_description_tags(root_path / "index.md")
        icon = get_icon_for_path("home", title, tags)
        nav_lines.append(f"* {icon} [{title}](/)")
    else:
        nav_lines.append("* 🏠 [Inicio](/)")
    
    # Procesar elementos de primer nivel
    for child in sorted(root_path.iterdir()):
        if child.name in IGNORE_DIRS or child.name.startswith('.'):
            continue
        if child.is_dir():
            process_dir(child, indent_level=1, relative_path=f"/{child.name}")
        elif child.suffix in MARKDOWN_EXTS and child.name != "index.md":
            title, desc, tags = get_title_description_tags(child)
            icon = get_icon_for_path(str(child), title, tags)
            nav_lines.append(f"* {icon} [{title}](/{child.stem})")
    
    # Escribir SUMMARY.md
    summary_content = "\n".join(nav_lines)
    with mkdocs_gen_files.open("SUMMARY.md", 'w') as f:
        f.write(summary_content)

def main():
    generate_summary_and_indexes()

if __name__ == "__main__":
    main()
