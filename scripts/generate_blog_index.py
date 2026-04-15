#!/usr/bin/env python3
import os
import re
import frontmatter
from collections import defaultdict
from datetime import datetime, date

def get_posts(posts_dir):
    """Lee todos los archivos .md de posts_dir y devuelve lista de diccionarios con metadatos."""
    posts = []
    for filename in os.listdir(posts_dir):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(posts_dir, filename)
        try:
            post = frontmatter.load(filepath)
            # Obtener fecha: puede ser string o date
            date_value = post.get('date')
            if not date_value:
                continue
            # Convertir a datetime si es string
            if isinstance(date_value, str):
                try:
                    # Asumimos formato YYYY-MM-DD
                    date_obj = datetime.strptime(date_value, '%Y-%m-%d').date()
                except:
                    # Si falla, intentamos otro formato o saltamos
                    continue
            else:
                date_obj = date_value
            # Asegurar que es date
            if not isinstance(date_obj, date):
                continue
            title = post.get('title', filename.replace('.md', ''))
            tags = post.get('tags', [])
            if isinstance(tags, str):
                tags = [tags]
            slug = filename.replace('.md', '')
            url = f"/blog/posts/{slug}/"
            posts.append({
                'date': date_obj,
                'title': title,
                'tags': tags,
                'url': url,
                'filename': filename
            })
        except Exception as e:
            print(f"Error leyendo {filename}: {e}")
    return posts

def write_index(posts, output_file):
    if not posts:
        print("No hay posts con fecha, no se genera índice.")
        return
    sorted_posts = sorted(posts, key=lambda p: p['date'], reverse=True)
    content = """# Blog

Lista de artículos ordenados por fecha (más reciente primero):

"""
    for p in sorted_posts:
        date_str = p['date'].strftime('%Y-%m-%d')
        content += f"- **{date_str}** – [{p['title']}]({p['url']})\n"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generado {output_file}")

def write_archive(posts, output_file):
    if not posts:
        return
    by_year = defaultdict(list)
    for p in posts:
        year = p['date'].year
        by_year[year].append(p)
    content = """# Archivo por años

"""
    for year in sorted(by_year.keys(), reverse=True):
        content += f"## {year}\n\n"
        sorted_posts = sorted(by_year[year], key=lambda p: p['date'], reverse=True)
        for p in sorted_posts:
            date_str = p['date'].strftime('%Y-%m-%d')
            content += f"- **{date_str}** – [{p['title']}]({p['url']})\n"
        content += "\n"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generado {output_file}")

def write_tags(posts, output_file):
    if not posts:
        return
    by_tag = defaultdict(list)
    for p in posts:
        for tag in p['tags']:
            by_tag[tag].append(p)
    content = """# Índice de etiquetas

"""
    for tag in sorted(by_tag.keys()):
        content += f"## {tag}\n\n"
        sorted_posts = sorted(by_tag[tag], key=lambda p: p['date'], reverse=True)
        for p in sorted_posts:
            date_str = p['date'].strftime('%Y-%m-%d')
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
    write_index(posts, 'docs/blog/posts/index.md')
    write_archive(posts, 'docs/blog/archive.md')
    write_tags(posts, 'docs/blog/tags.md')

if __name__ == '__main__':
    main()
