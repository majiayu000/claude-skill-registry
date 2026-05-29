---
name: frappe-syntax-print
description: >
  Use when creating print formats or generating PDFs in Frappe v14-v16.
  Covers Jinja print formats, Print Designer [v15+], Letter Head,
  PDF generation API (get_pdf, download_pdf), Report print formats
  ({%= %} syntax), page breaks, and print CSS patterns.
  Prevents common mistakes with template engine confusion and PDF rendering.
  Keywords: print format, PDF, get_pdf, Jinja, Letter Head, print designer,
  wkhtmltopdf, WeasyPrint, page-break, download_pdf.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "3.0"
---

# Frappe Print Formats & PDF Generation

> Deterministic reference for print formats, Letter Head, and PDF generation in Frappe v14/v15/v16.

---

## When to Use This Skill

USE when:
- Creating or modifying Print Formats (Jinja or JS)
- Generating PDFs programmatically (`get_pdf`, download endpoints)
- Configuring Letter Head (header/footer) for print output
- Working with Print Designer (v15+)
- Implementing page breaks, print CSS, or landscape layouts
- Building Report Print Formats ({%= %} syntax)

DO NOT USE for:
- General Jinja template syntax (emails, portals) -- see `frappe-syntax-jinja`
- Client Script UI logic -- see `frappe-syntax-clientscripts`
- Web views or portal pages -- see `frappe-syntax-jinja`

---

## Decision Tree: Which Print Format Type?

```
Need a printable/PDF document?
├─ YES → Is it a Query/Script Report?
│        ├─ YES → Use JS Template ({%= %} microtemplate)
│        │        Set print_format_for = "Report"
│        └─ NO  → Need visual drag-and-drop editor?
│                  ├─ YES → On v15+?
│                  │        ├─ YES → Use Print Designer (WeasyPrint)
│                  │        └─ NO  → NOT available on v14. Use Jinja.
│                  └─ NO  → Need full layout control?
│                           ├─ YES → Use Jinja Print Format (custom_format=1)
│                           └─ NO  → Use Standard Print Format (auto layout)
└─ NO  → This skill does not apply.
```

---

## Print Format Types

| Type | Engine | Version | When to Use |
|------|--------|---------|-------------|
| Standard | Auto from DocType field layout | v14+ | No customization needed |
| Jinja | Server-side Jinja2 (wkhtmltopdf) | v14+ | Full layout control |
| JS Template | Client-side microtemplate | v14+ | Report print formats only |
| Print Designer | WeasyPrint / Chrome | v15+ | Visual drag-and-drop builder |

### Standard Print Format

ALWAYS the default. Frappe auto-generates layout from DocType fields. No code needed. Controlled via Print Settings and field `print_hide` property.

### Jinja Print Format

Set `custom_format = 1` on the Print Format document. Full Jinja2 with server-side rendering.

**Context variables available in every Jinja Print Format:**

| Variable | Type | Content |
|----------|------|---------|
| `doc` | Document | The document being printed |
| `meta` | Meta | DocType metadata |
| `layout` | list | Field layout sections |
| `letter_head` | str | Rendered Letter Head HTML |
| `footer` | str | Rendered footer HTML |
| `print_settings` | dict | Print Settings configuration |
| `frappe` | module | Full frappe module access |

**Example — Minimal Jinja Print Format:**

```html
<h1>{{ doc.name }}</h1>
<p>Customer: {{ doc.customer_name }}</p>
<p>Date: {{ doc.posting_date | global_date_format }}</p>

<table class="table table-bordered">
  <thead>
    <tr><th>Item</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>
  </thead>
  <tbody>
    {% for row in doc.items %}
    <tr>
      <td>{{ row.item_name }}</td>
      <td>{{ row.qty }}</td>
      <td>{{ frappe.utils.fmt_money(row.rate, currency=doc.currency) }}</td>
      <td>{{ frappe.utils.fmt_money(row.amount, currency=doc.currency) }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>

<p><strong>Grand Total:</strong> {{ frappe.utils.fmt_money(doc.grand_total, currency=doc.currency) }}</p>
```

### JS Template (Report Print Formats)

ONLY for Query Reports and Script Reports. Uses `{%= %}` microtemplate syntax, NOT Jinja.

