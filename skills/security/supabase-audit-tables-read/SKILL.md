---
name: supabase-audit-tables-read
description: Attempt to read data from exposed tables to verify actual data exposure and RLS effectiveness.
---

# Table Data Access Test

> 🔴 **CRITICAL: PROGRESSIVE FILE UPDATES REQUIRED**
>
> You MUST write to context files **AS YOU GO**, not just at the end.
> - Write to `.sb-pentest-context.json` **IMMEDIATELY after each table tested**
> - Log to `.sb-pentest-audit.log` **BEFORE and AFTER each test**
> - **DO NOT** wait until the skill completes to update files
> - If the skill crashes or is interrupted, all prior findings must already be saved
>
> **This is not optional. Failure to write progressively is a critical error.**

This skill attempts to read data from exposed tables to determine what information is actually accessible.

## When to Use This Skill

- After listing tables, to verify actual access
- To test RLS policy effectiveness
- To assess the severity of data exposure
- To document exactly what data can be retrieved

## Prerequisites

- Tables listed (auto-invokes `supabase-audit-tables-list` if needed)
- Anon key available

## How It Works

The skill performs SELECT queries on each exposed table:

```
GET https://[project].supabase.co/rest/v1/[table]?select=*&limit=5
Authorization: Bearer [anon-key]
```

**Important:** This is READ-ONLY. No data is modified or deleted.

## Test Modes

| Mode | Description | Queries |
|------|-------------|---------|
| **Quick** | First 5 rows from each table | `?limit=5` |
| **Sample** | Random sample across tables | `?limit=10&order=random` |
| **Count** | Just row counts, no data | `HEAD` request |

## Usage

### Basic Read Test

```
Test read access on exposed tables
```

### Quick Count Only

```
Count accessible rows in all tables (no data retrieval)
```

### Specific Table

```
Test read access on the users table
```

## Output Format

```
═══════════════════════════════════════════════════════════
 DATA ACCESS TEST RESULTS
═══════════════════════════════════════════════════════════

 Test Mode: Quick (5 rows per table)
 Tables Tested: 8

 ─────────────────────────────────────────────────────────
 Results by Table
 ─────────────────────────────────────────────────────────

 1. users
    Status: 🔴 P0 - DATA EXPOSED
    Rows Retrieved: 5 (of 1,247 total)
    Sample Data:
    ┌─────────────────────────────────────────────────────┐
    │ id: 550e8400-e29b-41d4-a716-446655440001           │
    │ email: john.doe@example.com ← PII EXPOSED          │
    │ name: John Doe ← PII EXPOSED                       │
    │ avatar_url: https://...                            │
    │ created_at: 2025-01-15T10:30:00Z                   │
    └─────────────────────────────────────────────────────┘
    Finding: User emails and names accessible without auth

 2. profiles
    Status: 🟠 P1 - PARTIAL ACCESS
    Rows Retrieved: 5
    Note: Only public fields returned (RLS working partially)
    Columns Visible: id, bio, website
    Columns Blocked: user_id, social_links, private_notes

 3. posts
    Status: ✅ EXPECTED ACCESS
    Rows Retrieved: 5
    Note: Only published=true posts returned (RLS working)
    Data: Public content, appropriate access level

 4. orders
    Status: ✅ BLOCKED
    Response: 403 Forbidden
    Message: "new row violates row-level security policy"
    Note: RLS properly blocking access

 5. api_keys
    Status: ✅ BLOCKED
    Response: 403 Forbidden
    Note: RLS properly protecting secrets

 6. products
    Status: ✅ EXPECTED ACCESS
    Rows Retrieved: 5
    Note: Public catalog data, appropriate access

 7. comments
    Status: 🟠 P1 - MORE DATA THAN EXPECTED
    Rows Retrieved: 5
    Issue: user_id column exposed (can correlate to users)
    Recommendation: Use a view to hide user_id

 8. settings
    Status: 🔴 P0 - SENSITIVE DATA EXPOSED
    Rows Retrieved: 3
    Sample Data:
    ┌─────────────────────────────────────────────────────┐
    │ key: stripe_webhook_secret                          │
    │ value: whsec_xxxxxxxxxxxx ← SECRET EXPOSED         │
    └─────────────────────────────────────────────────────┘
    Finding: Application secrets in accessible table!

 ─────────────────────────────────────────────────────────
 Summary
 ─────────────────────────────────────────────────────────

 P0 (Critical): 2 tables with sensitive data exposed
 P1 (High): 2 tables with partial/unexpected exposure
 Blocked: 2 tables properly protected
 Expected: 2 tables with appropriate public access

 Total Rows Accessible: 1,892 across exposed tables

 Immediate Actions:
 1. Fix 'settings' table - remove from public or add RLS
 2. Fix 'users' table - add RLS to protect email/name
 3. Review 'comments' to hide user correlation

═══════════════════════════════════════════════════════════
```

