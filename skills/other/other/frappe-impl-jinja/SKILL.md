---
name: frappe-impl-jinja
description: >
  Use when building Jinja templates in Frappe: Print Formats, Email
  Templates, Notification templates, Portal Pages, and custom Jinja
  methods. Covers template creation workflows, child table handling,
  conditional sections, styling, multi-language support, and debugging.
  Prevents N+1 queries, wrong formatting, and Report Print confusion.
  Keywords: create print format, email template, portal page, pdf
  template, invoice template, jinja methods, notification template,
  web page template, print format styling.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Jinja Templates Implementation Workflow

Step-by-step workflows for building Jinja templates. For syntax reference, see `frappe-syntax-jinja`.

**Version**: v14/v15/v16 (V16 Chrome PDF noted)

---

## Master Decision: What Are You Creating?

```
WHAT IS YOUR OUTPUT?
│
├─► Printable PDF (invoice, PO, report)?
│   ├─► Standard DocType → Print Format (Jinja)
│   └─► Query/Script Report → Report Print Format (JAVASCRIPT!)
│       ⚠️ Uses {%= %} NOT {{ }}
│
├─► Automated email with dynamic content?
│   └─► Email Template (Jinja, linked to DocType)
│
├─► System notification?
│   └─► Notification (Setup > Notification, uses Jinja)
│
├─► Customer-facing web page?
│   └─► Portal Page (myapp/www/*.html + *.py)
│
└─► Reusable template functions/filters?
    └─► Custom jenv methods in hooks.py
```

---

## Workflow 1: Create a Print Format

### Step 1: Create via UI

```
Setup > Printing > Print Format > New
- Name: My Invoice Format
- DocType: Sales Invoice
- Module: Accounts
- Standard: No (custom)
- Print Format Type: Jinja
```

### Step 2: Write the Template

```jinja
<style>
    .print-format { font-family: Arial, sans-serif; font-size: 11px; }
    .header { margin-bottom: 20px; }
    .table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    .table th, .table td { border: 1px solid #ddd; padding: 8px; }
    .table th { background: #f0f0f0; }
    .text-right { text-align: right; }
</style>

<div class="header">
    <h1>{{ doc.select_print_heading or _("Invoice") }}</h1>
    <p><strong>{{ doc.name }}</strong> |
       {{ doc.get_formatted("posting_date") }}</p>
</div>

<p><strong>{{ doc.customer_name }}</strong></p>
{% if doc.address_display %}
    <p>{{ doc.address_display | safe }}</p>
{% endif %}

<table class="table">
    <thead>
        <tr>
            <th>#</th>
            <th>{{ _("Item") }}</th>
            <th class="text-right">{{ _("Qty") }}</th>
            <th class="text-right">{{ _("Rate") }}</th>
            <th class="text-right">{{ _("Amount") }}</th>
        </tr>
    </thead>
    <tbody>
        {% for row in doc.items %}
        <tr>
            <td>{{ row.idx }}</td>
            <td>{{ row.item_name }}</td>
            <td class="text-right">{{ row.qty }}</td>
            <td class="text-right">{{ row.get_formatted("rate", doc) }}</td>
            <td class="text-right">{{ row.get_formatted("amount", doc) }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

{% for tax in doc.taxes %}
<p class="text-right">{{ tax.description }}: {{ tax.get_formatted("tax_amount", doc) }}</p>
{% endfor %}

<p class="text-right">
    <strong>{{ _("Grand Total") }}: {{ doc.get_formatted("grand_total") }}</strong>
</p>

{% if doc.terms %}
<div style="margin-top: 30px; border-top: 1px solid #ddd; padding-top: 10px;">
    <strong>{{ _("Terms and Conditions") }}</strong>
    {{ doc.terms | safe }}
</div>
{% endif %}
```

### Step 3: Test

1. Open a Sales Invoice
2. Menu > Print > Select "My Invoice Format"
3. Verify layout and formatting
4. **ALWAYS** test PDF download — wkhtmltopdf renders differently from browser

### Critical Rules for Print Formats

- **ALWAYS** use `doc.get_formatted("field")` for currency, dates, numbers
- **ALWAYS** pass parent doc for child rows: `row.get_formatted("rate", doc)`
- **ALWAYS** wrap user-facing text with `_("text")` for translation
- **ALWAYS** put CSS in a `<style>` block at the top (not external files)
- **NEVER** use flexbox in v14/v15 (wkhtmltopdf does not support it) — V16 Chrome PDF does
- **NEVER** use `| safe` on user-supplied input — only on trusted system HTML

---

## Workflow 2: Create an Email Template

### Step 1: Create via UI

```
Setup > Email > Email Template > New
- Name: Payment Reminder
- Subject: Invoice {{ doc.name }} - Payment Reminder
- DocType: Sales Invoice
```

### Step 2: Write Email Content

