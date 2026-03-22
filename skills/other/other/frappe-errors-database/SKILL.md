---
name: frappe-errors-database
description: >
  Use when handling database errors in Frappe/ERPNext. Covers
  DuplicateEntryError, LinkValidationError, MandatoryError,
  TimestampMismatchError, CharacterLengthExceededError, InReadOnlyMode,
  QueryTimeoutError, SQL injection errors, frappe.db.sql parameter format
  (% vs %s), get_value returning None, transaction deadlocks, MariaDB gone
  away, too many connections. Error-to-fix mapping for v14/v15/v16.
  Keywords: database error, DuplicateEntryError, TimestampMismatchError,
  SQL injection, deadlock, MariaDB gone away, query timeout.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Database Error Diagnosis & Resolution

Cross-ref: `frappe-core-database` (API syntax), `frappe-errors-controllers` (controller errors).

---

## Error-to-Fix Mapping Table

| Error / Exception | HTTP | Cause | Fix |
|-------------------|------|-------|-----|
| `DuplicateEntryError` | 409 | Unique constraint violation on insert/rename | Check existence first OR catch and return existing |
| `DoesNotExistError` | 404 | `get_doc()` on missing record | Use `frappe.db.exists()` first OR catch exception |
| `LinkValidationError` | 417 | Link field points to non-existent record | Validate link target exists before save |
| `LinkExistsError` | N/A | Delete blocked by linked documents | Show linked docs to user; use `force=True` carefully |
| `MandatoryError` | 417 | Required field is empty on save | Set all mandatory fields before insert/save |
| `TimestampMismatchError` | N/A | Concurrent edit detected (`modified` changed) | Reload doc and retry, or inform user to refresh |
| `CharacterLengthExceededError` | 417 | String exceeds field maxlength / DB column size | Truncate input or increase field length |
| `DataTooLongException` | 417 | Value exceeds DB column storage capacity | Same as CharacterLengthExceededError |
| `InReadOnlyMode` | 503 | Write attempted during read-only mode | Check `frappe.flags.in_import` or site config |
| `QueryTimeoutError` | N/A | Query exceeded time limit [v15+] | Add indexes, reduce result set, paginate |
| `QueryDeadlockError` | N/A | Two transactions waiting on each other | Retry with backoff; reduce transaction scope |
| `TooManyWritesError` | N/A | Excessive writes in single request | Batch operations; use background jobs |
| `InternalError` (gone away) | N/A | MariaDB connection dropped | Reconnect with `frappe.db.connect()` |
| `InternalError` (too many) | N/A | Connection pool exhausted | Check `max_connections`; close idle connections |
| `ValidationError` | 417 | General validation failure in save | Read error message; fix field values |
| SQL syntax error | N/A | Wrong `frappe.db.sql()` parameter format | Use `%(name)s` with dict, NOT `%s` with tuple |

---

## Exception Hierarchy

```
Exception
├── frappe.ValidationError (HTTP 417)
│   ├── frappe.MandatoryError
│   ├── frappe.LinkValidationError
│   ├── frappe.CharacterLengthExceededError
│   ├── frappe.DataTooLongException
│   ├── frappe.UniqueValidationError
│   ├── frappe.UpdateAfterSubmitError
│   └── frappe.DataError
├── frappe.DoesNotExistError (HTTP 404)
├── frappe.DuplicateEntryError (HTTP 409)  ← inherits NameError
├── frappe.TimestampMismatchError
├── frappe.LinkExistsError
├── frappe.QueryTimeoutError
├── frappe.QueryDeadlockError
├── frappe.TooManyWritesError
├── frappe.InReadOnlyMode (HTTP 503)
└── frappe.db.InternalError  ← MariaDB/Postgres driver error
```

---

## frappe.db.sql() Parameter Format