## Severity Assessment

| Status | Severity | Criteria |
|--------|----------|----------|
| 🔴 DATA EXPOSED | P0 | Sensitive data (PII, secrets, financial) accessible |
| 🟠 PARTIAL ACCESS | P1 | More data than expected, but not critical |
| 🟡 UNEXPECTED | P2 | Accessible but low-risk data |
| ✅ BLOCKED | - | RLS properly preventing access |
| ✅ EXPECTED | - | Public data, appropriate access |

## Data Classification

The skill identifies sensitive data types:

| Type | Patterns | Severity if Exposed |
|------|----------|---------------------|
| PII | email, phone, name, address | P0 |
| Financial | amount, total, card, payment | P0 |
| Secrets | key, secret, token, password | P0 |
| Auth | user_id, session, jwt | P1 |
| Metadata | created_at, updated_at | P2 |

## Context Output

```json
{
  "data_access": {
    "timestamp": "2025-01-31T10:30:00Z",
    "tables_tested": 8,
    "summary": {
      "p0_exposed": 2,
      "p1_partial": 2,
      "blocked": 2,
      "expected": 2
    },
    "results": [
      {
        "table": "users",
        "status": "exposed",
        "severity": "P0",
        "rows_accessible": 1247,
        "sensitive_columns": ["email", "name"],
        "sample_redacted": true
      },
      {
        "table": "settings",
        "status": "exposed",
        "severity": "P0",
        "rows_accessible": 3,
        "sensitive_data_types": ["secrets"],
        "finding": "Application secrets exposed"
      }
    ],
    "total_rows_accessible": 1892
  }
}
```

## Audit Log Entry

```
[2025-01-31T10:30:00Z] READ_TEST_START tables=8
[2025-01-31T10:30:01Z] READ_TEST table=users status=200 rows=5 severity=P0
[2025-01-31T10:30:01Z] READ_TEST table=orders status=403 severity=none
[2025-01-31T10:30:02Z] READ_TEST_COMPLETE exposed=4 blocked=2
```

## Remediation Examples

### For User Tables

```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Only authenticated users see their own data
CREATE POLICY "Users see own data"
  ON users FOR SELECT
  USING (auth.uid() = id);

-- Or create a public view with limited columns
CREATE VIEW public.users_public AS
  SELECT id, avatar_url, created_at FROM users;
```

### For Settings Tables

```sql
-- Remove from public access entirely
REVOKE ALL ON TABLE settings FROM anon, authenticated;

-- Access only via Edge Functions
-- In your Edge Function:
const { data } = await supabaseAdmin
  .from('settings')
  .select('*')
  .eq('key', 'stripe_webhook_secret')
  .single()
```

### For Content Tables

```sql
-- RLS for published content only
CREATE POLICY "Public sees published posts"
  ON posts FOR SELECT
  USING (published = true);

-- Authors see their own drafts
CREATE POLICY "Authors see own posts"
  ON posts FOR SELECT
  USING (auth.uid() = author_id);
```

## Common Issues

❌ **Problem:** All tables return 403
✅ **Solution:** RLS may be too restrictive or anon key invalid. This is actually good from a security standpoint.

❌ **Problem:** Empty results but no error
✅ **Solution:** RLS is filtering all rows. Table structure is exposed but no data.

