# Blog

## Depuración

- Número total de archivos: {{ files|length }}

Archivos en blog/posts/:
{% for f in files %}
  {% if f.src_path.startswith('blog/posts/') %}
    - {{ f.src_path }}
  {% endif %}
{% endfor %}
---

# Blog

{% set posts = [] %}
{% for f in files %}
  {% if f.src_path.startswith('blog/posts/') %}
    {% if f.page and f.page.meta and f.page.meta.date %}
      {% set _ = posts.append((f.page.meta.date, f)) %}
    {% endif %}
  {% endif %}
{% endfor %}

{% if posts|length == 0 %}
No hay posts aún.
{% else %}
{% for date, f in posts|sort(reverse=true) %}
- **{{ date }}** – [{{ f.page.title or f.name }}]({{ f.url }})
{% endfor %}
{% endif %}