```python
# ❌ WRONG — %s with positional tuple (works but fragile)
frappe.db.sql("SELECT * FROM `tabItem` WHERE name = %s", ("ITEM-001",))

# ❌ WRONG — f-string or .format() — SQL INJECTION!
frappe.db.sql(f"SELECT * FROM `tabItem` WHERE name = '{item_name}'")
frappe.db.sql("SELECT * FROM `tabItem` WHERE name = '{}'".format(item_name))

# ❌ WRONG — bare % operator
frappe.db.sql("SELECT * FROM `tabItem` WHERE name = '%s'" % item_name)

# ✅ CORRECT — named parameters with dict (ALWAYS use this)
frappe.db.sql(
    "SELECT * FROM `tabItem` WHERE name = %(name)s AND warehouse = %(wh)s",
    {"name": item_name, "wh": warehouse},
    as_dict=True
)

# ✅ CORRECT — frappe.qb (query builder, no injection risk)
Item = frappe.qb.DocType("Item")
result = (
    frappe.qb.from_(Item)
    .select(Item.name, Item.item_name)
    .where(Item.warehouse == warehouse)
    .run(as_dict=True)
)
```

**Rule**: ALWAYS use `%(name)s` with a dict parameter. NEVER use string formatting for SQL values.

---

## get_value Returns None — Not an Exception

```python
# ❌ DANGEROUS — get_value returns None, not raises
credit = frappe.db.get_value("Customer", "CUST-001", "credit_limit")
if credit > 1000:  # TypeError: '>' not supported between NoneType and int
    pass

# ✅ CORRECT — handle None explicitly
credit = frappe.db.get_value("Customer", "CUST-001", "credit_limit")
if credit is None:
    frappe.throw(_("Customer not found"))
credit = credit or 0  # Default to 0 if field is empty

# ✅ CORRECT — get_value with as_dict for multiple fields
data = frappe.db.get_value("Customer", "CUST-001",
    ["credit_limit", "disabled"], as_dict=True)
if not data:  # None when record not found
    frappe.throw(_("Customer not found"))
if data.disabled:
    frappe.throw(_("Customer is disabled"))
```

**Key behavior by method**:
| Method | Record Not Found | Empty Field |
|--------|-----------------|-------------|
| `get_doc()` | Raises `DoesNotExistError` | Returns field default |
| `get_value()` | Returns `None` | Returns `None` or `""` |
| `get_all()` | Returns `[]` | Included in result |
| `exists()` | Returns `False` | N/A |
| `set_value()` | Silently does nothing | N/A |
| `db.sql()` | Returns `[]` or `()` | Included in result |

---

## Handling Each Exception Type

### DuplicateEntryError

```python
# Pattern: Insert with duplicate handling
def create_or_get(doctype, data):
    try:
        doc = frappe.get_doc({"doctype": doctype, **data})
        doc.insert()
        return doc
    except frappe.DuplicateEntryError:
        # Race condition safe: someone else created it
        name = frappe.db.get_value(doctype, data, "name")
        return frappe.get_doc(doctype, name)
```

### TimestampMismatchError

```python
# Pattern: Concurrent edit detection
try:
    doc = frappe.get_doc("Sales Invoice", name)
    doc.update(updates)
    doc.save()
except frappe.TimestampMismatchError:
    frappe.throw(
        _("Document modified by another user. Please refresh and try again."),
        title=_("Concurrent Edit")
    )
```

### LinkValidationError & MandatoryError

```python
# Pattern: Pre-validate before save
def safe_create_invoice(data):
    errors = []

    # Check mandatory fields
    if not data.get("customer"):
        errors.append(_("Customer is required"))
    if not data.get("items"):
        errors.append(_("At least one item is required"))

    # Check link validity
    if data.get("customer"):
        if not frappe.db.exists("Customer", data["customer"]):
            errors.append(_("Customer '{0}' not found").format(data["customer"]))

    if errors:
        frappe.throw("<br>".join(errors))

    doc = frappe.get_doc({"doctype": "Sales Invoice", **data})
    doc.insert()
    return doc
```

### CharacterLengthExceededError

```python
# Pattern: Truncate before save
def safe_set_description(doc, description):
    max_len = 140  # Match field length in DocType
    if len(description) > max_len:
        description = description[:max_len - 3] + "..."
        frappe.msgprint(_("Description truncated to {0} characters").format(max_len))
    doc.description = description
```

