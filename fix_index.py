#!/usr/bin/env python3
import json
import re
from pathlib import Path

BASE = Path('/home/scott/src/scottrix.github.io')

# Load subjects
with open(BASE / 'alevelrevise' / 'subjects.json') as f:
    data = json.load(f)

subjects = data['subjects']

# Build category mapping from subjects
categories = {
    'Core': ['Mathematics', 'Further Mathematics', 'English Literature', 'English Language'],
    'Sciences': ['Biology', 'Chemistry', 'Physics', 'Computer Science'],
    'Social Sciences': ['Economics', 'Psychology', 'Sociology', 'Politics', 'Law', 'Business Studies'],
    'Humanities': ['History', 'Geography', 'Religious Studies', 'Philosophy'],
    'Languages': ['French', 'Spanish', 'German', 'Latin'],
    'Creative & Physical': ['Art and Design', 'Music', 'Drama and Theatre', 'Media Studies', 'Physical Education'],
    'Other': ['Accounting']
}

# Read current index template
index_path = BASE / 'alevelrevise' / 'index.html'
content = index_path.read_text(encoding='utf-8')

# Build new subjects grid from subjects.json
subjects_html = []
for cat, subjs in categories.items():
    cards = []
    for s in subjs:
        # Find the slug from subjects.json
        slug = None
        for subj in subjects:
            if subj['name'] == s:
                slug = subj['slug']
                break
        if slug:
            cards.append(f'            <a href="{slug}.html" class="subject-card" data-category="{cat}"><span class="subject-name">{s}</span></a>')
    if cards:
        subjects_html.append(f'''        <div class="subject-category" data-category="{cat}">
          <h3 class="category-heading">{cat}</h3>
          <div class="category-subjects">
{chr(10).join(cards)}
          </div>
        </div>''')

new_grid = '\n'.join(subjects_html)

# Replace the subjects grid section
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
content = re.sub(r'<span class="stat-number">\d+</span>', '<span class="stat-number">28</span>', content, count=1)
content = re.sub(r'<span class="stat-number">\d+\+</span>', '<span class="stat-number">1000+</span>', content, count=1)

# Update exam boards section
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

# Write updated index for both sites
for site in ['alevelrevise', 'alevellessons']:
    site_index = BASE / site / 'index.html'
    site_index.write_text(content, encoding='utf-8')
    print(f'Updated {site_index}')

print("Index pages fixed")