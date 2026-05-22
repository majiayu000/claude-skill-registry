---
name: supabase-audit-buckets-public
description: Identify storage buckets that are publicly accessible and may contain sensitive data.
---

# Public Bucket Audit

> 🔴 **CRITICAL: PROGRESSIVE FILE UPDATES REQUIRED**
>
> You MUST write to context files **AS YOU GO**, not just at the end.
> - Write to `.sb-pentest-context.json` **IMMEDIATELY after each bucket analyzed**
> - Log to `.sb-pentest-audit.log` **BEFORE and AFTER each test**
> - **DO NOT** wait until the skill completes to update files
> - If the skill crashes or is interrupted, all prior findings must already be saved
>
> **This is not optional. Failure to write progressively is a critical error.**

This skill specifically focuses on identifying misconfigured public buckets and exposed sensitive content.

## When to Use This Skill

- Quick check for public bucket misconfigurations
- When you suspect sensitive data in public storage
- As a focused security check for storage
- Before deploying to production

## Prerequisites

- Supabase URL and anon key available

## Why Public Buckets Are Risky

Public buckets allow:

| Access Type | Description |
|-------------|-------------|
| Direct URL | Anyone with the URL can download |
| Enumeration | File listing may be possible |
| No Auth | No authentication required |
| Caching | CDN may cache sensitive files |

## Common Misconfiguration Scenarios

1. **Development mistake** — Bucket set public during development
2. **Wrong bucket** — Sensitive file uploaded to public bucket
3. **Legacy** — Bucket was public before RLS existed
4. **Intentional but wrong** — Assumed "nobody knows the URL"

## Usage

### Quick Public Bucket Check

```
Check for misconfigured public buckets
```

### Deep Scan

```
Deep scan public buckets for sensitive content
```

## Output Format

```
═══════════════════════════════════════════════════════════
 PUBLIC BUCKET SECURITY AUDIT
═══════════════════════════════════════════════════════════

 Project: abc123def.supabase.co

 ─────────────────────────────────────────────────────────
 Public Bucket Discovery
 ─────────────────────────────────────────────────────────

 Public Buckets Found: 3/5

 ─────────────────────────────────────────────────────────
 1. avatars ✅ APPROPRIATE
 ─────────────────────────────────────────────────────────

 Status: Public (Expected)
 Purpose: User profile pictures
 Content Analysis:
 ├── All files are images (jpg, png, webp)
 ├── No sensitive filenames detected
 ├── File sizes appropriate for avatars (< 1MB)
 └── No metadata concerns

 Assessment: This bucket appropriately contains only
             public user-facing content.

 ─────────────────────────────────────────────────────────
 2. uploads 🟠 P1 - NEEDS REVIEW
 ─────────────────────────────────────────────────────────

 Status: Public (Unexpected for this content)
 Purpose: User file uploads

 Content Analysis:
 ├── Mixed file types (PDF, DOC, images)
 ├── Some sensitive filenames detected
 └── Should likely be private with RLS

 Sensitive Content Indicators:
 ├── 12 files with 'invoice' in name
 ├── 8 files with 'contract' in name
 ├── 3 files with 'passport' in name
 └── 156 PDF files (may contain sensitive data)

 Risk Assessment:
 └── 🟠 User-uploaded content publicly accessible
     Anyone with filename can access any user's files

 Recommendation:
 ```sql
 -- Make bucket private
 UPDATE storage.buckets
 SET public = false
 WHERE name = 'uploads';

 -- Add user-specific RLS
 CREATE POLICY "Users access own uploads"
   ON storage.objects FOR ALL
   USING (
     bucket_id = 'uploads'
     AND auth.uid()::text = (storage.foldername(name))[1]
   );
 ```

 ─────────────────────────────────────────────────────────
 3. backups 🔴 P0 - CRITICAL MISCONFIGURATION
 ─────────────────────────────────────────────────────────

 Status: Public (SHOULD NEVER BE PUBLIC)
 Purpose: Database backups

 ⚠️ CRITICAL: Backup files publicly accessible!

 Exposed Content:
 ├── 🔴 db-backup-2025-01-30.sql (125MB)
 │   └── Full database dump with all user data
 ├── 🔴 db-backup-2025-01-29.sql (124MB)
 │   └── Previous day backup
 ├── 🔴 users-export.csv (2.3MB)
 │   └── User data export with emails, names
 ├── 🔴 secrets.env (1KB)
 │   └── Contains API keys and passwords!
 └── 🔴 .env.production (1KB)
     └── Production environment secrets!

 Public URLs (Currently Accessible):
 https://abc123def.supabase.co/storage/v1/object/public/backups/db-backup-2025-01-30.sql
 https://abc123def.supabase.co/storage/v1/object/public/backups/secrets.env

 Impact:
 ├── Complete database can be downloaded
 ├── All user PII exposed
 ├── All API secrets exposed
 └── Full application compromise possible

 ═══════════════════════════════════════════════════════════
 🚨 IMMEDIATE ACTION REQUIRED 🚨
 ═══════════════════════════════════════════════════════════

 1. MAKE BUCKET PRIVATE NOW:
    ```sql
    UPDATE storage.buckets
    SET public = false
    WHERE name = 'backups';
    ```

 2. DELETE PUBLIC FILES:
    Delete or move all sensitive files from public access

 3. ROTATE ALL EXPOSED SECRETS:
    - Stripe API keys
    - Database passwords
    - JWT secrets
    - Any other keys in exposed files

 4. AUDIT ACCESS LOGS:
    Check if files were accessed by unauthorized parties

 5. INCIDENT RESPONSE:
    Consider this a data breach and follow your
    incident response procedures

 ─────────────────────────────────────────────────────────
 Summary
 ─────────────────────────────────────────────────────────

 Public Buckets: 3
 ├── ✅ Appropriate: 1 (avatars)
 ├── 🟠 P1 Review: 1 (uploads)
 └── 🔴 P0 Critical: 1 (backups)

 Exposed Sensitive Files: 47
 Exposed Secret Files: 2

 Critical Finding: Database backups and secrets
                   publicly accessible via direct URL

═══════════════════════════════════════════════════════════
```

