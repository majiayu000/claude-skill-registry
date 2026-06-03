---
name: dev-security
description: Security audit with Sentinel. Checks for vulnerabilities, secrets, dependencies, and security best practices. Use before shipping or when working on auth/crypto/sensitive areas.
---

# Dev Security - Security Audit

Delegate to Sentinel for comprehensive security review.

## Philosophy

"Every line of code is guilty until proven innocent."

## Flow

### 1. Context Gathering

```bash
# What changed?
git diff --name-only HEAD~10 2>/dev/null || git diff --name-only

# What's the scope?
ls -la
```

### 2. Invoke Sentinel

Delegate to Sentinel agent:

```
"Sentinel, security audit time.

Scope: {describe what changed or focus area}

Run your full checklist:
1. Secrets scan
2. Dependency audit
3. Injection vectors
4. Auth/authz review
5. Crypto check

Files changed: {list from git diff}

Be thorough. We're not shipping vulnerabilities."
```

### 3. Review Sentinel's Findings

Sentinel returns findings by severity:
- **CRITICAL**: Must fix before merge
- **HIGH**: Should fix before merge
- **MEDIUM**: Should fix soon
- **LOW**: Consider fixing

### 4. Action on Findings

**If CRITICAL or HIGH found:**
```
Security audit found issues:

CRITICAL:
- [Issue 1 with location and fix]

HIGH:
- [Issue 2 with location and fix]

Options:
1. Fix now (Bob will implement Sentinel's fixes)
2. Fix manually, run /dev-security again
3. Accept risk (requires explicit acknowledgment)
4. Get second opinion (run deeper audit)
```

**If only MEDIUM/LOW:**
```
Security audit passed with notes.

MEDIUM:
- [Issue with suggestion]

LOW:
- [Issue with suggestion]

These don't block shipping but should be tracked.
Add to backlog? (y/n)
```

**If clean:**
```
Security audit passed!

Sentinel says: "Huh. Someone actually read the OWASP guide. Respect."

Ready for:
- /dev-rc - Release candidate
- /dev-finish - Close the cycle
```

### 5. Log Results

If active dev-cycle session:
```markdown
## Security Audit
- **Date**: {timestamp}
- **Status**: PASSED | PASSED_WITH_NOTES | FAILED
- **Critical**: 0
- **High**: 0
- **Medium**: 2
- **Low**: 1

### Findings
{Summary of what was found and resolved}
```

## Focus Modes

### Full Audit (default)
```
/dev-security
```
Everything: secrets, deps, code, config, infra

### Quick Scan
```
/dev-security quick
```
Just the critical stuff: secrets, known CVEs, obvious injection

### Specific Focus
```
/dev-security auth
/dev-security crypto
/dev-security deps
/dev-security secrets
```

Focus on one area for deeper review.

## What Sentinel Checks

| Area | What | Why |
|------|------|-----|
| Secrets | Hardcoded keys, tokens, passwords | #1 breach cause |
| Dependencies | Known CVEs, outdated packages | Supply chain attacks |
| Injection | SQL, XSS, command, path traversal | OWASP Top 10 |
| Auth | Broken auth, missing authz | Gateway to everything |
| Crypto | Weak algorithms, hardcoded keys | Data protection |
| Config | Exposed debug, permissive CORS | Misconfiguration |

## Integration

**With dev-cycle**: Logs findings to session
**With dev-rc**: Security must pass for release candidate
**With Bob**: Implements fixes for findings
**With Sentinel**: The security brain

## When to Run

- Before any PR
- After implementing auth/authz
- After adding new dependencies
- After handling user input
- After touching crypto
- Before any release
- When Sentinel whispers "trust nothing"
