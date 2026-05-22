---
name: supabase-audit-buckets-read
description: Attempt to list and read files from storage buckets to verify access controls.
---

# Bucket File Access Test

> 🔴 **CRITICAL: PROGRESSIVE FILE UPDATES REQUIRED**
>
> You MUST write to context files **AS YOU GO**, not just at the end.
> - Write to `.sb-pentest-context.json` **IMMEDIATELY after each bucket tested**
> - Log to `.sb-pentest-audit.log` **BEFORE and AFTER each file access test**
> - **DO NOT** wait until the skill completes to update files
> - If the skill crashes or is interrupted, all prior findings must already be saved
>
> **This is not optional. Failure to write progressively is a critical error.**

This skill tests actual file access in storage buckets to verify permissions.

## When to Use This Skill

- After listing buckets, to verify actual access
- To test storage RLS policy effectiveness
- To check for sensitive file exposure
- To document what files are accessible

## Prerequisites

- Buckets listed (auto-invokes if needed)
- Anon key available

## How It Works

The skill attempts to:

1. **List files** in each bucket
2. **Read file metadata**
3. **Download sample files** (for content type verification)
4. **Check public URL access**

**Important:** This is READ-ONLY. No files are modified or deleted.

## Test Approach

| Bucket Type | Tests Performed |
|-------------|-----------------|
| Public | Direct URL access, listing, metadata |
| Private | API listing with anon key, authenticated access |

## Usage

### Basic Read Test

```
Test read access on storage buckets
```

### Specific Bucket

```
Test file access on the documents bucket
```

### List Only (No Download)

```
List accessible files without downloading content
```

## Output Format

```
═══════════════════════════════════════════════════════════
 BUCKET FILE ACCESS TEST
═══════════════════════════════════════════════════════════

 Project: abc123def.supabase.co
 Buckets Tested: 5

 ─────────────────────────────────────────────────────────
 avatars (Public Bucket)
 ─────────────────────────────────────────────────────────

 Status: ✅ Expected Access
 Files Found: 1,247

 Sample Files:
 ├── user-550e8400.jpg (45KB) - Public URL works
 ├── user-6ba7b810.png (32KB) - Public URL works
 └── default.png (12KB) - Public URL works

 Access Methods:
 ├── Public URL: ✅ Accessible
 ├── API Listing: ✅ Works
 └── Metadata: ✅ Visible

 Assessment: Expected behavior for avatar storage.

 ─────────────────────────────────────────────────────────
 documents (Private Bucket)
 ─────────────────────────────────────────────────────────

 Status: ✅ PROPERLY PROTECTED
 Files Found: 0 (via anon key)

 Access Methods:
 ├── Public URL: ❌ 403 Forbidden (correct)
 ├── API Listing: ❌ Empty result (RLS working)
 └── Metadata: ❌ Not accessible (correct)

 Assessment: RLS policies working correctly.

 ─────────────────────────────────────────────────────────
 uploads (Public Bucket)
 ─────────────────────────────────────────────────────────

 Status: 🟠 P1 - SENSITIVE FILES EXPOSED
 Files Found: 3,891

 Sensitive Files Detected:
 ├── 🔴 invoice-2025-001.pdf - Contains financial data
 ├── 🔴 contract-signed.pdf - Legal document
 ├── 🔴 id-verification.jpg - Personal ID photo!
 ├── ⚠️ database-export.csv - Possible data export
 └── ⚠️ config.json - Configuration file

 File Types Distribution:
 ├── PDF: 1,234 (31%)
 ├── Images: 2,100 (54%)
 ├── Documents: 450 (12%)
 └── Other: 107 (3%)

 Assessment: Bucket contains sensitive files that should not be public!

 ─────────────────────────────────────────────────────────
 backups (Public - CRITICAL)
 ─────────────────────────────────────────────────────────

 Status: 🔴 P0 - CRITICAL DATA EXPOSURE
 Files Found: 45

 Exposed Files:
 ├── 🔴 db-backup-2025-01-30.sql (125MB) - DATABASE BACKUP!
 ├── 🔴 db-backup-2025-01-29.sql (124MB) - DATABASE BACKUP!
 ├── 🔴 users-export.csv (2.3MB) - USER DATA EXPORT!
 ├── 🔴 secrets.env (1KB) - ENVIRONMENT SECRETS!
 └── 🔴 .env.production (1KB) - PRODUCTION SECRETS!

 Sample Content (secrets.env):
 ┌─────────────────────────────────────────────────────────┐
 │ STRIPE_SECRET_KEY=sk_live_xxxxxxxxxxxx                 │
 │ DATABASE_URL=postgresql://postgres:xxx@...             │
 │ JWT_SECRET=super-secret-jwt-key                        │
 └─────────────────────────────────────────────────────────┘

 ⚠️ IMMEDIATE ACTION REQUIRED:
 1. Make bucket private NOW
 2. Rotate ALL exposed secrets
 3. Delete backup files from public access
 4. Audit for unauthorized access in logs

 ─────────────────────────────────────────────────────────
 temp (Private Bucket)
 ─────────────────────────────────────────────────────────

 Status: ✅ PROPERLY PROTECTED
 Files Found: 0 (via anon key)
 Assessment: Access correctly restricted.

 ─────────────────────────────────────────────────────────
 Summary
 ─────────────────────────────────────────────────────────

 P0 Critical: 1 bucket (backups - DB dumps & secrets exposed)
 P1 High: 1 bucket (uploads - sensitive documents in public bucket)
 Protected: 2 buckets (documents, temp)
 Expected: 1 bucket (avatars)

 Total Files Accessible: 5,183
 Sensitive Files Exposed: 52
 Secret Files Exposed: 3

 Immediate Actions:
 1. 🔴 DELETE or make private 'backups' bucket
 2. 🔴 Rotate Stripe key, DB password, JWT secret
 3. 🟠 Move sensitive files from 'uploads' to private bucket
 4. Review all 52 sensitive files for exposure impact

═══════════════════════════════════════════════════════════
```

