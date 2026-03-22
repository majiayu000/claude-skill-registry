---
version: 1.1.0
name: dev-security
description: >
  Security review aligned with OWASP Top 10:2025. Auto-detects backend (.NET)
  and frontend (Angular/TypeScript) from project files. Runs both in mixed
  projects. Reports findings with severity and offers to fix inline. Filter
  with "dotnet" or "angular" to target one stack. Use when the user says
  "security review", "check security", "audit security", or invokes /dev-security.
disable-model-invocation: true
user-invocable: true
argument-hint: "[dotnet | angular | --checklist | --scan | --full]"
---

# Security Review — Unified Entry Point

Routes to the appropriate backend and/or frontend security skill, aligned
with OWASP Top 10:2025. Presents findings with severity ratings and offers
to fix them inline.

> **References:**
> - [OWASP Top 10:2025](https://owasp.org/Top10/2025/)
> - [OWASP Top 10 for Agentic Applications:2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)

## Step 1: Detect Stacks

1. **Explicit filter** — if the user passed `dotnet` or `angular`, use only that stack
2. **Project detection**:
   - .NET: any `*.csproj`, `*.sln` file exists
   - Angular: `angular.json` or `package.json` with `@angular/core` exists
3. **workflow.json fallback**:
   - `type: "api"` or `type: "library"` → .NET
   - `type: "frontend"` → Angular
   - `type: "docs"` → skip

If both detected and no filter, run both — security should cover the full stack.

## Step 2: Run Review

Run all checklist items and scans from the appropriate sub-skill(s). Collect
all findings without stopping.

### .NET (if applicable)

Read and follow `.claude/skills/dev-security-backend/SKILL.md`.

### Angular (if applicable)

Read and follow `.claude/skills/dev-security-frontend/SKILL.md`.

## Step 3: Present Findings with Fix Menu

After all checks complete, present findings grouped by severity:

```
SECURITY REVIEW — OWASP Top 10:2025
════════════════════════════════════

  Critical
  ────────
  1. [A04] Hardcoded connection string in appsettings.json:12
  2. [A05] String concatenation in SQL query — OrderRepository.cs:45

  High
  ────
  3. [A01] Missing auth on POST /api/admin/reset — AdminEndpoints.cs:28
  4. [A03] npm audit: 2 high-severity vulnerabilities in lodash, axios

  Medium
  ──────
  5. [A02] Security headers missing (X-Frame-Options, CSP)
  6. [A07] Session cookie missing SameSite attribute
  7. [A10] Empty catch block in PaymentService.cs:92

  Low
  ───
  8. [A09] console.log with user email in auth.service.ts:34

  Info
  ────
  ✓ A06 Insecure Design: Rate limiting configured
  ✓ A08 Integrity: Anti-forgery tokens enabled
  ✓ Event Sourcing: Stream isolation verified

  ───────────────────────────────────────────
  Fix?  [a]ll  [1-8] pick  [c]ritical only  [s]kip
```

Wait for user input.

## Step 4: Fix Selected Issues

Based on user selection:

- **`a` (all)** — Fix every finding in severity order (critical first)
- **`1-8` (pick)** — Fix selected issues: `1,3,5` or `1-4`
- **`c` (critical only)** — Fix only critical and high severity
- **`s` (skip)** — Done, report only

### Fix Strategies by OWASP Category

| Category | Fix Strategy |
|----------|-------------|
| **A01 Access Control** | Add `RequireAuthorization()`, add route guards |
| **A02 Misconfiguration** | Add security headers middleware, disable debug |
| **A03 Supply Chain** | Run `npm audit fix` / `dotnet update`, review |
| **A04 Cryptographic** | Move secrets to config/Key Vault, remove hardcoded values |
| **A05 Injection** | Replace string concat with parameterized queries |
| **A06 Insecure Design** | Add rate limiting, input constraints |
| **A07 Auth Failures** | Fix cookie config, add session timeout |
| **A08 Integrity** | Add anti-forgery, fix SW config |
| **A09 Logging** | Remove sensitive data from logs, add alerting |
| **A10 Exceptions** | Add error handlers, fix empty catches |

**Security fixes always show the proposed change and ask before applying** — unlike formatting fixes, security changes need review.

### After Fixing

Re-run only the checks that had findings to verify fixes:

```
  Re-check
  ────────
  1. [A04] Connection string:  ✓ moved to User Secrets
  2. [A05] SQL injection:      ✓ parameterized
  3. [A01] Missing auth:       ✓ RequireAuthorization() added

  Remaining: 5 findings (4 medium, 1 low)
  ─────────────────────────────────────────
  Fix more?  [5-8] pick  [s]kip
```

## Step 5: Final Report

```
  Security Review Complete
  ────────────────────────
  OWASP Top 10:2025 coverage: 10/10 categories checked
  Findings: 8 total → 3 fixed, 5 remaining (4 medium, 1 low)
  Stacks:   .NET ✓  Angular ✓
```

## Flags

| Flag | Behavior |
|------|----------|
| `dotnet` | Run .NET security review only |
| `angular` | Run Angular security review only |
| `--checklist` | Pre-deployment checklist (no scans, no fixes) |
| `--scan` | Automated scans only (secret grep, audit, vulnerable packages) |
| `--full` | Checklist + scans + code review + fix menu (default) |