**ALWAYS** use inline styles for emails — most clients strip `<style>` blocks.

```jinja
<div style="font-family: Arial, sans-serif; max-width: 600px;">
    <p>{{ _("Dear") }} {{ doc.customer_name }},</p>

    <p>{{ _("Invoice") }} <strong>{{ doc.name }}</strong>
    {{ _("for") }} {{ doc.get_formatted("grand_total") }}
    {{ _("is due for payment.") }}</p>

    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
        <tr style="background: #f5f5f5;">
            <td style="padding: 10px; border: 1px solid #ddd;">
                <strong>{{ _("Due Date") }}</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">
                {{ frappe.format_date(doc.due_date) }}</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">
                <strong>{{ _("Outstanding") }}</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd; color: #c00;">
                {{ doc.get_formatted("outstanding_amount") }}</td>
        </tr>
    </table>

    {% if doc.items %}
    <p><strong>{{ _("Items") }}:</strong></p>
    <ul>
    {% for item in doc.items[:5] %}
        <li>{{ item.item_name }} ({{ item.qty }})</li>
    {% endfor %}
    {% if doc.items | length > 5 %}
        <li style="color: #666;">{{ _("and {0} more...").format(doc.items|length - 5) }}</li>
    {% endif %}
    </ul>
    {% endif %}

    <p>{{ _("Best regards") }},<br>
    {{ frappe.db.get_value("Company", doc.company, "company_name") }}</p>
</div>
```

### Step 3: Use in Notification or Code

**Option A: Auto-triggered Notification**

```
Setup > Notification > New
- Channel: Email
- Document Type: Sales Invoice
- Send Alert On: Days After (7 days after due_date)
- Condition: doc.outstanding_amount > 0
- Email Template: Payment Reminder
```

**Option B: Send from code**

```python
template = frappe.get_doc("Email Template", "Payment Reminder")
frappe.sendmail(
    recipients=[doc.contact_email],
    subject=frappe.render_template(template.subject, {"doc": doc}),
    message=frappe.render_template(template.response, {"doc": doc}),
    reference_doctype=doc.doctype,
    reference_name=doc.name
)
```

---

## Workflow 3: Create a Notification Template

### Step 1: Create via UI

```
Setup > Notification > New
- Name: Low Stock Alert
- Channel: Email (or Slack, System Notification)
- Document Type: Stock Ledger Entry
- Send Alert On: Method (on change)
- Condition: doc.actual_qty < 10
```

### Step 2: Write Message (Jinja)

```jinja
<h3>{{ _("Low Stock Alert") }}</h3>
<p>{{ _("Item") }}: <strong>{{ doc.item_code }}</strong></p>
<p>{{ _("Warehouse") }}: {{ doc.warehouse }}</p>
<p>{{ _("Current Stock") }}: {{ doc.actual_qty }}</p>
<p>{{ _("Please reorder.") }}</p>
```

---

## Workflow 4: Create a Portal Page

### Step 1: Create directory structure

```
myapp/
└── www/
    └── my-orders/
        ├── index.html    # Jinja template
        └── index.py      # Python context
```

### Step 2: Create context (index.py)

```python
import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect

    context.title = "My Orders"
    context.no_cache = True

    customer = frappe.db.get_value("Contact",
        {"user": frappe.session.user}, "link_name")

    context.orders = frappe.get_all("Sales Order",
        filters={"customer": customer, "docstatus": ["!=", 2]},
        fields=["name", "transaction_date", "grand_total", "status"],
        order_by="transaction_date desc",
        limit=50
    ) if customer else []

    return context
```

### Step 3: Create template (index.html)

```jinja
{% extends "templates/web.html" %}

{% block title %}{{ _("My Orders") }}{% endblock %}

{% block page_content %}
<div class="container my-4">
    <h1>{{ _("My Orders") }}</h1>

    {% if orders %}
    <table class="table table-hover">
        <thead>
            <tr>
                <th>{{ _("Order") }}</th>
                <th>{{ _("Date") }}</th>
                <th>{{ _("Status") }}</th>
                <th class="text-right">{{ _("Total") }}</th>
            </tr>
        </thead>
        <tbody>
            {% for order in orders %}
            <tr>
                <td><a href="/orders/{{ order.name }}">{{ order.name }}</a></td>
                <td>{{ frappe.format_date(order.transaction_date) }}</td>
                <td>{{ order.status }}</td>
                <td class="text-right">
                    {{ frappe.format(order.grand_total, {"fieldtype": "Currency"}) }}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p class="text-muted">{{ _("No orders found.") }}</p>
    {% endif %}
</div>
{% endblock %}
```

### Step 4: Test at `https://yoursite.com/my-orders`

---

## Workflow 5: Register Custom Jinja Methods

### Step 1: Add to hooks.py

