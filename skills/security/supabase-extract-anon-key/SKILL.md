---
name: supabase-extract-anon-key
description: Extract the Supabase anon/public API key from client-side code. This key is expected in client apps but important for RLS testing.
---

# Supabase Anon Key Extraction

> 🔴 **CRITICAL: PROGRESSIVE FILE UPDATES REQUIRED**
>
> You MUST write to context files **AS YOU GO**, not just at the end.
> - Write to `.sb-pentest-context.json` **IMMEDIATELY after each discovery**
> - Log to `.sb-pentest-audit.log` **BEFORE and AFTER each action**
> - **DO NOT** wait until the skill completes to update files
> - If the skill crashes or is interrupted, all prior findings must already be saved
>
> **This is not optional. Failure to write progressively is a critical error.**

This skill extracts the Supabase anonymous (public) API key from client-side code.

## When to Use This Skill

- After extracting the Supabase URL, to get the API key for testing
- To verify that only the anon key (not service key) is exposed
- Before running API audit skills that require authentication

## Prerequisites

- Supabase URL extracted (or will auto-invoke `supabase-extract-url`)
- Target application accessible

## Understanding Anon Keys

The **anon key** (also called public key) is:

- ✅ **Expected** to be in client-side code
- ✅ **Safe** when RLS (Row Level Security) is properly configured
- ⚠️ **Risky** if RLS is missing or misconfigured
- ❌ **Not the same** as the service_role key (which should NEVER be in client code)

### Key Format

