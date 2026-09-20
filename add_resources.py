#!/usr/bin/env python3
"""Add video, past_papers, and external_links resources to all topics in generate_alevel.py"""

import ast

def add_resources_to_topics():
    """Add video, past_papers, and external_links to each topic in SUBJECTS"""
    
    with open('generate_alevel.py', 'r') as f:
        content = f.read()
    
    # Find the SUBJECTS list
    subj_start = content.find('SUBJECTS = [')
    if subj_start == -1:
        print("Could not find SUBJECTS")
        return
    
    # Find the end of SUBJECTS (before REDIRECT_TEMPLATE)
    redirect_pos = content.find('REDIRECT_TEMPLATE')
    subj_section = content[subj_start:redirect_pos]
    
    # Parse the SUBJECTS list using ast
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
    
    if list_end is None:
        print("Could not find end of SUBJECTS list")
        return
    
    subjects_code = subj_section[list_start:list_end]
    print(f"Found SUBJECTS list: {len(subjects_code)} chars")
    
    # Parse with ast
    try:
        tree = ast.parse(subjects_code, mode='eval')
        subjects = eval(compile(tree, '<string>', 'eval'))
        
        print(f"Parsed {len(subjects)} subjects")
        
    except Exception as e:
        print(f"Error parsing SUBJECTS: {e}")
        return
    
    # Now add resources to each topic
    for subject in subjects:
        sname = subject['name']
        for topic in subject['topics']:
            if 'videos' not in topic:
                topic['videos'] = []
            if 'past_papers' not in topic:
                topic['past_papers'] = []
            if 'external_links' not in topic:
                topic['external_links'] = []
    
    # Now we need to write back the modified SUBJECTS
    # Convert back to string representation
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
    
    subjects_str = dict_to_str(subjects)
    
    # Replace the SUBJECTS list in the content
    new_subj_section = 'SUBJECTS = ' + subjects_str
    
    # Find the exact boundaries
    subj_start_full = content.find('SUBJECTS = [')
    
    # Find the exact end of SUBJECTS list
    bracket_count = 0
    list_start_rel = content[subj_start_full:].find('[')
    abs_list_start = subj_start_full + list_start_rel
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
        before = content[:subj_start_full]
        after = content[list_end:]
        new_content = before + 'SUBJECTS = ' + subjects_str + after
        
        with open('generate_alevel.py', 'w') as f:
            f.write(new_content)
        print("Successfully updated generate_alevel.py")
    else:
        print("Could not find end of SUBJECTS list")

if __name__ == '__main__':
    add_resources_to_topics()