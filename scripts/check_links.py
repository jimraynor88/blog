#!/usr/bin/env python3
"""
Verifica enlaces estilo wiki ([[alias|texto]] o [[página]]) en archivos Markdown.
Genera un reporte con:
- Enlaces rotos (destino no encontrado)
- Páginas sin alias definido en el frontmatter
- Índice de todos los alias y su ruta destino
"""

import os
import re
import sys
from pathlib import Path
import frontmatter
from collections import defaultdict

# Configuración
DOCS_DIR = "docs"          # Carpeta donde están los archivos .md
REPORT_FILE = "docs/alias_report.md"   # Reporte generado (se incluirá en el sitio)
IGNORE_PATTERNS = [r"\.git", r"\.github", r"node_modules", r"site"]  # Carpetas a ignorar

# Expresión regular para capturar [[...]] (wikilinks)
WIKILINK_PATTERN = re.compile(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')

def get_all_md_files(base_dir):
    """Recorre recursivamente el directorio base y devuelve lista de rutas relativas de archivos .md"""
    md_files = []
    for root, dirs, files in os.walk(base_dir):
        # Ignorar directorios no deseados
        dirs[:] = [d for d in dirs if not any(re.search(p, d) for p in IGNORE_PATTERNS)]
        for file in files:
            if file.endswith('.md'):
                rel_path = os.path.relpath(os.path.join(root, file), base_dir)
                md_files.append(rel_path)
    return md_files

def extract_alias(file_path):
    """Lee el frontmatter y devuelve el alias (si existe) o None"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            alias = post.get('alias')
            if alias and isinstance(alias, str):
                return alias.strip()
            # También puede ser lista, pero normalmente string
            return None
    except Exception:
        return None

def build_alias_map(docs_dir):
    """Construye un diccionario: alias -> ruta relativa (sin extensión)"""
    alias_map = {}
    md_files = get_all_md_files(docs_dir)
    for rel_path in md_files:
        full_path = os.path.join(docs_dir, rel_path)
        alias = extract_alias(full_path)
        if alias:
            # La ruta destino será / + ruta sin extensión
            dest = '/' + rel_path[:-3] + '/'
            alias_map[alias] = dest
        # También mapear el nombre del archivo (sin extensión) a su ruta
        base_name = os.path.splitext(os.path.basename(rel_path))[0]
        alias_map[base_name] = dest if alias else ('/' + rel_path[:-3] + '/')
    return alias_map

def check_wikilinks(md_file, alias_map):
    """Analiza un archivo md y devuelve lista de enlaces rotos (tupla: línea, texto, destino)"""
    broken = []
    full_path = os.path.join(DOCS_DIR, md_file)
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line_num, line in enumerate(lines, 1):
                matches = WIKILINK_PATTERN.findall(line)
                for target, display in matches:
                    # target puede ser alias o nombre de archivo
                    if target not in alias_map:
                        broken.append((md_file, line_num, target, display or target))
    except Exception as e:
        print(f"Error leyendo {md_file}: {e}")
    return broken

def find_missing_aliases(docs_dir):
    """Devuelve lista de archivos .md que no tienen alias en frontmatter"""
    missing = []
    md_files = get_all_md_files(docs_dir)
    for rel_path in md_files:
        full_path = os.path.join(docs_dir, rel_path)
        alias = extract_alias(full_path)
        if not alias:
            missing.append(rel_path)
    return missing

def generate_report(alias_map, broken_links, missing_aliases):
    """Genera el reporte en formato Markdown"""
    lines = []
    lines.append("# Reporte de Enlaces y Alias\n")
    lines.append("## 🔍 Enlaces rotos\n")
    if broken_links:
        lines.append("| Archivo | Línea | Enlace | Destino buscado |")
        lines.append("|---------|-------|--------|-----------------|")
        for file, line, target, text in broken_links:
            lines.append(f"| {file} | {line} | `[[{target}|{text}]]` | `{target}` |")
    else:
        lines.append("✅ No se encontraron enlaces rotos.\n")
    
    lines.append("\n## 📄 Páginas sin alias\n")
    if missing_aliases:
        lines.append("Los siguientes archivos no tienen definido un `alias:` en su frontmatter:")
        lines.append("")
        for f in missing_aliases:
            lines.append(f"- `{f}`")
    else:
        lines.append("✅ Todos los archivos tienen alias definido.\n")
    
    lines.append("\n## 📚 Índice de alias\n")
    lines.append("| Alias | Ruta destino |")
    lines.append("|-------|--------------|")
    for alias, dest in sorted(alias_map.items()):
        lines.append(f"| `{alias}` | `{dest}` |")
    
    return "\n".join(lines)

def main():
    print("🔍 Verificando enlaces y alias...")
    alias_map = build_alias_map(DOCS_DIR)
    print(f"   → {len(alias_map)} alias/nombres mapeados.")
    
    # Analizar todos los archivos .md buscando enlaces rotos
    all_broken = []
    md_files = get_all_md_files(DOCS_DIR)
    for md_file in md_files:
        broken = check_wikilinks(md_file, alias_map)
        all_broken.extend(broken)
    
    missing_aliases = find_missing_aliases(DOCS_DIR)
    
    report = generate_report(alias_map, all_broken, missing_aliases)
    
    # Escribir el reporte
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✅ Reporte generado en {REPORT_FILE}")
    
    # Si hay enlaces rotos, podemos fallar el build (opcional)
    if all_broken:
        print(f"⚠️ Se encontraron {len(all_broken)} enlaces rotos. Revisa el reporte.")
        # Descomentar la siguiente línea si quieres que el workflow falle
        # sys.exit(1)
    else:
        print("✅ No se detectaron enlaces rotos.")

if __name__ == "__main__":
    main()
