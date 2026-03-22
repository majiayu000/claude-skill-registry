---
name: frappe-core-database
description: >
  Use when performing database operations in ERPNext/Frappe v14-v16. Covers
  frappe.db methods, ORM patterns (frappe.get_doc, frappe.get_list), raw SQL,
  caching patterns, and performance optimization. Prevents common mistakes
  with database transactions and query building. Keywords: frappe.db,
  frappe.get_doc, database query, SQL, ORM, caching, database performance.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Database Operations

## Quick Reference

| Action | Method | Permissions |
|--------|--------|-------------|
| Get document | `frappe.get_doc(doctype, name)` | Yes |
| Cached document | `frappe.get_cached_doc(doctype, name)` | No |
| New document | `frappe.new_doc(doctype)` | — |
| Insert | `doc.insert()` | Yes |
| Save | `doc.save()` | Yes |
| Delete document | `frappe.delete_doc(doctype, name)` | Yes |
| List (with perms) | `frappe.db.get_list(doctype, ...)` | Yes |
| List (no perms) | `frappe.get_all(doctype, ...)` | No |
| Single field | `frappe.db.get_value(doctype, name, field)` | No |
| Single DocType | `frappe.db.get_single_value(doctype, field)` | No |
| Cached value | `frappe.db.get_value(..., cache=True)` | No |
| Direct update | `frappe.db.set_value(doctype, name, field, val)` | No |
| Direct update | `doc.db_set(field, value)` | No |
| Exists check | `frappe.db.exists(doctype, name)` | No |
| Count | `frappe.db.count(doctype, filters)` | No |
| Delete rows | `frappe.db.delete(doctype, filters)` | No |
| Raw SQL | `frappe.db.sql(query, values, as_dict)` | No |
| Query Builder | `frappe.qb.from_(doctype).select(...)` | No |

> **"Permissions" = Yes** means user permission filters are applied automatically.

---

## Decision Tree

```
What do you need?
│
├─ Create / Update / Delete a document?
│  ├─ With validations + hooks → frappe.get_doc() + .insert()/.save()/.delete()
│  └─ Direct DB (no hooks) → frappe.db.set_value() or doc.db_set()
│
├─ Read a single document?
│  ├─ Need full object with methods → frappe.get_doc()
│  ├─ Read-only, rarely changes → frappe.get_cached_doc()
│  └─ Only need 1-2 fields → frappe.db.get_value()
│
├─ List of documents?
│  ├─ Respect user permissions → frappe.db.get_list()
│  └─ System/admin context → frappe.get_all()
│
├─ Single DocType value?
│  └─ frappe.db.get_single_value('Settings', 'field')
│
├─ Check existence?
│  └─ frappe.db.exists() — NEVER use get_doc in try/except
│
├─ Complex query (JOINs, aggregates)?
│  ├─ Cross-DB compatible → frappe.qb (Query Builder)
│  └─ DB-specific SQL → frappe.db.sql() with parameters
│
└─ DB-specific logic?
   └─ frappe.db.multisql({'mariadb': q1, 'postgres': q2})
```

**RULE**: ALWAYS use the highest abstraction level: ORM > Database API > Query Builder > Raw SQL.

---

## ORM — Document Operations

### Get Document
```python
doc = frappe.get_doc('Sales Invoice', 'SINV-00001')

# Single DocType (no name needed)
settings = frappe.get_doc('System Settings')

# Cached (read-only, for rarely-changing docs)
company = frappe.get_cached_doc('Company', 'My Company')

# Last created
last_task = frappe.get_last_doc('Task', filters={'status': 'Open'})
```

### Create Document
```python
doc = frappe.get_doc({
    'doctype': 'Task',
    'subject': 'Review report',
    'status': 'Open'
})
doc.insert()

# Alternative
doc = frappe.new_doc('Task')
doc.subject = 'Review report'
doc.insert()
```

