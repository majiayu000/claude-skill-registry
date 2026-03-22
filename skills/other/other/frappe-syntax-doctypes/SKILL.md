---
name: frappe-syntax-doctypes
description: >
  Use when creating or modifying DocType JSON definitions, choosing fieldtypes, configuring naming rules, adding child tables, or setting up tree structures.
  Prevents invalid DocType configurations from wrong fieldtype choices, broken naming rules, and misconfigured child table links.
  Covers DocType JSON schema, all fieldtypes and their properties, autoname/naming_rule patterns, child table (Table fieldtype), tree DocTypes, virtual DocTypes, Single DocTypes.
  Keywords: DocType, fieldtype, naming_rule, autoname, child table, tree, virtual DocType, Single, JSON definition.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# DocType JSON Design

DocTypes are the foundation of every Frappe application. A DocType defines both the **data model** (database schema) and the **view** (form layout). ALWAYS design DocTypes before writing any controller logic.

## Quick Reference

### DocType JSON Top-Level Properties

| Property | Type | Purpose |
|----------|------|---------|
| `name` | str | DocType identifier (singular, e.g. "Sales Invoice") |
| `module` | str | App module this DocType belongs to |
| `is_submittable` | bool | Enables Draft -> Submitted -> Cancelled workflow |
| `is_tree` | bool | Enables NestedSet hierarchy (lft/rgt columns) |
| `is_virtual` | bool | No database table; data from custom backend |
| `issingle` | bool | Single-instance settings document |
| `istable` | bool | Child table DocType (embedded in parent) |
| `is_calendar_and_gantt` | bool | Enables calendar/gantt views |
| `track_changes` | bool | Stores version history on every save |
| `track_seen` | bool | Tracks which users viewed the document |
| `track_views` | bool | Counts total document views |
| `allow_rename` | bool | Permits renaming after creation |
| `allow_copy` | bool | Enables "Duplicate" action |
| `allow_import` | bool | Enables Data Import for this DocType |
| `naming_rule` | str | Naming method selector (see Naming section) |
| `autoname` | str | Naming pattern string |
| `title_field` | str | Field used as display title |
| `search_fields` | str | Comma-separated fields for search results |
| `show_title_field_in_link` | bool | Display title instead of name in Link fields |
| `image_field` | str | Field containing image for avatar display |
| `sort_field` | str | Default sort column |
| `sort_order` | str | "ASC" or "DESC" |
| `default_print_format` | str | Print Format name |
| `max_attachments` | int | Attachment limit |

### Common Fieldtypes (Quick Lookup)

| Fieldtype | Stores | DB Column |
|-----------|--------|-----------|
| Data | Text up to 140 chars | VARCHAR(140) |
| Link | Reference to another DocType | VARCHAR(140) |
| Dynamic Link | Reference to any DocType | VARCHAR(140) |
| Select | Single choice from options | VARCHAR(140) |
| Table | Child table rows | Separate table |
| Table MultiSelect | Multi-select link rows | Separate table |
| Check | Boolean 0/1 | TINYINT |
| Int | Whole number | INT |
| Float | Decimal (9 places) | DECIMAL |
| Currency | Money value (6 decimals) | DECIMAL |
| Date | Calendar date | DATE |
| Datetime | Date + time | DATETIME |
| Text Editor | Rich text (HTML) | LONGTEXT |
| Attach | File reference | VARCHAR(140) |
| Small Text | Short multi-line text | TEXT |
| Long Text | Unlimited text | LONGTEXT |

> Full fieldtype reference with all 35+ types: [references/fieldtypes.md](references/fieldtypes.md)

### Essential Field Properties

| Property | Type | Purpose |
|----------|------|---------|
| `reqd` | bool | Field is mandatory |
| `unique` | bool | Database UNIQUE constraint |
| `search_index` | bool | Database INDEX for faster queries |
| `in_list_view` | bool | Show in list view columns |
| `in_standard_filter` | bool | Show as filter in list view |
| `in_preview` | bool | Show in document preview |
| `allow_on_submit` | bool | Editable after submission |
| `read_only` | bool | Not editable by user |
| `hidden` | bool | Not visible on form |
| `depends_on` | str | Visibility condition (e.g. `eval:doc.status=="Active"`) |
| `mandatory_depends_on` | str | Conditional mandatory |
| `read_only_depends_on` | str | Conditional read-only |
| `fetch_from` | str | Auto-populate from linked doc (e.g. `customer.customer_name`) |
| `fetch_if_empty` | bool | Only fetch when field is empty |
| `options` | str | Fieldtype-specific (DocType name, select options, etc.) |
| `default` | str | Default value (supports `__user`, `Today`, etc.) |
| `description` | str | Help text below field |
| `collapsible` | bool | Section starts collapsed (Section Break only) |

