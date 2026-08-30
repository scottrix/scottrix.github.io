#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from pathlib import Path

BASE = Path('/home/scott/src')

# Load A-Level subjects data
with open(BASE / 'alevelrevise' / 'subjects.json') as f:
    data = json.load(f)

subjects = data['subjects']
for s in subjects:
    if 'slug' not in s:
        s['slug'] = s['name'].lower().replace(' ', '-')

# Subject landing pages are built cleanly from subjects.json by the dedicated
# generator (which handles per-board + single-topic legacy subjects and emits
# correct canonical/og URLs). Run it here so a full regenerate keeps every
# landing page in sync.
script = Path(__file__).parent / 'generate_alevel_subject_pages.py'
subprocess.check_call([sys.executable, str(script)])
print("Subject pages generated")

# Update categories for index
categories = {
    'Core': ['Mathematics', 'Further Mathematics', 'English Literature', 'English Language'],
    'Sciences': ['Biology', 'Chemistry', 'Physics', 'Computer Science'],
    'Social Sciences': ['Economics', 'Psychology', 'Sociology', 'Politics', 'Law', 'Business Studies'],
    'Humanities': ['History', 'Geography', 'Religious Studies', 'Philosophy'],
    'Languages': ['French', 'Spanish', 'German', 'Latin'],
    'Creative & Physical': ['Art and Design', 'Music', 'Drama and Theatre', 'Media Studies', 'Physical Education'],
    'Other': ['Accounting']
}

# Regenerate index with new categories
index_path = BASE / 'alevelrevise' / 'index.html'
content = index_path.read_text(encoding='utf-8')

# Ensure we have the latest subject data for the index cards
# (using the subjects list created earlier)
# Map slugs for the links
subject_slugs = {s['name']: s['slug'] for s in subjects}

subjects_html = []
for cat, subjs in categories.items():
    cards = []
    for s in subjs:
        slug = subject_slugs.get(s, s.lower().replace(' ', '-').replace('&', '').replace('–', ''))
        cards.append(f'            <a href="{slug}.html" class="subject-card" data-category="{cat}"><span class="subject-name">{s}</span></a>')
    subjects_html.append(f'''        <div class="subject-category" data-category="{cat}">
          <h3 class="category-heading">{cat}</h3>
          <div class="category-subjects">
{chr(10).join(cards)}
          </div>
        </div>''')

new_grid = '\n'.join(subjects_html)

pattern = r'(<div id="subjects-grid" class="subjects-grid">).*?(</div>\s*</section>\s*<section class="site-section" id="about")'
replacement = f'<div id="subjects-grid" class="subjects-grid">\n{new_grid}\n          </div>\n        </section>\n        <section class="site-section" id="about"'
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Update category tabs
tabs_pattern = r'(<div class="category-tabs">).*?(</div>)'
tabs_replacement = '''<div class="category-tabs">
                <button class="category-tab active" data-category="all">All</button>
                <button class="category-tab" data-category="Core">Core</button>
                <button class="category-tab" data-category="Sciences">Sciences</button>
                <button class="category-tab" data-category="Social Sciences">Social Sciences</button>
                <button class="category-tab" data-category="Humanities">Humanities</button>
                <button class="category-tab" data-category="Languages">Languages</button>
                <button class="category-tab" data-category="Creative & Physical">Creative & Physical</button>
                <button class="category-tab" data-category="Other">Other</button>
            </div>'''
content = re.sub(tabs_pattern, tabs_replacement, content, flags=re.DOTALL)

# Update hero stats
content = re.sub(r'<span class="stat-number">12</span>', '<span class="stat-number">28</span>', content)
content = re.sub(r'<span class="stat-number">300\+</span>', '<span class="stat-number">1000+</span>', content)

# Write updated index for both sites
for site in ['alevelrevise', 'alevellessons']:
    site_index = BASE / site / 'index.html'
    site_index.write_text(content, encoding='utf-8')
    print(f'Updated {site_index}')

print("All pages regenerated")