```javascript
// In report's .js file
{%= row.item_name %}
{% if (row.qty > 10) { %}
  <strong>Bulk order</strong>
{% } %}

{% for (var i = 0; i < rows.length; i++) { %}
  <tr>
    <td>{%= rows[i].item_name %}</td>
    <td>{%= rows[i].qty %}</td>
  </tr>
{% } %}
```

**CRITICAL:** NEVER mix Jinja `{{ }}` and JS `{%= %}` syntax. They are completely separate template engines.

### Print Designer (v15+ Only)

- Separate app: `bench get-app print_designer`
- Uses WeasyPrint (not wkhtmltopdf)
- Visual drag-and-drop builder in the browser
- NEVER attempt to use Print Designer on v14 -- it does not exist

---

## Letter Head

Letter Head provides consistent header/footer across all print formats.

### Configuration

| Field | Purpose |
|-------|---------|
| `source` | `"Image"` or `"HTML"` |
| `content` | Header HTML (Jinja-rendered with `doc` context) |
| `footer` | Footer HTML (Jinja-rendered, **PDF only**) |
| `image` | Header image (when source = "Image") |
| `align` | Image alignment: Left, Center, Right |

**IMPORTANT:** The `footer` field only displays in PDF output, never in browser print preview.

### Letter Head in Jinja Templates

```python
# Server-side: render Letter Head programmatically
from frappe.utils.print_format import render_letterhead_for_print

letterhead_html = render_letterhead_for_print(
    letter_head_name="My Company",
    doc=doc
)
```

### Dynamic Letter Head Content

Letter Head `content` and `footer` fields support Jinja with `doc` context:

```html
<!-- In Letter Head content field -->
<div style="text-align: right;">
  <strong>{{ doc.company }}</strong><br>
  Date: {{ doc.posting_date | global_date_format }}
</div>
```

---

## PDF Generation API

> See `references/pdf-api.md` for complete API reference.

### Quick Reference

```python
# Generate PDF bytes from HTML
from frappe.utils.pdf import get_pdf
pdf_bytes = get_pdf(html_string, options=None)

# Generate PDF from a specific document + print format
from frappe.utils.print_format import download_pdf
download_pdf(doctype, name, format=None, doc=None, no_letterhead=0)
```

### Download Endpoints

```
# Single document PDF
GET /api/method/frappe.utils.print_format.download_pdf
    ?doctype=Sales Invoice
    &name=SINV-00001
    &format=My Print Format
    &no_letterhead=0

# Multiple documents in one PDF
GET /api/method/frappe.utils.print_format.download_multi_pdf
    ?doctype=Sales Invoice
    &name=["SINV-00001","SINV-00002"]
    &format=My Print Format
```

### PDF Engine Selection (v15+)

| Engine | When | Config |
|--------|------|--------|
| wkhtmltopdf | Default on v14, fallback on v15+ | Default |
| Chrome | v15+ with Chromium installed | `pdf_generator = "chrome"` on Print Format |
| WeasyPrint | Print Designer formats only | Automatic for Print Designer |

ALWAYS use wkhtmltopdf on v14. On v15+, Chrome produces better CSS3 support.

---

## Page Breaks & Print CSS

### Page Break Classes

```html
<!-- Force page break after this element -->
<div class="page-break"></div>

<!-- Or use CSS directly -->
<div style="page-break-after: always;"></div>

<!-- Page break before -->
<div style="page-break-before: always;"></div>
```

### Print CSS Classes (Frappe Built-in)

| Class | Effect |
|-------|--------|
| `.print-format` | Container: max-width 8.3in, min-height 11.69in (A4 portrait) |
| `.print-format.landscape` | Width 11.69in (A4 landscape) |
| `.page-break` | `page-break-after: always` |
| `.print-heading` | Print title styling |
| `.hidden-pdf` | Hidden in PDF output only |
| `.visible-pdf` | Visible in PDF output only |

### PDF Header/Footer HTML

```python
# In hooks.py — inject header/footer into every PDF
pdf_header_html = "myapp.utils.get_pdf_header"
pdf_body_html = "myapp.utils.get_pdf_body"
pdf_footer_html = "myapp.utils.get_pdf_footer"
```

