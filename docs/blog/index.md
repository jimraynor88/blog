# Blog

## Depuración (quitar después)
Número de archivos en blog/posts: 
{% set posts_files = [] %}
{% for f in files %}
  {% if f.src_path.startswith('blog/posts/') %}
    {% set _ = posts_files.append(f) %}
  {% endif %}
{% endfor %}
{{ posts_files|length }}

### Metadatos del primer archivo (si existe):
{% if posts_files|length > 0 %}
  {% set sample = posts_files[0] %}
  - Ruta: {{ sample.src_path }}
  - Page meta: {{ sample.page.meta }}
  - Page title: {{ sample.page.title }}
  - Page meta.title: {{ sample.page.meta.title }}
  - Page meta.date: {{ sample.page.meta.date }}
{% else %}
No se encontraron archivos en blog/posts.
{% endif %}

---

# Lista de posts

{% set posts = [] %}
{% for f in files %}
  {% if f.src_path.startswith('blog/posts/') and f.page %}
    {% set meta = f.page.meta %}
    {% if meta and meta.date %}
      {% set _ = posts.append((meta.date, f)) %}
    {% endif %}
  {% endif %}
{% endfor %}

{% if posts|length == 0 %}
No hay posts con fecha válida. Asegúrate de que cada post tenga una línea `date: YYYY-MM-DD` en su frontmatter.
{% else %}
{% for date, f in posts|sort(reverse=true) %}
- **{{ date }}** – [{{ f.page.meta.title or f.page.title or f.name }}]({{ f.url }})
{% endfor %}
{% endif %}
