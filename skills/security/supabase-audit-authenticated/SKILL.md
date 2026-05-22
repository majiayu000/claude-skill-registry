---
name: supabase-audit-authenticated
description: Create a test user (with explicit permission) to audit what authenticated users can access vs anonymous users. Detects IDOR, cross-user access, and privilege escalation.
---

# Authenticated User Audit

> 🔴 **CRITICAL: PROGRESSIVE FILE UPDATES REQUIRED**
>
> You MUST write to context files **AS YOU GO**, not just at the end.
> - Write to `.sb-pentest-context.json` **IMMEDIATELY after each test**
> - Log to `.sb-pentest-audit.log` **BEFORE and AFTER each action**
> - **DO NOT** wait until the skill completes to update files
> - If the skill crashes or is interrupted, all prior findings must already be saved
>
> **This is not optional. Failure to write progressively is a critical error.**

This skill creates a test user (with explicit permission) to compare authenticated vs anonymous access and detect IDOR vulnerabilities.

## ⚠️ IMPORTANT: User Consent Required

```
╔═══════════════════════════════════════════════════════════════════╗
║  🔐 USER CREATION CONSENT REQUIRED                                ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  This skill will CREATE A TEST USER in your Supabase project.     ║
║                                                                   ║
║  The user will be created with:                                   ║
║  • Email: pentest-[random]@security-audit.local                   ║
║  • Password: Strong random password (32+ chars)                   ║
║  • Purpose: Testing authenticated access vs anonymous             ║
║                                                                   ║
║  At the end of the audit, you will be asked if you want to        ║
║  DELETE the test user (recommended).                              ║
║                                                                   ║
║  Do you authorize the creation of a test user?                    ║
║  Type "yes, create test user" to proceed.                         ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

**DO NOT proceed without explicit user consent.**

## When to Use This Skill

- After completing anonymous access tests
- To detect IDOR (Insecure Direct Object Reference) vulnerabilities
- To test cross-user data access
- To verify RLS policies work for authenticated users
- To find privilege escalation issues

## Prerequisites

- Signup must be open (or use invite flow)
- Anon key available
- Anonymous audit completed (recommended)

## Why Authenticated Testing Matters

Many vulnerabilities only appear with authentication:

| Vulnerability | Anonymous | Authenticated |
|---------------|-----------|---------------|
| **RLS bypass (no RLS)** | ✓ Detectable | ✓ Detectable |
| **IDOR** | ✗ Not visible | ✓ **Only visible** |
| **Cross-user access** | ✗ Not visible | ✓ **Only visible** |
| **Privilege escalation** | ✗ Not visible | ✓ **Only visible** |
| **Overly permissive RLS** | Partial | ✓ **Full detection** |

## Test User Creation

### Email Format

```
pentest-[8-char-random]@security-audit.local
```

Example: `pentest-a7b3c9d2@security-audit.local`

### Password Generation

Strong password with:
- 32+ characters
- Uppercase, lowercase, numbers, symbols
- Cryptographically random

Example: `Xk9$mP2#vL5@nQ8&jR4*wY7!hT3%bU6^`

**The password is displayed ONCE and saved to evidence.**

## Tests Performed

### 1. User Creation & Login

```bash
# Create user
curl -X POST "$SUPABASE_URL/auth/v1/signup" \
  -H "apikey: $ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "pentest-xxx@security-audit.local", "password": "[STRONG_PASSWORD]"}'

# Login and get JWT
curl -X POST "$SUPABASE_URL/auth/v1/token?grant_type=password" \
  -H "apikey: $ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "pentest-xxx@security-audit.local", "password": "[STRONG_PASSWORD]"}'
```

### 2. Authenticated vs Anonymous Comparison

For each table:

| Test | Anonymous | Authenticated | Finding |
|------|-----------|---------------|---------|
| SELECT | 0 rows | 1,247 rows | 🔴 Auth-only exposure |
| Own data | N/A | Only own row | ✅ RLS working |
| Other users' data | N/A | All rows | 🔴 Cross-user access |

