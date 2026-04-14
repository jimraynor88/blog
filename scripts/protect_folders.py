#!/usr/bin/env python3
"""
Protege múltiples carpetas con diferentes niveles o contraseñas.
Lee la configuración desde protect_config.yml.
Permite excluir archivos o carpetas y activar/desactivar reglas.
"""
import os
import sys
import yaml
import frontmatter
from pathlib import Path
import fnmatch  # para patrones wildcard

CONFIG_FILE = "protect_config.yml"
DOCS_DIR = "docs"

def load_config():
    """Carga el archivo YAML de configuración."""
    if not os.path.exists(CONFIG_FILE):
        print(f"⚠️ No se encontró {CONFIG_FILE}. Usando configuración por defecto.")
        return []
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config.get('protections', [])

def is_excluded(file_path, exclude_list, base_folder):
    """
    Determina si un archivo debe ser excluido.
    file_path: ruta completa del archivo (ej. docs/Astrologia/Carta_Natal/Casa_01.md)
    exclude_list: lista de patrones/strings de exclusión
    base_folder: carpeta base de la regla (ej. docs/Astrologia/Carta_Natal)
    """
    # Ruta relativa desde la carpeta base (para comparar con exclusión)
    rel_path = os.path.relpath(file_path, base_folder)
    # Nombre del archivo (para exclusión simple)
    filename = os.path.basename(file_path)

    for pattern in exclude_list:
        # Si el patrón es una ruta relativa (contiene '/')
        if '/' in pattern or '\\' in pattern:
            # Usar fnmatch para soportar comodines como **/borrador.md
            if fnmatch.fnmatch(rel_path, pattern):
                return True
        else:
            # Patrón simple: coincidencia con nombre de archivo o con nombre dentro de subcarpeta?
            # También puede ser patrón con wildcard (ej. *.bkp.md)
            if fnmatch.fnmatch(filename, pattern):
                return True
            # Opcional: si el patrón coincide con alguna parte de la ruta relativa
            # (menos común, pero útil)
            if fnmatch.fnmatch(rel_path, pattern):
                return True
    return False

def process_markdown_file(filepath, protection, base_folder):
    """Añade o actualiza la protección en un archivo Markdown."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        # Añadir nivel o contraseña
        if 'level' in protection:
            post['level'] = protection['level']
        elif 'password' in protection:
            post['password'] = protection['password']
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        print(f"✅ Procesado: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error en {filepath}: {e}")
        return False

def main():
    protections = load_config()
    if not protections:
        print("No hay carpetas configuradas. Nada que hacer.")
        return

    total_processed = 0
    for rule in protections:
        # Verificar si la regla está habilitada (por defecto true)
        if not rule.get('enabled', True):
            print(f"⏩ Regla deshabilitada (enabled: false): {rule.get('folder')}")
            continue

        folder = rule.get('folder')
        if not folder:
            print("⚠️ Regla sin carpeta, saltando.")
            continue

        # Construir ruta absoluta
        if folder.startswith('docs/'):
            target_dir = folder
        else:
            target_dir = os.path.join(DOCS_DIR, folder)

        if not os.path.isdir(target_dir):
            print(f"⚠️ Carpeta no existe: {target_dir}")
            continue

        exclude_list = rule.get('exclude', [])
        print(f"\n📁 Procesando carpeta: {target_dir}")
        if exclude_list:
            print(f"   Excluyendo: {exclude_list}")

        # Recorrer todos los archivos .md dentro de la carpeta (recursivo)
        md_files = list(Path(target_dir).rglob('*.md'))
        for md_file in md_files:
            file_path_str = str(md_file)
            # Comprobar exclusión
            if is_excluded(file_path_str, exclude_list, target_dir):
                print(f"⏩ Excluido: {file_path_str}")
                continue
            if process_markdown_file(file_path_str, rule, target_dir):
                total_processed += 1

    print(f"\n✅ Proceso completado. {total_processed} archivos procesados.")

if __name__ == "__main__":
    main()