### QueryTimeoutError [v15+]

```python
# Pattern: Paginated query to avoid timeout
def get_large_report(filters):
    try:
        return frappe.db.sql(query, filters, as_dict=True)
    except frappe.QueryTimeoutError:
        frappe.log_error(frappe.get_traceback(), "Report Query Timeout")
        frappe.throw(
            _("Report too large. Please narrow your date range or add filters."),
            title=_("Query Timeout")
        )
```

### InReadOnlyMode

```python
# Pattern: Check before write
def safe_write(doctype, name, field, value):
    if frappe.flags.in_import:
        frappe.db.set_value(doctype, name, field, value)
        return
    try:
        frappe.db.set_value(doctype, name, field, value)
    except frappe.InReadOnlyMode:
        frappe.log_error(f"Write blocked: {doctype}/{name}", "Read-Only Mode")
        frappe.throw(_("System is in read-only mode. Please try again later."))
```

---

## Transaction Deadlocks

```python
# ❌ CAUSES DEADLOCKS — long transaction with many writes
def process_all():
    for inv in frappe.get_all("Sales Invoice", limit=10000):
        doc = frappe.get_doc("Sales Invoice", inv.name)
        doc.custom_field = "value"
        doc.save()  # Each save locks rows; other processes wait

# ✅ CORRECT — batch with commits to release locks
def process_all():
    invoices = frappe.get_all("Sales Invoice", limit=10000)
    BATCH = 100
    for i in range(0, len(invoices), BATCH):
        for inv in invoices[i:i + BATCH]:
            frappe.db.set_value("Sales Invoice", inv.name, "custom_field", "value")
        frappe.db.commit()  # Release locks after each batch

# ✅ CORRECT — retry on deadlock
import time
def with_deadlock_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except frappe.QueryDeadlockError:
            if attempt < max_retries - 1:
                frappe.db.rollback()
                time.sleep(0.5 * (attempt + 1))
            else:
                raise
```

---

## MariaDB Gone Away / Too Many Connections

```python
# Pattern: Connection recovery
def reliable_operation():
    try:
        return frappe.db.sql("SELECT 1")
    except frappe.db.InternalError as e:
        msg = str(e).lower()
        if "gone away" in msg or "lost connection" in msg:
            frappe.db.connect()  # Reconnect
            return frappe.db.sql("SELECT 1")
        if "too many connections" in msg:
            frappe.log_error("Too many DB connections", "Connection Pool")
            frappe.throw(_("Server busy. Please try again in a moment."))
        raise  # Unknown InternalError — re-raise
```

**Prevention**:
- Set `wait_timeout` in MariaDB config (default 28800s)
- Check `max_connections` setting matches your workload
- Use connection pooling in production (Gunicorn workers)

---

## Transaction Rules

### When to Commit

| Context | Auto-Commit? | Manual Commit? |
|---------|:------------:|:--------------:|
| Web request (POST/PUT) | YES | NEVER |
| Controller hooks (validate, on_update) | YES | NEVER |
| doc_events hooks | YES | NEVER |
| Scheduler tasks | NO | ALWAYS |
| Background jobs (frappe.enqueue) | NO | ALWAYS |
| bench execute | NO | ALWAYS |

### Savepoints for Partial Rollback

```python
def complex_operation():
    frappe.db.savepoint("before_risky")
    try:
        risky_database_operation()
    except Exception:
        frappe.db.rollback(save_point="before_risky")
        safe_alternative()  # Continue with fallback

# Transaction hooks [v15+]
frappe.db.after_commit.add(lambda: send_notification())
frappe.db.after_rollback.add(lambda: cleanup_files())
```

---

## SQL Injection Prevention

