#!/usr/bin/env python3
"""
Generador de índices del blog con diseño mejorado (tarjetas, extractos, etiquetas).
Lee los archivos .md de docs/blog/posts/ y genera:
- docs/blog/index.md (lista de posts en tarjetas)
- docs/blog/archive.md (archivo por años)
- docs/blog/tags.md (índice de etiquetas)
"""
import os
import re
import frontmatter
from collections import defaultdict
from datetime import datetime, date

# Mapeo de números de mes a nombres en español
MESES = {
    1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
    5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
    9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
}

def formatear_fecha(fecha, incluir_año=True):
    """Devuelve fecha en formato español: '20 de marzo de 2026' o '20 de marzo'."""
    dia = fecha.day
    mes = MESES[fecha.month]
    if incluir_año:
        año = fecha.year
        return f"{dia} de {mes} de {año}"
    else:
        return f"{dia} de {mes}"

def get_posts(posts_dir):
    """Lee todos los archivos .md de posts_dir y devuelve lista de diccionarios con metadatos y extracto."""
    posts = []
    for filename in os.listdir(posts_dir):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(posts_dir, filename)
        try:
            post = frontmatter.load(filepath)
            date_value = post.get('date')
            if not date_value:
                continue
            # Convertir fecha
            if isinstance(date_value, str):
                try:
                    date_obj = datetime.strptime(date_value, '%Y-%m-%d').date()
                except:
                    continue
            else:
                date_obj = date_value
            if not isinstance(date_obj, date):
                continue

            title = post.get('title', filename.replace('.md', ''))
            tags = post.get('tags', [])
            if isinstance(tags, str):
                tags = [tags]
            slug = filename.replace('.md', '')
            url = f"/blog/posts/{slug}/"

            # Extraer extracto: primeras líneas del contenido (sin frontmatter)
            content_text = post.content
            lines = content_text.split('\n')
            excerpt_lines = []
            for line in lines:
                if line.strip() and not line.startswith('#') and not line.startswith('!') and not line.startswith('['):
                    excerpt_lines.append(line.strip())
                if len(' '.join(excerpt_lines)) > 200:
                    break
            excerpt = ' '.join(excerpt_lines)[:250] + ('...' if len(' '.join(excerpt_lines)) > 250 else '')

            posts.append({
                'date': date_obj,
                'title': title,
                'tags': tags,
                'url': url,
                'filename': filename,
                'excerpt': excerpt
            })
        except Exception as e:
            print(f"Error leyendo {filename}: {e}")
    return posts

def write_index(posts, output_file):
    """Genera página principal del blog con tarjetas."""
    if not posts:
        print("No hay posts con fecha, no se genera índice.")
        return
    sorted_posts = sorted(posts, key=lambda p: p['date'], reverse=True)

    content = """# Blog

Últimos artículos y reflexiones.

<div class="blog-grid">
"""
    for p in sorted_posts:
        date_str = formatear_fecha(p['date'], incluir_año=True)
        tags_html = ''
        if p['tags']:
            tags_html = '<div class="blog-tags">' + ''.join(f'<span class="blog-tag">{tag}</span>' for tag in p['tags']) + '</div>'
        content += f"""
<div class="blog-card">
  <h3><a href="{p['url']}">{p['title']}</a></h3>
  <div class="blog-meta">{date_str}</div>
  {tags_html}
  <p class="blog-excerpt">{p['excerpt']}</p>
  <a href="{p['url']}" class="blog-readmore">Leer más →</a>
</div>
"""
    content += """</div>

<style>
.blog-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}
.blog-card {
    background: var(--md-default-bg-color);
    border: 1px solid var(--md-default-fg-color--lighter);
    border-radius: 8px;
    padding: 1.2rem;
    transition: transform 0.2s, box-shadow 0.2s;
}
.blog-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.1);
}
.blog-card h3 {
    margin-top: 0;
    margin-bottom: 0.5rem;
}
.blog-meta {
    font-size: 0.8rem;
    color: var(--md-default-fg-color--light);
    margin-bottom: 0.5rem;
}
.blog-tags {
    margin: 0.5rem 0;
}
.blog-tag {
    display: inline-block;
    background: var(--md-primary-fg-color--light);
    color: var(--md-primary-bg-color);
    font-size: 0.7rem;
    padding: 0.2rem 0.5rem;
    border-radius: 12px;
    margin-right: 0.3rem;
}
.blog-excerpt {
    font-size: 0.9rem;
    line-height: 1.4;
    margin-bottom: 1rem;
}
.blog-readmore {
    display: inline-block;
    font-size: 0.85rem;
    font-weight: 500;
    text-decoration: none;
    color: var(--md-primary-fg-color);
}
.blog-readmore:hover {
    text-decoration: underline;
}
</style>
"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generado {output_file}")

def write_archive(posts, output_file):
    """Genera página de archivo por años (formato compacto)."""
    if not posts:
        return
    by_year = defaultdict(list)
    for p in posts:
        by_year[p['date'].year].append(p)

    content = """# Archivo por años

"""
    for year in sorted(by_year.keys(), reverse=True):
        content += f"## {year}\n\n"
        sorted_posts = sorted(by_year[year], key=lambda p: p['date'], reverse=True)
        for p in sorted_posts:
            date_str = formatear_fecha(p['date'], incluir_año=False)
            content += f"- **{date_str}** – [{p['title']}]({p['url']})\n"
        content += "\n"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generado {output_file}")

def write_tags(posts, output_file):
    """Genera índice de etiquetas con listado de posts."""
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
            date_str = formatear_fecha(p['date'], incluir_año=True)
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
    write_archive(posts, 'docs/blog/posts/index.md')
    write_tags(posts, 'docs/blog/tags.md')

if __name__ == '__main__':
    main()