### 3. IDOR Testing

```bash
# As test user, try to access other user's data
curl "$SUPABASE_URL/rest/v1/orders?user_id=eq.[OTHER_USER_ID]" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer [TEST_USER_JWT]"

# If returns data: IDOR vulnerability!
```

### 4. Cross-User Access

```bash
# Get test user's ID from JWT
TEST_USER_ID=$(echo $JWT | jq -r '.sub')

# Try to access data belonging to a different user
curl "$SUPABASE_URL/rest/v1/profiles?id=neq.$TEST_USER_ID" \
  -H "Authorization: Bearer [TEST_USER_JWT]"

# If returns other users' profiles: Cross-user access!
```

### 5. Storage with Authentication

```bash
# Test authenticated storage access
curl "$SUPABASE_URL/storage/v1/object/list/documents" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer [TEST_USER_JWT]"

# Compare with anonymous results
```

### 6. Realtime with Authentication

```javascript
// Subscribe to table changes as authenticated user
const channel = supabase.channel('test')
  .on('postgres_changes', {
    event: '*',
    schema: 'public',
    table: 'orders'
  }, payload => console.log(payload))
  .subscribe()

// Does it receive OTHER users' order changes?
```

## Output Format

```
═══════════════════════════════════════════════════════════
 AUTHENTICATED USER AUDIT
═══════════════════════════════════════════════════════════

 ─────────────────────────────────────────────────────────
 Test User Creation
 ─────────────────────────────────────────────────────────

 Status: ✅ User created successfully

 Test User Details:
 ├── Email: pentest-a7b3c9d2@security-audit.local
 ├── User ID: 550e8400-e29b-41d4-a716-446655440099
 ├── Password: [Saved to evidence - shown once]
 └── JWT obtained: ✅

 ─────────────────────────────────────────────────────────
 Anonymous vs Authenticated Comparison
 ─────────────────────────────────────────────────────────

 Table: users
 ├── Anonymous access: 0 rows
 ├── Authenticated access: 1,247 rows ← ALL USERS!
 └── Status: 🔴 P0 - Data hidden from anon but exposed to any auth user

 Table: orders
 ├── Anonymous access: 0 rows (blocked)
 ├── Authenticated access: 1 row (own orders only)
 └── Status: ✅ RLS working correctly

 Table: profiles
 ├── Anonymous access: 0 rows
 ├── Authenticated access: 1,247 rows ← ALL PROFILES!
 ├── Own profile only expected: ❌ NO
 └── Status: 🔴 P0 - Cross-user profile access

 ─────────────────────────────────────────────────────────
 IDOR Testing
 ─────────────────────────────────────────────────────────

 Test: Access other user's orders by ID
 ├── Request: GET /orders?user_id=eq.[other-user-id]
 ├── Auth: Test user JWT
 ├── Response: 200 OK - 15 orders returned
 └── Status: 🔴 P0 - IDOR VULNERABILITY

 Proof:
 curl "$URL/rest/v1/orders?user_id=eq.other-user-uuid" \
   -H "Authorization: Bearer [test-user-jwt]"
 # Returns orders belonging to other-user-uuid!

 Test: Access admin endpoints
 ├── Request: GET /functions/v1/admin-panel
 ├── Auth: Test user JWT (regular user)
 ├── Response: 200 OK - Admin data returned!
 └── Status: 🔴 P0 - PRIVILEGE ESCALATION

 ─────────────────────────────────────────────────────────
 Storage with Authentication
 ─────────────────────────────────────────────────────────

 Bucket: documents
 ├── Anonymous: ❌ 0 files (blocked)
 ├── Authenticated: ✅ 523 files visible ← ALL USERS' FILES!
 └── Status: 🔴 P1 - Auth users see all documents

 Bucket: user-uploads
 ├── Anonymous: ❌ 0 files
 ├── Authenticated: 3 files (own files only)
 └── Status: ✅ RLS working correctly

 ─────────────────────────────────────────────────────────
 Summary
 ─────────────────────────────────────────────────────────

 New Findings (Auth-only):
 ├── 🔴 P0: users table - all users visible to any auth user
 ├── 🔴 P0: profiles table - cross-user access
 ├── 🔴 P0: IDOR in orders - can access any user's orders
 ├── 🔴 P0: Privilege escalation in admin-panel
 └── 🟠 P1: documents bucket - all files visible to auth users

 Comparison:
 ├── Issues found (Anonymous): 3
 ├── Issues found (Authenticated): 8 ← 5 NEW ISSUES!
 └── Auth-only vulnerabilities: 5

 Recommendation:
 These issues were NOT visible in anonymous testing!
 Always test with authenticated users.

 ─────────────────────────────────────────────────────────
 Cleanup
 ─────────────────────────────────────────────────────────

 ⚠️  Test user still exists in database.

 Do you want to delete the test user?
 Email: pentest-a7b3c9d2@security-audit.local

 [This requires service_role key or manual deletion]

═══════════════════════════════════════════════════════════
```

