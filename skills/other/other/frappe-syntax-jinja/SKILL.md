---
name: frappe-syntax-jinja
description: >
  Use when writing Jinja templates for ERPNext/Frappe Print Formats, Email
  Templates, and Portal Pages. Covers template syntax, context variables,
  filters, macros, and v16 Chrome PDF rendering. Prevents common mistakes
  with doc context and child table iteration. Keywords: Jinja, print format,
  email template, portal page, template syntax, PDF, v14-v16.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Jinja Templates Syntax

> Deterministic Jinja reference for Print Formats, Email Templates, Notification Templates, and Portal Pages in Frappe v14/v15/v16.

---

## When to Use This Skill

USE when:
- Creating or modifying Print Formats (Jinja-based)
- Writing Email Templates with dynamic fields
- Building Portal Pages (`www/*.html`) with Python controllers
- Writing Notification Templates (system/email/SMS)
- Registering custom Jinja methods or filters via `hooks.py`

DO NOT USE for:
- Report Print Formats — they use JavaScript templating (`{%= %}`), NOT Jinja
- Client Scripts — see `frappe-syntax-clientscripts`
- Server Scripts — see `frappe-syntax-serverscripts`

---

## Decision Tree: Which Template Type?

```
Need a printable document?
├─ YES → Is it for a Query/Script Report?
│        ├─ YES → Use JS Template ({%= %}), NOT Jinja
│        └─ NO  → Use Jinja Print Format
└─ NO  → Is it for email?
         ├─ YES → Is it triggered by workflow/notification?
         │        ├─ YES → Notification Template (Jinja)
         │        └─ NO  → Email Template (Jinja)
         └─ NO  → Is it a web page?
                  ├─ YES → Portal Page (www/*.html + .py controller)
                  └─ NO  → frappe.render_template() for ad-hoc rendering
```

---

## Quick Reference: Jinja Syntax

| Syntax | Purpose | Example |
|--------|---------|---------|
| `{{ }}` | Output expression | `{{ doc.name }}` |
| `{% %}` | Control statement | `{% if doc.status == "Paid" %}` |
| `{# #}` | Comment | `{# This is a comment #}` |
| `{{ _("text") }}` | Translation | `{{ _("Invoice") }}` |
| `{{ val \| filter }}` | Filter | `{{ name \| default("N/A") }}` |

### CRITICAL: Jinja vs JS Template Syntax

| Aspect | Jinja (Print Formats) | JS Template (Report Print Formats) |
|--------|----------------------|-------------------------------------|
| Output | `{{ expression }}` | `{%= expression %}` |
| Code block | `{% statement %}` | `{% js_code %}` |
| Language | Python | JavaScript |
| Context | `doc`, `frappe` | `data`, `filters` |

**NEVER use Jinja syntax in Report Print Formats. NEVER use `{%= %}` in standard Print Formats.**

---

## Context Objects by Template Type

### Print Formats

| Object | Description |
|--------|-------------|
| `doc` | The document being printed (full Document object) |
| `frappe` | Frappe module (whitelisted methods only) |
| `frappe.utils` | Utility functions |
| `_()` | Translation function |
| `doc.items`, `doc.taxes` | Child table accessors (by fieldname) |

### Email Templates

| Object | Description |
|--------|-------------|
| `doc` | The linked document (when triggered from a DocType) |
| `frappe` | Frappe module (limited) |
| `_()` | Translation function |

### Notification Templates

| Object | Description |
|--------|-------------|
| `doc` | The document that triggered the notification |
| `frappe` | Frappe module |
| `_()` | Translation function |

### Portal Pages (www/*.html)

| Object | Description |
|--------|-------------|
| `frappe` | Frappe module |
| `frappe.session.user` | Current authenticated user |
| `frappe.form_dict` | Query parameters from URL |
| `frappe.lang` | Current language code |
| Custom context | Set via `get_context(context)` in `.py` controller |

> **Full details**: `references/context-objects.md`

---

## Essential Methods (Whitelisted in Jinja)

### Formatting — ALWAYS Use for Display