## Sensitive File Detection

The skill identifies sensitive files by:

### Filename Patterns

| Pattern | Risk | Type |
|---------|------|------|
| `*.sql`, `backup*` | P0 | Database dumps |
| `.env*`, `*secrets*` | P0 | Secret files |
| `*password*`, `*credential*` | P0 | Credentials |
| `*invoice*`, `*payment*` | P1 | Financial |
| `*contract*`, `*agreement*` | P1 | Legal |
| `*id*`, `*passport*`, `*license*` | P1 | Identity |
| `*export*`, `*dump*` | P1 | Data exports |

### Content Detection

For accessible files, the skill samples content for:
- API keys (patterns like `sk_live_`, `pk_test_`)
- Database credentials
- JWT secrets
- Personal information patterns

## Context Output

```json
{
  "storage_access": {
    "timestamp": "2025-01-31T11:30:00Z",
    "buckets_tested": 5,
    "findings": [
      {
        "bucket": "backups",
        "severity": "P0",
        "public": true,
        "files_exposed": 45,
        "sensitive_files": [
          {
            "path": "db-backup-2025-01-30.sql",
            "size": 131072000,
            "type": "database_backup",
            "risk": "Full database accessible"
          },
          {
            "path": "secrets.env",
            "size": 1024,
            "type": "secrets",
            "exposed_secrets": ["STRIPE_SECRET_KEY", "DATABASE_URL", "JWT_SECRET"]
          }
        ]
      }
    ],
    "summary": {
      "total_files_accessible": 5183,
      "sensitive_files": 52,
      "secret_files": 3
    }
  }
}
```

## Remediation Steps

### For Exposed Secrets

```bash
# 1. Rotate Stripe keys
# Stripe Dashboard → Developers → API Keys → Roll Keys

# 2. Change database password
# Supabase Dashboard → Settings → Database → Reset Password

# 3. Regenerate JWT secret
# Supabase Dashboard → Settings → API → Regenerate JWT Secret

# 4. Update application environment variables
# Redeploy with new secrets
```

### For Public Bucket Fix

```sql
-- Make bucket private
UPDATE storage.buckets
SET public = false
WHERE name = 'backups';

-- Delete sensitive files or move to secure location
DELETE FROM storage.objects
WHERE bucket_id = 'backups';
```

### For Upload Bucket

```sql
-- Add RLS to restrict access
CREATE POLICY "Users access own uploads"
  ON storage.objects FOR ALL
  USING (
    bucket_id = 'uploads'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );
```

