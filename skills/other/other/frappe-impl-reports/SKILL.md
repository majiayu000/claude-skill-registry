---
name: frappe-impl-reports
description: >
  Use when building Script Reports, Query Reports, dashboard charts, or Number Cards in ERPNext.
  Prevents empty report output from wrong column definitions, broken filters, and unoptimized SQL in large datasets.
  Covers Report Builder, Script Report (Python + JS), Query Report, Report filters, dashboard Chart DocType, Number Card, report permissions.
  Keywords: report, Script Report, Query Report, dashboard, chart, Number Card, filters, columns, execute, get_data.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Report Building

## Quick Reference

| Report Type | Best For | Access | Files |
|---|---|---|---|
| Query Report | Simple SQL queries | System Manager only | SQL in DocType or `.py` |
| Script Report | Complex logic, charts | Administrator + Dev Mode | `.py` + `.js` |
| Report Builder | End-user ad-hoc reports | Any permitted user | UI only |
| Prepared Report | Large datasets (>100k rows) | Same as source report | Background job |

## Decision Tree: Which Report Type?

```
Need a report?
├─ End user builds it themselves? → Report Builder
├─ Simple SQL with no Python logic? → Query Report
├─ Complex logic / charts / summary? → Script Report
│   └─ Dataset > 100k rows or timeout? → Add prepared_report = True
└─ Real-time KPI on workspace? → Number Card or Dashboard Chart
```

## 1. Creating a Script Report

### File Structure

```
my_app/my_module/report/sales_summary/
├── sales_summary.json    # Report DocType definition
├── sales_summary.py      # Python: execute() function
└── sales_summary.js      # JavaScript: filters + config
```

ALWAYS create via Desk: Report > New > Script Report > set "Is Standard = Yes" in Developer Mode.

### Python: The execute() Function

```python
# sales_summary.py
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    report_summary = get_summary(data)
    return columns, data, None, chart, report_summary

def get_columns():
    return [
        {"fieldname": "customer", "label": _("Customer"), "fieldtype": "Link",
         "options": "Customer", "width": 200},
        {"fieldname": "total", "label": _("Total"), "fieldtype": "Currency",
         "options": "currency", "width": 120},
        {"fieldname": "qty", "label": _("Qty"), "fieldtype": "Int", "width": 80},
        {"fieldname": "posting_date", "label": _("Date"), "fieldtype": "Date", "width": 100},
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql("""
        SELECT
            si.customer, SUM(si.grand_total) as total,
            SUM(si.total_qty) as qty, si.posting_date
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1 {conditions}
        GROUP BY si.customer
        ORDER BY total DESC
    """.format(conditions=conditions), filters, as_dict=True)

def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND si.posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND si.posting_date <= %(to_date)s"
    if filters.get("company"):
        conditions += " AND si.company = %(company)s"
    return conditions
```

**Return value order** (positional — ALWAYS maintain this order):

| Position | Name | Type | Required |
|---|---|---|---|
| 1 | `columns` | list[dict] | YES |
| 2 | `data` | list[dict] or list[list] | YES |
| 3 | `message` | str or None | NO |
| 4 | `chart` | dict or None | NO |
| 5 | `report_summary` | list[dict] or None | NO |
| 6 | `skip_total_rows` | bool | NO |

### JavaScript: Filters

```javascript
// sales_summary.js
frappe.query_reports["Sales Summary"] = {
    filters: [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("company"),
            reqd: 1
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1
        },
        {
            fieldname: "customer_group",
            label: __("Customer Group"),
            fieldtype: "Link",
            options: "Customer Group",
            depends_on: "eval:doc.company"
        }
    ],
    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (column.fieldname === "total" && data.total > 100000) {
            value = "<span style='color:green;font-weight:bold'>" + value + "</span>";
        }
        return value;
    }
};
```

## 2. Creating a Query Report

Query Reports use raw SQL. ALWAYS use the legacy column format in SQL aliases:

```sql
SELECT
    `tabWork Order`.name AS "Work Order:Link/Work Order:200",
    `tabWork Order`.creation AS "Date:Date:120",
    `tabWork Order`.company AS "Company:Link/Company:150",
    `tabWork Order`.qty AS "Qty:Int:80",
    `tabWork Order`.grand_total AS "Total:Currency:120"
FROM `tabWork Order`
WHERE `tabWork Order`.docstatus = 1
ORDER BY `tabWork Order`.creation DESC
```

**Column format**: `"Label:Fieldtype/Options:Width"`

Use `%(filter_name)s` for filter variables in WHERE clauses.

## 3. Adding Charts to Reports

Return a chart dict as the 4th element from `execute()`:

```python
def get_chart(data):
    labels = [d.customer for d in data[:10]]
    values = [d.total for d in data[:10]]
    return {
        "data": {
            "labels": labels,
            "datasets": [{"name": _("Revenue"), "values": values}]
        },
        "type": "bar",            # bar | line | pie | donut | percentage
        "colors": ["#7cd6fd"],
        "barOptions": {"stacked": False},  # for bar charts
        "height": 300
    }
```

