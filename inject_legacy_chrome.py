#!/usr/bin/env python3
"""Inject gcserevise-style chrome into legacy flat topic pages.

Adds:
  - fastmail/dynadot banner rotation after topic-header article
  - aside.ad-right sidebar with affiliate cards before </main>
  - footer.site-footer before </body>
  - theme-toggle script (if missing) before </body>
  - sidebar.js + affiliate-images.js before </body>

Runs idempotently (skips pages already containing ad-right).
"""
import json, os, re
from pathlib import Path

BASE = Path('/home/scott/src')
SITES = ['alevelrevise', 'alevellessons']

# Subject -> Amazon affiliate cards for the ad-right sidebar
AFFILIATES = {
  "mathematics": [
    ("Scientific Calculators", "scientific+calculator+A-Level", "Essential for A-Level Maths exams"),
    ("Graph Paper Pads", "graph+paper+a4+pad", "A4 squared paper for maths"),
    ("Maths Revision Guides", "A-Level+Maths+revision+guides", "CGP and other revision guides"),
  ],
  "further-mathematics": [
    ("Further Maths Guides", "A-Level+Further+Maths+revision", "Core Pure and option guides"),
    ("Graphic Calculators", "graphic+calculator+student", "CAS and graphing calculators"),
    ("Maths Revision Guides", "A-Level+Maths+revision+guides", "CGP and other revision guides"),
  ],
  "biology": [
    ("Biology Revision Guides", "A-Level+Biology+revision+guides", "CGP, Oxford, and more"),
    ("Microscope Slides", "microscope+slides+prepared", "Prepared slides for practicals"),
    ("Biology Field Guides", "A-Level+biology+fieldwork+guide", "Required practical support"),
  ],
  "chemistry": [
    ("Chemistry Revision Guides", "A-Level+Chemistry+revision+guides", "CGP, Oxford, and more"),
    ("Molecular Model Kits", "molecular+model+kit+organic", "Visualise chemical structures"),
    ("Periodic Table Posters", "periodic+table+poster+large", "Wall reference for chemistry"),
  ],
  "physics": [
    ("Physics Revision Guides", "A-Level+Physics+revision+guides", "CGP, Oxford, and more"),
    ("Data Loggers", "data+logger+physics+education", "For required practicals"),
    ("Multimeters", "digital+multimeter+student", "Essential for electricity practicals"),
  ],
  "english-literature": [
    ("Literature Study Guides", "A-Level+English+Literature+guides", "York Notes, CGP, and more"),
    ("Set Text Collections", "A-Level+English+Literature+set+texts", "Complete play/novel editions"),
    ("Annotation Sticky Notes", "sticky+notes+annotation", "For text analysis"),
  ],
  "english-language": [
    ("English Language Guides", "A-Level+English+Language+revision", "CGP, York Notes, and more"),
    ("Set Text Editions", "A-Level+English+set+texts", "Annotated editions for study"),
    ("Highlighters & Pens", "highlighter+pens+study", "For text annotation"),
  ],
  "history": [
    ("History Revision Guides", "A-Level+History+revision+guides", "Topic-specific guides"),
    ("Timeline Wall Charts", "history+timeline+poster", "Visual reference for chronology"),
    ("Source Analysis Workbooks", "A-Level+history+source+analysis", "Practice source questions"),
  ],
  "geography": [
    ("Geography Revision Guides", "A-Level+Geography+revision+guides", "CGP, Oxford, and more"),
    ("Atlas", "world+atlas+student", "Essential for map skills"),
    ("Case Study Flashcards", "A-Level+geography+case+study+cards", "Key facts for case studies"),
  ],
  "economics": [
    ("Economics Revision Guides", "A-Level+Economics+revision+guides", "Micro and macro"),
    ("Economics Textbooks", "A-Level+Economics+textbook", "Core textbooks"),
    ("Graph Paper", "economics+graph+paper+a4", "For diagrams"),
  ],
  "psychology": [
    ("Psychology Revision Guides", "A-Level+Psychology+revision+guides", "Studies, theories, methods"),
    ("Research Methods Workbooks", "psychology+research+methods+A-Level", "Experiments, ethics"),
    ("Study Cards", "psychology+flashcards+A-Level", "Key studies and theories"),
  ],
  "business-studies": [
    ("Business Revision Guides", "A-Level+Business+revision+guides", "CGP, Tutor2u, and more"),
    ("Case Study Books", "A-Level+business+case+studies", "Real business examples"),
    ("Financial Calculators", "financial+calculator+student", "For finance topics"),
  ],
  "computer-science": [
    ("CS Revision Guides", "A-Level+Computer+Science+revision", "CGP, PG Online, and more"),
    ("Python Books", "python+programming+A-Level", "Beginner to advanced Python"),
    ("Raspberry Pi Kits", "raspberry+pi+starter+kit", "For programming projects"),
  ],
  "sociology": [
    ("Sociology Revision Guides", "A-Level+Sociology+revision+guides", "Families, education, crime"),
    ("Sociology Textbooks", "A-Level+Sociology+textbook", "Core concepts and theorists"),
    ("Essay Planning Pads", "essay+planning+pad+a4", "Structure long answers"),
  ],
  "french": [
    ("French Revision Guides", "A-Level+French+revision+guides", "AQA, Edexcel, Eduqas"),
    ("French Dictionaries", "french+english+dictionary+student", "Collins, Oxford, Larousse"),
    ("Verb Conjugation Books", "french+verb+conjugation+guide", "Bescherelle and alternatives"),
  ],
  "spanish": [
    ("Spanish Revision Guides", "A-Level+Spanish+revision+guides", "AQA, Edexcel, Eduqas"),
    ("Spanish Dictionaries", "spanish+english+dictionary+student", "Collins, Oxford, Larousse"),
    ("Verb Practice Books", "spanish+verb+practice+A-Level", "Conjugation drills"),
  ],
  "german": [
    ("German Revision Guides", "A-Level+German+revision+guides", "AQA, Edexcel, Eduqas"),
    ("German Dictionaries", "german+english+dictionary+student", "Collins, Oxford, Langenscheidt"),
    ("Grammar Workbooks", "german+grammar+workbook+A-Level", "Cases, word order, verbs"),
  ],
  "latin": [
    ("Latin Revision Guides", "A-Level+Latin+revision+guides", "OCR, Eduqas, Edexcel"),
    ("Latin Dictionaries", "latin+dictionary+student", "Pocket Oxford, Cassell's"),
    ("Set Text Editions", "A-Level+Latin+set+texts+edition", "Annotated Virgil, Cicero"),
  ],
  "art-and-design": [
    ("Art Sketchbooks", "A3+sketchbook+art+student", "Quality paper for portfolio"),
    ("Drawing Pencils Set", "drawing+pencils+graphite+set", "2H to 8B range"),
    ("Watercolour Sets", "watercolour+paint+set+student", "Winsor & Newton, Daler-Rowney"),
  ],
  "music": [
    ("Music Theory Guides", "A-Level+Music+theory+guide", "ABRSM, Trinity, A-Level"),
    ("Manuscript Paper", "music+manuscript+paper+a4", "For composition practice"),
    ("Revision Audio", "A-Level+music+listening+revision", "Set works recordings"),
  ],
  "drama-and-theatre": [
    ("Drama Revision Guides", "A-Level+Drama+revision+guides", "Set text analysis, devising"),
    ("Script Collections", "plays+A-Level+drama+set+texts", "Published play editions"),
    ("Performance Journals", "drama+rehearsal+journal", "Track devising process"),
  ],
  "media-studies": [
    ("Media Revision Guides", "A-Level+Media+Studies+revision", "Key concepts, industries"),
    ("Media Theory Books", "media+theory+introduction", "Barthes, Baudrillard, etc."),
    ("Production Equipment", "video+camera+student+beginner", "For NEA production"),
  ],
  "physical-education": [
    ("PE Revision Guides", "A-Level+PE+revision+guides", "Anatomy, training, psychology"),
    ("Heart Rate Monitors", "heart+rate+monitor+chest+strap", "For training analysis"),
    ("Sports Science Books", "sports+science+introduction", "Physiology, biomechanics"),
  ],
  "religious-studies": [
    ("RS Revision Guides", "A-Level+Religious+Studies+revision", "Christianity, Islam, and more"),
    ("Holy Text Extracts", "bible+quran+extracts+study", "For quotation learning"),
    ("Ethics Workbooks", "A-Level+religious+studies+ethics", "Theme-based practice"),
  ],
  "philosophy": [
    ("Philosophy Revision Guides", "A-Level+Philosophy+revision+guides", "Epistemology, ethics, mind"),
    ("Logic Textbooks", "logic+textbook+student", "Formal logic and reasoning"),
    ("Ethics Guides", "ethics+philosophy+guide", "Moral philosophy"),
  ],
  "politics": [
    ("Politics Revision Guides", "A-Level+Politics+revision+guides", "UK, US, ideologies"),
    ("Political Theory Books", "political+theory+textbook", "Liberalism, conservatism, socialism"),
    ("Case Study Workbooks", "A-Level+politics+case+studies", "Elections, referendums"),
  ],
  "law": [
    ("Law Revision Guides", "A-Level+Law+revision+guides", "English legal system"),
    ("Case Law Books", "english+legal+system+cases", "Key cases and principles"),
    ("Statute Books", "statute+book+student", "Key legislation"),
  ],
  "accounting": [
    ("Accounting Revision Guides", "A-Level+Accounting+revision+guides", "Financial, management"),
    ("Accounting Software Guides", "accounting+software+tutorial", "Sage, QuickBooks"),
    ("Financial Calculators", "financial+calculator+student", "For accounting exams"),
  ],
}

