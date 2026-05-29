---
name: supabase-extract-url
description: Extract the Supabase project URL from client-side JavaScript code, environment variables, and configuration files.
---

# Supabase URL Extraction

> 🔴 **CRITICAL: PROGRESSIVE FILE UPDATES REQUIRED**
>
> You MUST write to context files **AS YOU GO**, not just at the end.
> - Write to `.sb-pentest-context.json` **IMMEDIATELY after each discovery**
> - Log to `.sb-pentest-audit.log` **BEFORE and AFTER each action**
> - **DO NOT** wait until the skill completes to update files
> - If the skill crashes or is interrupted, all prior findings must already be saved
>
> **This is not optional. Failure to write progressively is a critical error.**

This skill extracts the Supabase project URL from a web application's client-side code.

## When to Use This Skill

- After detecting Supabase usage, to get the exact project URL
- When you need the API base URL for further testing
- To identify which Supabase project an application uses

## Prerequisites

- Target URL accessible
- Supabase usage detected (or suspected)

## How It Works

The skill scans for URL patterns in:

### 1. JavaScript Source Code

```javascript
// Direct URL references
const SUPABASE_URL = 'https://abc123.supabase.co'
createClient('https://abc123.supabase.co', key)

// Environment variable patterns
process.env.SUPABASE_URL
process.env.NEXT_PUBLIC_SUPABASE_URL
import.meta.env.VITE_SUPABASE_URL
```

### 2. HTML Meta Tags and Scripts

```html
<meta name="supabase-url" content="https://abc123.supabase.co">
<script>
  window.SUPABASE_URL = 'https://abc123.supabase.co'
</script>
```

### 3. Configuration Objects

```javascript
const config = {
  supabase: {
    url: 'https://abc123.supabase.co'
  }
}
```

## URL Pattern Matching

Recognized patterns:

| Pattern | Example |
|---------|---------|
| Standard | `https://abc123.supabase.co` |
| With region | `https://abc123.eu-central-1.supabase.co` |
| Custom domain | Detected via API endpoint patterns |

## Usage

### Basic Extraction

```
Extract Supabase URL from https://myapp.example.com
```

### From Local Files

If you have downloaded the source:
```
Extract Supabase URL from ./dist/assets/
```

## Output Format

```
═══════════════════════════════════════════════════════════
 SUPABASE URL EXTRACTED
═══════════════════════════════════════════════════════════

 Project URL: https://abc123def.supabase.co
 Project Ref: abc123def
 Region: us-east-1 (inferred)

 Found in:
 ├── /static/js/main.abc123.js (line 1247)
 │   └── const SUPABASE_URL = 'https://abc123def.supabase.co'
 │
 └── /static/js/chunk.def456.js (line 89)
     └── createClient('https://abc123def.supabase.co', ...)

 API Endpoints:
 ├── REST API: https://abc123def.supabase.co/rest/v1/
 ├── Auth API: https://abc123def.supabase.co/auth/v1/
 ├── Storage: https://abc123def.supabase.co/storage/v1/
 └── Realtime: wss://abc123def.supabase.co/realtime/v1/

 Context updated: .sb-pentest-context.json
═══════════════════════════════════════════════════════════
```

## Context Output

Saved to `.sb-pentest-context.json`:

```json
{
  "supabase": {
    "project_url": "https://abc123def.supabase.co",
    "project_ref": "abc123def",
    "region": "us-east-1",
    "endpoints": {
      "rest": "https://abc123def.supabase.co/rest/v1/",
      "auth": "https://abc123def.supabase.co/auth/v1/",
      "storage": "https://abc123def.supabase.co/storage/v1/",
      "realtime": "wss://abc123def.supabase.co/realtime/v1/",
      "functions": "https://abc123def.supabase.co/functions/v1/"
    },
    "sources": [
      {
        "file": "/static/js/main.abc123.js",
        "line": 1247,
        "context": "const SUPABASE_URL = 'https://abc123def.supabase.co'"
      }
    ]
  }
}
```

