#!/usr/bin/env python3
"""Regenerate A-Level subject landing pages from subjects.json.

Builds a clean landing page for every subject directly from subjects.json
(not by string-patching a template -- that approach produced stale/broken
pages with the wrong sidebar and copy-pasted canonical tags). Covers both the
per-board generated subjects and the single-topic legacy subjects.
"""
import html as html_mod
import json
import re
from pathlib import Path

BASE = Path('/home/scott/src')

SITES = {
    'alevelrevise': 'Revise',
    'alevellessons': 'Lessons',
}

def esc(s):
    return html_mod.escape(str(s), quote=True)

def subject_slug(name):
    return name.lower().replace(' ', '-').replace('&', '-and-').replace('–', '-').replace('/', '-')

def build_landing(subject, site, site_display):
    name = subject['name']
    subj_slug = subject['id'] or subject_slug(name)
    boards = subject.get('boards', [])
    domain = f'https://scottrix.github.io/{site}'
    canonical = f'{domain}/{subj_slug}.html'

    # Collect topics. Deduplicate by (title) but keep board info for the badge.
    topics = []
    seen_titles = set()
    for board in boards:
        bname = board.get('board', 'General')
        for topic in board.get('topics', []):
            title = topic['title']
            page = topic['page']
            key = (title, page)
            topics.append({'title': title, 'page': page, 'board': bname})
            seen_titles.add(title)

    total_topics = len(topics)
    unique_titles = sorted({t['title'] for t in topics})

    # Sidebar: unique topics (dedup titles so a 5-board subject lists each topic once).
    sidebar_by_title = {}
    for t in topics:
        sidebar_by_title.setdefault(t['title'], t)
    sidebar_items = ''.join(
        f'<li><a href="{esc(t["page"])}">{esc(title)}</a></li>'
        for title, t in sidebar_by_title.items()
    )

    # Group by first word (strand) for the topics-grid sections.
    grouped = {}
    for t in topics:
        key = t['title'].split()[0]
        grouped.setdefault(key, []).append(t)

    sections = []
    for strand in sorted(grouped, key=lambda k: k.lower()):
        cards = ''.join(
            f'<a href="{esc(t["page"])}" class="topic-card"><span class="topic-name">{esc(t["title"])}</span></a>'
            for t in grouped[strand]
        )
        sections.append(
            f'<section id="{re.sub(r"[^a-z0-9-]", "", strand.lower())}" class="section">\n'
            f'<h2>{esc(strand)} ({len(grouped[strand])} topic{"s" if len(grouped[strand]) != 1 else ""})</h2>\n'
            f'<div class="topics-grid">{cards}</div>\n'
            f'</section>'
        )

    sections_html = '\n'.join(sections)
    topic_desc = (f'Free A-Level {name} revision notes. {total_topics} topics '
                  f'across AQA, Edexcel, OCR, WJEC, and CCEA specifications.')

    title = f'A-Level {name} - Free {site_display} Notes'

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script>/* gcanonical-redirect */(function(){{var p=location.pathname,q=location.search,h=location.hash,m=/^(.*)\\/index\\.html$/.exec(p);if(m){{location.replace(m[1]+"/"+q+h);return}}if(!p.endsWith("/")&&!/\\.[a-z0-9]{{1,10}}$/i.test(p)){{location.replace(p+".html"+q+h)}}}})();</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(topic_desc)}">
<meta name="keywords" content="A-Level {esc(name)}, {esc(name)} revision notes, past papers, AQA, Edexcel, OCR, WJEC, CCEA">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(topic_desc)}">
<meta property="og:type" content="article">
<meta property="og:url" content="{esc(canonical)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:site_name" content="A-Level {site_display}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="A-Level {esc(name)}">
<meta name="twitter:description" content="{esc(topic_desc)}">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site-header">
<div class="header-content">
<a href="index.html" class="logo">📚 A-Level {site_display}</a>
<nav class="nav">
<a href="index.html#subjects">Subjects</a>
<a href="index.html">Home</a>
</nav>
<button id="theme-toggle" class="theme-btn">🌙</button>
</div>
</header>

<div class="sidebar">
  <h3>Topics</h3>
  <ul>{sidebar_items}</ul>
</div>

<div class="ad-right">
  <div class="ad-unit">Advertisement</div>
</div>

<main class="topic-content">
<div class="disclaimer-banner"><strong>A-Level Revision Aid:</strong> This resource is designed to support your revision and may contain errors. If you find a discrepancy with your class teaching, your teacher is correct — please let us know at <a href="mailto:alevelrevise@scott.scottrix.co.uk">alevelrevise@scott.scottrix.co.uk</a>.</div>

<nav class="breadcrumb">
<a href="index.html">Home</a> <span>›</span>
<span>{esc(name)}</span>
</nav>

<article class="topic-header">
<h1>📐 A-Level {esc(name)}</h1>
<div class="topic-meta">
<span class="badge foundation">Year 1 / AS</span>
<span class="badge higher">Year 2 / A-Level</span>
<span class="badge">All Boards (AQA, Edexcel, OCR, WJEC, CCEA)</span>
</div>
<p class="topic-desc">{esc(topic_desc)}</p>
</article>

<section class="section">
<h2>📊 Course Overview</h2>
<p>A-Level {esc(name)} covers {len(grouped)} topic area{"s" if len(grouped) != 1 else ""} with {total_topics} topic{"s" if total_topics != 1 else ""} total across AQA, Edexcel, OCR, WJEC, and CCEA specifications.</p>
{sections_html}
</section>
</main>
</body>
</html>
'''
    return page

def main():
    for site, display in SITES.items():
        with open(BASE / site / 'subjects.json') as f:
            data = json.load(f)
        for subject in data['subjects']:
            subj_slug = subject['id'] or subject_slug(subject['name'])
            html = build_landing(subject, site, display)
            out = BASE / site / f'{subj_slug}.html'
            out.write_text(html, encoding='utf-8')
            print(f'Generated {out}')

if __name__ == '__main__':
    main()