DEFAULT_AFFILIATES = [
  ("A-Level Revision Guides", "A-Level+revision+guides", "All subjects covered"),
  ("Study Stationery", "study+stationery+student", "Pens, highlighters, flashcards"),
  ("Revision Timetable", "revision+timetable+planner", "Plan your study schedule"),
]


def affiliate_cards(subject_id):
    affs = AFFILIATES.get(subject_id, DEFAULT_AFFILIATES)
    cards = []
    for title, search, desc in affs[:3]:
        cards.append(
            '<a href="https://www.amazon.co.uk/s?k={}&tag=scottrix-21" class="affiliate-card" target="_blank" rel="nofollow noopener">\n'
            '<div class="affiliate-card-title">{}</div>\n'
            '<div class="affiliate-card-desc">{}</div>\n'
            '<div class="affiliate-card-store"><img src="../../amazon-smile.svg" alt="Amazon"> amazon.co.uk</div>\n'
            '</a>'.format(search, title, desc)
        )
    cards += [
        '<a href="https://join.fastmail.com/0d63b2d52105" class="affiliate-card" target="_blank" rel="nofollow noopener">'
        '<div class="affiliate-card-title">Fastmail — Private Email</div>'
        '<div class="affiliate-card-desc">Privacy-first email with no ads and no tracking</div>'
        '<div class="affiliate-card-store">fastmail.com</div></a>',
        '<a href="https://www.dynadot.com/?ref=scottrix" class="affiliate-card" target="_blank" rel="nofollow noopener">'
        '<div class="affiliate-card-title">Dynadot — Domain Registration →</div>'
        '<div class="affiliate-card-desc">Register or transfer domains with free SSL and affordable pricing</div>'
        '<div class="affiliate-card-store">dynadot.com</div></a>',
        '<a href="https://zen.mention-me.com/m/ol/yv3qsjix-scott-harrison" class="affiliate-card" target="_blank" rel="nofollow noopener">'
        '<div class="affiliate-card-title">Zen Internet — UK Broadband →</div>'
        '<div class="affiliate-card-desc">Award-winning UK broadband with no data caps and great customer service</div>'
        '<div class="affiliate-card-store">zen.co.uk</div></a>',
    ]
    return "\n".join(cards)


