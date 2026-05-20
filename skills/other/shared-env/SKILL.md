---
name: shared-env
description: Environment variable management with validation, documentation, and .env.example generation.
argument-hint: "[--validate] [--generate-example] [--document] [--check-secrets]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Manage environment variables safely: validate required vars are set, generate `.env.example`, document variables, and detect accidentally committed secrets.

## Arguments
- `--validate` — Check all required env vars are set (default)
- `--generate-example` — Create/update `.env.example` from `.env`
- `--document` — Generate ENV.md documentation
- `--check-secrets` — Scan for secrets in codebase

## What gets created/updated

```
.env.example          # Template with placeholders
ENV.md                # Documentation of all variables
.gitignore            # Ensure .env is ignored
```

## Environment file hierarchy
```
.env                  # Local overrides (git-ignored)
.env.local            # Local secrets (git-ignored)
.env.development      # Dev defaults (committed)
.env.production       # Prod defaults (committed, no secrets)
.env.example          # Template (committed)
```

## Validation rules
For each variable, specify:
- **required** — Must be set
- **optional** — May be empty
- **format** — URL, email, number, boolean, etc.
- **secret** — Should never be committed

## .env.example format
```bash
# Database
MONGODB_URI=mongodb://localhost:27017/myapp  # Required: MongoDB connection string

# Auth (obtain from Google Cloud Console)
GOOGLE_CLIENT_ID=                            # Required: OAuth client ID
GOOGLE_CLIENT_SECRET=                        # Required: OAuth client secret (secret)

# Optional
LOG_LEVEL=info                               # Optional: debug|info|warn|error
```

## Workflow

### Validate (`--validate`)
1. Load env schema (from code or config)
2. Check each required var is set
3. Validate formats
4. Report missing/invalid

### Generate example (`--generate-example`)
1. Read current `.env`
2. Redact secret values
3. Add placeholder comments
4. Write `.env.example`

### Document (`--document`)
1. Parse all env vars from codebase
2. Extract from schema (Zod, etc.)
3. Generate ENV.md with descriptions

### Check secrets (`--check-secrets`)
1. Scan codebase for env patterns
2. Detect hardcoded secrets
3. Report violations

## Output
- Validation results (pass/fail per var)
- Files created/updated
- Warnings for potential issues

## Reference
For schema patterns and validation, see `reference/shared-env-reference.md`