## Common Issues

❌ **Problem:** Cannot list files in private bucket
✅ **Solution:** This is correct behavior. RLS is working.

❌ **Problem:** Large number of files to scan
✅ **Solution:** Use sampling mode for large buckets.

❌ **Problem:** File download fails
✅ **Solution:** May be RLS restriction or network issue.

## MANDATORY: Progressive Context File Updates

⚠️ **This skill MUST update tracking files PROGRESSIVELY during execution, NOT just at the end.**

### Critical Rule: Write As You Go

**DO NOT** batch all writes at the end. Instead:

1. **Before testing each bucket** → Log the action to `.sb-pentest-audit.log`
2. **After each sensitive file found** → Immediately update `.sb-pentest-context.json`
3. **After each bucket completed** → Log the summary

This ensures that if the skill is interrupted, crashes, or times out, all findings up to that point are preserved.

### Required Actions (Progressive)

1. **Update `.sb-pentest-context.json`** with results:
   ```json
   {
     "storage_access": {
       "timestamp": "...",
       "buckets_tested": 5,
       "findings": [ ... ],
       "summary": { "total_files_accessible": 5183, ... }
     }
   }
   ```

2. **Log to `.sb-pentest-audit.log`**:
   ```
   [TIMESTAMP] [supabase-audit-buckets-read] [START] Testing bucket file access
   [TIMESTAMP] [supabase-audit-buckets-read] [FINDING] P0: backups bucket has exposed secrets
   [TIMESTAMP] [supabase-audit-buckets-read] [CONTEXT_UPDATED] .sb-pentest-context.json updated
   ```

3. **If files don't exist**, create them before writing.

**FAILURE TO UPDATE CONTEXT FILES IS NOT ACCEPTABLE.**

## MANDATORY: Evidence Collection

📁 **Evidence Directory:** `.sb-pentest-evidence/04-storage-audit/buckets/`

### Evidence Files to Create

| File | Content |
|------|---------|
| `buckets/[name]/file-list.json` | Files found in bucket |
| `buckets/[name]/sensitive-files.json` | Sensitive files detected |
| `buckets/[name]/sample-contents/` | Redacted content samples |

### Evidence Format (Sensitive Files Exposed)

```json
{
  "evidence_id": "STG-READ-001",
  "timestamp": "2025-01-31T10:40:00Z",
  "category": "storage-audit",
  "type": "file_access",
  "severity": "P0",

  "bucket": "backups",
  "public": true,

  "files_found": 45,
  "sensitive_files": [
    {
      "path": "db-backup-2025-01-30.sql",
      "size": 131072000,
      "type": "database_backup",
      "public_url": "https://abc123def.supabase.co/storage/v1/object/public/backups/db-backup-2025-01-30.sql",
      "curl_command": "curl -o backup.sql 'https://abc123def.supabase.co/storage/v1/object/public/backups/db-backup-2025-01-30.sql'"
    },
    {
      "path": "secrets.env",
      "size": 1024,
      "type": "secrets_file",
      "content_sample": "STRIPE_SECRET_KEY=sk_live_[REDACTED]\nDATABASE_URL=postgresql://[REDACTED]",
      "exposed_secrets": ["STRIPE_SECRET_KEY", "DATABASE_URL", "JWT_SECRET"]
    }
  ],

  "impact": {
    "data_breach": true,
    "secrets_exposed": true,
    "affected_records": "All database records",
    "credentials_to_rotate": ["Stripe API key", "Database password", "JWT secret"]
  }
}
```

### Add to curl-commands.sh

```bash
# === STORAGE FILE ACCESS TESTS ===
# List files in backups bucket
curl -s "$SUPABASE_URL/storage/v1/object/list/backups" \
  -H "apikey: $ANON_KEY"

# Direct access to public file (P0 if accessible)
curl -I "https://abc123def.supabase.co/storage/v1/object/public/backups/secrets.env"

# Download exposed backup (for evidence - be careful with size)
# curl -o evidence-backup-sample.sql "https://abc123def.supabase.co/storage/v1/object/public/backups/db-backup-2025-01-30.sql" | head -1000
```

## Related Skills

- `supabase-audit-buckets-list` — List buckets first
- `supabase-audit-buckets-public` — Focus on public access issues
- `supabase-report` — Generate full report
