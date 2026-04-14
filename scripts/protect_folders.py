#!/usr/bin/env python3
"""
Protege múltiples carpetas con diferentes niveles o contraseñas.
Lee la configuración desde protect_config.yml.
"""
import os
import sys
import yaml
import frontmatter
from pathlib import Path

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

def process_markdown_file(filepath, protection):
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
        folder = rule.get('folder')
        if not folder:
            print("⚠️ Regla sin carpeta, saltando.")
            continue
        # Construir ruta absoluta relativa a DOCS_DIR si la carpeta empieza con 'docs/'
        if folder.startswith('docs/'):
            target_dir = folder
        else:
            target_dir = os.path.join(DOCS_DIR, folder)
        
        if not os.path.isdir(target_dir):
            print(f"⚠️ Carpeta no existe: {target_dir}")
            continue
        
        print(f"\n📁 Procesando carpeta: {target_dir}")
        # Recorrer todos los archivos .md dentro de la carpeta (recursivo)
        md_files = list(Path(target_dir).rglob('*.md'))
        for md_file in md_files:
            process_markdown_file(str(md_file), rule)
            total_processed += 1
    
    print(f"\n✅ Proceso completado. {total_processed} archivos procesados.")

if __name__ == "__main__":
    main()
