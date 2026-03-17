---
name: erpnext-impl-jinja
description: "Implementation workflows and decision trees for Jinja templates in ERPNext/Frappe. Use when determining HOW to implement Print Formats, Email Templates, Portal Pages, or custom Jinja methods. Covers template type selection, context variables, styling, and V16 Chrome PDF rendering. Triggers: create print format, email template, portal page, custom jinja filter, print format styling, pdf template, invoice template, report template."
---

# ERPNext Jinja Templates - Implementation

This skill helps you determine HOW to implement Jinja templates. For exact syntax, see `erpnext-syntax-jinja`.

**Version**: v14/v15/v16 compatible (with V16-specific features noted)

## Main Decision: What Are You Trying to Create?

```
┌─────────────────────────────────────────────────────────────────────────┐
│ WHAT DO YOU WANT TO CREATE?                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ► Printable document (invoice, PO, report)?                             │
│   ├── Standard DocType → Print Format (Jinja)                           │
│   └── Query/Script Report → Report Print Format (JavaScript!)           │
│                                                                         │
│ ► Automated email with dynamic content?                                 │
│   └── Email Template (Jinja)                                            │
│                                                                         │
│ ► Customer-facing web page?                                             │
│   └── Portal Page (www/*.html + *.py)                                   │
│                                                                         │
│ ► Reusable template functions/filters?                                  │
│   └── Custom jenv methods in hooks.py                                   │
│                                                                         │
│ ► Notification content?                                                 │
│   └── Notification Template (uses Jinja syntax)                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

⚠️ CRITICAL: Report Print Formats use JAVASCRIPT templating, NOT Jinja!
   - Jinja: {{ variable }}
   - JS Report: {%= variable %}
```

---

## Decision Tree: Print Format Type

```
WHAT ARE YOU PRINTING?
│
├─► Standard DocType (Invoice, PO, Quotation)?
│   │
│   │ WHERE TO CREATE?
│   ├─► Quick/simple format → Print Format Builder (Setup > Print)
│   │   - Drag-drop interface
│   │   - Limited customization
│   │
│   └─► Complex layout needed → Custom HTML Print Format
│       - Full Jinja control
│       - Custom CSS styling
│       - Dynamic logic
│
├─► Query Report or Script Report?
│   └─► Report Print Format (JAVASCRIPT template!)
│       ⚠️ NOT Jinja! Uses {%= %} and {% %}
│
└─► Letter or standalone document?
    └─► Letter Head + Print Format combination
```

---

## Decision Tree: Where to Store Template

```
IS THIS A ONE-OFF OR REUSABLE?
│
├─► Site-specific, managed via UI?
│   └─► Create via Setup > Print Format / Email Template
│       - Stored in database
│       - Easy to edit without code
│
├─► Part of your custom app?
│   │
│   │ WHAT TYPE?
│   ├─► Print Format → myapp/fixtures or db records
│   │
│   ├─► Portal Page → myapp/www/pagename/
│   │   - index.html (template)
│   │   - index.py (context)
│   │
│   └─► Custom methods/filters → myapp/jinja/
│       - Registered via hooks.py jenv
│
└─► Template for multiple sites?
    └─► Include in app, export as fixture
```

---

## Implementation Workflow: Print Format

### Step 1: Create via UI (Recommended Start)

```
Setup > Printing > Print Format > New
- DocType: Sales Invoice
- Module: Accounts
- Standard: No (Custom)
- Print Format Type: Jinja
```

### Step 2: Basic Template Structure

```jinja
{# ALWAYS include styles at top #}
<style>
    .print-format { font-family: Arial, sans-serif; }
    .header { background: #f5f5f5; padding: 15px; }
    .table { width: 100%; border-collapse: collapse; }
    .table th, .table td { border: 1px solid #ddd; padding: 8px; }
    .text-right { text-align: right; }
    .footer { margin-top: 30px; border-top: 1px solid #ddd; }
</style>

{# Document header #}
<div class="header">
    <h1>{{ doc.select_print_heading or _("Invoice") }}</h1>
    <p><strong>{{ doc.name }}</strong></p>
    <p>{{ _("Date") }}: {{ doc.get_formatted("posting_date") }}</p>
</div>

{# Items table #}
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

{# Totals #}
<div class="text-right">
    <p><strong>{{ _("Grand Total") }}:</strong> {{ doc.get_formatted("grand_total") }}</p>
</div>
```

