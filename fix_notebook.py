#!/usr/bin/env python3
"""
Fix the notebook by replacing the Google Colab path with local path
"""

import json

# Read the original notebook
with open('major_project_used_cars.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Fix the path in the notebook
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        if isinstance(source, list):
            for i, line in enumerate(source):
                if '/content/used_cars.csv' in line:
                    source[i] = line.replace('/content/used_cars.csv', 'used_cars.csv')
        elif isinstance(source, str):
            if '/content/used_cars.csv' in source:
                source = source.replace('/content/used_cars.csv', 'used_cars.csv')
                cell['source'] = source

# Save the fixed notebook
with open('major_project_used_cars_fixed.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print("Notebook fixed! Saved as 'major_project_used_cars_fixed.ipynb'")
