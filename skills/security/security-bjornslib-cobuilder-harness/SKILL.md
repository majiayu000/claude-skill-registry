---
name: codebase-quality:security
description: Security vulnerability scanning including secrets detection, dependency audits, and injection risk analysis. Use when checking for security issues, scanning for secrets, auditing dependencies, or before production deployment. First skill in codebase-quality chain. Triggers on security scan, secrets detection, vulnerability check, dependency audit, security review.
version: 1.0.0
title: "Codebase Quality:Security"
status: active
---

# Security Sub-Skill

Part of the [codebase-quality](../using-codebase-quality/SKILL.md) skill family.

## Purpose

Identify and prevent security vulnerabilities including exposed secrets, dependency vulnerabilities, and code injection risks.

## Priority

**ALWAYS RUN FIRST** in any codebase-quality workflow.

Security issues can be obscured by subsequent refactoring or formatting. Catch them before any other changes.

## Quick Reference

### Commands

```bash
# Full security scan
/codebase-quality security

# Specific scans
/codebase-quality secrets
/codebase-quality deps
/codebase-quality injection
```

### Invocation

```python
# As first step in audit
Skill("codebase-quality:security")

# After security passes, chain to code quality
Skill("codebase-quality:code-quality")
```

## Security Checks

### 1. Secrets Detection

**Patterns Scanned**:
- API keys (AWS, GCP, Azure, OpenAI, etc.)
- Private keys (RSA, SSH, PGP)
- Passwords and tokens
- Database connection strings
- OAuth secrets
- JWT signing keys

**Detection Methods**:
```bash
# Using git-secrets
git secrets --scan

# Using trufflehog
trufflehog git file://. --only-verified

# Manual regex patterns
grep -rn "sk-[a-zA-Z0-9]" .              # OpenAI
grep -rn "AKIA[A-Z0-9]{16}" .            # AWS
grep -rn "-----BEGIN.*PRIVATE KEY" .     # Private keys
```

**Severity**: CRITICAL - Always blocks merge

**Remediation**:
1. Remove secret from code immediately
2. Rotate the compromised credential
3. Add to `.gitignore` / `.env`
4. Use environment variables

### 2. Dependency Vulnerabilities

**Frontend**:
```bash
npm audit
npm audit --audit-level=high  # Only high/critical
```

**Backend**:
```bash
pip-audit                     # Python packages
safety check                  # Alternative scanner
```

**Severity Mapping**:
| Level | Action |
|-------|--------|
| Critical | Block merge, fix immediately |
| High | Block merge |
| Moderate | Warn, fix within sprint |
| Low | Info, track in backlog |

**Remediation**:
```bash
# Auto-fix where possible
npm audit fix

# For breaking changes
npm audit fix --force  # Use with caution

# Python
pip install --upgrade <package>
```

### 3. Injection Risks

**SQL Injection**:
```python
# BAD - vulnerable
query = f"SELECT * FROM users WHERE id = {user_id}"

# GOOD - parameterized
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

**XSS (Cross-Site Scripting)**:
```typescript
// BAD - vulnerable
element.innerHTML = userInput;

// GOOD - sanitized
element.textContent = userInput;
// or use DOMPurify
element.innerHTML = DOMPurify.sanitize(userInput);
```

**Command Injection**:
```python
# BAD - vulnerable
os.system(f"ls {user_path}")

# GOOD - safe
subprocess.run(["ls", user_path], shell=False)
```

### 4. Authentication/Authorization

**Checked Patterns**:
- Hardcoded credentials
- Missing authentication on endpoints
- Broken access control
- Session management issues

**API Endpoint Check**:
```python
# Every API endpoint should have auth
@app.route("/api/sensitive")
@require_auth  # ← Required
def sensitive_endpoint():
    pass
```

## Security Report Format

```markdown
# Security Scan Report - 2025-12-19

## Summary
- **Scan Status**: ❌ FAILED (2 critical issues)
- **Files Scanned**: 234
- **Critical**: 2
- **High**: 1
- **Moderate**: 3

## CRITICAL Issues (Block Merge)

### C001: Exposed API Key
- **File**: `my-project-backend/config.py:45`
- **Type**: OpenAI API Key
- **Pattern**: `sk-proj-xxxxx...`
- **Action Required**:
  1. Remove from code
  2. Rotate key in OpenAI dashboard
  3. Use OPENAI_API_KEY environment variable

### C002: Exposed Database Credentials
- **File**: `.env.example:12` (committed to git)
- **Type**: PostgreSQL connection string
- **Action Required**:
  1. Remove from git history
  2. Rotate database password
  3. Never commit .env files

## HIGH Issues (Block Merge)

### H001: Known Vulnerability in lodash
- **Package**: lodash@4.17.15
- **CVE**: CVE-2021-23337
- **Severity**: High (Prototype Pollution)
- **Fix**: `npm install lodash@4.17.21`

## MODERATE Issues (Warn)

### M001: npm audit moderate vulnerability
- **Package**: nth-check@1.0.2 (transitive)
- **Via**: css-select → svgo
- **Fix**: Update svgo to latest

## Passed Checks

✅ No hardcoded passwords found
✅ No SQL injection patterns detected
✅ No XSS vulnerabilities in React components
✅ All API endpoints have authentication
```

## Automatic Actions

### On Critical Finding

```
CRITICAL issue found
    ↓
1. STOP all other checks
2. Generate security report
3. Notify immediately
4. DO NOT proceed to code-quality
5. Require manual remediation
```

### On High Finding

```
HIGH issue found
    ↓
1. Add to security report
2. Block merge if in pre-merge mode
3. Continue scan for other issues
4. Require fix before merge
```

### On Moderate/Low Finding

```
MODERATE/LOW issue found
    ↓
1. Add to security report
2. Log warning
3. Continue to code-quality
4. Track for future fix
```

## Integration with Workflow

### In codebase-quality:full-audit

```
codebase-quality:security  ← YOU ARE HERE
    ↓
1. Scan for secrets
2. Audit dependencies
3. Check injection patterns
4. Verify auth on endpoints
    ↓
If CRITICAL/HIGH: STOP, report, require fix
If MODERATE/LOW: Continue with warnings
    ↓
codebase-quality:code-quality
```

### In Pre-Merge Check

```
/codebase-quality pre-merge
    ↓
security scan:
- CRITICAL → Block merge, alert
- HIGH → Block merge
- MODERATE → Warn, allow merge
- LOW → Info, allow merge
```

## Best Practices

1. **Never Commit Secrets**: Use `.env` files and environment variables
2. **Rotate Compromised Keys**: Always rotate after exposure
3. **Keep Dependencies Updated**: Regular `npm audit` / `pip-audit`
4. **Parameterize Queries**: Never string-interpolate user input
5. **Sanitize Output**: Always escape user content for display

## Chaining

After security passes:

```python
# Continue to code quality
Skill("codebase-quality:code-quality")
```

If security has critical issues:

```python
# DO NOT continue
# Report and require human remediation
# Only proceed after issues resolved
```

## Emergency Response

If secrets are found in git history:

```bash
# 1. Immediately rotate the credential

# 2. Remove from git history (if not pushed)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/file' \
  --prune-empty --tag-name-filter cat -- --all

# 3. If already pushed, notify security team
# Consider repository compromise procedures
```

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-12-19
**Parent Skill**: [using-codebase-quality](../using-codebase-quality/SKILL.md)
