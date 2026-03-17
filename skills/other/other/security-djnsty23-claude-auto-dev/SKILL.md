---
name: security
description: Pre-deploy security audit with vulnerability pattern scanning. Auto-loaded with review, audit, ship.
triggers:
  - security
allowed-tools: Bash, Grep, Read, Glob
model: opus
user-invocable: true
argument-hint: "[scope: full|quick|file]"
---

# Security Check

Run before every deploy.

## Automated Checks

### 1. Secrets Scan
```bash
# Check for hardcoded secrets in source AND migrations
grep -rn "sk_live\|sk_test\|api_key\s*=\s*['\"][^'\"]\+" src/ supabase/ --include="*.ts" --include="*.tsx" --include="*.sql"
grep -rn "password\s*=\s*['\"][^'\"]\+" src/ supabase/ --include="*.ts" --include="*.tsx" --include="*.sql"
grep -rn "service_role\|supabase_admin\|cron\.\|pg_cron" supabase/migrations/ --include="*.sql" 2>/dev/null
```

If found: move to env vars or Edge Function secrets. CRON secrets must use `vault.secrets`, never hardcoded in migrations.

### 2. Environment Variables
```bash
# Check .env files not committed
git status | grep ".env"
```

If .env tracked: add to .gitignore immediately.

### 3. Supabase RLS (Enabled + Policy Quality)
```bash
# Check all tables have RLS
npx supabase db lint
```

If RLS disabled: enable RLS before proceeding.

**Beyond enabled — check policy quality:**

```sql
-- Find tables with public SELECT (data exposure risk)
SELECT schemaname, tablename, policyname, cmd, qual
FROM pg_policies WHERE schemaname = 'public';
```

Flag these patterns:
- Tables with PII (emails, names, tokens) that allow SELECT without `auth.uid() = user_id`
- OAuth/refresh tokens accessible via public SELECT policy
- Profiles table without row-level restriction (`auth.uid() = id`)
- Service role keys or admin tokens stored in queryable tables

**Supabase auth config checks:**
- Email enumeration protection enabled
- MFA available for admin accounts
- Note: Leaked password protection requires Supabase Pro plan ($20/mo) — skip if free tier

### 4. Input Validation
```typescript
// Check for unvalidated inputs
grep -rn "req.body\." src/ --include="*.ts" | grep -v "zod\|schema\|validate"
```

If unvalidated: **WARN** - add Zod validation.

### 5. XSS Vectors
```bash
grep -rn "dangerouslySetInnerHTML\|innerHTML\|document.write" src/
```

If found: **WARN** - sanitize or remove.

## Report

```
Security Check
==============
Secrets:     Pass/Fail
Env files:   Pass/Fail
RLS:         Pass/Fail
Validation:  Pass/Warn
XSS:         Pass/Warn

Result: PASS/FAIL (N warnings)
Ready to deploy: Yes/No
```

## Auto-Fix

For common issues:
- Move secrets -> `.env.local`
- Add `.env*` to `.gitignore`
- Add `ALTER TABLE x ENABLE ROW LEVEL SECURITY`

---

## Vulnerability Patterns

Quick reference for security vulnerabilities to catch during code review.

### Command Injection

#### GitHub Actions Workflows
**Path**: `.github/workflows/*.yml`

**Unsafe** (user input in run command):
```yaml
run: echo "${{ github.event.issue.title }}"
```

**Safe** (use environment variables):
```yaml
env:
  TITLE: ${{ github.event.issue.title }}
run: echo "$TITLE"
```

**Risky inputs to watch:**
- `github.event.issue.title/body`
- `github.event.pull_request.title/body`
- `github.event.comment.body`
- `github.event.commits.*.message`
- `github.head_ref`

#### Node.js child_process
**Unsafe**:
```javascript
exec(`command ${userInput}`)
```

**Safe**:
```javascript
execFile('command', [userInput])
```

### Code Injection

| Pattern | Risk | Alternative |
|---------|------|-------------|
| `eval()` | Arbitrary code execution | `JSON.parse()` for data |
| `new Function()` | Code injection | Static functions |
| `pickle` (Python) | Arbitrary code execution | `json` module |
| `os.system()` | Shell injection | `subprocess.run()` with list args |

### XSS (Cross-Site Scripting)

| Pattern | Risk | Alternative |
|---------|------|-------------|
| `dangerouslySetInnerHTML` | XSS if unsanitized | DOMPurify sanitizer |
| `document.write()` | XSS + performance | `createElement` + `appendChild` |
| `.innerHTML =` | XSS if unsanitized | `.textContent` or sanitizer |

### When to Flag

**Flag these:**
- User input flowing into dangerous functions
- Hardcoded secrets/credentials
- Missing input validation at system boundaries

**Don't flag:**
- Internal code with trusted input
- Properly sanitized content
- Test fixtures with mock data

Reference: [GitHub Actions Security Guide](https://github.blog/security/vulnerability-research/how-to-catch-github-actions-workflow-injections-before-attackers-do/)

---

## Cloud Credential Hygiene (GCP / Vercel / Supabase)

### 6. API Key & Service Account Audit
```bash
# Check for unrestricted or long-lived keys in source
grep -rn "AIza\|GOOG\|ya29\.\|service_account" src/ --include="*.ts" --include="*.tsx" --include="*.json" --include="*.env*"
# Check for keys committed to git history
git log -p --all -S "AIza" --diff-filter=A -- "*.ts" "*.json" 2>/dev/null | head -20
```

**Rules:**
- **Zero code storage**: Never commit API keys or service account JSON. Use Secret Manager or env vars injected at runtime.
- **Disable dormant keys**: Any key unused for 30+ days should be decommissioned.
- **Restrict every API key**: Limit to specific APIs (e.g., Maps JS only) and bind to IP/referrer/bundle ID.
- **Least privilege**: Service accounts get minimum required permissions only. Use IAM recommender to prune unused roles.
- **Enforce rotation**: Set max key lifespan via org policy. Disable key creation entirely if not needed.

### 7. Operational Safeguards
Flag if missing:
- **Essential contacts** configured for security notifications
- **Billing anomaly alerts** enabled (consumption spike = first sign of compromised credential)
- **Budget alerts** with notification channels that are actively monitored