## Multiple URLs

If multiple Supabase URLs are found:

```
═══════════════════════════════════════════════════════════
 MULTIPLE SUPABASE URLS FOUND
═══════════════════════════════════════════════════════════

 ⚠️  Multiple Supabase projects detected

 1. https://abc123.supabase.co (primary - most references)
    └── Found in: main.js, config.js

 2. https://xyz789.supabase.co (secondary)
    └── Found in: analytics.js

 Using primary URL for further analysis.
 To use a different URL, specify it manually.
═══════════════════════════════════════════════════════════
```

## Validation

The skill validates extracted URLs by:

1. **Format check** — Matches expected Supabase URL patterns
2. **Reachability check** — Attempts to reach the REST API endpoint
3. **Response validation** — Confirms Supabase-like response

```
Validation:
├── Format: ✅ Valid Supabase URL format
├── Reachable: ✅ REST API responds (200 OK)
└── Confirmed: ✅ Response matches Supabase pattern
```

## Common Issues

❌ **Problem:** URL not found despite Supabase detection
✅ **Solution:** The URL may be in a dynamically loaded chunk. Try:
```
Extract URL with deep scan from https://myapp.example.com
```

❌ **Problem:** URL found but validation fails
✅ **Solution:** The project may be paused or the region may have connectivity issues. The URL is still recorded.

❌ **Problem:** Only custom domain found
✅ **Solution:** Custom domains are valid. The skill will note it as a custom domain and attempt to identify the underlying project.

## Security Notes

- This skill only reads publicly available code
- No authentication is attempted
- The URL alone does not grant access (key is also required)

## Next Steps

After extracting the URL:
1. Run `supabase-extract-anon-key` to find the API key
2. Run `supabase-extract-service-key` to check for leaked service keys
3. Proceed to API auditing skills

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
       "project_url": "https://[ref].supabase.co",
       "project_ref": "[ref]",
       "endpoints": { ... }
     }
   }
   ```

2. **Log to `.sb-pentest-audit.log`**:
   ```
   [TIMESTAMP] [supabase-extract-url] [START] Beginning URL extraction
   [TIMESTAMP] [supabase-extract-url] [SUCCESS] URL extracted: https://[ref].supabase.co
   [TIMESTAMP] [supabase-extract-url] [CONTEXT_UPDATED] .sb-pentest-context.json updated
   ```

3. **If files don't exist**, create them before writing.

**FAILURE TO UPDATE CONTEXT FILES IS NOT ACCEPTABLE.**

## MANDATORY: Evidence Collection

📁 **Evidence Directory:** `.sb-pentest-evidence/02-extraction/`

### Evidence Files to Create

| File | Content |
|------|---------|
| `extracted-url.json` | URL extraction details with source locations |

### Evidence Format

```json
{
  "evidence_id": "EXT-URL-001",
  "timestamp": "2025-01-31T10:05:00Z",
  "category": "extraction",
  "type": "url_extraction",

  "extracted_data": {
    "project_url": "https://abc123def.supabase.co",
    "project_ref": "abc123def",
    "region": "us-east-1"
  },

  "sources": [
    {
      "file": "/static/js/main.js",
      "line": 1247,
      "context": "const SUPABASE_URL = 'https://abc123def.supabase.co'"
    }
  ],

  "endpoints_discovered": {
    "rest": "https://abc123def.supabase.co/rest/v1/",
    "auth": "https://abc123def.supabase.co/auth/v1/",
    "storage": "https://abc123def.supabase.co/storage/v1/",
    "realtime": "wss://abc123def.supabase.co/realtime/v1/"
  }
}
```

## Related Skills

- `supabase-detect` — Detect Supabase usage first
- `supabase-extract-anon-key` — Extract the anon key
- `supabase-extract-service-key` — Check for service key leaks