### Update Document
```python
# Via ORM — triggers validate, on_update, etc.
doc = frappe.get_doc('Task', 'TASK-001')
doc.status = 'Completed'
doc.save()

# Direct DB — SKIPS all validations and hooks
frappe.db.set_value('Task', 'TASK-001', 'status', 'Completed')

# Direct DB on loaded doc
doc.db_set('status', 'Completed')
doc.db_set('status', 'Completed', update_modified=False)
doc.db_set({'status': 'Completed', 'priority': 'High'})
```

### Delete Document
```python
frappe.delete_doc('Task', 'TASK-001')
# Also removes linked Communications, Comments, etc.
```

### Insert Flags
```python
doc.insert(
    ignore_permissions=True,     # Bypass permission check
    ignore_links=True,           # Skip link validation
    ignore_if_duplicate=True,    # No error on duplicate
    ignore_mandatory=True        # Skip required field check
)
```

> **RULE**: NEVER use multiple ignore flags together unless you have a documented reason. Each flag you add weakens data integrity.

---

## Database API — Reading

### get_value
```python
# Single field → scalar
status = frappe.db.get_value('Task', 'TASK-001', 'status')

# Multiple fields → tuple
subject, status = frappe.db.get_value('Task', 'TASK-001', ['subject', 'status'])

# As dict
data = frappe.db.get_value('Task', 'TASK-001', ['subject', 'status'], as_dict=True)

# With filters instead of name
status = frappe.db.get_value('Task', {'project': 'PROJ-001'}, 'status')

# Cached (for values that rarely change)
country = frappe.db.get_value('Company', 'MyCompany', 'country', cache=True)
```

### get_single_value
```python
timezone = frappe.db.get_single_value('System Settings', 'time_zone')
```

### get_list / get_all
```python
# get_list — applies user permissions
tasks = frappe.db.get_list('Task',
    filters={'status': 'Open'},
    fields=['name', 'subject', 'assigned_to'],
    order_by='creation desc',
    start=0,
    page_length=50
)

# get_all — NO permission check (same API, different default)
all_tasks = frappe.get_all('Task', filters={'status': 'Open'})

# pluck — returns flat list of single field
names = frappe.get_all('Task', filters={'status': 'Open'}, pluck='name')
# Returns: ['TASK-001', 'TASK-002', ...]
```

### exists / count
```python
exists = frappe.db.exists('User', 'admin@example.com')
exists = frappe.db.exists('User', {'email': 'admin@example.com'})

total = frappe.db.count('Task')
open_count = frappe.db.count('Task', {'status': 'Open'})
```

---

## Filter Operators

```python
{'status': 'Open'}                                    # =
{'status': ['!=', 'Cancelled']}                       # !=
{'amount': ['>', 1000]}                               # >
{'amount': ['>=', 1000]}                              # >=
{'status': ['in', ['Open', 'Working']]}               # IN
{'status': ['not in', ['Cancelled', 'Closed']]}       # NOT IN
{'date': ['between', ['2024-01-01', '2024-12-31']]}   # BETWEEN
{'subject': ['like', '%urgent%']}                      # LIKE
{'description': ['is', 'set']}                         # IS NOT NULL
{'description': ['is', 'not set']}                     # IS NULL
```

### Combining Filters
```python
# AND — all conditions in one dict
filters = {'status': 'Open', 'priority': 'High'}

# AND — list format (allows duplicate fields)
filters = [['status', '=', 'Open'], ['priority', '=', 'High']]

# OR — separate parameter
or_filters = {'priority': 'Urgent', 'status': 'Overdue'}
```

---

## Database API — Writing

### set_value
```python
# Single field
frappe.db.set_value('Task', 'TASK-001', 'status', 'Closed')

# Multiple fields
frappe.db.set_value('Task', 'TASK-001', {'status': 'Closed', 'priority': 'Low'})

# Without updating modified timestamp
frappe.db.set_value('Task', 'TASK-001', 'status', 'Closed', update_modified=False)
```

### delete / truncate
```python
# Delete with filters (DML — can be rolled back)
frappe.db.delete('Error Log', {'creation': ['<', '2024-01-01']})

# Truncate (DDL — CANNOT be rolled back)
frappe.db.truncate('Error Log')
```

