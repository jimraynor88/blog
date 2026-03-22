# Blog

{% set posts = [] %}
{% for f in files %}
  {% if f.src_path.startswith('blog/posts/') %}
    {% set post = f.page %}
    {% if post.meta.date %}
      {% set _ = posts.append((post.meta.date, post)) %}
    {% endif %}
  {% endif %}
{% endfor %}

{% for date, post in posts|sort(reverse=true) %}
- **{{ date }}** – [{{ post.title }}]({{ post.url }})
{% endfor %}
