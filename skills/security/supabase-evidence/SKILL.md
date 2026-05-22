---
name: supabase-evidence
description: Initialize and manage the evidence collection directory for professional security audits with documented proof of findings.
---

# Evidence Collection Management

> 🔴 **CRITICAL: PROGRESSIVE FILE UPDATES REQUIRED**
>
> You MUST write evidence files **AS YOU GO**, not just at the end.
> - Save each piece of evidence **IMMEDIATELY after collection**
> - **DO NOT** wait until the skill completes to save evidence
> - If the audit crashes or is interrupted, all prior evidence must already be saved
>
> **This is not optional. Failure to save evidence progressively is a critical error.**

This skill initializes and manages the evidence collection system for professional security audits.

## When to Use This Skill

- Automatically invoked at the start of `supabase-pentest`
- When you need to organize evidence for a professional report
- When conducting audits that require documented proof
- For compliance and legal purposes

## Why Evidence Collection Matters

Professional security audits require:

| Requirement | Purpose |
|-------------|---------|
| **Reproducibility** | Others can verify findings |
| **Legal proof** | Documentation for legal/compliance |
| **Remediation verification** | Prove issues existed before fix |
| **Audit trail** | Complete record of what was tested |

## Evidence Directory Structure

The skill creates `.sb-pentest-evidence/` with this structure:

```
.sb-pentest-evidence/
├── README.md                    # Evidence index and summary
├── curl-commands.sh             # All curl commands used (reproducible)
├── timeline.md                  # Chronological evidence timeline
│
├── 01-detection/
│   ├── initial-scan.json        # Raw detection results
│   ├── supabase-endpoints.txt   # Discovered endpoints
│   └── client-code-snippets/    # Relevant code excerpts
│       └── supabase-init.js
│
├── 02-extraction/
│   ├── extracted-url.json       # URL extraction proof
│   ├── extracted-anon-key.json  # Anon key with decoded JWT
│   ├── extracted-jwts.json      # All JWTs found
│   ├── service-key-exposure/    # If service key found (P0)
│   │   ├── location.txt
│   │   └── decoded-payload.json
│   └── db-string-exposure/      # If DB string found (P0)
│       └── connection-details.json
│
├── 03-api-audit/
│   ├── openapi-schema.json      # Raw OpenAPI/PostgREST schema
│   ├── tables/
│   │   ├── tables-list.json     # All exposed tables
│   │   └── tables-metadata.json # Column details per table
│   ├── data-samples/            # Sample data retrieved (redacted)
│   │   ├── users-sample.json
│   │   ├── orders-sample.json
│   │   └── ...
│   ├── rls-tests/               # RLS policy test results
│   │   ├── users-anon.json      # Anon access attempt
│   │   ├── users-auth.json      # Authenticated access
│   │   └── cross-user-test.json # Cross-user access attempt
│   └── rpc-tests/               # RPC function test results
│       ├── function-list.json
│       └── vulnerable-functions/
│           └── get-all-users.json
│
├── 04-storage-audit/
│   ├── buckets-config.json      # Bucket configurations
│   ├── buckets/
│   │   ├── avatars/
│   │   │   └── file-list.json
│   │   ├── backups/             # If sensitive (P0)
│   │   │   ├── file-list.json
│   │   │   └── sample-contents/ # Redacted samples
│   │   └── ...
│   └── public-url-tests/        # Direct URL access tests
│       └── backup-access.json
│
├── 05-auth-audit/
│   ├── auth-settings.json       # Auth configuration
│   ├── signup-tests/
│   │   ├── open-signup.json     # Signup availability
│   │   ├── weak-password.json   # Weak password test
│   │   └── rate-limit.json      # Rate limiting test
│   └── enumeration-tests/
│       ├── login-timing.json    # Timing attack data
│       ├── recovery-timing.json
│       └── otp-enumeration.json
│
├── 06-realtime-audit/
│   ├── websocket-connection.json
│   ├── postgres-changes/        # Table subscription tests
│   │   └── users-streaming.json
│   ├── broadcast-channels/      # Channel access tests
│   │   └── admin-channel.json
│   └── presence-data/
│       └── exposed-users.json
│
├── 07-functions-audit/
│   ├── discovered-functions.json
│   └── function-tests/
│       ├── hello-world.json
│       ├── get-user-data-idor.json
│       └── admin-panel-escalation.json
│
└── screenshots/                 # Optional: browser screenshots
    └── ...
```