BANNER_HTML = '''<a class="fastmail-topbar" data-banner="fastmail" href="https://join.fastmail.com/0d63b2d52105" target="_blank" rel="noopener"><img src="../../FM Billboard 970x250.png" alt="Fastmail" loading="lazy"></a>
<a class="fastmail-topbar" data-banner="dynadot" href="https://www.dynadot.com/?ref=scottrix" target="_blank" rel="nofollow noopener" hidden><img src="../../dynadot-banner.jpg" alt="Dynadot — register a new domain, web hosting, SSL" loading="lazy" onerror="this.parentElement.style.display='none';document.querySelector('[data-banner=fastmail]').hidden=false"></a>
<script>(function(){var fm=document.querySelector('[data-banner=fastmail]');var dd=document.querySelector('[data-banner=dynadot]');if(Math.random()<0.5){fm.hidden=true;dd.hidden=false}})();</script>'''

FOOTER_HTML = '''<footer class="site-footer">
<p>A-Level Revise - Free revision notes for all subjects and exam boards</p>
<p>Content for educational purposes only. Always cross-reference with official specifications.</p>
<p>This site contains affiliate links. We may earn a commission if you purchase through these links.</p>
<p>© 2025 | <a href="https://github.com/scottrix/alevelrevise">GitHub</a> | <a href="../../privacy.html">Privacy Policy</a> | <a href="mailto:alevelrevise@scott.scottrix.co.uk">Contact</a></p>
</footer>'''