### Step 3: Test and Refine

```
1. Open a document (e.g., Sales Invoice)
2. Menu > Print > Select your format
3. Check layout, adjust CSS as needed
4. Test PDF generation
```

---

## Implementation Workflow: Email Template

### Step 1: Create via UI

```
Setup > Email > Email Template > New
- Name: Payment Reminder
- Subject: Invoice {{ doc.name }} - Payment Due
- DocType: Sales Invoice
```

### Step 2: Template Content

```jinja
<p>{{ _("Dear") }} {{ doc.customer_name }},</p>

<p>{{ _("This is a reminder that invoice") }} <strong>{{ doc.name }}</strong>
{{ _("for") }} {{ doc.get_formatted("grand_total") }} {{ _("is due.") }}</p>

<table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
    <tr>
        <td style="padding: 8px; border: 1px solid #ddd;">
            <strong>{{ _("Due Date") }}</strong>
        </td>
        <td style="padding: 8px; border: 1px solid #ddd;">
            {{ frappe.format_date(doc.due_date) }}
        </td>
    </tr>
    <tr>
        <td style="padding: 8px; border: 1px solid #ddd;">
            <strong>{{ _("Outstanding") }}</strong>
        </td>
        <td style="padding: 8px; border: 1px solid #ddd;">
            {{ doc.get_formatted("outstanding_amount") }}
        </td>
    </tr>
</table>

{% if doc.items %}
<p><strong>{{ _("Items") }}:</strong></p>
<ul>
{% for item in doc.items %}
    <li>{{ item.item_name }} ({{ item.qty }})</li>
{% endfor %}
</ul>
{% endif %}

<p>{{ _("Best regards") }},<br>
{{ frappe.db.get_value("Company", doc.company, "company_name") }}</p>
```

### Step 3: Use in Notifications or Code

```python
# In Server Script or Controller
frappe.sendmail(
    recipients=[doc.email],
    subject=frappe.render_template(
        frappe.db.get_value("Email Template", "Payment Reminder", "subject"),
        {"doc": doc}
    ),
    message=frappe.get_template("Payment Reminder").render({"doc": doc})
)
```

---

## Implementation Workflow: Portal Page

### Step 1: Create Directory Structure

```
myapp/
└── www/
    └── projects/
        ├── index.html    # Jinja template
        └── index.py      # Python context
```

### Step 2: Create Template (index.html)

```jinja
{% extends "templates/web.html" %}

{% block title %}{{ _("Projects") }}{% endblock %}

{% block page_content %}
<div class="container">
    <h1>{{ title }}</h1>
    
    {% if frappe.session.user != 'Guest' %}
        <p>{{ _("Welcome") }}, {{ frappe.get_fullname() }}</p>
    {% endif %}
    
    <div class="row">
        {% for project in projects %}
        <div class="col-md-4">
            <div class="card">
                <h3>{{ project.title }}</h3>
                <p>{{ project.description | truncate(100) }}</p>
                <a href="/projects/{{ project.name }}">{{ _("View Details") }}</a>
            </div>
        </div>
        {% else %}
        <p>{{ _("No projects found.") }}</p>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

### Step 3: Create Context (index.py)

```python
import frappe

def get_context(context):
    context.title = "Projects"
    context.no_cache = True  # Dynamic content
    
    # Fetch data
    context.projects = frappe.get_all(
        "Project",
        filters={"is_public": 1},
        fields=["name", "title", "description"],
        order_by="creation desc"
    )
    
    return context
```

### Step 4: Test

```
Visit: https://yoursite.com/projects
```

---

## Implementation Workflow: Custom Jinja Methods

### Step 1: Register in hooks.py

```python
# myapp/hooks.py
jenv = {
    "methods": ["myapp.jinja.methods"],
    "filters": ["myapp.jinja.filters"]
}
```

### Step 2: Create Methods Module

```python
# myapp/jinja/methods.py
import frappe

def get_company_logo(company):
    """Returns company logo URL - usable in any template"""
    return frappe.db.get_value("Company", company, "company_logo") or ""

def get_address_display(address_name):
    """Format address for display"""
    if not address_name:
        return ""
    return frappe.get_doc("Address", address_name).get_display()