```python
# ❌ INJECTION VULNERABLE — all of these
frappe.db.sql(f"SELECT * FROM `tabItem` WHERE name = '{user_input}'")
frappe.db.sql("SELECT * FROM `tabItem` WHERE name = '%s'" % user_input)
frappe.db.sql("SELECT * FROM `tabItem` WHERE name = '{}'".format(user_input))

# ❌ ALSO VULNERABLE — in permission_query_conditions
def query_conditions(user):
    return f"owner = '{user}'"  # Unescaped!

# ✅ SAFE — parameterized query
frappe.db.sql("SELECT * FROM `tabItem` WHERE name = %(name)s", {"name": user_input})

# ✅ SAFE — frappe.db.escape() for dynamic SQL (permission hooks)
def query_conditions(user):
    return f"owner = {frappe.db.escape(user)}"

# ✅ SAFE — query builder
Item = frappe.qb.DocType("Item")
frappe.qb.from_(Item).where(Item.name == user_input).run()

# ✅ SAFE — ORM methods
frappe.get_all("Item", filters={"name": user_input})
frappe.db.get_value("Item", user_input, "item_name")
```

---

## db.set_value Silent Failure

```python
# ❌ DANGEROUS — no error if record doesn't exist
frappe.db.set_value("Customer", "NONEXISTENT", "status", "Active")
# Returns without error! No rows updated.

# ✅ ALWAYS verify existence before set_value
if not frappe.db.exists("Customer", customer_name):
    frappe.throw(_("Customer '{0}' not found").format(customer_name))
frappe.db.set_value("Customer", customer_name, "status", "Active")

# Note: set_value skips validate/on_update hooks
# Use doc.save() when you need validation to run
```

---

## Critical Rules

### ALWAYS
1. Use `%(name)s` dict params in `frappe.db.sql()` — NEVER string formatting
2. Check `frappe.db.exists()` before `get_doc()` — or catch `DoesNotExistError`
3. Handle `DuplicateEntryError` on every `insert()` call
4. Handle `TimestampMismatchError` on every `save()` in APIs
5. Call `frappe.db.commit()` in scheduler and background jobs
6. Paginate large queries — use `limit` parameter
7. Check `get_value()` result for `None` before using it
8. Use `frappe.db.escape()` in dynamic SQL strings

### NEVER
1. Use string formatting (`f""`, `.format()`, `%`) for SQL values
2. Call `frappe.db.commit()` in controller hooks or doc_events
3. Catch bare `Exception` and `pass` — log or re-raise specific types
4. Assume `db.set_value()` succeeded — it fails silently on missing records
5. Expose raw database error messages to users — log details, show generic message
6. Run unbounded queries without `limit` — memory/timeout risk

---

## Quick Reference: Exception Handling

```python
try:
    doc = frappe.get_doc("Customer", name)
except frappe.DoesNotExistError:
    frappe.throw(_("Not found"))

try:
    doc.insert()
except frappe.DuplicateEntryError:
    existing = frappe.db.get_value("Customer", filters, "name")
except frappe.MandatoryError as e:
    frappe.throw(_("Missing required field: {0}").format(e))

try:
    doc.save()
except frappe.TimestampMismatchError:
    frappe.throw(_("Document modified. Please refresh."))
except frappe.CharacterLengthExceededError:
    frappe.throw(_("Text too long for field"))

try:
    frappe.delete_doc("Customer", name)
except frappe.LinkExistsError:
    frappe.throw(_("Cannot delete — linked documents exist"))

try:
    frappe.db.sql(query, values)
except frappe.QueryTimeoutError:          # [v15+]
    frappe.throw(_("Query too slow. Add filters."))
except frappe.QueryDeadlockError:
    frappe.db.rollback()                   # Retry with backoff
except frappe.db.InternalError as e:
    frappe.log_error(frappe.get_traceback(), "DB Error")
```

---

## Reference Files

| File | Contents |
|------|----------|
| `references/patterns.md` | Complete error handling patterns for all DB operations |
| `references/examples.md` | Full working examples with error handling |
| `references/anti-patterns.md` | Common mistakes with wrong/correct pairs |

---

## See Also

- `frappe-core-database` — Database API syntax and query builder
- `frappe-errors-controllers` — Controller error handling
- `frappe-errors-hooks` — Hook error handling
- `frappe-core-permissions` — Permission patterns