```jinja
{# ALWAYS use get_formatted() for fields in Print Formats #}
{{ doc.get_formatted("posting_date") }}
{{ doc.get_formatted("grand_total") }}

{# Child table rows — ALWAYS pass parent doc for currency context #}
{% for row in doc.items %}
    {{ row.get_formatted("rate", doc) }}
    {{ row.get_formatted("amount", doc) }}
{% endfor %}

{# General formatting with explicit fieldtype #}
{{ frappe.format(value, {'fieldtype': 'Currency'}) }}
{{ frappe.format_date(doc.posting_date) }}
```

### Document Retrieval

```jinja
{# Full document — use only when multiple fields needed #}
{% set customer = frappe.get_doc("Customer", doc.customer) %}

{# Single field — ALWAYS prefer over get_doc for one field #}
{% set abbr = frappe.db.get_value("Company", doc.company, "abbr") %}

{# List of records (no permission check) #}
{% set tasks = frappe.get_all("Task",
    filters={"status": "Open"},
    fields=["title", "due_date"],
    order_by="due_date asc",
    page_length=10) %}

{# List with permission check (portal pages) #}
{% set orders = frappe.get_list("Sales Order",
    filters={"customer": doc.customer},
    fields=["name", "grand_total"]) %}
```

### Translation — REQUIRED for All User-Facing Strings

```jinja
<h1>{{ _("Invoice") }}</h1>
<p>{{ _("Total: {0}").format(doc.get_formatted("grand_total")) }}</p>
```

### System & Session

```jinja
{{ frappe.get_url() }}
{{ frappe.get_fullname() }}
{{ frappe.get_fullname(doc.owner) }}
{{ frappe.db.get_single_value("System Settings", "time_zone") }}
{% if frappe.session.user != "Guest" %}...{% endif %}
```

> **Full method reference**: `references/methods-reference.md`

---

## Control Structures

### Conditionals

```jinja
{% if doc.status == "Paid" %}
    <span class="paid">{{ _("Paid") }}</span>
{% elif doc.status == "Overdue" %}
    <span class="overdue">{{ _("Overdue") }}</span>
{% else %}
    <span>{{ doc.status }}</span>
{% endif %}
```

### Loops with Child Tables

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
| `loop.index0` | 0-indexed position |
| `loop.first` | `True` on first iteration |
| `loop.last` | `True` on last iteration |
| `loop.length` | Total number of items |

### Variables

```jinja
{% set total = 0 %}
{% set name = doc.customer_name | default("Unknown") %}
```

---

## Filters

| Filter | Example | Notes |
|--------|---------|-------|
| `default` | `{{ val \| default("N/A") }}` | ALWAYS use for optional fields |
| `length` | `{{ items \| length }}` | Count items |
| `join` | `{{ names \| join(", ") }}` | Join list to string |
| `truncate` | `{{ text \| truncate(100) }}` | Truncate with ellipsis |
| `escape` | `{{ input \| escape }}` | HTML-escape (default behavior) |
| `safe` | `{{ html \| safe }}` | Render raw HTML — NEVER for user input |
| `round` | `{{ num \| round(2) }}` | Round number |
| `lower` / `upper` | `{{ text \| upper }}` | Case conversion |

> **Full filter reference**: `references/filters-reference.md`

---

## Custom Jinja Methods & Filters via hooks.py

### hooks.py Registration

```python
# hooks.py
jenv = {
    "methods": [
        "myapp.jinja.methods"       # Module with callable functions
    ],
    "filters": [
        "myapp.jinja.filters"       # Module with filter functions
    ]
}
```

### Custom Method

```python
# myapp/jinja/methods.py
import frappe

def get_company_logo(company):
    """Returns company logo URL. Called as get_company_logo() in Jinja."""
    return frappe.db.get_value("Company", company, "company_logo") or ""
```

```jinja
<img src="{{ get_company_logo(doc.company) }}" alt="Logo">
```

### Custom Filter

```python
# myapp/jinja/filters.py
def nl2br(text):
    """Convert newlines to <br> tags. Used as {{ text | nl2br }}."""
    return (text or "").replace("\n", "<br>")
```

```jinja
{{ doc.notes | nl2br | safe }}
```

> **Details**: `references/methods.md`

---

## Print Format Patterns

### Minimal Print Format Template