## Context Output

```json
{
  "authenticated_audit": {
    "timestamp": "2025-01-31T12:00:00Z",
    "test_user": {
      "email": "pentest-a7b3c9d2@security-audit.local",
      "user_id": "550e8400-e29b-41d4-a716-446655440099",
      "created_at": "2025-01-31T12:00:00Z",
      "deleted": false
    },
    "comparison": {
      "tables": {
        "users": {
          "anon_access": 0,
          "auth_access": 1247,
          "expected_auth_access": "own_row_only",
          "severity": "P0",
          "finding": "All users visible to any authenticated user"
        },
        "orders": {
          "anon_access": 0,
          "auth_access": 1,
          "expected_auth_access": "own_rows_only",
          "severity": null,
          "finding": "RLS working correctly"
        }
      },
      "idor_tests": [
        {
          "test": "access_other_user_orders",
          "vulnerable": true,
          "severity": "P0",
          "proof": "curl command..."
        }
      ],
      "privilege_escalation": [
        {
          "endpoint": "/functions/v1/admin-panel",
          "vulnerable": true,
          "severity": "P0"
        }
      ]
    },
    "summary": {
      "anon_issues": 3,
      "auth_issues": 8,
      "auth_only_issues": 5
    }
  }
}
```

## RLS Policy Examples

### Correct: Users see only their own data

```sql
-- This RLS policy is correct
CREATE POLICY "Users see own data"
  ON users FOR SELECT
  USING (auth.uid() = id);

-- Result:
-- Anonymous: 0 rows
-- Authenticated: 1 row (own data)
```

### Incorrect: All authenticated users see everything

```sql
-- This RLS policy is WRONG
CREATE POLICY "Authenticated users see all"
  ON users FOR SELECT
  USING (auth.role() = 'authenticated');  -- ❌ Too permissive!

-- Result:
-- Anonymous: 0 rows
-- Authenticated: ALL rows ← VULNERABILITY!
```

### Correct fix:

```sql
-- Fix: Add user ownership check
CREATE POLICY "Users see own data"
  ON users FOR SELECT
  USING (auth.uid() = id);  -- ✅ Only own row
```

## Cleanup Options

### Option 1: Manual deletion (Dashboard)

```
Supabase Dashboard → Authentication → Users → Find test user → Delete
```

### Option 2: Via service_role key (if available)

```bash
curl -X DELETE "$SUPABASE_URL/auth/v1/admin/users/[USER_ID]" \
  -H "apikey: $SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SERVICE_ROLE_KEY"
```

### Option 3: Leave for later

The test user uses a non-functional email domain (`security-audit.local`) and cannot be used maliciously.

## MANDATORY: Evidence Collection

📁 **Evidence Directory:** `.sb-pentest-evidence/05-auth-audit/authenticated-tests/`

