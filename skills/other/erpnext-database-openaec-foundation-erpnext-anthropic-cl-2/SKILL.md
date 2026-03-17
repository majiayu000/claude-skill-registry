---
name: erpnext-database
version: 1.0.0
description: Database operations and ORM patterns for ERPNext/Frappe v14-v16
author: OpenAEC-Foundation
triggers:
  - frappe database
  - frappe.db
  - frappe.get_doc
  - database query
  - SQL frappe
  - ORM frappe
  - caching frappe
  - database performance
---

# ERPNext Database Operations

## Quick Overview

Frappe provides three abstraction levels for database operations:

| Level | API | Usage |
|-------|-----|-------|
| **High-level ORM** | `frappe.get_doc`, `frappe.new_doc` | Document CRUD with validations |
| **Mid-level Query** | `frappe.db.get_list`, `frappe.db.get_value` | Reading with filters |
| **Low-level SQL** | `frappe.db.sql`, `frappe.qb` | Complex queries, reports |

**RULE**: Always use the highest abstraction level appropriate for your use case.

---

## Decision Tree

```
What do you want to do?
│
├─ Create/modify/delete document?
│  └─ frappe.get_doc() + .insert()/.save()/.delete()
│
├─ Get single document?
│  ├─ Changes frequently? → frappe.get_doc()
│  └─ Changes rarely? → frappe.get_cached_doc()
│
├─ List of documents?
│  ├─ With user permissions? → frappe.db.get_list()
│  └─ Without permissions? → frappe.get_all()
│
├─ Single field value?
│  ├─ Regular DocType → frappe.db.get_value()
│  └─ Single DocType → frappe.db.get_single_value()
│
├─ Direct update without triggers?
│  └─ frappe.db.set_value() or doc.db_set()
│
└─ Complex query with JOINs?
   └─ frappe.qb (Query Builder) or frappe.db.sql()
```

---

## Most Used Patterns

### Get Document
```python
# With ORM (triggers validations)
doc = frappe.get_doc('Sales Invoice', 'SINV-00001')

# Cached (faster for frequently accessed docs)
doc = frappe.get_cached_doc('Company', 'My Company')
```

### List Query
```python
# With user permissions
tasks = frappe.db.get_list('Task',
    filters={'status': 'Open'},
    fields=['name', 'subject'],
    order_by='creation desc',
    page_length=50
)

# Without permissions
all_tasks = frappe.get_all('Task', filters={'status': 'Open'})
```

### Single Value
```python
# Single field
status = frappe.db.get_value('Task', 'TASK001', 'status')

# Multiple fields
subject, status = frappe.db.get_value('Task', 'TASK001', ['subject', 'status'])

# As dict
data = frappe.db.get_value('Task', 'TASK001', ['subject', 'status'], as_dict=True)
```

### Create Document
```python
doc = frappe.get_doc({
    'doctype': 'Task',
    'subject': 'New Task',
    'status': 'Open'
})
doc.insert()
```

### Update Document
```python
# Via ORM (with validations)
doc = frappe.get_doc('Task', 'TASK001')
doc.status = 'Completed'
doc.save()

# Direct (without validations) - use carefully!
frappe.db.set_value('Task', 'TASK001', 'status', 'Completed')
```

---

## Filter Operators

```python
{'status': 'Open'}                          # =
{'status': ['!=', 'Cancelled']}             # !=
{'amount': ['>', 1000]}                     # >
{'amount': ['>=', 1000]}                    # >=
{'status': ['in', ['Open', 'Working']]}     # IN
{'date': ['between', ['2024-01-01', '2024-12-31']]}  # BETWEEN
{'subject': ['like', '%urgent%']}           # LIKE
{'description': ['is', 'set']}              # IS NOT NULL
{'description': ['is', 'not set']}          # IS NULL
```

---

## Query Builder (frappe.qb)

```python
Task = frappe.qb.DocType('Task')

results = (
    frappe.qb.from_(Task)
    .select(Task.name, Task.subject)
    .where(Task.status == 'Open')
    .orderby(Task.creation, order='desc')
    .limit(10)
).run(as_dict=True)
```

