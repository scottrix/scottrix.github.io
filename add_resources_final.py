#!/usr/bin/env python3
"""Add video, past_papers, and external_links resources to all topics in generate_alevel.py"""

import ast

def dict_to_str(obj, indent=2):
    """Convert dict/list to Python source code string"""
    if isinstance(obj, dict):
        if not obj:
            return '{}'
        items = []
        for k, v in obj.items():
            items.append(f'{" " * (indent + 2)}"{k}": {dict_to_str(v, indent + 2)}')
        return '{\n' + ',\n'.join(items) + '\n' + ' ' * indent + '}'
    elif isinstance(obj, list):
        if not obj:
            return '[]'
        items = [dict_to_str(v, indent + 2) for v in obj]
        return '[\n' + ',\n'.join(items) + '\n' + ' ' * indent + ']'
    elif isinstance(obj, str):
        escaped = obj.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
        return f'"{escaped}"'
    elif isinstance(obj, bool):
        return 'True' if obj else 'False'
    elif isinstance(obj, (int, float)):
        return str(obj)
    elif obj is None:
        return 'None'
    else:
        return str(obj)

def add_resources():
    with open('generate_alevel.py', 'r') as f:
        content = f.read()

    subj_start = content.find('SUBJECTS = [')
    redirect_pos = content.find('REDIRECT_TEMPLATE')
    subj_section = content[subj_start:redirect_pos]
    list_start = subj_section.find('[')
    bracket_count = 0
    list_end = None
    for i, ch in enumerate(subj_section[list_start:]):
        if ch == '[':
            bracket_count += 1
        elif ch == ']':
            bracket_count -= 1
            if bracket_count == 0:
                list_end = list_start + i + 1
                break
    subjects_code = subj_section[list_start:list_end]
    tree = ast.parse(subjects_code, mode='eval')
    subjects = eval(compile(tree, '<string>', 'eval'))

    # Add resources to each topic
    for subject in subjects:
        sname = subject['name']
        for topic in subject['topics']:
            # Add videos
            if 'videos' not in topic:
                topic['videos'] = [
                    {"title": f"{topic['title']} - Overview", "url": f"https://www.youtube.com/results?search_query={topic['title'].replace(' ', '+')}+A-Level", "source": "YouTube Search"},
                    {"title": f"{topic['title']} - Exam Questions", "url": f"https://www.youtube.com/results?search_query={topic['title'].replace(' ', '+')}+exam+questions", "source": "YouTube Search"}
                ]
            # Add past_papers
            if 'past_papers' not in topic:
                topic['past_papers'] = [
                    {"title": f"AQA A-Level {subject['name']} - {topic['title']}", "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes", "board": "AQA"},
                    {"title": f"Edexcel A-Level {subject['name']} - {topic['title']}", "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html", "board": "Edexcel"},
                    {"title": f"OCR A-Level {subject['name']} - {topic['title']}", "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/", "board": "OCR"}
                ]
            # Add external_links
            if 'external_links' not in topic:
                topic['external_links'] = [
                    {"title": f"Physics & Maths Tutor - {topic['title']}", "url": f"https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/{topic['title'].lower().replace(' ', '-')}/", "description": "Free notes, worksheets, and past paper questions by topic"},
                    {"title": f"Dr Frost Maths - {topic['title']}", "url": "https://drfrostmaths.com/", "description": "Free resources, slides, and interactive questions"},
                    {"title": f"BBC Bitesize - {topic['title']}", "url": f"https://www.bbc.co.uk/bitesize/search?q={topic['title'].replace(' ', '+')}", "description": "BBC Bitesize revision resources"}
                ]

    # Convert back to string
    def dict_to_str(obj, indent=2):
        if isinstance(obj, dict):
            if not obj:
                return '{}'
            items = []
            for k, v in obj.items():
                items.append(f'{" " * (indent + 2)}"{k}": {dict_to_str(v, indent + 2)}')
            return '{\n' + ',\n'.join(items) + '\n' + ' ' * indent + '}'
        elif isinstance(obj, list):
            if not obj:
                return '[]'
            items = [dict_to_str(v, indent + 2) for v in obj]
            return '[\n' + ',\n'.join(items) + '\n' + ' ' * indent + ']'
        elif isinstance(obj, str):
            escaped = obj.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
            return f'"{escaped}"'
        elif isinstance(obj, bool):
            return 'True' if obj else 'False'
        elif isinstance(obj, (int, float)):
            return str(obj)
        elif obj is None:
            return 'None'
        else:
            return str(obj)

    # Parse the SUBJECTS list
    subj_start = content.find('SUBJECTS = [')
    redirect_pos = content.find('REDIRECT_TEMPLATE')
    subj_section = content[subj_start:redirect_pos]
    list_start = subj_section.find('[')
    bracket_count = 0
    list_end = None
    for i, ch in enumerate(subj_section[list_start:]):
        if ch == '[':
            bracket_count += 1
        elif ch == ']':
            bracket_count -= 1
            if bracket_count == 0:
                list_end = list_start + i + 1
                break
    subjects_code = subj_section[list_start:list_end]
    tree = ast.parse(subjects_code, mode='eval')
    subjects = eval(compile(tree, '<string>', 'eval'))

    # Add resources to each topic
    for subject in subjects:
        sname = subject['name']
        for topic in subject['topics']:
            if 'videos' not in topic:
                topic['videos'] = [
                    {"title": f"{topic['title']} - Overview", "url": f"https://www.youtube.com/results?search_query={topic['title'].replace(' ', '+')}+A-Level", "source": "YouTube Search"},
                    {"title": f"{topic['title']} - Exam Questions", "url": f"https://www.youtube.com/results?search_query={topic['title'].replace(' ', '+')}+exam+questions", "source": "YouTube Search"}
                ]
            if 'past_papers' not in topic:
                topic['past_papers'] = [
                    {"title": f"AQA A-Level {subject['name']} - {topic['title']}", "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes", "board": "AQA"},
                    {"title": f"Edexcel A-Level {subject['name']} - {topic['title']}", "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html", "board": "Edexcel"},
                    {"title": f"OCR A-Level {subject['name']} - {topic['title']}", "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/", "board": "OCR"}
                ]
            if 'external_links' not in topic:
                topic['external_links'] = [
                    {"title": f"Physics & Maths Tutor - {topic['title']}", "url": f"https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/{topic['title'].lower().replace(' ', '-')}/", "description": "Free notes, worksheets, and past paper questions by topic"},
                    {"title": f"Dr Frost Maths - {topic['title']}", "url": "https://drfrostmaths.com/", "description": "Free resources, slides, and interactive questions"},
                    {"title": f"BBC Bitesize - {topic['title']}", "url": f"https://www.bbc.co.uk/bitesize/search?q={topic['title'].replace(' ', '+')}", "description": "BBC Bitesize revision resources"}
                ]

    subjects_str = dict_to_str(subjects)

    # Replace the SUBJECTS list in the content
    subj_start = content.find('SUBJECTS = [')
    list_start_rel = content[subj_start:].find('[')
    abs_list_start = subj_start + list_start_rel
    bracket_count = 0
    list_end = None
    for i, ch in enumerate(content[abs_list_start:]):
        if ch == '[':
            bracket_count += 1
        elif ch == ']':
            bracket_count -= 1
            if bracket_count == 0:
                list_end = abs_list_start + i + 1
                break

    if list_end:
        before = content[:subj_start]
        after = content[list_end:]
        new_content = before + 'SUBJECTS = ' + dict_to_str(subjects) + after

        with open('generate_alevel.py', 'w') as f:
            f.write(new_content)
        print('Successfully updated generate_alevel.py')
    else:
        print('Could not find end of SUBJECTS list')

if __name__ == '__main__':
    add_resources()