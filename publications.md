---
layout: default
title: Publications
permalink: /publications/
---

<div class="entries">
{% for p in site.data.publications %}
  <article class="entry">
    <div class="year">{{ p.year }}</div>
    <div>
      <h2 class="title">{{ p.title }}</h2>
      <p class="authors">{{ p.authors }}</p>
      <p class="venue">{{ p.venue }}</p>
      {% if p.award %}<span class="award">{{ p.award }}</span>{% endif %}
      <div class="links">
        {% if p.link %}<a href="{{ p.link }}">Journal</a>{% endif %}
        {% if p.pdf %}<a href="{{ p.pdf | relative_url }}">PDF</a>{% endif %}
      </div>
      {% if p.abstract %}
      <details class="abstract">
        <summary>Abstract</summary>
        <p>{{ p.abstract }}</p>
      </details>
      {% endif %}
    </div>
  </article>
{% endfor %}
</div>
