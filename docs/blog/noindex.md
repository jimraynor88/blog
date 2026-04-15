
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
## [{{ post.title }}]({{ post.url }})

*{{ date }}*  
{{ post.meta.description | default('') }}

{% if post.meta.tags %}
**Etiquetas:**  
{% for tag in post.meta.tags %}
  [{{ tag }}](/blog/tags/{{ tag | lower | replace(' ', '-') }}/) 
{% endfor %}
{% endif %}

---

{% endfor %}