```html
<!-- Header/footer elements in print format HTML -->
<div id="header-html">
  <span class="page"></span> of <span class="topage"></span>
</div>

<div id="footer-html">
  <p style="text-align: center; font-size: 9px;">
    Printed on {{ frappe.utils.nowdate() }}
  </p>
</div>
```

### Print CSS Best Practices

```css
/* ALWAYS use relative units for print widths */
@media print {
  .print-format {
    max-width: 100%;
    margin: 0;
    padding: 15mm;
  }

  /* Prevent table rows from splitting across pages */
  tr {
    page-break-inside: avoid;
  }

  /* Constrain images */
  img {
    max-width: 100%;
    height: auto;
  }
}
```

---

## Custom App Print Formats

### Ship a Print Format with Your App

```
myapp/
└── mymodule/
    └── print_format/
        └── my_custom_format/
            ├── my_custom_format.json   # Print Format doc
            └── my_custom_format.html   # Jinja template
```

**In the JSON file, ALWAYS set:**

```json
{
  "doctype": "Print Format",
  "name": "My Custom Format",
  "doc_type": "Sales Invoice",
  "module": "My Module",
  "standard": "Yes",
  "custom_format": 1,
  "print_format_type": "Jinja"
}
```

ALWAYS set `standard = "Yes"` and `module` for app-shipped print formats. This ensures they are recognized as part of the app and not as site-level customizations.

---

## Jinja Filters for Print Formats

| Filter | Purpose | Example |
|--------|---------|---------|
| `global_date_format` | Format date per system settings | `{{ doc.posting_date \| global_date_format }}` |
| `json` | Serialize to JSON string | `{{ doc.items \| json }}` |
| `len` | Get length | `{{ doc.items \| len }}` |
| `int` | Cast to integer | `{{ value \| int }}` |
| `flt` | Cast to float | `{{ value \| flt }}` |
| `markdown` | Render Markdown to HTML | `{{ doc.description \| markdown }}` |
| `abs` | Absolute value | `{{ value \| abs }}` |

### Register Custom Jinja Filters/Methods

```python
# In hooks.py
jinja = {
    "methods": [
        "myapp.utils.jinja.my_custom_method"
    ],
    "filters": [
        "myapp.utils.jinja.my_custom_filter"
    ]
}
```

```python
# myapp/utils/jinja.py
def my_custom_method(value):
    """Available as {{ my_custom_method(doc.field) }} in templates."""
    return value.upper()

def my_custom_filter(value, arg=None):
    """Available as {{ doc.field | my_custom_filter }} in templates."""
    return f"[{value}]"
```

---

## Version Compatibility Matrix

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| Jinja Print Formats | Yes | Yes | Yes |
| JS Report Templates | Yes | Yes | Yes |
| Standard Print Formats | Yes | Yes | Yes |
| Letter Head (Image/HTML) | Yes | Yes | Yes |
| wkhtmltopdf | Default | Fallback | Fallback |
| Chrome PDF engine | No | Yes | Yes |
| WeasyPrint | No | Yes | Yes |
| Print Designer app | No | Yes | Yes |
| `pdf_header_html` hook | Yes | Yes | Yes |
| `download_multi_pdf` | Yes | Yes | Yes |

---

## Common Anti-Patterns

> See `references/anti-patterns.md` for the complete list with fixes.

1. **NEVER** use `{{ }}` in Report Print Formats -- they use `{%= %}` (JS microtemplate)
2. **NEVER** call `frappe.get_doc()` inside a `{% for %}` loop in templates -- causes N+1 queries
3. **NEVER** put heavy business logic in Jinja templates -- move to Python and pass results
4. **NEVER** hardcode page dimensions in CSS -- use `.print-format` class or relative units
5. **NEVER** ignore the `no_letterhead` parameter when generating PDFs programmatically
6. **NEVER** use Print Designer on v14 -- it requires v15+
7. **NEVER** embed large base64 images in print templates -- use URLs with `max-width: 100%`

---

## Reference Files

- [Jinja Print Formats](references/jinja-print-formats.md) -- Jinja syntax, variables, filters, macros
- [PDF API](references/pdf-api.md) -- get_pdf(), download endpoints, page breaks, hooks
- [Anti-Patterns](references/anti-patterns.md) -- Common print format mistakes with fixes
