---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: invoice-template
description: "Generate professional PDF invoices from templates"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: finance
tags:
  - invoice
  - template
  - billing
department: Finance

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
    - create_docx
    - fill_docx_template
    - docx_to_pdf

# Skill Capabilities
capabilities:
  - template_creation
  - invoice_formatting

# Language Support
languages:
  - en
  - zh
---

# Invoice Template Skill

## Overview

This skill generates professional PDF invoices from structured data and templates. Create invoices with company branding, itemized lists, tax calculations, and payment details.

## How to Use

1. Describe what you want to accomplish
2. Provide any required input data or files
3. I'll execute the appropriate operations

**Example prompts:**
- "Generate invoices from order data"
- "Create recurring invoices"
- "Batch generate monthly invoices"
- "Customize invoice templates per client"

## Domain Knowledge


### Invoice Data Structure

```python
invoice_data = {
    "invoice_number": "INV-2026-001",
    "date": "2026-01-30",
    "due_date": "2026-02-28",
    
    "from": {
        "name": "Your Company",
        "address": "123 Business St",
        "email": "billing@company.com"
    },
    
    "to": {
        "name": "Client Name",
        "address": "456 Client Ave",
        "email": "client@example.com"
    },
    
    "items": [
        {"description": "Consulting", "quantity": 10, "rate": 150.00},
        {"description": "Development", "quantity": 20, "rate": 100.00}
    ],
    
    "tax_rate": 0.08,
    "notes": "Payment due within 30 days"
}
```

### PDF Generation with ReportLab

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def create_invoice(data: dict, output_path: str):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(1*inch, height - 1*inch, "INVOICE")
    
    # Invoice details
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 1.5*inch, f"Invoice #: {data['invoice_number']}")
    c.drawString(1*inch, height - 1.75*inch, f"Date: {data['date']}")
    
    # From/To
    y = height - 2.5*inch
    c.drawString(1*inch, y, f"From: {data['from']['name']}")
    c.drawString(4*inch, y, f"To: {data['to']['name']}")
    
    # Items table
    y = height - 4*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Description")
    c.drawString(4*inch, y, "Qty")
    c.drawString(5*inch, y, "Rate")
    c.drawString(6*inch, y, "Amount")
    
    c.setFont("Helvetica", 10)
    subtotal = 0
    for item in data['items']:
        y -= 0.3*inch
        amount = item['quantity'] * item['rate']
        subtotal += amount
        c.drawString(1*inch, y, item['description'])
        c.drawString(4*inch, y, str(item['quantity']))
        c.drawString(5*inch, y, f"${item['rate']:.2f}")
        c.drawString(6*inch, y, f"${amount:.2f}")
    
    # Totals
    tax = subtotal * data['tax_rate']
    total = subtotal + tax
    
    y -= 0.5*inch
    c.drawString(5*inch, y, f"Subtotal: ${subtotal:.2f}")
    y -= 0.25*inch
    c.drawString(5*inch, y, f"Tax ({data['tax_rate']*100}%): ${tax:.2f}")
    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(5*inch, y, f"Total: ${total:.2f}")
    
    c.save()
    return output_path
```

### HTML Template Approach

```python
from weasyprint import HTML
from jinja2 import Template

invoice_template = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; margin: 40px; }
        .header { display: flex; justify-content: space-between; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        .total { font-weight: bold; font-size: 18px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>INVOICE</h1>
        <div>
            <p>Invoice #: {{ invoice_number }}</p>
            <p>Date: {{ date }}</p>
        </div>
    </div>
    <table>
        <tr><th>Description</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>
        {% for item in items %}
        <tr>
            <td>{{ item.description }}</td>
            <td>{{ item.quantity }}</td>
            <td>${{ "%.2f"|format(item.rate) }}</td>
            <td>${{ "%.2f"|format(item.quantity * item.rate) }}</td>
        </tr>
        {% endfor %}
    </table>
    <p class="total">Total: ${{ "%.2f"|format(total) }}</p>
</body>
</html>
"""

def create_invoice_html(data: dict, output_path: str):
    template = Template(invoice_template)
    
    # Calculate total
    total = sum(i['quantity'] * i['rate'] for i in data['items'])
    total *= (1 + data.get('tax_rate', 0))
    data['total'] = total
    
    html = template.render(**data)
    HTML(string=html).write_pdf(output_path)
    return output_path
```


## Best Practices

1. **Validate required fields before generation**
2. **Use templates for consistent branding**
3. **Auto-calculate totals (don't trust input)**
4. **Include payment instructions and terms**

## Installation

```bash
# Install required dependencies
pip install python-docx openpyxl python-pptx reportlab jinja2
```

## Resources

- [easy-invoice-pdf Repository](https://github.com/nickmitchko/easy-invoice-pdf)
- [Claude Office Skills Hub](https://github.com/claude-office-skills/skills)
