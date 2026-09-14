---
layout: default
title: Working papers
permalink: /research/
---

<div class="entries">
{% for w in site.data.working_papers %}
  <article class="entry">
    <div class="year">{{ w.status }}</div>
    <div>
      <h2 class="title">{{ w.title }}</h2>
      {% if w.authors %}<p class="authors">{{ w.authors }}</p>{% endif %}
      {% if w.pdf %}
      <div class="links"><a href="{{ w.pdf | relative_url }}">PDF</a></div>
      {% endif %}
      {% if w.abstract %}
      <details class="abstract">
        <summary>Abstract</summary>
        <p>{{ w.abstract }}</p>
      </details>
      {% endif %}
    </div>
  </article>
{% endfor %}
</div>