SCRIPTS_HTML = '''<script>
document.getElementById('theme-toggle').addEventListener('click', function() {
const root = document.documentElement;
if (root.classList.contains('light-mode')) {
root.classList.remove('light-mode'); this.textContent = '🌙'; localStorage.setItem('alevelrevise-theme', 'dark');
} else {
root.classList.add('light-mode'); this.textContent = '☀️'; localStorage.setItem('alevelrevise-theme', 'light');
}
});
if (localStorage.getItem('alevelrevise-theme') === 'light') {
document.documentElement.classList.add('light-mode'); document.getElementById('theme-toggle').textContent = '☀️';
}
</script>
<script src="../../sidebar.js"></script>
<script src="../../affiliate-images.js"></script>'''


def inject_chrome(html, subject_id):
    # Already has full chrome?
    if 'class="ad-right"' in html:
        return html, False

    # 1. Insert banner after </article> (topic-header)
    # Legacy pages have <article class="topic-header">... close with </article>
    m = re.search(r'</article>', html)
    if m:
        pos = m.end()
        html = html[:pos] + '\n' + BANNER_HTML + '\n' + html[pos:]

    # 2. Insert ad-right sidebar before </main>
    m = re.search(r'</main>', html)
    if m:
        ad_right = f'\n<aside class="ad-right">\n{affiliate_cards(subject_id)}\n</aside>\n'
        pos = m.start()
        html = html[:pos] + ad_right + html[pos:]

    # 3. Insert footer + scripts before </body>
    m = re.search(r'</body>', html)
    if m:
        pos = m.start()
        # Legacy pages don't have footer; add it
        html = html[:pos] + FOOTER_HTML + '\n' + SCRIPTS_HTML + '\n' + html[pos:]

    return html, True


def main():
    for site in SITES:
        base = BASE / site
        subjects_path = base / 'subjects.json'
        if not subjects_path.exists():
            print(f"{site}: no subjects.json, skipping")
            continue
        with open(subjects_path) as f:
            data = json.load(f)
        # Build a map of page -> subject_id
        page_to_subj = {}
        for s in data.get('subjects', []):
            sid = s.get('id') or s['name'].lower().replace(' ', '-').replace('&', '-and-').replace('–', '-')
            for t in s.get('topics', []):
                pg = t.get('page')
                if pg:
                    page_to_subj[pg] = sid
        # Process each legacy page
        for pg, sid in page_to_subj.items():
            path = base / pg
            if not path.exists():
                continue
            html = path.read_text(encoding='utf-8')
            if 'class="ad-right"' in html:
                continue
            new_html, changed = inject_chrome(html, sid)
            if changed:
                path.write_text(new_html, encoding='utf-8')
                print(f"  Injected chrome into {pg} (subject={sid})")
            else:
                print(f"  Skipped (already has chrome) {pg}")

if __name__ == '__main__':
    main()