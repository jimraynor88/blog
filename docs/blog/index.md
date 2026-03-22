# Blog

## Depuración

- Número total de archivos: {{ files|length }}

Archivos en blog/posts/:
{% for f in files %}
  {% if f.src_path.startswith('blog/posts/') %}
    - {{ f.src_path }}
  {% endif %}
{% endfor %}