### With JOIN
```python
SI = frappe.qb.DocType('Sales Invoice')
Customer = frappe.qb.DocType('Customer')

results = (
    frappe.qb.from_(SI)
    .inner_join(Customer)
    .on(SI.customer == Customer.name)
    .select(SI.name, Customer.customer_name)
    .where(SI.docstatus == 1)
).run(as_dict=True)
```

---

## Caching

### Basics
```python
# Set/Get
frappe.cache.set_value('key', 'value')
value = frappe.cache.get_value('key')

# With expiry
frappe.cache.set_value('key', 'value', expires_in_sec=3600)

# Delete
frappe.cache.delete_value('key')
```

### @redis_cache Decorator
```python
from frappe.utils.caching import redis_cache

@redis_cache(ttl=300)  # 5 minutes
def get_dashboard_data(user):
    return expensive_calculation(user)

# Invalidate cache
get_dashboard_data.clear_cache()
```

---

## Transactions

Framework manages transactions automatically:

| Context | Commit | Rollback |
|---------|--------|----------|
| POST/PUT request | After success | On exception |
| Background job | After success | On exception |

### Manual (rarely needed)
```python
frappe.db.savepoint('my_savepoint')
try:
    # operations
    frappe.db.commit()
except:
    frappe.db.rollback(save_point='my_savepoint')
```

---

## Critical Rules

### 1. NEVER Use String Formatting in SQL
```python
# ❌ SQL Injection risk!
frappe.db.sql(f"SELECT * FROM `tabUser` WHERE name = '{user_input}'")

# ✅ Parameterized
frappe.db.sql("SELECT * FROM `tabUser` WHERE name = %(name)s", {'name': user_input})
```

### 2. NEVER Commit in Controller Hooks
```python
# ❌ WRONG
def validate(self):
    frappe.db.commit()  # Never do this!

# ✅ Framework handles commits
```

### 3. ALWAYS Paginate
```python
# ✅ Always limit
docs = frappe.get_all('Sales Invoice', page_length=100)
```

### 4. Avoid N+1 Queries
```python
# ❌ N+1 problem
for name in names:
    doc = frappe.get_doc('Customer', name)

# ✅ Batch fetch
docs = frappe.get_all('Customer', filters={'name': ['in', names]})
```

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| Transaction hooks | ❌ | ✅ | ✅ |
| bulk_update | ❌ | ✅ | ✅ |
| Aggregate syntax | String | String | Dict |

### v16 Aggregate Syntax
```python
# v14/v15
fields=['count(name) as count']

# v16
fields=[{'COUNT': 'name', 'as': 'count'}]
```

---

## Reference Files

See the `references/` folder for detailed documentation:

- **methods-reference.md** - All Database and Document API methods
- **query-patterns.md** - Filter operators and Query Builder syntax
- **caching-patterns.md** - Redis cache patterns and @redis_cache
- **examples.md** - Complete working examples
- **anti-patterns.md** - Common mistakes and how to avoid them

---

## Quick Reference

| Action | Method |
|--------|--------|
| Get document | `frappe.get_doc(doctype, name)` |
| Cached document | `frappe.get_cached_doc(doctype, name)` |
| New document | `frappe.new_doc(doctype)` or `frappe.get_doc({...})` |
| Save document | `doc.save()` |
| Insert document | `doc.insert()` |
| Delete document | `doc.delete()` or `frappe.delete_doc()` |
| Get list | `frappe.db.get_list()` / `frappe.get_all()` |
| Single value | `frappe.db.get_value()` |
| Single value | `frappe.db.get_single_value()` |
| Direct update | `frappe.db.set_value()` / `doc.db_set()` |
| Exists check | `frappe.db.exists()` |
| Count records | `frappe.db.count()` |
| Raw SQL | `frappe.db.sql()` |
| Query Builder | `frappe.qb.from_()` |