## Usage

### Initialize Evidence Directory

```
Initialize evidence collection for audit
```

### Manual Evidence Save

```
Save evidence: [description] to [category]
```

## Evidence File Format

Each evidence file follows this structure:

```json
{
  "evidence_id": "API-001",
  "timestamp": "2025-01-31T10:30:00Z",
  "category": "api-audit",
  "type": "data-sample",
  "finding_id": "P0-001",
  "description": "Users table data accessible without authentication",

  "request": {
    "method": "GET",
    "url": "https://abc123.supabase.co/rest/v1/users?select=*&limit=5",
    "headers": {
      "apikey": "[REDACTED - anon key]",
      "Authorization": "Bearer [REDACTED - anon key]"
    },
    "curl_command": "curl -X GET 'https://abc123.supabase.co/rest/v1/users?select=*&limit=5' -H 'apikey: eyJ...' -H 'Authorization: Bearer eyJ...'"
  },

  "response": {
    "status": 200,
    "headers": {
      "content-type": "application/json",
      "x-total-count": "1247"
    },
    "body": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "email": "[REDACTED]@example.com",
        "name": "[REDACTED]",
        "created_at": "2025-01-15T10:30:00Z"
      }
    ],
    "body_redacted": true,
    "total_rows_indicated": 1247
  },

  "analysis": {
    "severity": "P0",
    "impact": "All user PII accessible without authentication",
    "affected_data": ["email", "name", "id"],
    "row_count": 1247
  }
}
```

## Curl Commands File

All curl commands are collected in `curl-commands.sh`:

```bash
#!/bin/bash
# Supabase Security Audit - Reproducible Commands
# Target: https://myapp.example.com
# Project: abc123def.supabase.co
# Date: 2025-01-31
#
# IMPORTANT: Replace [ANON_KEY] with actual key before running
# WARNING: These commands may modify data - use with caution

SUPABASE_URL="https://abc123def.supabase.co"
ANON_KEY="eyJ..."

# === DETECTION ===
# Check if Supabase is used
curl -s "$SUPABASE_URL/rest/v1/" -H "apikey: $ANON_KEY" | head -100

# === TABLE LISTING ===
# Get OpenAPI schema (list all tables)
curl -s "$SUPABASE_URL/rest/v1/" -H "apikey: $ANON_KEY"

# === DATA ACCESS TESTS ===
# Test: Users table (P0 - should be blocked)
curl -s "$SUPABASE_URL/rest/v1/users?select=*&limit=5" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ANON_KEY"

# Test: Orders table (should be blocked by RLS)
curl -s "$SUPABASE_URL/rest/v1/orders?select=*&limit=5" \
  -H "apikey: $ANON_KEY" \
  -H "Authorization: Bearer $ANON_KEY"

# === RLS BYPASS TESTS ===
# ... additional commands ...
```

## Timeline File

The `timeline.md` provides chronological evidence:

```markdown
# Audit Timeline

## 2025-01-31 10:00:00 - Audit Started
- Target: https://myapp.example.com
- Authorization confirmed

## 2025-01-31 10:05:00 - Detection Phase
- Supabase detected with high confidence
- Project URL: https://abc123def.supabase.co
- Evidence: `01-detection/initial-scan.json`

## 2025-01-31 10:10:00 - P0 CRITICAL: Service Key Exposed
- Service role key found in client code
- Location: /static/js/admin.chunk.js:89
- Evidence: `02-extraction/service-key-exposure/`

## 2025-01-31 10:15:00 - API Audit Started
- 8 tables discovered
- Evidence: `03-api-audit/tables/tables-list.json`

## 2025-01-31 10:20:00 - P0 CRITICAL: Users Table Exposed
- All 1,247 user records accessible
- PII exposed: email, name
- Evidence: `03-api-audit/data-samples/users-sample.json`

...
```

