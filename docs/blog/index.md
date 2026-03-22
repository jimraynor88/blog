{% set posts = [] %}
{% for file in pages %}
  {% if file.src_path.startswith('blog/posts/') %}
    {% set page = file.page %}
    {% if page.meta.date %}
      {% set _ = posts.append((page.meta.date, page)) %}
    {% endif %}
  {% endif %}
{% endfor %}

{% for date, post in posts|sort(reverse=true) %}
- **{{ date }}** – [{{ post.title }}]({{ post.canonical_url }})
{% endfor %}
