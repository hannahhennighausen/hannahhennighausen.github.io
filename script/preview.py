#!/usr/bin/env python3
"""Minimal local preview renderer.

GitHub Pages builds this site with Jekyll. This script mimics just enough of the
Liquid layout to render static preview files for visual checks when Jekyll is not
installed. It writes into _preview/ and is not part of the published site.
"""
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "_preview"
OUT.mkdir(exist_ok=True)

cfg = yaml.safe_load((ROOT / "_config.yml").read_text())
pubs = yaml.safe_load((ROOT / "_data/publications.yml").read_text())
wps = yaml.safe_load((ROOT / "_data/working_papers.yml").read_text())

css = (ROOT / "assets/css/style.scss").read_text().split("---", 2)[-1]
# crude SCSS nesting flatten for preview only
def flatten(scss: str) -> str:
    out, stack = [], []
    for raw in scss.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.endswith("{"):
            sel = line[:-1].strip()
            if stack:
                parent = stack[-1]
                if sel.startswith("&"):
                    sel = parent + sel[1:]
                else:
                    sel = " ".join([parent, sel])
            stack.append(sel)
            out.append(sel + " {")
            continue
        if line == "}":
            stack.pop()
            out.append("}")
            continue
        out.append("  " + line)
    # remove empty rules
    text = "\n".join(out)
    return re.sub(r"[^{}]+\{\s*\}", "", text)

css = flatten(css)

NAV = cfg.get("nav", [])


def shell(title, body, here=""):
    nav = "".join(
        f'<a href="#" class="{"here" if n["url"] == here else ""}">{n["title"]}</a>'
        for n in NAV
    ) + '<a href="#">CV (PDF)</a>'
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Public+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{css}</style></head><body>
<div class="shell">
<aside class="sidebar">
  <a class="brand" href="#"><img class="portrait" src="../assets/img/me2026.jpg" alt=""><span class="brand-name">{cfg['title']}</span></a>
  <p class="role">{cfg["title_line"]}<br>{cfg["institution"]}</p>
  <nav class="nav">{nav}</nav>
  <div class="contact"><p>{cfg['email']}</p><p>{cfg['office']}</p><p>{cfg['phone']}</p></div>
</aside>
<main class="content">{body}</main>
</div>
<footer class="foot"><p>{cfg['title']} · {cfg['institution']}</p></footer>
</body></html>"""


def entries(items, kind):
    rows = []
    for it in items:
        left = it.get("year") or it.get("status") or "Draft"
        award = f'<span class="award">{it["award"]}</span>' if it.get("award") else ""
        links = []
        if it.get("link"):
            links.append('<a href="#">Journal</a>')
        if it.get("pdf"):
            links.append('<a href="#">PDF</a>')
        linkhtml = f'<div class="links">{"".join(links)}</div>' if links else ""
        authors = f'<p class="authors">{it["authors"]}</p>' if it.get("authors") else ""
        venue = f'<p class="venue">{it["venue"]}</p>' if it.get("venue") else ""
        rows.append(f"""<article class="entry"><div class="year">{left}</div><div>
<h2 class="title">{it['title']}</h2>{authors}{venue}{award}{linkhtml}
<details class="abstract"><summary>Abstract</summary><p>{it.get('abstract','')}</p></details>
</div></article>""")
    return f'<div class="entries">{"".join(rows)}</div>'


home = f"""<img class="banner" src="../assets/img/mountains3.jpeg" alt="">
<p>I am an Associate Professor in the <a href="#">Department of Economics</a> at the University of Alaska Anchorage.</p>
<p>My research examines how individuals, markets and communities respond and adapt to changing environmental risks, and how public policies and institutions shape these responses. My work focuses on natural hazards, including floods, hurricanes, wildfires and landslides.</p>
<p>You can contact me at <a href="#">{cfg['email']}</a>.</p>
<p><a href="#">My CV is here.</a></p>
<figure><img src="../assets/img/mountains2.jpeg" alt=""></figure>"""

(OUT / "index.html").write_text(shell("Home", home, "/"))
(OUT / "publications.html").write_text(
    shell("Publications",
          '<h1 class="page-title">Publications</h1>' + entries(pubs, "pub"), "/publications/"))
(OUT / "research.html").write_text(
    shell("Working papers",
          '<h1 class="page-title">Working papers</h1>' + entries(wps, "wp"), "/research/"))

courses = [("2026","Environmental Economics","Instructor \u00b7 University of Alaska Anchorage"),
("2022\u20132027","Statistics for Business and Economics","Instructor \u00b7 University of Alaska Anchorage"),
("2025, 2026","Principles of Macroeconomics","Instructor \u00b7 University of Alaska Anchorage"),
("2020, 2021, 2027","Principles of Microeconomics","Instructor \u00b7 University of Alaska Anchorage"),
("2019","Quantitative Methods in Economic Research","Co-instructor \u00b7 University of Graz"),
("2016","Principles of Microeconomics","Co-instructor \u00b7 University of Graz")]

teach_html = '<div class="entries">' + "".join(
    f'<article class="entry"><div class="year">{y}</div><div><h2 class="title">{t}</h2><p class="authors">{w}</p></div></article>'
    for y, t, w in courses) + '</div>'
(OUT / "teaching.html").write_text(shell("Teaching", '<h1 class="page-title">Teaching</h1>' + teach_html, "/teaching/"))

names = ["ski-tour","flightseeing","skating","ridge-walk","dipnet-river","dipnet-beach","biking"]
gal = '<div class="gallery">' + "".join(
    f'<figure><img src="../assets/img/alaska/{n}.jpg" alt=""></figure>' for n in names) + '</div>'
(OUT / "alaska.html").write_text(shell("Alaska", '<h1 class="page-title">Alaska</h1>' + gal, "/alaska/"))

print("wrote", OUT)
