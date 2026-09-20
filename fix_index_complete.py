#!/usr/bin/env python3
import json
import re
from pathlib import Path

BASE = Path('/home/scott/src/scottrix.github.io')

# Load subjects
with open(BASE / 'alevelrevise' / 'subjects.json') as f:
    data = json.load(f)

subjects = data['subjects']

# Build category mapping from subjects.json (slug -> category)
subject_to_category = {}
for s in subjects:
    name = s['name']
    slug = s['slug']
    if name in ['Mathematics', 'Further Mathematics', 'English Literature', 'English Language']:
        subject_to_category[name] = ('Core', slug)
    elif name in ['Biology', 'Chemistry', 'Physics', 'Computer Science']:
        subject_to_category[name] = ('Sciences', slug)
    elif name in ['Economics', 'Psychology', 'Sociology', 'Politics', 'Law', 'Business Studies']:
        subject_to_category[name] = ('Social Sciences', slug)
    elif name in ['History', 'Geography', 'Religious Studies', 'Philosophy']:
        subject_to_category[name] = ('Humanities', slug)
    elif name in ['French', 'Spanish', 'German', 'Latin']:
        subject_to_category[name] = ('Languages', slug)
    elif name in ['Art and Design', 'Music', 'Drama and Theatre', 'Media Studies', 'Physical Education']:
        subject_to_category[name] = ('Creative & Physical', slug)
    elif name in ['Accounting']:
        subject_to_category[name] = ('Other', slug)

# Categories in order
categories_order = ['Core', 'Sciences', 'Social Sciences', 'Humanities', 'Languages', 'Creative & Physical', 'Other']

# Build the new subjects section
subjects_html_parts = []
for cat in categories_order:
    cards = []
    for name, (cat_name, slug) in subject_to_category.items():
        if cat_name == cat:
            cards.append(f'            <a href="{slug}.html" class="subject-card" data-category="{cat}"><span class="subject-name">{name}</span></a>')
    if cards:
        subjects_html_parts.append(f'''        <div class="subject-category" data-category="{cat}">
          <h3 class="category-heading">{cat}</h3>
          <div class="category-subjects">
{chr(10).join(cards)}
          </div>
        </div>''')

new_subjects_section = f'''        <section id="subjects" class="subjects">
            <h2>Browse by Subject</h2>
            <div class="category-tabs">
                <button class="category-tab active" data-category="all">All</button>
                <button class="category-tab" data-category="Core">Core</button>
                <button class="category-tab" data-category="Sciences">Sciences</button>
                <button class="category-tab" data-category="Social Sciences">Social Sciences</button>
                <button class="category-tab" data-category="Humanities">Humanities</button>
                <button class="category-tab" data-category="Languages">Languages</button>
                <button class="category-tab" data-category="Creative & Physical">Creative & Physical</button>
                <button class="category-tab" data-category="Other">Other</button>
            </div>
      <div id="subjects-grid" class="subjects-grid">
{chr(10).join(subjects_html_parts)}
      </div>
        </section>'''

# Read current index
index_path = BASE / 'alevelrevise' / 'index.html'
content = index_path.read_text(encoding='utf-8')

# Replace the entire subjects section
pattern = r'(<section id="subjects" class="subjects">).*?(</section>\s*<section id="about" class="about">)'
replacement = new_subjects_section + '\n        <section id="about" class="about">'
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Also fix exam boards section
boards_html = '''        <section id="exam-boards" class="exam-boards">
            <h2>Supported Exam Boards</h2>
            <div class="board-grid">
                <div class="board-card" data-board="AQA">
                    <h3>AQA</h3>
                    <p>Assessment and Qualifications Alliance</p>
                    <span class="subject-count">28 subjects</span>
                </div>
                <div class="board-card" data-board="Edexcel">
                    <h3>Edexcel</h3>
                    <p>Pearson Edexcel</p>
                    <span class="subject-count">28 subjects</span>
                </div>
                <div class="board-card" data-board="OCR">
                    <h3>OCR</h3>
                    <p>Oxford, Cambridge and RSA</p>
                    <span class="subject-count">28 subjects</span>
                </div>
                <div class="board-card" data-board="WJEC">
                    <h3>WJEC</h3>
                    <p>Welsh Joint Education Committee</p>
                    <span class="subject-count">28 subjects</span>
                </div>
                <div class="board-card" data-board="CCEA">
                    <h3>CCEA</h3>
                    <p>Council for the Curriculum, Examinations & Assessment</p>
                    <span class="subject-count">28 subjects</span>
                </div>
            </div>
        </section>'''

boards_pattern = r'(<section id="exam-boards" class="exam-boards">).*?(</section>)'
content = re.sub(boards_pattern, boards_html, content, flags=re.DOTALL)

# Update hero stats
content = re.sub(r'<span class="stat-number">\d+</span>', '<span class="stat-number">28</span>', content, count=1)
content = re.sub(r'<span class="stat-number">\d+\+</span>', '<span class="stat-number">1000+</span>', content, count=1)

# Write for both sites
for site in ['alevelrevise', 'alevellessons']:
    site_index = BASE / site / 'index.html'
    site_index.write_text(content, encoding='utf-8')
    print(f'Updated {site_index}')

print("Index completely fixed")