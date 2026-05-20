---
name: supabase
description: Supabase REST API via curl. Use this skill for database CRUD operations, filtering, pagination, and real-time data management.
vm0_secrets:
  - SUPABASE_SECRET_KEY
vm0_vars:
  - SUPABASE_URL
  - SUPABASE_PUBLISHABLE_KEY
---

# Supabase REST API

Use the Supabase REST API via direct `curl` calls to **perform database CRUD operations**.

Supabase auto-generates a RESTful API from your PostgreSQL database schema using [PostgREST](https://postgrest.org/).

> Official docs: `https://supabase.com/docs/guides/api`

---

## When to Use

Use this skill when you need to:

- **Read data** from Supabase tables with filtering and pagination
- **Insert rows** into tables (single or bulk)
- **Update rows** based on conditions
- **Delete rows** from tables
- **Upsert data** (insert or update)
- **Query with complex filters** using PostgREST operators

---

## Prerequisites

1. Create a Supabase project at https://supabase.com
2. Go to **Project Settings → API Keys**
3. Click **Create new API Keys** if needed
4. Copy the **Project URL** and keys

```bash
export SUPABASE_URL="https://your-project-ref.supabase.co"
export SUPABASE_PUBLISHABLE_KEY="sb_publishable_..."
export SUPABASE_SECRET_KEY="sb_secret_..."
```

**API Keys:**

| Key Type | Format | Use Case |
|----------|--------|----------|
| Publishable | `sb_publishable_...` | Client-side, respects Row Level Security (RLS) |
| Secret | `sb_secret_...` | Server-side only, bypasses RLS |

> **Note:** Legacy `anon` and `service_role` JWT keys still work but are deprecated. Use the new `sb_publishable_` and `sb_secret_` keys instead.

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

Base URL: `${SUPABASE_URL}/rest/v1`

All requests require the `apikey` header with your API key.

---

### 1. Read All Rows

Get all rows from a table:

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/users?select=*" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

---

### 2. Select Specific Columns

Get only specific columns:

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/users?select=id,name,email" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

---

### 3. Filter with Operators

Filter rows using PostgREST operators.

**Equal to:**

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/users?status=eq.active" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

**Greater than:**

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/products?price=gt.100" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

**Multiple conditions (AND):**

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/users?age=gte.18&status=eq.active" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

**Available Operators:**

| Operator | Meaning | Example |
|----------|---------|---------|
| `eq` | Equals | `?status=eq.active` |
| `neq` | Not equals | `?status=neq.deleted` |
| `gt` | Greater than | `?age=gt.18` |
| `gte` | Greater than or equal | `?age=gte.21` |
| `lt` | Less than | `?price=lt.100` |
| `lte` | Less than or equal | `?price=lte.50` |
| `like` | Pattern match (use `*` for `%`) | `?name=like.*john*` |
| `ilike` | Case-insensitive pattern | `?name=ilike.*john*` |
| `in` | In list | `?id=in.(1,2,3)` |
| `is` | Is null/true/false | `?deleted_at=is.null` |

---

### 4. OR Conditions

Use `or` for OR logic:

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/users?or=(status.eq.active,status.eq.pending)" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

---

### 5. Ordering

Sort results.

**Ascending:**

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/users?order=created_at.asc" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

**Descending:**

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/users?order=created_at.desc" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

**Multiple columns:**

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/users?order=status.asc,created_at.desc" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

---

### 6. Pagination

Use `limit` and `offset`.

**First 10 rows:**

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/users?limit=10" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

**Page 2 (rows 11-20):**

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/users?limit=10&offset=10" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

---

### 7. Get Row Count

Use `Prefer: count=exact` header:

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/users?select=*" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}" -H "Prefer: count=exact" -I | grep -i "content-range"'
```

---

### 8. Insert Single Row

Write to `/tmp/supabase_request.json`:

```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${SUPABASE_URL}/rest/v1/users" -H "apikey: ${SUPABASE_SECRET_KEY}" -H "Content-Type: application/json" -H "Prefer: return=representation" -d @/tmp/supabase_request.json'
```

---

### 9. Insert Multiple Rows

Write to `/tmp/supabase_request.json`:

```json
[
  {"name": "John", "email": "john@example.com"},
  {"name": "Jane", "email": "jane@example.com"}
]
```

Then run:

```bash
bash -c 'curl -s -X POST "${SUPABASE_URL}/rest/v1/users" -H "apikey: ${SUPABASE_SECRET_KEY}" -H "Content-Type: application/json" -H "Prefer: return=representation" -d @/tmp/supabase_request.json'
```

---

### 10. Update Rows

Update rows matching a filter.

Write to `/tmp/supabase_request.json`:

```json
{
  "status": "inactive"
}
```

Then run:

```bash
bash -c 'curl -s -X PATCH "${SUPABASE_URL}/rest/v1/users?id=eq.1" -H "apikey: ${SUPABASE_SECRET_KEY}" -H "Content-Type: application/json" -H "Prefer: return=representation" -d @/tmp/supabase_request.json'
```

---

### 11. Upsert (Insert or Update)

Use `Prefer: resolution=merge-duplicates`.

Write to `/tmp/supabase_request.json`:

```json
{
  "id": 1,
  "name": "John Updated",
  "email": "john@example.com"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${SUPABASE_URL}/rest/v1/users" -H "apikey: ${SUPABASE_SECRET_KEY}" -H "Content-Type: application/json" -H "Prefer: resolution=merge-duplicates,return=representation" -d @/tmp/supabase_request.json'
```

---

### 12. Delete Rows

Delete rows matching a filter:

```bash
bash -c 'curl -s -X DELETE "${SUPABASE_URL}/rest/v1/users?id=eq.1" -H "apikey: ${SUPABASE_SECRET_KEY}" -H "Prefer: return=representation"'
```

---

### 13. Query Related Tables

Embed related data using foreign keys.

**Get posts with their author:**

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/posts?select=*,author:users(*)" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

**Get users with their posts:**

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/users?select=*,posts(*)" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

---

### 14. Full-Text Search

Search text columns:

```bash
bash -c 'curl -s "${SUPABASE_URL}/rest/v1/posts?title=fts.hello" -H "apikey: ${SUPABASE_PUBLISHABLE_KEY}"'
```

---

### 15. Call RPC Functions

Call PostgreSQL functions.

Write to `/tmp/supabase_request.json`:

```json
{
  "param1": "value1"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${SUPABASE_URL}/rest/v1/rpc/my_function" -H "apikey: ${SUPABASE_SECRET_KEY}" -H "Content-Type: application/json" -d @/tmp/supabase_request.json'
```

---

## Response Headers

| Header | Description |
|--------|-------------|
| `Content-Range` | Row range and total count (e.g., `0-9/100`) |
| `Preference-Applied` | Confirms applied preferences |

---

## Guidelines

1. **Use publishable key** for read operations with RLS enabled
2. **Use secret key** only server-side for write operations or admin access
3. **Enable RLS** on tables for security when using publishable key
4. **Use `select`** to limit returned columns for better performance
5. **Add indexes** on frequently filtered columns
6. **Use `Prefer: return=representation`** to get inserted/updated rows back
7. **Avoid full-table operations** without filters to prevent accidental data loss

---

## API Reference

- Supabase API Docs: https://supabase.com/docs/guides/api
- API Keys Guide: https://supabase.com/docs/guides/api/api-keys
- PostgREST Docs: https://postgrest.org/en/stable/
- API Settings: https://supabase.com/dashboard/project/_/settings/api-keys
