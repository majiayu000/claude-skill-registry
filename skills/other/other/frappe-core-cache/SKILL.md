---
name: frappe-core-cache
description: >
  Use when implementing Redis caching, cache invalidation, or distributed locking in Frappe.
  Prevents stale cache bugs, race conditions from missing locks, and memory bloat from unbounded cache keys.
  Covers frappe.cache(), @redis_cache decorator, cache.get_value/set_value, cache invalidation patterns, frappe.lock, TTL strategies.
  Keywords: cache, Redis, redis_cache, invalidation, locking, frappe.cache, get_value, set_value, TTL, distributed lock.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Cache & Locking

## Quick Reference

| Action | Method | Notes |
|--------|--------|-------|
| Set value | `frappe.cache.set_value(key, val)` | With optional TTL |
| Get value | `frappe.cache.get_value(key)` | Returns `None` if missing |
| Get or generate | `frappe.cache.get_value(key, generator=fn)` | Calls `fn()` on cache miss |
| Delete value | `frappe.cache.delete_value(key)` | Single key or list of keys |
| Delete by pattern | `frappe.cache.delete_keys(pattern)` | Wildcard `*` matching |
| Hash set | `frappe.cache.hset(name, key, val)` | Redis hash field |
| Hash get | `frappe.cache.hget(name, key)` | Single hash field |
| Hash get all | `frappe.cache.hgetall(name)` | Full hash as dict |
| Hash delete | `frappe.cache.hdel(name, key)` | Remove hash field |
| Hash exists | `frappe.cache.hexists(name, key)` | Returns bool |
| Cached document | `frappe.get_cached_doc(dt, dn)` | Full doc from cache |
| Clear doc cache | `frappe.clear_document_cache(dt, dn)` | Invalidate cached doc |
| Decorator cache | `@redis_cache` | Auto-cache function result |
| Request cache | `frappe.local.cache` | Per-request dict (not Redis) |

---

## Decision Tree

```
What caching pattern do you need?
│
├─ Cache a function result automatically?
│  ├─ Pure function (same args → same result) → @redis_cache
│  └─ Need custom key/TTL → manual get_value/set_value
│
├─ Cache a document?
│  ├─ Read-only access → frappe.get_cached_doc()
│  └─ Need to invalidate → frappe.clear_document_cache()
│
├─ Cache structured data (multiple fields)?
│  └─ Redis hash → hset/hget/hgetall
│
├─ Per-request cache (avoid repeated DB calls in one request)?
│  └─ frappe.local.cache dict
│
├─ Prevent concurrent execution?
│  └─ Distributed lock → frappe.lock("resource_name")
│
└─ Invalidate cache?
   ├─ Single key → delete_value(key)
   ├─ Pattern → delete_keys("prefix*")
   └─ All site cache → frappe.clear_cache()
```

---

## String Operations

### Set and Get

```python
# Set a value (persists until evicted or deleted)
frappe.cache.set_value("exchange_rate_USD", 1.08)

# Set with TTL (expires after N seconds)
frappe.cache.set_value("exchange_rate_USD", 1.08, expires_in_sec=3600)

# Get value (returns None if missing)
rate = frappe.cache.get_value("exchange_rate_USD")

# Get with generator (calls function on cache miss, stores result)
rate = frappe.cache.get_value(
    "exchange_rate_USD",
    generator=lambda: fetch_exchange_rate("USD"),
)
```

### User-Scoped Values

```python
# Store per-user preference
frappe.cache.set_value("dashboard_layout", "compact", user="user@example.com")

# Retrieve for specific user
layout = frappe.cache.get_value("dashboard_layout", user="user@example.com")
```

### Delete

```python
# Single key
frappe.cache.delete_value("exchange_rate_USD")

# Multiple keys
frappe.cache.delete_value(["exchange_rate_USD", "exchange_rate_EUR"])

# Pattern-based deletion (wildcard)
frappe.cache.delete_keys("exchange_rate*")
```

---

## Hash Operations

Use hashes to group related fields under a single key.

```python
# Set hash fields
frappe.cache.hset("config|notifications", "email_enabled", True)
frappe.cache.hset("config|notifications", "sms_enabled", False)
frappe.cache.hset("config|notifications", "max_retries", 3)

# Get single field
email_on = frappe.cache.hget("config|notifications", "email_enabled")

# Get all fields as dict
config = frappe.cache.hgetall("config|notifications")
# {"email_enabled": True, "sms_enabled": False, "max_retries": 3}

# Delete field
frappe.cache.hdel("config|notifications", "sms_enabled")

# Check existence
exists = frappe.cache.hexists("config|notifications", "email_enabled")
```

### Hash with Generator

```python
# hget with generator — calls function on miss
value = frappe.cache.hget(
    "user|permissions",
    "user@example.com",
    generator=lambda: compute_permissions("user@example.com"),
)
```

---

## @redis_cache Decorator

Automatically cache function return values based on arguments.

```python
from frappe.utils.caching import redis_cache

@redis_cache
def get_item_price(item_code, price_list):
    """Expensive query — cached automatically."""
    return frappe.db.get_value("Item Price",
        {"item_code": item_code, "price_list": price_list},
        "price_list_rate",
    )

# First call — hits database, stores in Redis
price = get_item_price("ITEM-001", "Standard Selling")

# Second call — returns from cache
price = get_item_price("ITEM-001", "Standard Selling")

# Clear all cached results for this function
get_item_price.clear_cache()
```

### With TTL

```python
@redis_cache(ttl=300)  # expires after 5 minutes
def get_exchange_rate(from_currency, to_currency):
    return fetch_rate_from_api(from_currency, to_currency)
```

