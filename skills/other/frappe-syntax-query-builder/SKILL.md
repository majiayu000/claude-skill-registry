---
name: frappe-syntax-query-builder
description: >
  Use when building database queries with frappe.qb in Frappe v14-v16.
  Covers the PyPika-based query builder: SELECT, INSERT, UPDATE, DELETE,
  joins, aggregation, subqueries, cross-DB compatibility (MariaDB/PostgreSQL),
  and migration from raw SQL. Prevents SQL injection and DB-specific bugs.
  Keywords: frappe.qb, query builder, DocType, Field, pypika, join,
  aggregate, ImportMapper, cross-database, parameterized query.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "3.0"
---

# Frappe Query Builder (frappe.qb)

## Quick Reference

```python
from frappe.query_builder import DocType, Field
from frappe.query_builder.functions import Count, Sum, IfNull
from frappe.query_builder.custom import ConstantColumn, GROUP_CONCAT
from frappe.query_builder.terms import SubQuery
from frappe.query_builder.utils import ImportMapper, db_type_is
from pypika.terms import Case, ValueWrapper
from pypika import CustomFunction, Order
```

| Action | Pattern |
|--------|---------|
| SELECT | `frappe.qb.from_("DocType").select("field1", "field2")` |
| WHERE | `.where(Field("status") == "Open")` |
| ORDER | `.orderby("creation", order=Order.desc)` |
| LIMIT | `.limit(10).offset(0)` |
| JOIN | `.left_join(dt2).on(dt2.name == dt1.parent)` |
| COUNT | `.select(Count("*"))` |
| INSERT | `frappe.qb.into("DocType").columns("f1", "f2").insert("v1", "v2")` |
| UPDATE | `frappe.qb.update("DocType").set("field", "value").where(...)` |
| DELETE | `frappe.qb.from_("DocType").delete().where(...)` |
| RUN | `.run()` (tuples) / `.run(as_dict=True)` (dicts) |

---

## Decision Tree

```
Need to query the database?
│
├─ Simple get/list → frappe.db.get_value(), frappe.get_all()
│  (See frappe-core-database skill)
│
├─ Complex query with joins/aggregates/subqueries → frappe.qb ✓
│
├─ Very complex SQL not expressible in qb → frappe.db.sql()
│  (ALWAYS use parameterized values: frappe.db.sql(query, values))
│
└─ Need cross-DB compatibility → frappe.qb + ImportMapper ✓

Using frappe.qb?
│
├─ Table reference → DocType("Sales Order") — NEVER use Table()
├─ Field reference → dt.field_name or Field("field_name")
├─ Execute → .run() for tuples, .run(as_dict=True) for dicts
├─ DB-specific function → ImportMapper({db_type_is.MARIADB: X, db_type_is.POSTGRES: Y})
└─ Get SQL string → query.get_sql() — NEVER pass to frappe.db.sql()
```

---

## Core Patterns

### SELECT with DocType

```python
# ALWAYS use DocType() for table references — adds "tab" prefix
so = frappe.qb.DocType("Sales Order")
soi = frappe.qb.DocType("Sales Order Item")

orders = (
    frappe.qb.from_(so)
    .select(so.name, so.customer, so.grand_total)
    .where(so.status == "To Deliver and Bill")
    .where(so.docstatus == 1)
    .orderby(so.creation, order=Order.desc)
    .limit(20)
    .run(as_dict=True)
)
```

### JOIN

```python
result = (
    frappe.qb.from_(so)
    .left_join(soi).on(soi.parent == so.name)
    .select(so.name, so.customer, soi.item_code, soi.qty)
    .where(so.docstatus == 1)
    .where(soi.item_code.like("ITEM-%"))
    .run(as_dict=True)
)
```

### Aggregation

