# Archivo por años

{% set posts_by_year = {} %}
{% for f in files %}
  {% if f.src_path.startswith('blog/posts/') %}
    {% set post = f.page %}
    {% if post.meta.date %}
      {% set year = post.meta.date[:4] %}
      {% if year not in posts_by_year %}
        {% set _ = posts_by_year.update({year: []}) %}
      {% endif %}
      {% set _ = posts_by_year[year].append(post) %}
    {% endif %}
  {% endif %}
{% endfor %}

{% for year in posts_by_year|sort(reverse=true) %}
## {{ year }}

{% for post in posts_by_year[year]|sort(attribute='meta.date', reverse=true) %}
- [{{ post.title }}]({{ post.url }}) ({{ post.meta.date }})
{% endfor %}

{% endfor %}