**Chart types**: `bar`, `line`, `pie`, `donut`, `percentage`.

For multi-dataset charts (e.g., comparing periods):
```python
"datasets": [
    {"name": "2024", "values": [10, 20, 30]},
    {"name": "2025", "values": [15, 25, 35]}
]
```

## 4. Adding Report Summary

Return a list of summary dicts as the 5th element:

```python
def get_summary(data):
    total_revenue = sum(d.total for d in data)
    total_qty = sum(d.qty for d in data)
    return [
        {"value": total_revenue, "label": _("Total Revenue"),
         "datatype": "Currency", "currency": "USD",
         "indicator": "Green" if total_revenue > 0 else "Red"},
        {"value": total_qty, "label": _("Total Qty"),
         "datatype": "Int", "indicator": "Blue"},
        {"value": len(data), "label": _("Customers"),
         "datatype": "Int", "indicator": "Grey"}
    ]
```

**Indicator colors**: `Green`, `Blue`, `Orange`, `Red`, `Grey`.

## 5. Prepared Reports

For reports that timeout on large datasets, add to the `.js` file:

```javascript
frappe.query_reports["Heavy Report"] = {
    filters: [ /* ... */ ],
    prepared_report: true    // enables background generation
};
```

When `prepared_report: true`, Frappe queues the report via background job. Users see cached results and can regenerate on demand.

## 6. Number Cards

Three types of Number Cards for workspace dashboards:

| Type | Source | Use Case |
|---|---|---|
| Document Type | DocType aggregate | Count/sum of documents |
| Report | Script/Query Report | KPI from report data |
| Custom | Whitelisted method | Any computed value |

### Document Type Number Card
Create via Desk > Number Card. Set DocType, aggregate function (Count/Sum/Avg), and filters.

### Report-Based Number Card
Point to an existing report. The card displays the first row's first numeric column.

### Custom Method Number Card
```python
# In your app, create a whitelisted method:
@frappe.whitelist()
def get_open_tickets():
    count = frappe.db.count("Issue", {"status": "Open"})
    return {"value": count, "fieldtype": "Int", "route_options": {"status": "Open"},
            "route": ["query-report", "Open Issues"]}
```

## 7. Dashboard Charts

Create via Desk > Dashboard Chart or programmatically in fixtures:

```python
# hooks.py
fixtures = [
    {"dt": "Dashboard Chart", "filters": [["module", "=", "My Module"]]}
]
```

**Source types**: Report, Group By, Custom (whitelisted method).

### Group By Chart
```json
{
    "chart_name": "Invoices by Status",
    "chart_type": "Group By",
    "document_type": "Sales Invoice",
    "group_by_type": "Count",
    "group_by_based_on": "status",
    "type": "Donut",
    "filters_json": "{\"docstatus\": 1}"
}
```

## 8. Building a Dashboard

Dashboards combine multiple charts and Number Cards:

```json
{
    "name": "Sales Dashboard",
    "module": "Selling",
    "charts": [
        {"chart": "Monthly Revenue", "width": "Full"},
        {"chart": "Invoices by Status", "width": "Half"},
        {"chart": "Top Customers", "width": "Half"}
    ],
    "cards": [
        {"card": "Total Revenue"},
        {"card": "Open Orders"}
    ]
}
```

## 9. Performance Optimization

- ALWAYS add indexes on columns used in WHERE/GROUP BY (`frappe.model.utils.add_index`)
- ALWAYS use `as_dict=True` in `frappe.db.sql()` — matches column fieldnames
- NEVER use `SELECT *` — specify exact columns
- NEVER load full documents (`frappe.get_doc`) inside report loops — use SQL
- Use `frappe.qb` (query builder) for parameterized queries in v14+
- For reports > 50k rows, ALWAYS enable `prepared_report: true`
- ALWAYS filter by `docstatus` to exclude draft/cancelled documents

## 10. Common Patterns

### Date Range Filter Pattern
```python
if filters.get("from_date") and filters.get("to_date"):
    conditions += " AND posting_date BETWEEN %(from_date)s AND %(to_date)s"
```

### Multi-Currency Pattern
```python
{"fieldname": "amount", "label": _("Amount"), "fieldtype": "Currency",
 "options": "currency", "width": 120}
# "options": "currency" means use the row's "currency" field for formatting
```

### Group By with Totals Pattern
```python
data = frappe.db.sql("""
    SELECT customer, COUNT(*) as count, SUM(grand_total) as total
    FROM `tabSales Invoice`
    WHERE docstatus = 1 {conditions}
    GROUP BY customer WITH ROLLUP
""".format(conditions=conditions), filters, as_dict=True)
```

## See Also

- [references/examples.md](references/examples.md) — Complete report examples
- [references/anti-patterns.md](references/anti-patterns.md) — Common mistakes
- [references/workflows.md](references/workflows.md) — Step-by-step workflows
- `frappe-syntax-api` — Frappe Python API reference
- `frappe-core-database` — Database query patterns
