---
layout: default
title: Home
---

## Latest Posts

{% for post in site.posts %}
  <div class="post-item">
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <p>{{ post.excerpt }}</p>
    <a href="{{ post.url | relative_url }}" class="read-more">Read More</a>
  </div>
{% endfor %}