### Evidence Files to Create

| File | Content |
|------|---------|
| `test-user-created.json` | Test user details (password saved securely) |
| `anon-vs-auth-comparison.json` | Side-by-side comparison |
| `idor-tests/[table].json` | IDOR test results |
| `privilege-escalation.json` | Privilege escalation tests |

### Evidence Format

```json
{
  "evidence_id": "AUTH-TEST-001",
  "timestamp": "2025-01-31T12:00:00Z",
  "category": "auth-audit",
  "type": "authenticated_testing",

  "test_user": {
    "email": "pentest-a7b3c9d2@security-audit.local",
    "user_id": "550e8400-...",
    "password": "[STORED SECURELY - DO NOT COMMIT]"
  },

  "comparison_test": {
    "table": "users",
    "anonymous": {
      "curl_command": "curl '$URL/rest/v1/users' -H 'apikey: $ANON_KEY'",
      "response_status": 200,
      "rows_returned": 0
    },
    "authenticated": {
      "curl_command": "curl '$URL/rest/v1/users' -H 'apikey: $ANON_KEY' -H 'Authorization: Bearer $JWT'",
      "response_status": 200,
      "rows_returned": 1247
    },
    "finding": {
      "severity": "P0",
      "issue": "All users visible to any authenticated user",
      "expected": "Only own row should be visible",
      "impact": "Full user enumeration for any authenticated user"
    }
  }
}
```

### Add to curl-commands.sh

```bash
# === AUTHENTICATED TESTING ===
# NOTE: Replace [JWT] with test user's JWT

# Compare anonymous vs authenticated access
curl -s "$SUPABASE_URL/rest/v1/users?select=*&limit=5" -H "apikey: $ANON_KEY"
curl -s "$SUPABASE_URL/rest/v1/users?select=*&limit=5" -H "apikey: $ANON_KEY" -H "Authorization: Bearer [JWT]"

# IDOR test - access other user's data
curl -s "$SUPABASE_URL/rest/v1/orders?user_id=eq.[OTHER_USER_ID]" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer [JWT]"

# Cross-user profile access
curl -s "$SUPABASE_URL/rest/v1/profiles?id=neq.[TEST_USER_ID]" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer [JWT]"
```

## MANDATORY: Progressive Context File Updates

⚠️ **This skill MUST update tracking files PROGRESSIVELY during execution, NOT just at the end.**

### Critical Rule: Write As You Go

**DO NOT** batch all writes at the end. Instead:

1. **Before user creation** → Log consent and action to `.sb-pentest-audit.log`
2. **After user created** → Immediately save user details to context and evidence
3. **After each comparison test** → Update `.sb-pentest-context.json` with results
4. **After each IDOR test** → Save evidence immediately

This ensures that if the skill is interrupted, crashes, or times out, all findings up to that point are preserved.

### Required Actions (Progressive)

1. **Log user creation:**
   ```
   [TIMESTAMP] [supabase-audit-authenticated] [CONSENT] User authorized test user creation
   [TIMESTAMP] [supabase-audit-authenticated] [CREATED] Test user pentest-xxx@security-audit.local
   ```

2. **Save test user to context immediately:**
   ```json
   {
     "authenticated_audit": {
       "test_user": {
         "email": "...",
         "user_id": "...",
         "created_at": "..."
       }
     }
   }
   ```

3. **Log each finding as discovered:**
   ```
   [TIMESTAMP] [supabase-audit-authenticated] [FINDING] P0: IDOR in orders table
   ```

**FAILURE TO UPDATE CONTEXT FILES PROGRESSIVELY IS NOT ACCEPTABLE.**

## Related Skills

- `supabase-audit-auth-signup` — Test if signup is open first
- `supabase-audit-tables-read` — Compare with anonymous results
- `supabase-audit-rls` — Deep dive into RLS policies
- `supabase-audit-functions` — Test function access with auth
- `supabase-report` — Include auth-only findings in report