```python
from frappe.query_builder.functions import Count, Sum

gl = frappe.qb.DocType("GL Entry")
result = (
    frappe.qb.from_(gl)
    .select(gl.account, Sum(gl.debit).as_("total_debit"), Count("*").as_("entries"))
    .where(gl.docstatus == 1)
    .groupby(gl.account)
    .run(as_dict=True)
)

# Shortcut aggregation methods
total = frappe.qb.sum("GL Entry", "debit", filters={"account": "Sales"})
max_qty = frappe.qb.max("Stock Ledger Entry", "actual_qty", filters={"item_code": "ITEM-001"})
```

### INSERT / UPDATE / DELETE

```python
# INSERT
frappe.qb.into("Activity Log").columns("user", "action").insert("admin", "login").run()

# UPDATE
customer = frappe.qb.DocType("Customer")
(frappe.qb.update(customer)
    .set(customer.status, "Active")
    .where(customer.name == "CUST-001")
    .run())

# DELETE
frappe.qb.from_("Error Log").delete().where(Field("creation") < "2024-01-01").run()
```

---

## Filtering

```python
dt = frappe.qb.DocType("Sales Order")

# Equality
.where(dt.status == "Open")

# OR (pipe operator)
.where((dt.status == "Open") | (dt.status == "Draft"))

# AND (chain .where() calls)
.where(dt.status == "Open")
.where(dt.docstatus == 1)

# LIKE
.where(dt.customer.like("CUST-%"))

# IN
.where(dt.status.isin(["Open", "Draft"]))

# BETWEEN (bracket syntax)
.where(dt.creation[start_date:end_date])

# NULL checks
.where(dt.email.isnotnull())
.where(dt.phone.isnull())

# Comparison
.where(dt.grand_total > 1000)
.where(dt.grand_total >= 500)
.where(dt.status != "Cancelled")
```

---

## Cross-DB Compatibility

```python
from frappe.query_builder.utils import ImportMapper, db_type_is
from frappe.query_builder.custom import GROUP_CONCAT, STRING_AGG

# ImportMapper selects correct function per database
GroupConcat = ImportMapper({
    db_type_is.MARIADB: GROUP_CONCAT,
    db_type_is.POSTGRES: STRING_AGG,
})

dt = frappe.qb.DocType("Has Role")
result = (
    frappe.qb.from_(dt)
    .select(dt.parent, GroupConcat(dt.role))
    .groupby(dt.parent)
    .run(as_dict=True)
)
```

| MariaDB | PostgreSQL | Use ImportMapper |
|---------|-----------|-----------------|
| `GROUP_CONCAT` | `STRING_AGG` | Yes |
| `MATCH...AGAINST` | `TO_TSVECTOR` | Yes |
| `Locate` | `Strpos` | Yes |
| `Timestamp` | Extract-based | Auto-handled |

---

## Anti-patterns

1. **NEVER pass qb query to `frappe.db.sql()`** — bypasses parameterization
2. **NEVER use `Table()` for DocTypes** — use `DocType()` (adds `tab` prefix)
3. **NEVER forget `.run()`** — without it you get a query object, not results
4. **NEVER use raw SQL strings in `frappe.get_all(fields=[...])`** — use dict syntax
5. **ALWAYS use `ImportMapper` for DB-specific functions**
6. **ALWAYS chain `.run(as_dict=True)` when you need dicts** — default is tuples

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|:---:|:---:|:---:|
| Core qb API | Introduced | Yes | Yes |
| ImportMapper | Yes | Yes | Yes |
| SQLite backend | -- | -- | Added |
| Masked fields | -- | -- | Added |
| Union queries (.walk) | -- | Added | Yes |
| Child query execution | -- | -- | Added |

---

## Reference Files

- [Functions & Aggregates](references/functions-reference.md) — All available qb functions
- [Migration Guide](references/migration-from-sql.md) — Converting raw SQL and get_all patterns
- [Cross-DB Patterns](references/cross-db-patterns.md) — ImportMapper and DB-specific functions