## Decision Tree: Which DocType Type?

```
Need to store data?
├─ YES: Need multiple records?
│  ├─ YES: Need submit/cancel workflow?
│  │  ├─ YES → Standard DocType + is_submittable=1
│  │  └─ NO: Need hierarchy/tree?
│  │     ├─ YES → Tree DocType (is_tree=1)
│  │     └─ NO: Embedded in parent?
│  │        ├─ YES → Child DocType (istable=1)
│  │        └─ NO → Standard DocType
│  └─ NO: Single config/settings → Single DocType (issingle=1)
└─ NO: Data from external source → Virtual DocType (is_virtual=1)
```

## Naming Rules

ALWAYS set `naming_rule` on the DocType. The `autoname` field holds the pattern.

| naming_rule Value | autoname Pattern | Example Output |
|-------------------|------------------|----------------|
| Set by User | _(empty)_ | User types name manually |
| Autoincrement | _(empty)_ | `1`, `2`, `3` |
| By Fieldname | `field:{fieldname}` | Value of that field |
| By Naming Series | `naming_series:` | `INV-2024-00001` (from series field) |
| Expression | `PRE-.#####` | `PRE-00001`, `PRE-00002` |
| Expression (Old Style) | `{prefix}-{YYYY}-{#####}` | `INV-2024-00001` |
| Random | `hash` | Random 10-char string |
| UUID | _(empty)_ | `550e8400-e29b-...` |
| By Script | _(custom)_ | Controller `autoname()` decides |

> NEVER use Autoincrement in production -- gaps appear when records are deleted. Use Expression or Naming Series instead.

> Full naming reference: [references/naming.md](references/naming.md)

## Child Table Design

A Child DocType is a DocType with `istable=1`. It ALWAYS belongs to a parent.

**Parent side** -- add a field with:
- `fieldtype`: `Table` (or `Table MultiSelect`)
- `options`: Child DocType name

**Child records automatically get**:
- `parent` -- name of the parent document
- `parenttype` -- DocType of the parent
- `parentfield` -- fieldname of the Table field in parent
- `idx` -- row order (1-based)

```python
# Adding child rows programmatically
doc = frappe.get_doc("Sales Invoice", "INV-001")
doc.append("items", {
    "item_code": "ITEM-001",
    "qty": 5,
    "rate": 100.0
})
doc.save()
```

> NEVER create a Child DocType without `istable=1`. NEVER reference a non-child DocType in a Table field.

### Table vs Table MultiSelect

| Aspect | Table | Table MultiSelect |
|--------|-------|-------------------|
| UI | Full editable grid with "Add Row" | Tag-style picker, no "Add Row" |
| Child DocType | Full child with many fields | Typically 1 Link field only |
| Use case | Line items, detail rows | Multi-select references |

## Single DocType (Settings Pattern)

Set `issingle=1`. Data is stored in `tabSingles` as key-value pairs, NOT in a dedicated table.

```python
# Access Single DocType
settings = frappe.get_single("My Settings")
value = settings.some_field

# Or directly
value = frappe.db.get_single_value("My Settings", "some_field")
```

- NEVER expect a list view for Single DocTypes -- they have exactly one instance.
- ALWAYS use for app-wide configuration (API keys, default values, feature toggles).

## Tree DocType (NestedSet)

Set `is_tree=1`. Frappe adds `lft`, `rgt`, `parent_{doctype_fieldname}`, `old_parent` columns automatically.

- ALWAYS define a `parent_field` in the DocType JSON (e.g. `parent_account` for Chart of Accounts).
- The NestedSet model uses `lft`/`rgt` integers for efficient subtree queries.
- NEVER manually edit `lft`/`rgt` values. Use `frappe.utils.nestedset.rebuild_tree()` if corrupted.

