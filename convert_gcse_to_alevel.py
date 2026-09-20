#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path

BASE = Path('/home/scott/src/scottrix.github.io')

# Directories to process
dirs = ['alevelrevise', 'alevellessons']

# Replacements for text content
replacements = [
    (r'GCSE Revise', 'A-Level Revise'),
    (r'GCSE Revision', 'A-Level Revision'),
    (r'GCSE Mathematics', 'A-Level Mathematics'),
    (r'GCSE (Revise|Revision)', r'A-Level \1'),
    (r'gcserevise', 'alevelrevise'),
    (r'GCSE', 'A-Level'),
    (r'gcserevise@scott\.scottrix\.co\.uk', 'alevelrevise@scott.scottrix.co.uk'),
    (r'9-1', 'A-Level'),
    (r'Grades? 1-5', 'Grades A-E'),
    (r'Grades? 4-9', 'Grades A*-E'),
    (r'Foundation', 'Foundation'),
    (r'Higher', 'Higher'),
    (r'Eduqas', 'WJEC'),
    (r'37 Subjects', '12 Subjects'),
    (r'5 Exam Boards', '5 Exam Boards'),
    (r'600\+ Topics', '300+ Topics'),
    (r'97 topics', '300+ topics'),
    (r'All exam boards', 'All exam boards'),
    (r'Free GCSE Revision Notes', 'Free A-Level Revision Notes'),
    (r'Comprehensive GCSE revision notes', 'Comprehensive A-Level revision notes'),
    (r'Free GCSE Mathematics revision notes', 'Free A-Level Mathematics revision notes'),
    (r'GCSE Maths', 'A-Level Maths'),
    (r'GCSE Science', 'A-Level Science'),
]

# URL/path replacements
url_replacements = [
    (r'https://scottrix\.github\.io/gcserevise/', 'https://scottrix.github.io/alevelrevise/'),
    (r'gcserevise/', 'alevelrevise/'),
    (r'href="/', 'href="../'),
    (r'href="./', 'href="'),
    (r'src="FM Billboard', 'src="../FM Billboard'),
    (r'src="dynadot-banner', 'src="../dynadot-banner'),
    (r'src="fastmail_icon', 'src="../fastmail_icon'),
    (r'src="amazon-smile', 'src="../amazon-smile'),
    (r'href="mailto:gcserevise@', 'href="mailto:alevelrevise@'),
]

def process_file(filepath):
    try:
        content = filepath.read_text(encoding='utf-8')
        original = content
        
        # Apply text replacements
        for pattern, repl in replacements:
            content = re.sub(pattern, repl, content, flags=re.IGNORECASE)
        
        # Apply URL replacements
        for pattern, repl in url_replacements:
            content = re.sub(pattern, repl, content)
        
        # Fix canonical URLs
        content = re.sub(r'https://scottrix\.github\.io/gcserevise/', 'https://scottrix.github.io/alevelrevise/', content)
        content = re.sub(r'https://scottrix\.github\.io/alevellessons/', 'https://scottrix.github.io/alevellessons/', content)
        
        # Fix logo link
        content = re.sub(r'<a href="/" class="logo">', '<a href="../index.html" class="logo">', content)
        content = re.sub(r'<a href="/">', '<a href="../index.html">', content)
        
        if content != original:
            filepath.write_text(content, encoding='utf-8')
            return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    return False

# Process all HTML files in both directories
for d in dirs:
    for html_file in (BASE / d).rglob('*.html'):
        process_file(html_file)

# Process JS files
for d in dirs:
    for js_file in (BASE / d).rglob('*.js'):
        process_file(js_file)

# Process CSS
for d in dirs:
    for css_file in (BASE / d).rglob('*.css'):
        process_file(css_file)

# Update subjects.json for alevelrevise
subjects_data = {
    "subjects": [
        {"name": "Mathematics", "slug": "mathematics"},
        {"name": "Further Mathematics", "slug": "further-mathematics"},
        {"name": "Biology", "slug": "biology"},
        {"name": "Chemistry", "slug": "chemistry"},
        {"name": "Physics", "slug": "physics"},
        {"name": "Computer Science", "slug": "computer-science"},
        {"name": "Economics", "slug": "economics"},
        {"name": "Psychology", "slug": "psychology"},
        {"name": "History", "slug": "history"},
        {"name": "Geography", "slug": "geography"},
        {"name": "English Literature", "slug": "english-literature"},
        {"name": "Business Studies", "slug": "business-studies"},
    ]
}

for d in ['alevelrevise', 'alevellessons']:
    (BASE / d / 'subjects.json').write_text(json.dumps(subjects_data, indent=2))

print("Conversion complete")