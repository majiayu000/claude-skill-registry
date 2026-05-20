---
name: jupyter
description: Read, modify, execute, and convert Jupyter notebooks programmatically. Use when working with .ipynb files for data science workflows, including editing cells, clearing outputs, or converting to other formats.
triggers:
- ipynb
- jupyter
---

# Jupyter Notebook Guide

Notebooks are JSON files. Cells are in `nb['cells']`, each has `source` (list of strings) and `cell_type` ('code', 'markdown', or 'raw').

## Modifying Notebooks
```python
import json
with open('notebook.ipynb') as f:
    nb = json.load(f)
# Modify nb['cells'][i]['source'], then:
with open('notebook.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
```

## Executing & Converting
```bash
jupyter nbconvert --to notebook --execute --inplace notebook.ipynb  # Execute in place
jupyter nbconvert --to html notebook.ipynb      # Convert to HTML
jupyter nbconvert --to script notebook.ipynb    # Convert to Python
jupyter nbconvert --to markdown notebook.ipynb  # Convert to Markdown
```

## Finding Code
```bash
grep -n "search_term" notebook.ipynb
```

## Cell Structure
```python
# Code cell
{"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["code\n"]}
# Markdown cell
{"cell_type": "markdown", "metadata": {}, "source": ["# Title\n"]}
```

## Clear Outputs
```python
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None
```