❌ **Problem:** Timeout on large tables
✅ **Solution:** Use count mode or reduce limit.

## MANDATORY: Progressive Context File Updates

⚠️ **This skill MUST update tracking files PROGRESSIVELY during execution, NOT just at the end.**

### Critical Rule: Write As You Go

**DO NOT** batch all writes at the end. Instead:

1. **Before testing each table** → Log the action to `.sb-pentest-audit.log`
2. **After each table tested** → Immediately update `.sb-pentest-context.json` with results
3. **After each finding** → Log the severity to `.sb-pentest-audit.log`

This ensures that if the skill is interrupted, crashes, or times out, all findings up to that point are preserved.

### Required Actions (Progressive)

1. **Update `.sb-pentest-context.json`** with results:
   ```json
   {
     "data_access": {
       "timestamp": "...",
       "tables_tested": 8,
       "summary": { "p0_exposed": 2, ... },
       "results": [ ... ],
       "total_rows_accessible": 1892
     }
   }
   ```

2. **Log to `.sb-pentest-audit.log`**:
   ```
   [TIMESTAMP] [supabase-audit-tables-read] [START] Testing data access
   [TIMESTAMP] [supabase-audit-tables-read] [FINDING] P0: users table exposed
   [TIMESTAMP] [supabase-audit-tables-read] [CONTEXT_UPDATED] .sb-pentest-context.json updated
   ```

3. **If files don't exist**, create them before writing.

**FAILURE TO UPDATE CONTEXT FILES IS NOT ACCEPTABLE.**

## MANDATORY: Evidence Collection

📁 **Evidence Directory:** `.sb-pentest-evidence/03-api-audit/data-samples/`

### Evidence Files to Create

| File | Content |
|------|---------|
| `data-samples/[table]-sample.json` | Sample data from each accessible table |
| `data-samples/[table]-blocked.json` | Proof of blocked access (403 response) |

### Evidence Format (Data Exposed)

```json
{
  "evidence_id": "API-READ-001",
  "timestamp": "2025-01-31T10:20:00Z",
  "category": "api-audit",
  "type": "data_access",
  "severity": "P0",
  "finding_id": "P0-002",

  "table": "users",

  "request": {
    "method": "GET",
    "url": "https://abc123def.supabase.co/rest/v1/users?select=*&limit=5",
    "headers": {
      "apikey": "[REDACTED]",
      "Authorization": "Bearer [REDACTED]"
    },
    "curl_command": "curl -s 'https://abc123def.supabase.co/rest/v1/users?select=*&limit=5' -H 'apikey: $ANON_KEY' -H 'Authorization: Bearer $ANON_KEY'"
  },

  "response": {
    "status": 200,
    "headers": {
      "content-range": "0-4/1247"
    },
    "total_rows": 1247,
    "sample_data": [
      {
        "id": "550e8400-e29b-41d4-...",
        "email": "[REDACTED]@example.com",
        "name": "[REDACTED]",
        "created_at": "2025-01-15T10:30:00Z"
      }
    ],
    "data_redacted": true
  },

  "analysis": {
    "severity": "P0",
    "pii_exposed": ["email", "name"],
    "total_records_accessible": 1247,
    "authentication_required": false
  }
}
```

### Evidence Format (Properly Blocked)

```json
{
  "evidence_id": "API-READ-002",
  "timestamp": "2025-01-31T10:21:00Z",
  "table": "orders",
  "severity": null,

  "response": {
    "status": 403,
    "body": {"message": "new row violates row-level security policy"}
  },

  "analysis": {
    "rls_working": true,
    "access_blocked": true
  }
}
```

### Add to curl-commands.sh

```bash
# === DATA ACCESS TESTS ===
# Test: Users table access
curl -s "$SUPABASE_URL/rest/v1/users?select=*&limit=5" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ANON_KEY"

# Test: Orders table access (should be blocked)
curl -s "$SUPABASE_URL/rest/v1/orders?select=*&limit=5" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ANON_KEY"
```

## Related Skills

- `supabase-audit-tables-list` — List tables first
- `supabase-audit-rls` — Deep dive into RLS policies
- `supabase-report` — Generate full report
