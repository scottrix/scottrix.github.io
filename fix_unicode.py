#!/usr/bin/env python3
import re

with open('generate_alevel.py', 'r') as f:
    content = f.read()

# Replace problematic unicode chars
replacements = {
    '\u2192': '->',      # →
    '\u00d7': 'x',       # ×
    '\u00b2': '^2',      # ²
    '\u00b3': '^3',      # ³
    '\u00b1': '+/-',     # ±
    '\u2264': '<=',      # ≤
    '\u2265': '>=',      # ≥
    '\u2260': '!=',      # ≠
    '\u221e': 'inf',     # ∞
    '\u221a': 'sqrt',    # √
    '\u03c0': 'pi',      # π
    '\u0394': 'Delta',   # Δ
    '\u03c3': 'sigma',   # σ
    '\u00b0': ' deg ',   # °
    '\u2022': '*',       # •
    '\u2013': '-',       # –
    '\u2014': '--',      # —
    '\u2018': "'",       # '
    '\u2019': "'",       # '
    '\u201c': '"',       # "
    '\u201d': '"',       # "
    '\u2026': '...',     # …
    '\u00a3': 'GBP ',    # £
    '\u20ac': 'EUR ',    # €
    '\u00a9': '(c)',     # ©
    '\u00ae': '(r)',     # ®
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open('generate_alevel.py', 'w') as f:
    f.write(content)

print('Replacements done')