```python
# Get all descendants
descendants = frappe.get_all("Account",
    filters={"lft": [">", node.lft], "rgt": ["<", node.rgt]})

# Get ancestors (path to root)
ancestors = frappe.get_all("Account",
    filters={"lft": ["<", node.lft], "rgt": [">", node.rgt]},
    order_by="lft asc")
```

## Virtual DocType

Set `is_virtual=1`. No database table is created. ALWAYS implement these controller methods:

```python
class MyVirtualDoc(Document):
    def db_insert(self, *args, **kwargs):
        # Persist to your custom backend
        pass

    def load_from_db(self):
        # Load document data from your source
        pass

    def db_update(self, *args, **kwargs):
        # Update in your custom backend
        pass

    def delete(self):
        # Remove from your custom backend
        pass

    @staticmethod
    def get_list(args):
        # Return list of documents
        pass

    @staticmethod
    def get_count(args):
        # Return total count
        pass

    @staticmethod
    def get_stats(args):
        # Return statistics
        pass
```

> NEVER use `frappe.db.*` calls for Virtual DocType data -- they only work with the site database, not your custom backend.

## Customization APIs

### Custom Fields (Programmatic)

```python
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

# Dict format: {DocType: [field_dicts]}
create_custom_fields({
    "Sales Invoice": [
        dict(fieldname="custom_tracking", label="Tracking ID",
             fieldtype="Data", insert_after="naming_series")
    ],
    "Purchase Order": [
        dict(fieldname="custom_vendor_ref", label="Vendor Ref",
             fieldtype="Data", insert_after="supplier")
    ]
}, update=True)
```

### Property Setter (Programmatic)

```python
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

# Change a field property on an existing DocType
make_property_setter("Sales Invoice", "customer", "reqd", 1, "Check")
make_property_setter("Sales Invoice", "posting_date", "default", "Today", "Text")
```

> Full customization reference: [references/customization.md](references/customization.md)

## Data Masking (v16+)

Fields with `mask=1` hide sensitive values from users without `mask` permission at the field's `permlevel`. The server replaces values with patterns like `XXXXXXXX` before sending to the client. Administrator ALWAYS sees unmasked values.

```json
{ "fieldname": "phone", "fieldtype": "Data", "options": "Phone", "mask": 1, "permlevel": 1 }
```

> Full masking reference: [references/data-masking.md](references/data-masking.md)

## Python Type Stubs

Frappe auto-generates type annotations in controller files via `TypeExporter`. Fields get `DF.*` types inside a `TYPE_CHECKING` guard:

```python
if TYPE_CHECKING:
    from frappe.types import DF
    customer: DF.Link
    items: DF.Table[SalesInvoiceItem]
    status: DF.Literal["Draft", "Submitted", "Paid"]
```

NEVER modify code between `# begin: auto-generated types` and `# end: auto-generated types`.

> Full type stubs reference: [references/type-stubs.md](references/type-stubs.md)

## Critical Rules

1. ALWAYS name DocTypes in **singular** form ("Sales Invoice", not "Sales Invoices").
2. ALWAYS use the `tab` prefix mentally -- the DB table is `tabSales Invoice`.
3. NEVER exceed 140 characters for Data/Link/Select field values.
4. ALWAYS set `search_index=1` on fields used in frequent filters or `get_list` calls.
5. ALWAYS set `in_standard_filter=1` on fields users frequently filter by.
6. NEVER use `allow_on_submit=1` on child table fields that affect calculations without recalculating totals.
7. ALWAYS set `fetch_if_empty=1` alongside `fetch_from` unless you want to overwrite user edits.
8. NEVER define `depends_on` with raw Python -- use `eval:doc.fieldname == "value"` syntax.

## See Also

- [references/fieldtypes.md](references/fieldtypes.md) -- Complete fieldtype reference
- [references/naming.md](references/naming.md) -- All naming methods with examples
- [references/examples.md](references/examples.md) -- Real DocType JSON examples
- [references/anti-patterns.md](references/anti-patterns.md) -- Common schema design mistakes
- [references/customization.md](references/customization.md) -- Custom Fields and Property Setter APIs
- [references/data-masking.md](references/data-masking.md) -- Field-level data masking for privacy (v16+)
- [references/type-stubs.md](references/type-stubs.md) -- Python type hints, DF types, TypeExporter
