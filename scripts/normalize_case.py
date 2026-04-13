#!/usr/bin/env python3
"""
Normaliza a minúsculas todos los archivos y carpetas dentro de 'docs/',
y actualiza enlaces internos (Markdown y wikilinks) en todos los archivos .md.
"""
import os
import re
import shutil
from pathlib import Path

DOCS_DIR = "docs"

def get_all_paths(base_dir):
    paths = []
    for root, dirs, files in os.walk(base_dir):
        for d in dirs:
            rel_path = os.path.relpath(os.path.join(root, d), start=base_dir)
            paths.append(rel_path + '/')
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), start=base_dir)
            paths.append(rel_path)
    return paths

def rename_to_lowercase(base_dir):
    changes = []
    paths = get_all_paths(base_dir)
    paths.sort(key=lambda p: -p.count('/'))
    for old_rel in paths:
        old_abs = os.path.join(base_dir, old_rel)
        new_rel = old_rel.lower()
        if old_rel == new_rel:
            continue
        new_abs = os.path.join(base_dir, new_rel)
        if os.path.exists(new_abs):
            print(f"⚠️ Conflicto: {old_abs} -> {new_abs} ya existe. Saltando.")
            continue
        try:
            shutil.move(old_abs, new_abs)
            changes.append((old_rel, new_rel))
            print(f"✅ Renombrado: {old_rel} -> {new_rel}")
        except Exception as e:
            print(f"❌ Error al renombrar {old_abs}: {e}")
    return changes

def update_links_in_file(filepath, rename_map):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    def replace_md_link(match):
        text = match.group(1)
        url = match.group(2)
        if url.startswith(('http://', 'https://', 'mailto:', '#')):
            return match.group(0)
        new_url = url
        for old, new in rename_map.items():
            pattern = re.escape(old)
            new_url = re.sub(pattern, new, new_url)
        return f"[{text}]({new_url})"

    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_md_link, content)

    def replace_wikilink(match):
        full = match.group(0)
        inside = match.group(1)
        if '|' in inside:
            target, display = inside.split('|', 1)
        else:
            target = inside
            display = target
        new_target = target
        for old, new in rename_map.items():
            old_no_ext = old[:-3] if old.endswith('.md') else old
            new_no_ext = new[:-3] if new.endswith('.md') else new
            if target == old_no_ext:
                new_target = new_no_ext
                break
            if target.startswith(old_no_ext + '/'):
                new_target = new_no_ext + target[len(old_no_ext):]
                break
        if '|' in inside:
            new_inside = f"{new_target}|{display}"
        else:
            new_inside = new_target
        return f"[[{new_inside}]]"

    content = re.sub(r'\[\[([^\]]+)\]\]', replace_wikilink, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ↪ Enlaces actualizados en {filepath}")
        return True
    return False

def main():
    if not os.path.isdir(DOCS_DIR):
        print(f"Error: No se encuentra la carpeta '{DOCS_DIR}'.")
        return

    print("🔍 Renombrando archivos y carpetas a minúsculas...")
    rename_changes = rename_to_lowercase(DOCS_DIR)
    rename_map = dict(rename_changes)
    extra_map = {}
    for old, new in rename_map.items():
        if old.endswith('.md'):
            extra_map[old[:-3]] = new[:-3]
        if old.endswith('/'):
            extra_map[old] = new
    rename_map.update(extra_map)

    print("\n🔍 Actualizando enlaces en archivos .md...")
    md_files = list(Path(DOCS_DIR).rglob('*.md'))
    for md_file in md_files:
        update_links_in_file(md_file, rename_map)

    print("\n✅ Proceso completado.")

if __name__ == "__main__":
    main()
