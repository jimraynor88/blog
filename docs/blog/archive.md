# Archivo por años

{% set years = {} %}
{% for file in pages %}
  {% if file.src_path.startswith('blog/posts/') %}
    {% set page = file.page %}
    {% if page.meta.date %}
      {% set year = page.meta.date[:4] %}
      {% if year not in years %}
        {% set _ = years.update({year: []}) %}
      {% endif %}
      {% set _ = years[year].append(page) %}
    {% endif %}
  {% endif %}
{% endfor %}

{% for year, posts in years|sort(reverse=true) %}
## {{ year }}

{% for post in posts|sort(attribute='meta.date', reverse=true) %}
- [{{ post.title }}]({{ post.canonical_url }}) ({{ post.meta.date }})
{% endfor %}

{% endfor %}
