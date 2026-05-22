---
name: erpnext-syntax-jinja
version: 1.0.0
description: Deterministic Jinja template syntax for ERPNext/Frappe Print Formats, Email Templates, and Portal Pages
author: OpenAEC Foundation
tags: [erpnext, frappe, jinja, templates, print-formats, email-templates, portal-pages]
languages: [en]
frappe_versions: [v14, v15, v16]
---

# ERPNext Jinja Templates Syntax Skill

> Correct Jinja syntax for Print Formats, Email Templates, and Portal Pages in ERPNext/Frappe v14/v15/v16.

---

## When to Use This Skill

USE this skill when:
- Creating or modifying Print Formats
- Developing Email Templates
- Building Portal Pages (www/*.html)
- Adding custom Jinja filters/methods via hooks

DO NOT USE for:
- Report Print Formats (they use JavaScript templating, not Jinja)
- Client Scripts (use erpnext-syntax-clientscripts)
- Server Scripts (use erpnext-syntax-serverscripts)

---

## Context Objects per Template Type

### Print Formats

| Object | Description |
|--------|-------------|
| `doc` | The document being printed |
| `frappe` | Frappe module with utility methods |
| `_()` | Translation function |

### Email Templates

| Object | Description |
|--------|-------------|
| `doc` | The linked document |
| `frappe` | Frappe module (limited) |

### Portal Pages

| Object | Description |
|--------|-------------|
| `frappe.session.user` | Current user |
| `frappe.form_dict` | Query parameters |
| `frappe.lang` | Current language |
| Custom context | Via Python controller |

> **See**: `references/context-objects.md` for complete details.

---

## Essential Methods

### Formatting (ALWAYS use)

```jinja
{# RECOMMENDED for fields in print formats #}
{{ doc.get_formatted("posting_date") }}
{{ doc.get_formatted("grand_total") }}

{# For child table rows - pass parent doc #}
{% for row in doc.items %}
    {{ row.get_formatted("rate", doc) }}
    {{ row.get_formatted("amount", doc) }}
{% endfor %}

{# General formatting #}
{{ frappe.format(value, {'fieldtype': 'Currency'}) }}
{{ frappe.format_date(doc.posting_date) }}
```

### Document Retrieval

```jinja
{# Full document #}
{% set customer = frappe.get_doc("Customer", doc.customer) %}

{# Specific field value (more efficient) #}
{% set abbr = frappe.db.get_value("Company", doc.company, "abbr") %}

{# List of records #}
{% set tasks = frappe.get_all('Task', 
    filters={'status': 'Open'}, 
    fields=['title', 'due_date']) %}
```

### Translation (REQUIRED for user-facing strings)

```jinja
<h1>{{ _("Invoice") }}</h1>
<p>{{ _("Total: {0}").format(doc.grand_total) }}</p>
```

> **See**: `references/methods-reference.md` for all methods.

---

## Control Structures

### Conditionals

```jinja
{% if doc.status == "Paid" %}
    <span class="label-success">{{ _("Paid") }}</span>
{% elif doc.status == "Overdue" %}
    <span class="label-danger">{{ _("Overdue") }}</span>
{% else %}
    <span>{{ doc.status }}</span>
{% endif %}
```

### Loops

```jinja
{% for item in doc.items %}
    <tr>
        <td>{{ loop.index }}</td>
        <td>{{ item.item_name }}</td>
        <td>{{ item.get_formatted("amount", doc) }}</td>
    </tr>
{% else %}
    <tr><td colspan="3">{{ _("No items") }}</td></tr>
{% endfor %}
```

### Loop Variables

| Variable | Description |
|----------|-------------|
| `loop.index` | 1-indexed position |
| `loop.first` | True on first |
| `loop.last` | True on last |
| `loop.length` | Total items |

### Variables

```jinja
{% set total = 0 %}
{% set customer_name = doc.customer_name | default('Unknown') %}
```

---

## Filters

### Commonly Used

| Filter | Example |
|--------|---------|
| `default` | `{{ value \| default('N/A') }}` |
| `length` | `{{ items \| length }}` |
| `join` | `{{ names \| join(', ') }}` |
| `truncate` | `{{ text \| truncate(100) }}` |
| `safe` | `{{ html \| safe }}` (trusted content only!) |

> **See**: `references/filters-reference.md` for all filters.

---

## Print Format Template

```jinja
<style>
    .header { background: #f5f5f5; padding: 15px; }
    .table { width: 100%; border-collapse: collapse; }
    .table th, .table td { border: 1px solid #ddd; padding: 8px; }
    .text-right { text-align: right; }
</style>

<div class="header">
    <h1>{{ doc.select_print_heading or _("Invoice") }}</h1>
    <p>{{ doc.name }}</p>
    <p>{{ _("Date") }}: {{ doc.get_formatted("posting_date") }}</p>
</div>

<table class="table">
    <thead>
        <tr>
            <th>{{ _("Item") }}</th>
            <th class="text-right">{{ _("Qty") }}</th>
            <th class="text-right">{{ _("Amount") }}</th>
        </tr>
    </thead>
    <tbody>
        {% for row in doc.items %}
        <tr>
            <td>{{ row.item_name }}</td>
            <td class="text-right">{{ row.qty }}</td>
            <td class="text-right">{{ row.get_formatted("amount", doc) }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<p><strong>{{ _("Grand Total") }}:</strong> {{ doc.get_formatted("grand_total") }}</p>
```

---

## Email Template

```jinja
<p>{{ _("Dear") }} {{ doc.customer_name }},</p>

<p>{{ _("Invoice") }} <strong>{{ doc.name }}</strong> {{ _("for") }} 
{{ doc.get_formatted("grand_total") }} {{ _("is due.") }}</p>

<p>{{ _("Due Date") }}: {{ frappe.format_date(doc.due_date) }}</p>

{% if doc.items %}
<ul>
{% for item in doc.items %}
    <li>{{ item.item_name }} - {{ item.qty }} x {{ item.get_formatted("rate", doc) }}</li>
{% endfor %}
</ul>
{% endif %}

<p>{{ _("Best regards") }},<br>
{{ frappe.db.get_value("Company", doc.company, "company_name") }}</p>
```

---

## Portal Page with Controller

### www/projects/index.html

```jinja
{% extends "templates/web.html" %}

{% block title %}{{ _("Projects") }}{% endblock %}

{% block page_content %}
<h1>{{ _("Projects") }}</h1>

{% if frappe.session.user != 'Guest' %}
    <p>{{ _("Welcome") }}, {{ frappe.get_fullname() }}</p>
{% endif %}

{% for project in projects %}
    <div class="project">
        <h3>{{ project.title }}</h3>
        <p>{{ project.description | truncate(150) }}</p>
    </div>
{% else %}
    <p>{{ _("No projects found.") }}</p>
{% endfor %}
{% endblock %}
```

### www/projects/index.py

```python
import frappe

def get_context(context):
    context.title = "Projects"
    context.projects = frappe.get_all(
        "Project",
        filters={"is_public": 1},
        fields=["name", "title", "description"],
        order_by="creation desc"
    )
    return context
```

---

## Custom Filters/Methods via jenv Hook

### hooks.py

```python
jenv = {
    "methods": ["myapp.jinja.methods"],
    "filters": ["myapp.jinja.filters"]
}
```

### myapp/jinja/methods.py

```python
import frappe

def get_company_logo(company):
    """Get company logo URL"""
    return frappe.db.get_value("Company", company, "company_logo") or ""
```

### Usage

```jinja
<img src="{{ get_company_logo(doc.company) }}">
```

---

## Critical Rules

### ✅ ALWAYS

1. Use `_()` for all user-facing strings
2. Use `get_formatted()` for currency/date fields
3. Use default values: `{{ value | default('') }}`
4. Child table rows: `row.get_formatted("field", doc)`

### ❌ NEVER

1. Execute queries in loops (N+1 problem)
2. Use `| safe` for user input (XSS risk)
3. Heavy calculations in templates (do in Python)
4. Jinja syntax in Report Print Formats (they use JS)

---

## Report Print Formats (NOT Jinja!)

**WARNING**: Report Print Formats for Query/Script Reports use JavaScript templating.

| Aspect | Jinja (Print Formats) | JS (Report Print Formats) |
|--------|----------------------|---------------------------|
| Output | `{{ }}` | `{%= %}` |
| Code | `{% %}` | `{% %}` |
| Language | Python | JavaScript |

```html
<!-- JS Template for Reports -->
{% for(var i=0; i<data.length; i++) { %}
<tr><td>{%= data[i].name %}</td></tr>
{% } %}
```

---

## Version Compatibility

| Feature | v14 | v15 |
|---------|:---:|:---:|
| Basic Jinja API | ✅ | ✅ |
| get_formatted() | ✅ | ✅ |
| jenv hook | ✅ | ✅ |
| Portal pages | ✅ | ✅ |
| frappe.utils.format_date with format | ✅ | ✅+ |

---
## V16: Chrome PDF Rendering

**Version 16 introduced Chrome-based PDF rendering** replacing wkhtmltopdf.

### Key Differences

| Aspect | v14/v15 (wkhtmltopdf) | v16 (Chrome) |
|--------|----------------------|---------------|
| CSS Support | Limited CSS3 | Full modern CSS |
| Flexbox/Grid | Partial | Full support |
| Page breaks | `page-break-*` | `break-*` preferred |
| Fonts | System fonts | Web fonts supported |
| Performance | Faster | Slightly slower |

### CSS Updates for V16

```css
/* v14/v15 */
.page-break { page-break-before: always; }

/* v16 - both work, but break-* is preferred */
.page-break { break-before: page; }
```

### Configuration (V16)

```python
# In site_config.json
{
    "pdf_engine": "chrome",  # or "wkhtmltopdf" for legacy
    "chrome_path": "/usr/bin/chromium"
}
```

### Print Format Compatibility

Most print formats work unchanged. Update if using:
- Complex CSS layouts (flexbox/grid now fully supported)
- Custom fonts (web fonts now work)
- Advanced page break control

---


## Reference Files

| File | Contents |
|------|----------|
| `references/context-objects.md` | Available objects per template type |
| `references/methods-reference.md` | All frappe.* methods |
| `references/filters-reference.md` | Standard and custom filters |
| `references/examples.md` | Complete working examples |
| `references/anti-patterns.md` | Mistakes to avoid |

---

## See Also

- `erpnext-syntax-hooks` - For jenv configuration in hooks.py
- `erpnext-impl-jinja` - For implementation patterns
- `erpnext-errors-jinja` - For error handling