### bulk_update [v15+]
```python
frappe.db.bulk_update('Task', {
    'TASK-001': {'status': 'Closed'},
    'TASK-002': {'status': 'Closed'}
}, chunk_size=100)
```

---

## Raw SQL — ALWAYS Parameterized

```python
# ✅ CORRECT — parameterized query
results = frappe.db.sql("""
    SELECT name, subject FROM `tabTask`
    WHERE status = %(status)s AND owner = %(owner)s
""", {'status': 'Open', 'owner': frappe.session.user}, as_dict=True)
```

> **CRITICAL**: NEVER use f-strings, % formatting, or string concatenation in SQL. See [SQL Injection Prevention](#sql-injection-prevention).

### Return Types
```python
frappe.db.sql(query)                    # Tuple of tuples (default)
frappe.db.sql(query, as_dict=True)      # List of dicts
frappe.db.sql(query, as_list=True)      # List of lists
```

### Table Naming
ALWAYS use backtick-quoted `tab` prefix: `` `tabSales Invoice` ``, `` `tabTask` ``

### Database-Specific SQL
```python
frappe.db.multisql({
    'mariadb': "SELECT IFNULL(field, 0) FROM `tabDoc`",
    'postgres': "SELECT COALESCE(field, 0) FROM `tabDoc`"
})
```

---

## Query Builder (frappe.qb) [v14+]

The Query Builder uses PyPika under the hood. It generates parameterized SQL automatically.

```python
Task = frappe.qb.DocType('Task')

results = (
    frappe.qb.from_(Task)
    .select(Task.name, Task.subject, Task.status)
    .where(Task.status == 'Open')
    .orderby(Task.creation, order='desc')
    .limit(10)
).run(as_dict=True)
```

### JOINs
```python
SI = frappe.qb.DocType('Sales Invoice')
Customer = frappe.qb.DocType('Customer')

results = (
    frappe.qb.from_(SI)
    .inner_join(Customer).on(SI.customer == Customer.name)
    .select(SI.name, SI.grand_total, Customer.customer_name)
    .where(SI.docstatus == 1)
).run(as_dict=True)
```

### Aggregates
```python
from frappe.query_builder.functions import Count, Sum, Avg

stats = (
    frappe.qb.from_(Task)
    .select(Task.status, Count(Task.name).as_('count'))
    .groupby(Task.status)
).run(as_dict=True)
```

### OR Conditions
```python
customers = frappe.qb.DocType('Customer')
results = (
    frappe.qb.from_(customers)
    .select(customers.name)
    .where(
        (customers.territory == 'US') | (customers.territory == 'UK')
    )
).run(as_dict=True)
```

### Inspect Generated SQL
```python
query = frappe.qb.from_(Task).select('*').where(Task.name == 'X')
sql, params = query.walk()   # Returns (sql_string, param_dict)
sql_str = query.get_sql()    # Returns SQL string
```

> See `references/query-patterns.md` for subqueries, ImportMapper, ConstantColumn, and custom functions.

---

## Caching

### Document Cache
```python
doc = frappe.get_cached_doc('Company', 'My Company')   # Full document
val = frappe.db.get_value('Company', 'X', 'country', cache=True)  # Single value
```

### Redis Cache
```python
frappe.cache.set_value('key', data, expires_in_sec=3600)
data = frappe.cache.get_value('key')
frappe.cache.delete_value('key')
```

### @redis_cache Decorator
```python
from frappe.utils.caching import redis_cache

@redis_cache(ttl=300)
def get_dashboard_data(user):
    return expensive_calculation(user)

# Invalidate
get_dashboard_data.clear_cache()
```

> See `references/caching-patterns.md` for hash operations, invalidation strategies, and best practices.

---

## Transaction Management

The framework manages transactions automatically:

| Context | Commit | Rollback |
|---------|--------|----------|
| POST/PUT request | After success | On uncaught exception |
| GET request | Never | — |
| Background job | After success | On exception |
| Patch | After success | On exception |

### Manual Transactions (rarely needed)
```python
frappe.db.savepoint('before_payment')
try:
    # operations...
    frappe.db.commit()
except Exception:
    frappe.db.rollback(save_point='before_payment')
```

### Transaction Hooks [v15+]
```python
frappe.db.after_commit.add(sync_to_external_system)
frappe.db.after_rollback.add(cleanup_external_state)
```

---

## SQL Injection Prevention

**CRITICAL SECURITY RULE**: NEVER interpolate user input into SQL strings.

```python
# ❌ VULNERABLE — SQL injection risk
frappe.db.sql(f"SELECT * FROM `tabUser` WHERE name = '{user_input}'")
frappe.db.sql("SELECT * FROM `tabUser` WHERE name = '%s'" % user_input)
frappe.db.sql("SELECT * FROM `tabUser` WHERE name = " + user_input)

# ✅ SAFE — parameterized query
frappe.db.sql("SELECT * FROM `tabUser` WHERE name = %(name)s", {'name': user_input})

# ✅ SAFE — ORM / Query Builder (always parameterized)
frappe.get_all('User', filters={'name': user_input})

User = frappe.qb.DocType('User')
frappe.qb.from_(User).select('*').where(User.name == user_input).run()
```

**RULE**: When you MUST use `frappe.db.sql()`, ALWAYS use `%(param)s` placeholders with a dict. The Query Builder (`frappe.qb`) is ALWAYS preferred over raw SQL for new code.

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| Query Builder (frappe.qb) | Yes | Yes | Yes |
| Transaction hooks | No | Yes | Yes |
| `bulk_update` | No | Yes | Yes |
| `run=False` returns | SQL string | SQL string | Query Builder object |
| Aggregate field syntax | String | String | Dict |

### v16 Breaking Changes
```python
# v14/v15 — string aggregates
fields=['count(name) as count']

# v16 — dict aggregates
fields=[{'COUNT': 'name', 'as': 'count'}]

# v14/v15 — run=False returns SQL string
sql = frappe.db.get_list('Task', run=False)

# v16 — run=False returns Query Builder object
qb_obj = frappe.db.get_list('Task', run=False)
sql = qb_obj.get_sql()
```

---

## Critical Rules Summary

1. **NEVER** use string formatting in SQL — ALWAYS use parameterized queries
2. **NEVER** call `frappe.db.commit()` inside controller hooks (validate, on_update, etc.)
3. **ALWAYS** paginate list queries — use `page_length` parameter
4. **ALWAYS** specify fields — NEVER use `fields=['*']` in production
5. **ALWAYS** use `frappe.db.exists()` for existence checks — NEVER try/except with get_doc
6. **ALWAYS** prefix table names with `tab` in raw SQL: `` `tabSales Invoice` ``
7. **NEVER** use multiple ignore flags without documented justification
8. **ALWAYS** use batch fetching to avoid N+1 queries
9. **ALWAYS** prefer `frappe.qb` over `frappe.db.sql()` for new code
10. **NEVER** use `frappe.db.truncate()` without understanding it CANNOT be rolled back

---

## Query Builder — Dedicated Skill

For complex queries (joins, aggregations, subqueries, cross-DB compatibility), see **[frappe-syntax-query-builder](../../syntax/frappe-syntax-query-builder/SKILL.md)**.
- **frappe.db methods** (this skill) — Simple CRUD, get_value, get_list, exists checks
- **frappe.qb** (query-builder skill) — Joins, GROUP BY, HAVING, subqueries, cross-DB functions
- **frappe.db.sql** — Very complex SQL not expressible in qb (ALWAYS parameterized)

## Reference Files

- **[methods-reference.md](references/methods-reference.md)** — Complete API signatures for all database and document methods
- **[query-patterns.md](references/query-patterns.md)** — Query Builder patterns, subqueries, ImportMapper, custom functions
- **[caching-patterns.md](references/caching-patterns.md)** — Redis cache, @redis_cache, hash operations, invalidation
- **[examples.md](references/examples.md)** — Real-world patterns: CRUD, reports, batch processing, transactions
- **[anti-patterns.md](references/anti-patterns.md)** — SQL injection, N+1, commit mistakes, and 10 more anti-patterns