```python
jenv = {
    "methods": ["myapp.jinja_utils.methods"],
    "filters": ["myapp.jinja_utils.filters"]
}
```

### Step 2: Create methods module

```python
# myapp/jinja_utils/methods.py
import frappe

def get_company_logo(company):
    """Usage: {{ get_company_logo(doc.company) }}"""
    return frappe.db.get_value("Company", company, "company_logo") or ""

def format_address(address_name):
    """Usage: {{ format_address(doc.customer_address) | safe }}"""
    if not address_name:
        return ""
    return frappe.get_doc("Address", address_name).get_display()
```

### Step 3: Create filters module

```python
# myapp/jinja_utils/filters.py
def phone_format(value):
    """Usage: {{ doc.phone | phone_format }}"""
    if not value:
        return ""
    digits = ''.join(c for c in str(value) if c.isdigit())
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return value
```

### Step 4: Deploy

```bash
bench --site sitename migrate
bench --site sitename clear-cache
```

### Critical Rules for Custom Jinja Methods

- Custom methods should be **READ-ONLY** — **NEVER** write to database or commit
- **ALWAYS** handle None/empty input gracefully (return empty string)
- **NEVER** call slow external APIs — templates must render fast

---

## Workflow 6: Debug a Template

### Template Not Rendering?

```jinja
<!-- Step 1: Check if doc is available -->
<!-- DEBUG: {{ doc.name if doc else 'NO DOC' }} -->

<!-- Step 2: Check child table -->
<!-- DEBUG: items count = {{ doc.items | length if doc.items else 0 }} -->

<!-- Step 3: Check specific field -->
<!-- DEBUG: grand_total = {{ doc.grand_total }} -->
```

### Common Debugging Steps

1. Check **Error Log** (Setup > Error Log) for template exceptions
2. Use `frappe.render_template(template_string, {"doc": doc})` in bench console
3. For Print Formats: Menu > Print > check browser console for errors
4. For Portal Pages: check Python context — add `frappe.logger().info(context)` in `get_context`

### Common Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| Blank output | Wrong template type (Jinja in Report) | Reports use JS: `{%= %}` |
| "None" displayed | Field is null | Use `\| default('')` |
| Wrong currency format | Missing parent doc context | Use `row.get_formatted("rate", doc)` |
| HTML showing as text | Auto-escaping | Add `\| safe` (trusted content only) |
| Translations not working | Missing `_()` wrapper | Wrap all strings: `{{ _("text") }}` |

---

## Quick Patterns: Child Tables, Conditionals, Translation

```jinja
{# Child tables — ALWAYS pass parent doc for formatting context #}
{% for row in doc.items %}
  {{ row.get_formatted("rate", doc) }}  {# Correct: has currency context #}
{% endfor %}

{# Conditional sections #}
{% if doc.shipping_address_name %}
  {{ doc.shipping_address | safe }}
{% endif %}

{# Translation — ALWAYS wrap user-facing text #}
{{ _("Invoice") }}
{{ _("Page {0} of {1}").format(page, total_pages) }}
{{ doc.get_formatted("grand_total") }}  {# Auto-formats per locale #}
```

---

## Styling/CSS in Print Formats

```css
@page { margin: 1.5cm; }
.avoid-break { page-break-inside: avoid; }
thead { display: table-header-group; }   /* Repeat header on pages */
.page-break { page-break-before: always; }
/* V14/V15: NO flexbox (wkhtmltopdf). V16 Chrome PDF: flexbox OK */
.layout { display: table; width: 100%; }
.col { display: table-cell; vertical-align: top; }
```

---

## Context Variables Quick Reference

| Template Type | Available Objects |
|---------------|-------------------|
| Print Format | `doc`, `frappe`, `_()`, `frappe.format()` |
| Email Template | `doc`, `frappe` (limited), `_()` |
| Notification | `doc`, `frappe`, event data |
| Portal Page | `frappe.session`, `frappe.form_dict`, custom context |

---

## Version Differences

| Feature | V14 | V15 | V16 |
|---------|:---:|:---:|:---:|
| Jinja templates | Yes | Yes | Yes |
| get_formatted() | Yes | Yes | Yes |
| jenv hooks | Yes | Yes | Yes |
| wkhtmltopdf PDF | Yes | Yes | Deprecated |
| **Chrome PDF** | No | No | **Yes** |

> V16 Chrome PDF supports modern CSS (flexbox, grid, CSS variables). See `frappe-syntax-jinja` for details.

---

## Reference Files

| File | Contents |
|------|----------|
| [decision-tree.md](references/decision-tree.md) | Complete template type selection flowcharts |
| [print-format-decision.md](references/print-format-decision.md) | Jinja vs Print Designer vs JS Microtemplate decision tree |
| [workflows.md](references/workflows.md) | Step-by-step patterns for all template types |
| [examples.md](references/examples.md) | Production-ready templates (invoice, email, portal) |