def get_outstanding_amount(customer):
    """Get total outstanding for customer"""
    result = frappe.db.sql("""
        SELECT COALESCE(SUM(outstanding_amount), 0)
        FROM `tabSales Invoice`
        WHERE customer = %s AND docstatus = 1
    """, customer)
    return result[0][0] if result else 0
```

### Step 3: Create Filters Module

```python
# myapp/jinja/filters.py

def format_phone(value):
    """Format phone number: 1234567890 → (123) 456-7890"""
    if not value:
        return ""
    digits = ''.join(c for c in str(value) if c.isdigit())
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return value

def currency_words(amount, currency="EUR"):
    """Convert number to words (simplified)"""
    return f"{currency} {amount:,.2f}"
```

### Step 4: Use in Templates

```jinja
{# Methods - called as functions #}
<img src="{{ get_company_logo(doc.company) }}" alt="Logo">
<p>{{ get_address_display(doc.customer_address) }}</p>
<p>Outstanding: {{ get_outstanding_amount(doc.customer) }}</p>

{# Filters - piped after values #}
<p>Phone: {{ doc.phone | format_phone }}</p>
<p>Amount: {{ doc.grand_total | currency_words }}</p>
```

### Step 5: Deploy

```bash
bench --site sitename migrate
```

---

## Quick Reference: Context Variables

| Template Type | Available Objects |
|---------------|-------------------|
| Print Format | `doc`, `frappe`, `_()` |
| Email Template | `doc`, `frappe` (limited) |
| Portal Page | `frappe.session`, `frappe.form_dict`, custom context |
| Notification | `doc`, `frappe` |

---

## Quick Reference: Essential Methods

| Need | Method |
|------|--------|
| Format currency/date | `doc.get_formatted("fieldname")` |
| Format child row | `row.get_formatted("field", doc)` |
| Translate string | `_("String")` |
| Get linked doc | `frappe.get_doc("DocType", name)` |
| Get single field | `frappe.db.get_value("DT", name, "field")` |
| Current date | `frappe.utils.nowdate()` |
| Format date | `frappe.format_date(date)` |

---

## Critical Rules

### 1. ALWAYS use get_formatted for display values

```jinja
{# ❌ Raw database value #}
{{ doc.grand_total }}

{# ✅ Properly formatted with currency #}
{{ doc.get_formatted("grand_total") }}
```

### 2. ALWAYS pass parent doc for child table formatting

```jinja
{% for row in doc.items %}
    {# ❌ Missing currency context #}
    {{ row.get_formatted("rate") }}
    
    {# ✅ Has currency context from parent #}
    {{ row.get_formatted("rate", doc) }}
{% endfor %}
```

### 3. ALWAYS use translation function for user text

```jinja
{# ❌ Not translatable #}
<h1>Invoice</h1>

{# ✅ Translatable #}
<h1>{{ _("Invoice") }}</h1>
```

### 4. NEVER use Jinja in Report Print Formats

```html
<!-- Query/Script Reports use JAVASCRIPT templating -->
{% for(var i=0; i<data.length; i++) { %}
<tr><td>{%= data[i].name %}</td></tr>
{% } %}
```

### 5. NEVER execute queries in loops

```jinja
{# ❌ N+1 query problem #}
{% for item in doc.items %}
    {% set stock = frappe.db.get_value("Bin", ...) %}
{% endfor %}

{# ✅ Prefetch data in controller/context #}
{% for item in items_with_stock %}
    {{ item.stock_qty }}
{% endfor %}
```

---

## Version Differences

| Feature | V14 | V15 | V16 |
|---------|:---:|:---:|:---:|
| Jinja templates | ✅ | ✅ | ✅ |
| get_formatted() | ✅ | ✅ | ✅ |
| jenv hooks | ✅ | ✅ | ✅ |
| wkhtmltopdf PDF | ✅ | ✅ | ⚠️ |
| **Chrome PDF** | ❌ | ❌ | ✅ |

### V16 Chrome PDF Considerations

See `erpnext-syntax-jinja` for detailed Chrome PDF documentation.


---

## Reference Files

| File | Contents |
|------|----------|
| [decision-tree.md](references/decision-tree.md) | Complete template type selection |
| [workflows.md](references/workflows.md) | Step-by-step implementation patterns |
| [examples.md](references/examples.md) | Complete working examples |
| [anti-patterns.md](references/anti-patterns.md) | Common mistakes to avoid |