## Context Output

Updates `.sb-pentest-context.json`:

```json
{
  "evidence": {
    "directory": ".sb-pentest-evidence",
    "initialized_at": "2025-01-31T10:00:00Z",
    "files_count": 45,
    "categories": {
      "detection": 3,
      "extraction": 5,
      "api-audit": 15,
      "storage-audit": 8,
      "auth-audit": 7,
      "realtime-audit": 4,
      "functions-audit": 3
    },
    "critical_evidence": [
      "02-extraction/service-key-exposure/",
      "03-api-audit/data-samples/users-sample.json",
      "04-storage-audit/buckets/backups/"
    ]
  }
}
```

## Evidence Collection Rules

### What to Collect

| Category | Evidence Type | Example |
|----------|---------------|---------|
| **Always** | Raw API responses | JSON responses |
| **Always** | Curl commands | Reproducible commands |
| **Always** | Timestamps | When each test occurred |
| **P0/P1** | Data samples (redacted) | Sample rows with PII masked |
| **P0** | Full request/response | Complete HTTP exchange |
| **Optional** | Screenshots | Browser evidence |

### Redaction Rules

Sensitive data MUST be redacted in evidence files:

```json
{
  "original": "john.doe@example.com",
  "redacted": "[REDACTED]@example.com"
}

{
  "original": "John Doe",
  "redacted": "[REDACTED]"
}

{
  "original": "sk_live_xxxxxxxxxxxxxxxxxxxx",
  "redacted": "sk_live_[REDACTED]"
}
```

**NEVER store in evidence:**
- Actual passwords
- Full credit card numbers
- Full API keys (show first/last 4 chars only)
- Full personal data (partial redaction required)

### Naming Conventions

```
[category]-[test-name]-[timestamp].json
```

Examples:
- `users-anon-access-20250131-103000.json`
- `admin-function-no-auth-20250131-143000.json`

## MANDATORY: Evidence File Updates

⚠️ **Evidence MUST be saved PROGRESSIVELY during execution.**

### Critical Rule: Save As You Go

**DO NOT** batch all evidence at the end. Instead:

1. **Before each test** → Create evidence file placeholder
2. **After each request** → Save request details immediately
3. **After each response** → Save response immediately
4. **After analysis** → Add analysis to evidence file

### Directory Initialization

At audit start, create:

```bash
mkdir -p .sb-pentest-evidence/{01-detection,02-extraction,03-api-audit/tables,03-api-audit/data-samples,03-api-audit/rls-tests,03-api-audit/rpc-tests,04-storage-audit/buckets,04-storage-audit/public-url-tests,05-auth-audit/signup-tests,05-auth-audit/enumeration-tests,06-realtime-audit/postgres-changes,06-realtime-audit/broadcast-channels,07-functions-audit/function-tests,screenshots}
```

### Log to Audit Log

```
[TIMESTAMP] [supabase-evidence] [START] Initializing evidence directory
[TIMESTAMP] [supabase-evidence] [CREATED] .sb-pentest-evidence/
[TIMESTAMP] [supabase-evidence] [CONTEXT_UPDATED] Evidence tracking initialized
```

## Integration with Other Skills

This skill is automatically invoked by `supabase-pentest`. Each audit skill should:

1. Save evidence to the appropriate subdirectory
2. Use consistent naming conventions
3. Add entries to `curl-commands.sh`
4. Update `timeline.md` for significant findings

## Related Skills

- `supabase-pentest` — Orchestrator that initializes evidence collection
- `supabase-report` — Uses evidence for comprehensive reporting
- All audit skills — Contribute evidence to their respective directories
