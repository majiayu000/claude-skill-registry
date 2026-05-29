---
name: frappe-core-search
description: >
  Use when implementing search functionality in Frappe v14-v16.
  Covers link field search (search_link), global search, FullTextSearch
  (Whoosh), SQLiteSearch FTS5 [v15+], Awesomebar customization,
  search_fields configuration, custom search queries, and website search.
  Prevents common mistakes with missing search_fields and permission filtering.
  Keywords: search, search_link, global_search, FullTextSearch, Awesomebar,
  search_fields, standard_queries, SQLiteSearch, FTS5, Whoosh.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "3.0"
---

# Frappe Search System

## Four Search Subsystems

| Subsystem | Module | Purpose | Real-time? |
|-----------|--------|---------|:----------:|
| **Link Field Search** | `frappe.desk.search` | Autocomplete in link fields | Yes |
| **Global Search** | `frappe.utils.global_search` | Cross-doctype search (desk + web) | No (15min sync) |
| **FullTextSearch** | `frappe.search.full_text_search` | Whoosh-based index (website) | On rebuild |
| **SQLiteSearch** [v15+] | `frappe.search.sqlite_search` | FTS5 with scoring + spelling | Yes (5min queue) |

---

## Decision Tree

```
What search do you need?
│
├─ Link field autocomplete (user types in a Link field)?
│  ├─ Default behavior sufficient → Configure search_fields on DocType
│  └─ Custom logic needed → standard_queries hook or query parameter
│
├─ Cross-doctype search (user searches for anything)?
│  ├─ Desk users → Global Search (auto-enabled)
│  │  └─ Set in_global_search=1 on important fields
│  └─ Website visitors → web_search() or WebsiteSearch (Whoosh)
│
├─ Custom full-text search for your app [v15+]?
│  └─ SQLiteSearch subclass + sqlite_search hook
│     → Spelling correction, recency boost, custom scoring
│
└─ Awesomebar customization?
   └─ Client-side: override build_options or use search dialog
```

---

## Link Field Search

### Configuring search_fields (Most Common Need)

```python
# In DocType JSON or via customize form
{
    "search_fields": "customer_name, customer_group",
    "title_field": "customer_name",
    "show_title_field_in_link": 1
}
```

**ALWAYS set `search_fields`** — Without it, users can only search by `name` (often a code like `CUST-001`).

### How Link Search Works

1. User types in link field → calls `search_link(doctype, txt)`
2. Searches across: `name` + `title_field` + `search_fields`
3. Allowed field types: Data, Text, Small Text, Long Text, Link, Select, Autocomplete, Read Only, Text Editor
4. Prefix matches rank higher than substring matches
5. Respects `enabled`/`disabled` fields automatically

### Custom Link Query

```python
# hooks.py — override search for a specific DocType
standard_queries = {
    "Customer": "my_app.queries.customer_query"
}
```

```python
# my_app/queries.py — MUST be @frappe.whitelist()
@frappe.whitelist()
def customer_query(doctype, txt, searchfield, start, page_length, filters,
                   as_dict=False, reference_doctype=None,
                   ignore_user_permissions=False):
    # Return list of dicts: [{"value": name, "description": label}, ...]
    return frappe.db.sql("""
        SELECT name, customer_name as description
        FROM `tabCustomer`
        WHERE (name LIKE %(txt)s OR customer_name LIKE %(txt)s)
        AND status = 'Active'
        ORDER BY customer_name
        LIMIT %(start)s, %(page_length)s
    """, {"txt": f"%{txt}%", "start": start, "page_length": page_length},
    as_dict=True)
```

### Per-Field Query Override

```javascript
// In Client Script or Form JS
frappe.ui.form.on("Sales Order", {
    setup(frm) {
        frm.set_query("customer", () => ({
            filters: { status: "Active", territory: frm.doc.territory }
        }));
    }
});
```

---

## Global Search

### Enabling

Set `in_global_search = 1` on DocType fields that should be searchable.

### How It Works

- Indexed fields stored in `__global_search` table
- Synced via Redis queue every 15 minutes
- Uses DB-native fulltext: MariaDB `MATCH...AGAINST`, PostgreSQL `TSVECTOR`
- Permission-filtered results

### Rebuilding Index

```python
# Rebuild for specific DocType
from frappe.utils.global_search import rebuild_for_doctype
rebuild_for_doctype("Sales Order")

# Rebuild everything
from frappe.utils.global_search import rebuild
rebuild()
```

### hooks.py Configuration

```python
# Default doctypes for global search
global_search_doctypes = {
    "Default": [
        {"doctype": "Contact"},
        {"doctype": "Customer"},
        {"doctype": "Sales Order"},
    ]
}
```

---

## SQLiteSearch [v15+]

### Creating Custom Search

```python
# my_app/search.py
from frappe.search.sqlite_search import SQLiteSearch

class ProjectSearch(SQLiteSearch):
    INDEX_SCHEMA = {
        "metadata_fields": ["project", "owner", "status"],
        "tokenizer": "unicode61 remove_diacritics 2 tokenchars '-_'",
    }

    INDEXABLE_DOCTYPES = {
        "Task": {
            "fields": ["name", {"title": "subject"}, {"content": "description"},
                       "modified", "project"],
            "filters": {"status": ("!=", "Cancelled")}
        },
        "Project": {
            "fields": ["name", {"title": "project_name"}, {"content": "notes"},
                       "modified", "status"],
        }
    }

    def get_search_filters(self, query, scope=None):
        """Permission filtering — return additional WHERE conditions"""
        return {}
```

### Register in hooks.py

```python
sqlite_search = ['my_app.search.ProjectSearch']
```

### Features (automatic)

- **Spelling correction**: Trigram-based fuzzy matching
- **Recency boosting**: 1.8x (24h) → 1.5x (7d) → 1.2x (30d) → 1.1x (90d)
- **Resumable indexing**: Progress tracked, atomic replacement
- **Auto-scheduling**: Build every 3h, queue every 5min, doc events trigger updates

---

## Anti-Patterns

| NEVER | ALWAYS | Why |
|-------|--------|-----|
| Omit `search_fields` on DocType | Set `search_fields` for user-friendly names | Users can't find records by name codes |
| Custom query without `@frappe.whitelist()` | Decorate with `@frappe.whitelist()` | Silently fails — rejected by security check |
| Raw SQL without params in search | Use parameterized queries (`%(txt)s`) | SQL injection risk |
| Index all fields in global search | Only `in_global_search=1` on key fields | Bloats table, slows 15-min sync |
| Use global search for real-time | Use link field search for real-time | Global search has 15-min sync delay |
| Skip `get_search_filters()` in SQLiteSearch | Implement permission filtering | Returns all results regardless of access |
| Index cancelled/deleted docs | Set `filters` in `INDEXABLE_DOCTYPES` | Stale results confuse users |

---

## Version Differences

| Feature | v14 | v15+ |
|---------|:---:|:----:|
| Link search caching | -- | `@http_cache(max_age=60)` |
| `link_fieldname` param | -- | Added |
| `page_length` default | 20 | 10 |
| SQLiteSearch (FTS5) | -- | Full implementation |
| Spelling correction | -- | Trigram-based |
| Recency boosting | -- | Time-based multipliers |
| `sqlite_search` hook | -- | Available |
| Global search | Yes | Yes |
| Whoosh FullTextSearch | Yes | Yes (legacy) |

---

## Reference Files

- [Link Search API](references/link-search-api.md) — search_link, search_widget, custom queries
- [Global & Website Search](references/global-website-search.md) — Global search, WebsiteSearch, SQLiteSearch
