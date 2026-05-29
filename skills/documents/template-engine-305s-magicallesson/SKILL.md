---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: template-engine
description: "Auto-fill document templates with data - mail merge for any format"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: template
tags:
  - template
  - engine
  - autofill
  - docxtpl
department: All

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
mcp:
  server: office-mcp
  tools:
    - fill_docx_template

# Skill Capabilities
capabilities:
  - template_filling
  - document_automation

# Language Support
languages:
  - en
  - zh
---

# Template Engine Skill

## Overview

This skill enables template-based document generation - define templates with placeholders, then automatically fill them with data. Works with Word, Excel, PowerPoint, and more.

## How to Use

1. Describe what you want to accomplish
2. Provide any required input data or files
3. I'll execute the appropriate operations

**Example prompts:**
- "Mail merge for bulk letters/contracts"
- "Generate personalized reports from data"
- "Create certificates from templates"
- "Auto-fill forms with user data"

## Domain Knowledge


### Template Syntax (Jinja2-based)

```
{{ variable }}           - Simple substitution
{% for item in list %}   - Loop
{% if condition %}       - Conditional
{{ date | format_date }} - Filter
```

### Word Template Example

```python
from docxtpl import DocxTemplate

# Create template with placeholders:
# Dear {{ name }},
# Thank you for your order #{{ order_id }}...

def fill_template(template_path: str, data: dict, output_path: str):
    doc = DocxTemplate(template_path)
    doc.render(data)
    doc.save(output_path)
    return output_path

# Usage
fill_template(
    "templates/order_confirmation.docx",
    {
        "name": "John Smith",
        "order_id": "ORD-12345",
        "items": [
            {"name": "Product A", "qty": 2, "price": 29.99},
            {"name": "Product B", "qty": 1, "price": 49.99}
        ],
        "total": 109.97
    },
    "output/confirmation_john.docx"
)
```

### Excel Template

```python
from openpyxl import load_workbook
import re

def fill_excel_template(template_path: str, data: dict, output_path: str):
    wb = load_workbook(template_path)
    ws = wb.active
    
    # Find and replace placeholders like {{name}}
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                for key, value in data.items():
                    placeholder = "{{" + key + "}}"
                    if placeholder in cell.value:
                        cell.value = cell.value.replace(placeholder, str(value))
    
    wb.save(output_path)
    return output_path
```

### Bulk Generation (Mail Merge)

```python
import csv
from pathlib import Path

def mail_merge(template_path: str, data_csv: str, output_dir: str):
    """Generate documents for each row in CSV."""
    
    Path(output_dir).mkdir(exist_ok=True)
    
    with open(data_csv) as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader):
            output_path = f"{output_dir}/document_{i+1}.docx"
            fill_template(template_path, row, output_path)
            print(f"Generated: {output_path}")

# Usage with contacts.csv:
# name,email,company
# John,john@example.com,Acme
# Jane,jane@example.com,Corp

mail_merge(
    "templates/welcome_letter.docx",
    "data/contacts.csv",
    "output/letters"
)
```

### Advanced: Conditional Content

```python
from docxtpl import DocxTemplate

# Template with conditionals:
# {% if vip %}
# Thank you for being a VIP member!
# {% else %}
# Thank you for your purchase.
# {% endif %}

doc = DocxTemplate("template.docx")
doc.render({
    "name": "John",
    "vip": True,
    "discount": 20
})
doc.save("output.docx")
```


## Best Practices

1. **Use clear placeholder naming ({{client_name}})**
2. **Validate data before rendering**
3. **Handle missing data gracefully**
4. **Keep templates version-controlled**

## Installation

```bash
# Install required dependencies
pip install python-docx openpyxl python-pptx reportlab jinja2
```

## Resources

- [docxtpl / yumdocs Repository](https://github.com/elapouya/python-docxtpl)
- [Claude Office Skills Hub](https://github.com/claude-office-skills/skills)
