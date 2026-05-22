---
name: supabase-audit-tables-list
description: List all tables exposed via the Supabase PostgREST API to identify the attack surface.
---

# List Exposed Tables

> 🔴 **CRITICAL: PROGRESSIVE FILE UPDATES REQUIRED**
>
> You MUST write to context files **AS YOU GO**, not just at the end.
> - Write to `.sb-pentest-context.json` **IMMEDIATELY after each discovery**
> - Log to `.sb-pentest-audit.log` **BEFORE and AFTER each action**
> - **DO NOT** wait until the skill completes to update files
> - If the skill crashes or is interrupted, all prior findings must already be saved
>
> **This is not optional. Failure to write progressively is a critical error.**

This skill discovers all database tables exposed through the Supabase PostgREST API.

## When to Use This Skill

- To understand the API attack surface
- Before testing RLS policies
- To inventory exposed data models
- As part of a comprehensive security audit

## Prerequisites

- Supabase URL extracted (auto-invokes if needed)
- Anon key extracted (auto-invokes if needed)

## How It Works

Supabase exposes tables via PostgREST at:
```
https://[project-ref].supabase.co/rest/v1/
```

The skill uses the OpenAPI schema endpoint to enumerate tables:
```
https://[project-ref].supabase.co/rest/v1/?apikey=[anon-key]
```

## What Gets Exposed

By default, Supabase exposes tables in the `public` schema. Tables are exposed when:

1. They exist in an exposed schema (default: `public`)
2. No explicit `REVOKE` has been done
3. PostgREST can see them

## Usage

### Basic Table List

```
List tables exposed on my Supabase project
```

### With Schema Information

```
List all exposed tables with column details
```

## Output Format

```
═══════════════════════════════════════════════════════════
 EXPOSED TABLES
═══════════════════════════════════════════════════════════

 Project: abc123def.supabase.co
 Schema: public
 Tables Found: 8

 ─────────────────────────────────────────────────────────
 Table Inventory
 ─────────────────────────────────────────────────────────

 1. users
    ├── Columns: id, email, name, avatar_url, created_at
    ├── Primary Key: id (uuid)
    ├── RLS Status: Unknown (test with supabase-audit-rls)
    └── Risk: ⚠️ Contains user PII

 2. profiles
    ├── Columns: id, user_id, bio, website, social_links
    ├── Primary Key: id (uuid)
    ├── Foreign Key: user_id → auth.users
    └── Risk: ⚠️ Contains user PII

 3. posts
    ├── Columns: id, author_id, title, content, published, created_at
    ├── Primary Key: id (uuid)
    └── Risk: ℹ️ Content data

 4. comments
    ├── Columns: id, post_id, user_id, content, created_at
    ├── Primary Key: id (uuid)
    └── Risk: ℹ️ Content data

 5. orders
    ├── Columns: id, user_id, total, status, items, created_at
    ├── Primary Key: id (uuid)
    └── Risk: 🔴 Contains financial/transaction data

 6. products
    ├── Columns: id, name, description, price, stock, image_url
    ├── Primary Key: id (uuid)
    └── Risk: ℹ️ Public catalog data

 7. settings
    ├── Columns: id, key, value, updated_at
    ├── Primary Key: id (uuid)
    └── Risk: ⚠️ May contain sensitive configuration

 8. api_keys
    ├── Columns: id, user_id, key_hash, name, last_used
    ├── Primary Key: id (uuid)
    └── Risk: 🔴 Contains secrets

 ─────────────────────────────────────────────────────────
 Summary
 ─────────────────────────────────────────────────────────

 Total Tables: 8
 High Risk: 2 (orders, api_keys)
 Medium Risk: 3 (users, profiles, settings)
 Low Risk: 3 (posts, comments, products)

 Next Steps:
 ├── Run supabase-audit-tables-read to test actual data access
 ├── Run supabase-audit-rls to verify RLS policies
 └── Review high-risk tables first

═══════════════════════════════════════════════════════════
```

## Risk Classification

Tables are classified by likely content:

| Risk | Table Patterns | Examples |
|------|---------------|----------|
| 🔴 High | Financial, secrets, auth | orders, payments, api_keys, secrets |
| ⚠️ Medium | User PII, config | users, profiles, settings, preferences |
| ℹ️ Low | Public content | posts, products, categories, tags |

## Context Output

```json
{
  "tables": {
    "count": 8,
    "list": [
      {
        "name": "users",
        "schema": "public",
        "columns": ["id", "email", "name", "avatar_url", "created_at"],
        "primary_key": "id",
        "risk_level": "medium",
        "risk_reason": "Contains user PII"
      },
      {
        "name": "orders",
        "schema": "public",
        "columns": ["id", "user_id", "total", "status", "items", "created_at"],
        "primary_key": "id",
        "risk_level": "high",
        "risk_reason": "Contains financial data"
      }
    ],
    "by_risk": {
      "high": ["orders", "api_keys"],
      "medium": ["users", "profiles", "settings"],
      "low": ["posts", "comments", "products"]
    }
  }
}
```

## Hidden Tables

Some tables may not appear in the OpenAPI schema:

