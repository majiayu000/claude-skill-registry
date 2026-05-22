---
name: supabase-report
description: Generate a comprehensive Markdown security audit report with executive summary, findings, and remediation guidance.
---

# Security Report Generator

> 🔴 **CRITICAL: PROGRESSIVE FILE UPDATES REQUIRED**
>
> You MUST write to context files **AS YOU GO**, not just at the end.
> - Write to `.sb-pentest-audit.log` **IMMEDIATELY as you process each section**
> - Update `.sb-pentest-context.json` with report metadata **progressively**
> - **DO NOT** wait until the entire report is generated to update files
> - If the skill crashes or is interrupted, the partial progress must already be saved
>
> **This is not optional. Failure to write progressively is a critical error.**

This skill generates a comprehensive Markdown security audit report from all collected findings.

## When to Use This Skill

- After completing security audit phases
- To document findings for stakeholders
- To create actionable remediation plans
- For compliance and audit trail purposes

## Prerequisites

- Audit phases completed (context file populated)
- Findings collected in `.sb-pentest-context.json`

## Report Structure

The generated report includes:

1. **Executive Summary** — High-level overview for management
2. **Security Score** — Quantified risk assessment
3. **Critical Findings (P0)** — Immediate action required
4. **High Findings (P1)** — Address soon
5. **Medium Findings (P2)** — Plan to address
6. **Detailed Analysis** — Per-component breakdown
7. **Remediation Plan** — Prioritized action items
8. **Appendix** — Technical details, methodology

## Usage

### Generate Report

```
Generate security report from audit findings
```

### Custom Report Name

```
Generate report as security-audit-2025-01.md
```

### Specific Sections

```
Generate executive summary only
```

## Output Format

The skill generates `supabase-audit-report.md`:

```markdown
# Supabase Security Audit Report

**Target:** https://myapp.example.com
**Project:** abc123def.supabase.co
**Date:** January 31, 2025
**Auditor:** Internal Security Team

---

## Executive Summary

### Overview

This security audit identified **12 vulnerabilities** across the Supabase implementation, including **3 critical (P0)** issues requiring immediate attention.

### Key Findings

| Severity | Count | Status |
|----------|-------|--------|
| 🔴 P0 (Critical) | 3 | Immediate action required |
| 🟠 P1 (High) | 4 | Address within 7 days |
| 🟡 P2 (Medium) | 5 | Address within 30 days |

### Security Score

**Score: 35/100 (Grade: D)**

The application has significant security gaps that expose user data and allow privilege escalation. Critical issues must be addressed before the application can be considered secure.

### Most Critical Issues

1. **Service Role Key Exposed** — Full database access possible
2. **Database Backups Public** — All data downloadable
3. **Admin Function No Auth** — Any user can access admin features

### Recommended Actions

1. ⚡ **Immediate (Today):**
   - Rotate service role key
   - Make backup bucket private
   - Add admin role verification

2. 🔜 **This Week:**
   - Enable RLS on all tables
   - Enable email confirmation
   - Fix IDOR in Edge Functions

3. 📅 **This Month:**
   - Strengthen password policy
   - Restrict CORS origins
   - Add rate limiting to functions

---

## Critical Findings (P0)

### P0-001: Service Role Key Exposed in Client Code

**Severity:** 🔴 Critical
**Component:** Key Management
**CVSS:** 9.8 (Critical)

#### Description

The Supabase service_role key was found in client-side JavaScript code. This key bypasses all Row Level Security policies and provides full database access.

#### Location

```
File: /static/js/admin.chunk.js
Line: 89
Code: const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiI...'
```

#### Impact

- Full read/write access to all database tables
- Bypass of all RLS policies
- Access to auth.users table (all user data)
- Ability to delete or modify any data

#### Proof of Concept

```bash
curl 'https://abc123def.supabase.co/rest/v1/users' \
  -H 'apikey: [service_role_key]' \
  -H 'Authorization: Bearer [service_role_key]'

# Returns ALL users with full data
```

#### Remediation

**Immediate:**
1. Rotate the service role key in Supabase Dashboard
   - Settings → API → Regenerate service_role key
2. Remove the key from client code
3. Redeploy the application

**Long-term:**
```typescript
// Move privileged operations to Edge Functions
// supabase/functions/admin-action/index.ts

import { createClient } from '@supabase/supabase-js'

Deno.serve(async (req) => {
  // Service key only on server
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // Verify caller is admin before proceeding
  // ...
})
```

**Documentation:**
- [Supabase API Keys](https://supabase.com/docs/guides/api/api-keys)
- [Edge Functions](https://supabase.com/docs/guides/functions)

---

### P0-002: Database Backups Publicly Accessible

**Severity:** 🔴 Critical
**Component:** Storage
**CVSS:** 9.1 (Critical)

#### Description

The storage bucket named "backups" is configured as public, exposing database dumps, user exports, and environment secrets.

#### Exposed Files

| File | Size | Content |
|------|------|---------|
| db-backup-2025-01-30.sql | 125MB | Full database dump |
| users-export.csv | 2.3MB | All user data with PII |
| secrets.env | 1KB | API keys and passwords |

#### Impact

- Complete data breach (all database content)
- Exposed credentials for third-party services
- User PII exposed (emails, names, etc.)

#### Remediation

**Immediate:**
```sql
-- Make bucket private
UPDATE storage.buckets
SET public = false
WHERE name = 'backups';

