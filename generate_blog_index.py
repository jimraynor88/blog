#!/usr/bin/env python3
"""
Generador de índices para el blog manual de Material for MkDocs.
Crea:
- blog/index.md    : lista cronológica de posts.
- blog/archive.md  : posts agrupados por año.
- blog/tags.md     : posts agrupados por etiqueta.
"""

import os
import re
import frontmatter
from collections import defaultdict
from datetime import datetime

def natural_sort_key(s):
    """Clave de ordenación natural para nombres de archivo (ej. casa_01, casa_02)."""
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', s)]

def get_posts(posts_dir):
    """Lee todos los archivos .md de posts_dir y devuelve lista de diccionarios con metadatos."""
    posts = []
    for filename in os.listdir(posts_dir):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(posts_dir, filename)
        try:
            post = frontmatter.load(filepath)
            date = post.get('date')
            if not date:
                continue   # solo posts con fecha
            title = post.get('title', filename.replace('.md', ''))
            tags = post.get('tags', [])
            if isinstance(tags, str):
                tags = [tags]
            # Crear URL del post (MkDocs genera /blog/posts/nombre/ sin extensión)
            slug = filename.replace('.md', '')
            url = f"/blog/posts/{slug}/"
            posts.append({
                'date': date,
                'title': title,
                'tags': tags,
                'url': url,
                'filename': filename
            })
        except Exception as e:
            print(f"Error leyendo {filename}: {e}")
    return posts

def write_index(posts, output_file):
    """Escribe blog/index.md con lista cronológica."""
    if not posts:
        print("No hay posts con fecha, no se genera índice.")
        return
    # Ordenar por fecha descendente (más reciente primero)
    sorted_posts = sorted(posts, key=lambda p: p['date'], reverse=True)
    content = """# Blog

Lista de artículos ordenados por fecha (más reciente primero):

"""
    for p in sorted_posts:
        # Formato de fecha: YYYY-MM-DD (se puede cambiar)
        date_str = p['date'].strftime('%Y-%m-%d') if isinstance(p['date'], datetime) else p['date']
        content += f"- **{date_str}** – [{p['title']}]({p['url']})\n"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generado {output_file}")

def write_archive(posts, output_file):
    """Escribe blog/archive.md agrupado por año."""
    if not posts:
        return
    # Agrupar por año
    by_year = defaultdict(list)
    for p in posts:
        year = p['date'].year if isinstance(p['date'], datetime) else p['date'][:4]
        by_year[year].append(p)
    content = """# Archivo por años

"""
    for year in sorted(by_year.keys(), reverse=True):
        content += f"## {year}\n\n"
        # Ordenar posts dentro del año por fecha descendente
        sorted_posts = sorted(by_year[year], key=lambda p: p['date'], reverse=True)
        for p in sorted_posts:
            date_str = p['date'].strftime('%Y-%m-%d') if isinstance(p['date'], datetime) else p['date']
            content += f"- **{date_str}** – [{p['title']}]({p['url']})\n"
        content += "\n"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generado {output_file}")

def write_tags(posts, output_file):
    """Escribe blog/tags.md con índice de etiquetas."""
    if not posts:
        return
    # Agrupar por etiqueta
    by_tag = defaultdict(list)
    for p in posts:
        for tag in p['tags']:
            by_tag[tag].append(p)
    content = """# Índice de etiquetas

"""
    for tag in sorted(by_tag.keys()):
        content += f"## {tag}\n\n"
        # Ordenar posts por fecha descendente
        sorted_posts = sorted(by_tag[tag], key=lambda p: p['date'], reverse=True)
        for p in sorted_posts:
            date_str = p['date'].strftime('%Y-%m-%d') if isinstance(p['date'], datetime) else p['date']
            content += f"- **{date_str}** – [{p['title']}]({p['url']})\n"
        content += "\n"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generado {output_file}")

def main():
    posts_dir = 'docs/blog/posts'
    if not os.path.isdir(posts_dir):
        print(f"Error: {posts_dir} no existe.")
        return
    posts = get_posts(posts_dir)
    if not posts:
        print("No se encontraron posts con fecha válida.")
        return
    write_index(posts, 'docs/blog/index.md')
    write_archive(posts, 'docs/blog/archive.md')
    write_tags(posts, 'docs/blog/tags.md')

if __name__ == '__main__':
    main()