**Rules for @redis_cache:**
- ALWAYS ensure arguments are hashable (strings, numbers, tuples). NEVER pass dicts or lists as arguments.
- ALWAYS call `.clear_cache()` when underlying data changes.
- NEVER use on functions with side effects — the function will NOT execute on cache hits.

---

## frappe.local.cache — Request-Scoped Cache

`frappe.local.cache` is a plain Python dict that lives for the duration of a single HTTP request. It is NOT stored in Redis.

```python
def get_user_settings():
    """Avoid repeated DB calls within a single request."""
    if "user_settings" not in frappe.local.cache:
        frappe.local.cache["user_settings"] = frappe.get_doc(
            "User Settings", frappe.session.user
        )
    return frappe.local.cache["user_settings"]
```

Use `frappe.local.cache` when:
- The same data is needed multiple times in one request
- The data does NOT need to persist across requests
- You want zero Redis overhead

---

## Document Caching

```python
# Get cached document (read-only, no permission check)
settings = frappe.get_cached_doc("System Settings")
item = frappe.get_cached_doc("Item", "ITEM-001")

# Invalidate when document changes
frappe.clear_document_cache("Item", "ITEM-001")

# Cached single value
val = frappe.db.get_value("Item", "ITEM-001", "item_name", cache=True)
```

NEVER modify a document returned by `frappe.get_cached_doc()` — it returns a shared reference. Modifications corrupt the cache for all subsequent reads.

---

## Distributed Locking

Prevent concurrent execution of critical sections using Redis-based locks.

```python
# Context manager (recommended)
with frappe.lock("process_payroll"):
    # Only one worker executes this block at a time
    process_all_salary_slips()
    # Lock auto-released on exit

# Manual lock/unlock
frappe.lock("inventory_sync")
try:
    sync_inventory()
finally:
    frappe.unlock("inventory_sync")  # ALWAYS unlock in finally
```

**Rules:**
- ALWAYS use `with frappe.lock()` (context manager) to guarantee release.
- NEVER hold locks for more than a few seconds — long locks cause worker starvation.
- ALWAYS use descriptive lock names to avoid collisions.

---

## Cache Invalidation Patterns

### Pattern 1: TTL-Based (Time-to-Live)

```python
frappe.cache.set_value("dashboard_stats", compute_stats(), expires_in_sec=300)
```

Best for: Data that can be slightly stale (exchange rates, dashboard aggregates).

### Pattern 2: Event-Based Invalidation

```python
# In hooks.py
doc_events = {
    "Item Price": {
        "on_update": "my_app.cache.invalidate_price_cache",
        "on_trash": "my_app.cache.invalidate_price_cache",
    }
}

# In my_app/cache.py
def invalidate_price_cache(doc, method):
    frappe.cache.delete_keys("item_price*")
    # Or clear specific function cache:
    # get_item_price.clear_cache()
```

Best for: Data that MUST be fresh immediately after changes.

### Pattern 3: Hybrid (TTL + Event)

```python
@redis_cache(ttl=600)
def get_pricing_rules():
    return frappe.get_all("Pricing Rule", fields=["*"])

# Event hook clears cache immediately on change
def on_pricing_rule_update(doc, method):
    get_pricing_rules.clear_cache()
```

Best for: Frequently read data with occasional updates.

---

## Common Cache Keys (Internal)

| Key Pattern | Content |
|-------------|---------|
| `doctype::meta::{dt}` | DocType metadata |
| `user_permissions::{user}` | User permission cache |
| `bootinfo::{user}` | User boot info |
| `notifications::{user}` | Notification counts |
| `document_cache::{dt}::{dn}` | Cached document |

NEVER write to internal cache keys directly. ALWAYS use the documented API methods (`get_cached_doc`, `clear_document_cache`, etc.).

---

## Performance Guidelines

1. **ALWAYS set TTL** on cached values that derive from external data — without TTL, stale data persists until manual invalidation or Redis eviction.
2. **NEVER cache large objects** (>1 MB) — Redis uses pickle serialization, and large values increase serialization overhead and memory usage.
3. **ALWAYS use `frappe.local.cache`** for data needed multiple times within a single request — it avoids Redis round-trips entirely.
4. **NEVER use `frappe.clear_cache()`** as a routine invalidation strategy — it clears ALL cache keys for the site, causing a cold-cache performance hit.
5. **ALWAYS prefix custom cache keys** with your app name (e.g., `myapp|exchange_rate`) to avoid collisions with Frappe internals.

---

## Redis Configuration

Default config: `{bench}/config/redis_cache.conf`

| Setting | Default | Description |
|---------|---------|-------------|
| Port | 13000 | Redis cache port |
| Bind | 127.0.0.1 | Listen address |
| maxmemory-policy | allkeys-lru | Eviction policy |
| maxmemory | 256mb | Max memory (adjustable) |

---

## Key Namespacing

All cache keys are automatically prefixed by Frappe with the site name:

```python
# You write:
frappe.cache.set_value("my_key", "value")

# Redis stores:
# "mysite.localhost|my_key"
```

`frappe.cache.make_key(key, user, shared)` handles prefixing. The `shared=True` parameter removes the site prefix for cross-site keys (rare use case).

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| `frappe.cache.set_value` | Available | Available | Available |
| `@redis_cache` | Not available | Available | Available |
| `@redis_cache(ttl=)` | Not available | Available | Available |
| `frappe.lock` context mgr | Available | Available | Available |
| `frappe.local.cache` | Available | Available | Available |
| `hget` with generator | Available | Available | Available |

---

## See Also

- [references/examples.md](references/examples.md) — Cache implementation patterns
- [references/anti-patterns.md](references/anti-patterns.md) — Common cache mistakes
- [references/api-reference.md](references/api-reference.md) — Complete API signatures
- `frappe-core-database` — Database queries that benefit from caching
- `frappe-core-permissions` — User permission caching