```
═══════════════════════════════════════════════════════════
 ADDITIONAL DISCOVERY
═══════════════════════════════════════════════════════════

 Common Tables Not in Schema (testing existence):
 ├── _prisma_migrations: ❌ Not found
 ├── schema_migrations: ❌ Not found
 ├── audit_log: ✅ EXISTS but not in OpenAPI
 └── internal_config: ❌ Not found

 Note: 'audit_log' exists but may have restricted access.
       Test with supabase-audit-tables-read.
═══════════════════════════════════════════════════════════
```

## Schema Analysis

The skill also checks for non-public schemas:

```
Schema Exposure Check:
├── public: ✅ Exposed (8 tables)
├── auth: ❌ Not directly exposed (expected)
├── storage: ❌ Not directly exposed (expected)
├── extensions: ❌ Not exposed (good)
└── custom_schema: ⚠️ Exposed (3 tables) - Review if intentional
```

## Common Issues

❌ **Problem:** No tables found
✅ **Solution:**
- Check if anon key is valid
- Verify project URL is correct
- The API may be disabled in project settings

❌ **Problem:** Too many tables listed
✅ **Solution:** This may indicate overly permissive schema exposure. Consider:
```sql
-- Restrict exposed schemas
ALTER ROLE anon SET search_path TO public;
```

❌ **Problem:** Sensitive tables exposed
✅ **Solution:** Either remove from public schema or implement strict RLS.

## Recommendations by Table Type

### User Tables

```sql
-- Ensure RLS is enabled
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users see own data" ON users
  FOR SELECT USING (auth.uid() = id);
```

### Order/Payment Tables

```sql
-- Strict RLS for financial data
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users see own orders" ON orders
  FOR SELECT USING (auth.uid() = user_id);

-- No public access even for admins via API
-- Use Edge Functions for admin operations
```

### Secret Tables

```sql
-- Consider not exposing at all
REVOKE ALL ON TABLE api_keys FROM anon, authenticated;

-- Or use views that hide sensitive columns
CREATE VIEW public.api_keys_safe AS
  SELECT id, name, last_used FROM api_keys;
```

## MANDATORY: Progressive Context File Updates

⚠️ **This skill MUST update tracking files PROGRESSIVELY during execution, NOT just at the end.**

### Critical Rule: Write As You Go

**DO NOT** batch all writes at the end. Instead:

1. **Before starting any action** → Log the action to `.sb-pentest-audit.log`
2. **After each table discovered** → Immediately update `.sb-pentest-context.json`
3. **After each significant step** → Log completion to `.sb-pentest-audit.log`

This ensures that if the skill is interrupted, crashes, or times out, all findings up to that point are preserved.

### Required Actions (Progressive)

1. **Update `.sb-pentest-context.json`** with results:
   ```json
   {
     "tables": {
       "count": 8,
       "list": [ ... ],
       "by_risk": { "high": [], "medium": [], "low": [] }
     }
   }
   ```

2. **Log to `.sb-pentest-audit.log`**:
   ```
   [TIMESTAMP] [supabase-audit-tables-list] [START] Listing exposed tables
   [TIMESTAMP] [supabase-audit-tables-list] [SUCCESS] Found 8 tables
   [TIMESTAMP] [supabase-audit-tables-list] [CONTEXT_UPDATED] .sb-pentest-context.json updated
   ```

3. **If files don't exist**, create them before writing.

**FAILURE TO UPDATE CONTEXT FILES IS NOT ACCEPTABLE.**

## MANDATORY: Evidence Collection

📁 **Evidence Directory:** `.sb-pentest-evidence/03-api-audit/tables/`

### Evidence Files to Create

| File | Content |
|------|---------|
| `tables-list.json` | Complete list of exposed tables |
| `tables-metadata.json` | Column details and types per table |
| `openapi-schema.json` | Raw OpenAPI/PostgREST schema |

### Evidence Format

```json
{
  "evidence_id": "API-TBL-001",
  "timestamp": "2025-01-31T10:15:00Z",
  "category": "api-audit",
  "type": "table_enumeration",

  "request": {
    "method": "GET",
    "url": "https://abc123def.supabase.co/rest/v1/",
    "headers": {
      "apikey": "[REDACTED]"
    },
    "curl_command": "curl -s 'https://abc123def.supabase.co/rest/v1/' -H 'apikey: $ANON_KEY'"
  },

  "tables_found": [
    {
      "name": "users",
      "schema": "public",
      "columns": ["id", "email", "name", "created_at"],
      "primary_key": "id",
      "risk_level": "high",
      "risk_reason": "Contains PII"
    },
    {
      "name": "orders",
      "schema": "public",
      "columns": ["id", "user_id", "total", "status"],
      "primary_key": "id",
      "risk_level": "high",
      "risk_reason": "Financial data"
    }
  ],

  "summary": {
    "total_tables": 8,
    "high_risk": 2,
    "medium_risk": 3,
    "low_risk": 3
  }
}
```

### Add to curl-commands.sh

```bash
# === TABLE ENUMERATION ===
# List all exposed tables via OpenAPI schema
curl -s "$SUPABASE_URL/rest/v1/" -H "apikey: $ANON_KEY"
```

## Related Skills

- `supabase-audit-tables-read` — Test actual data access
- `supabase-audit-rls` — Verify RLS policies
- `supabase-audit-rpc` — Check exposed functions