```jinja
<style>
    .print-header { background: #f5f5f5; padding: 15px; }
    .item-table { width: 100%; border-collapse: collapse; }
    .item-table th, .item-table td { border: 1px solid #ddd; padding: 8px; }
    .text-right { text-align: right; }
</style>

<div class="print-header">
    <h1>{{ doc.select_print_heading or _("Invoice") }}</h1>
    <p>{{ doc.name }} — {{ doc.get_formatted("posting_date") }}</p>
</div>

<table class="item-table">
    <thead>
        <tr>
            <th>#</th>
            <th>{{ _("Item") }}</th>
            <th class="text-right">{{ _("Qty") }}</th>
            <th class="text-right">{{ _("Amount") }}</th>
        </tr>
    </thead>
    <tbody>
        {% for row in doc.items %}
        <tr>
            <td>{{ loop.index }}</td>
            <td>{{ row.item_name }}</td>
            <td class="text-right">{{ row.qty }}</td>
            <td class="text-right">{{ row.get_formatted("amount", doc) }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<p><strong>{{ _("Grand Total") }}: {{ doc.get_formatted("grand_total") }}</strong></p>
```

### Page Breaks

```css
/* v14/v15 (wkhtmltopdf) */
.page-break { page-break-before: always; }

/* v16 (Chrome PDF) — ALWAYS prefer break-* in v16 */
.page-break { break-before: page; }
```

> **Full examples**: `references/examples.md` | **Patterns**: `references/patterns.md`

---

## V16: Chrome PDF Rendering

| Aspect | v14/v15 (wkhtmltopdf) | v16 (Chrome) |
|--------|----------------------|--------------|
| CSS Support | Limited CSS3 | Full modern CSS |
| Flexbox/Grid | Partial | Full support |
| Page breaks | `page-break-*` | `break-*` preferred |
| Fonts | System fonts only | Web fonts supported |

### V16 Configuration

```json
// site_config.json
{
    "pdf_engine": "chrome",
    "chrome_path": "/usr/bin/chromium"
}
```

---

## Portal Page Pattern

### www/projects/index.html

```jinja
{% extends "templates/web.html" %}
{% block title %}{{ _("Projects") }}{% endblock %}

{% block page_content %}
<h1>{{ _("Projects") }}</h1>
{% for project in projects %}
    <h3>{{ project.title }}</h3>
    <p>{{ project.description | default("") | truncate(150) }}</p>
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
    context.no_cache = True
    context.projects = frappe.get_all("Project",
        filters={"is_public": 1},
        fields=["name", "title", "description"],
        order_by="creation desc")
    return context
```

> **Full structure**: `references/structure.md` | **Templates**: `references/templates.md`

---

## Critical Rules

### ALWAYS

1. Use `_()` for ALL user-facing strings
2. Use `get_formatted()` for currency, date, and numeric fields
3. Use `default()` filter for optional/nullable fields
4. Pass parent `doc` to child row `get_formatted("field", doc)`
5. Use `frappe.db.get_value()` when you need only one field
6. Keep calculations in Python controllers, not Jinja templates

### NEVER

1. Execute database queries inside loops (N+1 problem)
2. Use `| safe` on user-supplied input (XSS vulnerability)
3. Use Jinja syntax in Report Print Formats (they require JS `{%= %}`)
4. Use `frappe.get_doc()` when `frappe.db.get_value()` suffices
5. Hardcode strings without `_()` translation wrapper
6. Disable `safe_render` without security review

> **Anti-patterns with fixes**: `references/anti-patterns.md`

---

## Reference Files

| File | Contents |
|------|----------|
| `references/syntax.md` | Jinja syntax reference (tags, filters, tests, loops) |
| `references/methods.md` | Custom Jinja methods/filters via hooks |
| `references/context-objects.md` | Available objects per template type |
| `references/filters-reference.md` | All standard and custom Frappe filters |
| `references/methods-reference.md` | All frappe.* methods available in Jinja |
| `references/examples.md` | Complete Print Format, Email, Portal examples |
| `references/anti-patterns.md` | Common mistakes and correct alternatives |
| `references/templates.md` | Template structure patterns |
| `references/patterns.md` | Conditional rendering, loops, child tables |
| `references/structure.md` | File structure for template types |

---

## See Also

- `frappe-syntax-hooks` — jenv configuration in hooks.py
- `frappe-impl-printformat` — Print Format implementation patterns
- `frappe-errors-serverscripts` — Server-side error handling