## Bucket Classification

The skill classifies buckets by content:

| Classification | Criteria | Action |
|----------------|----------|--------|
| **Appropriate Public** | Profile images, public assets | None needed |
| **Needs Review** | User uploads, mixed content | Consider making private |
| **Critical Misconfiguration** | Backups, secrets, exports | Immediate remediation |

## Sensitive Content Patterns

### P0 - Critical (Never Public)

- `*.sql` - Database dumps
- `*.env*` - Environment files
- `*secret*`, `*credential*` - Secrets
- `*backup*` - Backup files
- `*export*` - Data exports

### P1 - High (Usually Private)

- `*invoice*`, `*payment*` - Financial
- `*contract*`, `*agreement*` - Legal
- `*passport*`, `*id*`, `*license*` - Identity
- User-uploaded documents

### P2 - Medium (Review Needed)

- Configuration files
- Log files
- Debug exports

## Context Output

```json
{
  "public_bucket_audit": {
    "timestamp": "2025-01-31T12:00:00Z",
    "public_buckets": 3,
    "findings": [
      {
        "bucket": "backups",
        "severity": "P0",
        "issue": "Database backups and secrets publicly accessible",
        "exposed_files": 45,
        "critical_files": [
          "db-backup-2025-01-30.sql",
          "secrets.env",
          ".env.production"
        ],
        "remediation": "Make bucket private immediately, rotate secrets"
      }
    ]
  }
}
```

## Prevention Checklist

After fixing issues, implement these controls:

### 1. Default Private Buckets

```sql
-- Supabase creates buckets public by default in UI
-- Always verify and change to private if needed
UPDATE storage.buckets
SET public = false
WHERE name = 'new-bucket';
```

### 2. Restrict Bucket Creation

```sql
-- Only allow admin to create buckets
REVOKE INSERT ON storage.buckets FROM authenticated;
REVOKE INSERT ON storage.buckets FROM anon;
```

### 3. File Upload Validation

```typescript
// Validate file type before upload
const allowedTypes = ['image/jpeg', 'image/png'];
if (!allowedTypes.includes(file.type)) {
  throw new Error('Invalid file type');
}

// Use user-specific paths
const path = `${user.id}/${file.name}`;
await supabase.storage.from('uploads').upload(path, file);
```

### 4. Regular Audits

Run this skill regularly:
- Before each production deployment
- Weekly automated scans
- After any storage configuration changes

## MANDATORY: Progressive Context File Updates

⚠️ **This skill MUST update tracking files PROGRESSIVELY during execution, NOT just at the end.**

### Critical Rule: Write As You Go

**DO NOT** batch all writes at the end. Instead:

1. **Before analyzing each bucket** → Log the action to `.sb-pentest-audit.log`
2. **After each misconfiguration found** → Immediately update `.sb-pentest-context.json`
3. **After each sensitive file detected** → Log the finding immediately

This ensures that if the skill is interrupted, crashes, or times out, all findings up to that point are preserved.

### Required Actions (Progressive)

1. **Update `.sb-pentest-context.json`** with results:
   ```json
   {
     "public_bucket_audit": {
       "timestamp": "...",
       "public_buckets": 3,
       "findings": [ ... ]
     }
   }
   ```

2. **Log to `.sb-pentest-audit.log`**:
   ```
   [TIMESTAMP] [supabase-audit-buckets-public] [START] Auditing public buckets
   [TIMESTAMP] [supabase-audit-buckets-public] [FINDING] P0: backups bucket is public
   [TIMESTAMP] [supabase-audit-buckets-public] [CONTEXT_UPDATED] .sb-pentest-context.json updated
   ```

3. **If files don't exist**, create them before writing.

**FAILURE TO UPDATE CONTEXT FILES IS NOT ACCEPTABLE.**

## MANDATORY: Evidence Collection

📁 **Evidence Directory:** `.sb-pentest-evidence/04-storage-audit/public-url-tests/`

### Evidence Files to Create

| File | Content |
|------|---------|
| `public-url-tests/[bucket]-access.json` | Public URL access test results |
| `public-url-tests/sensitive-content.json` | Sensitive content found |

### Evidence Format

```json
{
  "evidence_id": "STG-PUB-001",
  "timestamp": "2025-01-31T10:45:00Z",
  "category": "storage-audit",
  "type": "public_bucket_audit",
  "severity": "P0",

  "bucket": "backups",

  "public_url_test": {
    "url": "https://abc123def.supabase.co/storage/v1/object/public/backups/secrets.env",
    "curl_command": "curl -I 'https://abc123def.supabase.co/storage/v1/object/public/backups/secrets.env'",
    "response_status": 200,
    "content_type": "text/plain",
    "accessible": true
  },

  "assessment": {
    "classification": "critical_misconfiguration",
    "should_be_public": false,
    "contains_sensitive_data": true,
    "file_types_exposed": ["sql", "env", "csv"]
  },

  "remediation": {
    "immediate": "UPDATE storage.buckets SET public = false WHERE name = 'backups';",
    "secrets_to_rotate": ["All keys in secrets.env"],
    "incident_response": "Consider this a data breach"
  }
}
```

## Related Skills

- `supabase-audit-buckets-list` — List all buckets
- `supabase-audit-buckets-read` — Test file access
- `supabase-report` — Generate comprehensive report