-- Delete or move files
-- Consider incident response procedures
```

**Credential Rotation:**
- Stripe API keys
- Database password
- JWT secret
- Any other keys in secrets.env

---

### P0-003: Admin Edge Function Privilege Escalation

**Severity:** 🔴 Critical
**Component:** Edge Functions
**CVSS:** 8.8 (High)

#### Description

The `/functions/v1/admin-panel` Edge Function is accessible to any authenticated user without role verification.

[... additional P0 findings ...]

---

## High Findings (P1)

### P1-001: Email Confirmation Disabled

**Severity:** 🟠 High
**Component:** Authentication

[... P1 findings ...]

---

## Medium Findings (P2)

### P2-001: Weak Password Policy

**Severity:** 🟡 Medium
**Component:** Authentication

[... P2 findings ...]

---

## Detailed Analysis by Component

### API Security

| Table | RLS | Access Level | Status |
|-------|-----|--------------|--------|
| users | ❌ | Full read | 🔴 P0 |
| orders | ✅ | None | ✅ |
| posts | ✅ | Published only | ✅ |

### Storage Security

| Bucket | Public | Sensitive Files | Status |
|--------|--------|-----------------|--------|
| avatars | Yes | No | ✅ |
| backups | Yes | Yes (45 files) | 🔴 P0 |

### Authentication

| Setting | Current | Recommended | Status |
|---------|---------|-------------|--------|
| Email confirm | Disabled | Enabled | 🟠 P1 |
| Password min | 6 | 8+ | 🟡 P2 |

---

## Remediation Plan

### Phase 1: Critical (Immediate)

| ID | Action | Owner | Deadline |
|----|--------|-------|----------|
| P0-001 | Rotate service key | DevOps | Today |
| P0-002 | Make backups private | DevOps | Today |
| P0-003 | Add admin role check | Backend | Today |

### Phase 2: High Priority (This Week)

| ID | Action | Owner | Deadline |
|----|--------|-------|----------|
| P1-001 | Enable email confirmation | Backend | 3 days |
| P1-002 | Fix IDOR in get-user-data | Backend | 3 days |

### Phase 3: Medium Priority (This Month)

| ID | Action | Owner | Deadline |
|----|--------|-------|----------|
| P2-001 | Strengthen password policy | Backend | 14 days |
| P2-002 | Restrict CORS origins | DevOps | 14 days |

---

## Appendix

### A. Methodology

This audit was performed using the Supabase Pentest Skills toolkit, which includes:
- Passive reconnaissance of client-side code
- API endpoint testing with anon and service keys
- Storage bucket enumeration and access testing
- Authentication flow analysis
- Real-time channel subscription testing

### B. Tools Used

- supabase-pentest-skills v1.0.0
- curl for API testing
- Browser DevTools for client code analysis

### C. Audit Scope

- Target URL: https://myapp.example.com
- Supabase Project: abc123def
- Components tested: API, Storage, Auth, Realtime, Edge Functions
- Exclusions: None

### D. Audit Log

Full audit log available in `.sb-pentest-audit.log`

---

**Report generated by supabase-pentest-skills**
**Audit completed:** January 31, 2025 at 15:00 UTC
```

## Score Calculation

The security score is calculated based on:

| Factor | Weight | Calculation |
|--------|--------|-------------|
| P0 findings | -25 per issue | Critical vulnerabilities |
| P1 findings | -10 per issue | High severity issues |
| P2 findings | -5 per issue | Medium severity issues |
| RLS coverage | +10 if 100% | All tables have RLS |
| Auth hardening | +10 | Email confirm, strong passwords |
| Base score | 100 | Starting point |

### Grade Scale

| Score | Grade | Description |
|-------|-------|-------------|
| 90-100 | A | Excellent security posture |
| 80-89 | B | Good, minor improvements needed |
| 70-79 | C | Acceptable, address issues |
| 60-69 | D | Poor, significant issues |
| 0-59 | F | Critical, immediate action needed |

## Context Input

The report generator reads from `.sb-pentest-context.json`:

```json
{
  "target_url": "https://myapp.example.com",
  "supabase": {
    "project_url": "https://abc123def.supabase.co",
    "project_ref": "abc123def"
  },
  "findings": [
    {
      "id": "P0-001",
      "severity": "P0",
      "component": "keys",
      "title": "Service Role Key Exposed",
      "description": "...",
      "location": "...",
      "remediation": "..."
    }
  ],
  "audit_completed": "2025-01-31T15:00:00Z"
}
```

## Report Customization

### Include/Exclude Sections

```
Generate report without appendix
Generate report with executive summary only
```

### Different Formats

```
Generate report in JSON format
Generate report summary as HTML
```

## MANDATORY: Context File Dependency

⚠️ **This skill REQUIRES properly populated tracking files.**

### Prerequisites

Before generating a report, ensure:

1. **`.sb-pentest-context.json` exists** and contains findings from audit skills
2. **`.sb-pentest-audit.log` exists** with timestamped actions
3. **All relevant audit skills have updated these files**

### If Context Files Are Missing

If context files are missing or empty:
1. DO NOT generate an empty report
2. Inform the user that audit skills must be run first
3. Recommend running `supabase-pentest` for a complete audit

### Report Generation Output

After generating the report, this skill MUST:

1. **Log to `.sb-pentest-audit.log`**:
   ```
   [TIMESTAMP] [supabase-report] [START] Generating security report
   [TIMESTAMP] [supabase-report] [SUCCESS] Report generated: supabase-audit-report.md
   [TIMESTAMP] [supabase-report] [CONTEXT_UPDATED] Report generation logged
   ```

2. **Update `.sb-pentest-context.json`** with report metadata:
   ```json
   {
     "report": {
       "generated_at": "...",
       "filename": "supabase-audit-report.md",
       "findings_count": { "p0": 3, "p1": 4, "p2": 5 }
     }
   }
   ```

**FAILURE TO UPDATE CONTEXT FILES IS NOT ACCEPTABLE.**

## Related Skills

- `supabase-report-compare` — Compare with previous reports
- `supabase-pentest` — Run full audit first
- `supabase-help` — List all available skills