Supabase anon keys are JWTs:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiYzEyMyIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNjQwMDAwMDAwLCJleHAiOjE5NTUzNjAwMDB9.xxxx
```

Key characteristics:
- Starts with `eyJ` (base64 encoded `{"alg":`)
- Contains `"role":"anon"` in payload
- Project reference in `"ref"` claim

## Extraction Patterns

The skill searches for:

### 1. Direct Key Assignment

```javascript
const SUPABASE_KEY = 'eyJhbGci...'
const SUPABASE_ANON_KEY = 'eyJhbGci...'
```

### 2. Client Initialization

```javascript
createClient(url, 'eyJhbGci...')
createClient(url, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
```

### 3. Environment Variable Patterns

```javascript
NEXT_PUBLIC_SUPABASE_ANON_KEY
VITE_SUPABASE_ANON_KEY
REACT_APP_SUPABASE_KEY
SUPABASE_KEY
```

## Usage

### Basic Extraction

```
Extract Supabase anon key from https://myapp.example.com
```

### If URL Already Known

```
Extract anon key for project abc123def
```

## Output Format

```
═══════════════════════════════════════════════════════════
 ANON KEY EXTRACTED
═══════════════════════════════════════════════════════════

 Key Type: anon (public)
 Severity: ℹ️  Expected (verify RLS configuration)

 Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJz
      dXBhYmFzZSIsInJlZiI6ImFiYzEyM2RlZiIsInJvbGUiOiJhbm
      9uIiwiaWF0IjoxNjQwMDAwMDAwLCJleHAiOjE5NTUzNjAwMDB9
      .xxxxxxxxxxxxx

 Decoded Payload:
 ├── iss: supabase
 ├── ref: abc123def
 ├── role: anon
 ├── iat: 2021-12-20T00:00:00Z
 └── exp: 2031-12-20T00:00:00Z

 Found in:
 └── /static/js/main.js (line 1253)
     createClient('https://abc123def.supabase.co', 'eyJhbGci...')

 Next Steps:
 ├── Run supabase-audit-rls to test if RLS protects your data
 ├── Run supabase-audit-tables-read to see what's accessible
 └── Run supabase-extract-service-key to check for critical leaks

 Context updated: .sb-pentest-context.json
═══════════════════════════════════════════════════════════
```

## Key Validation

The skill validates the extracted key:

```
Validation:
├── Format: ✅ Valid JWT structure
├── Decode: ✅ Payload readable
├── Role: ✅ Confirmed "anon" role
├── Project: ✅ Matches extracted URL (abc123def)
└── Expiry: ✅ Not expired (expires 2031-12-20)
```

## Multiple Keys

If multiple keys are found:

```
═══════════════════════════════════════════════════════════
 MULTIPLE KEYS FOUND
═══════════════════════════════════════════════════════════

 ⚠️  2 potential Supabase keys detected

 1. Anon Key (confirmed)
    └── Role: anon, Project: abc123def

 2. Unknown Key
    └── Role: service_role ⚠️  SEE supabase-extract-service-key
        This may be a CRITICAL security issue!

═══════════════════════════════════════════════════════════
```

## Context Output

Saved to `.sb-pentest-context.json`:

```json
{
  "supabase": {
    "anon_key": "eyJhbGci...",
    "anon_key_decoded": {
      "iss": "supabase",
      "ref": "abc123def",
      "role": "anon",
      "iat": 1640000000,
      "exp": 1955360000
    },
    "anon_key_sources": [
      {
        "file": "/static/js/main.js",
        "line": 1253
      }
    ]
  }
}
```

## Security Assessment

| Finding | Severity | Description |
|---------|----------|-------------|
| Anon key in client | ℹ️ Info | Expected, but test RLS |
| Anon key expired | ⚠️ P2 | Key should be rotated |
| Multiple anon keys | ⚠️ P2 | May indicate key rotation issues |
| Role is not "anon" | 🔴 P0 | Wrong key type exposed! |

## Common Issues

❌ **Problem:** Key found but won't decode
✅ **Solution:** May be obfuscated or split. Try:
```
Extract anon key with deobfuscation from https://myapp.example.com
```

❌ **Problem:** Key doesn't match URL project
✅ **Solution:** App may use multiple Supabase projects. Both keys are recorded.

❌ **Problem:** No key found but Supabase detected
✅ **Solution:** Key may be fetched at runtime. Check network requests:
```
Monitor network for anon key on https://myapp.example.com
```

## Best Practices Reminder

For developers reading this report:

1. **Anon key in client is normal** — It's designed for this
2. **RLS is critical** — The anon key relies on RLS for security
3. **Never use service_role in client** — Use Edge Functions instead
4. **Rotate keys periodically** — Available in Supabase Dashboard

## MANDATORY: Progressive Context File Updates

⚠️ **This skill MUST update tracking files PROGRESSIVELY during execution, NOT just at the end.**

### Critical Rule: Write As You Go

**DO NOT** batch all writes at the end. Instead:

1. **Before starting any action** → Log the action to `.sb-pentest-audit.log`
2. **After each discovery** → Immediately update `.sb-pentest-context.json`
3. **After each significant step** → Log completion to `.sb-pentest-audit.log`

This ensures that if the skill is interrupted, crashes, or times out, all findings up to that point are preserved.

### Required Actions (Progressive)

1. **Update `.sb-pentest-context.json`** with extracted data:
   ```json
   {
     "supabase": {
       "anon_key": "eyJhbGci...",
       "anon_key_decoded": { ... },
       "anon_key_sources": [ ... ]
     }
   }
   ```

2. **Log to `.sb-pentest-audit.log`**:
   ```
   [TIMESTAMP] [supabase-extract-anon-key] [START] Beginning anon key extraction
   [TIMESTAMP] [supabase-extract-anon-key] [SUCCESS] Anon key extracted
   [TIMESTAMP] [supabase-extract-anon-key] [CONTEXT_UPDATED] .sb-pentest-context.json updated
   ```

3. **If files don't exist**, create them before writing.

**FAILURE TO UPDATE CONTEXT FILES IS NOT ACCEPTABLE.**

## MANDATORY: Evidence Collection

📁 **Evidence Directory:** `.sb-pentest-evidence/02-extraction/`

### Evidence Files to Create

| File | Content |
|------|---------|
| `extracted-anon-key.json` | Anon key with decoded JWT payload |

### Evidence Format

```json
{
  "evidence_id": "EXT-ANON-001",
  "timestamp": "2025-01-31T10:07:00Z",
  "category": "extraction",
  "type": "anon_key",
  "severity": "info",

  "key_data": {
    "key_prefix": "eyJhbGciOiJIUzI1NiI...",
    "key_suffix": "...xxxx",
    "full_key_length": 256
  },

  "decoded_payload": {
    "iss": "supabase",
    "ref": "abc123def",
    "role": "anon",
    "iat": "2021-12-20T00:00:00Z",
    "exp": "2031-12-20T00:00:00Z"
  },

  "source": {
    "file": "/static/js/main.js",
    "line": 1253,
    "context": "createClient('https://abc123def.supabase.co', 'eyJhbGci...')"
  },

  "validation": {
    "format_valid": true,
    "role_confirmed": "anon",
    "project_matches": true,
    "expired": false
  }
}
```

## Related Skills

- `supabase-extract-url` — Get URL first (auto-invoked if needed)
- `supabase-extract-service-key` — Check for critical service key leak
- `supabase-audit-rls` — Test if RLS protects your data
- `supabase-audit-tables-read` — See what data is accessible with this key
