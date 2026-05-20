---
name: security-review
description: Full security audit using OWASP Top 10. Reviews code for vulnerabilities, secrets exposure, injection risks, and insecure patterns. Invokes security-reviewer agent. Run before every release and when handling user input or auth code.
allowed-tools: Read, Grep, Glob, Bash
---

# Security Review

Invoke the **security-reviewer** agent to audit for vulnerabilities.

## When to Run

- Before any release
- When adding new tools that execute shell commands
- When changing authentication/OAuth flows
- When adding new file read/write operations
- When processing user-provided input
- After adding new dependencies

## Quick Audit Commands

```bash
# Dependency vulnerabilities
pnpm audit 2>&1

# Hardcoded secrets scan
grep -rn "sk-ant\|sk-\|apiKey.*=.*['\"]" src/ --include="*.ts" | grep -v "test\|mock\|example\|\.d\.ts\|schema"

# Shell injection risks
grep -rn "execa\|exec\|spawn" src/ --include="*.ts" | grep -v "test\|\.d\.ts" | head -20

# console.log with potential data exposure
grep -rn "console\.log.*key\|console\.log.*token\|console\.log.*secret" src/ --include="*.ts"

# Path operations (traversal risk)
grep -rn "readFile\|writeFile\|unlink\|readdir" src/ --include="*.ts" | grep -v "test" | head -20

# eval usage (never acceptable)
grep -rn "eval(\|new Function(" src/ --include="*.ts"
```

## Review Checklist

### Critical (fix immediately)
- [ ] No hardcoded API keys, tokens, passwords
- [ ] No `eval()` or `new Function()` with dynamic content
- [ ] execa uses array args (not string interpolation)
- [ ] File paths validated against `projectRoot` before access
- [ ] No secrets in log output

### High (fix before merge)
- [ ] All tool inputs validated with Zod before execution
- [ ] No unvalidated LLM output executed as code
- [ ] OAuth state parameter validated
- [ ] Error messages don't expose internal paths

### Medium (fix in this PR)
- [ ] `pnpm audit` shows no critical/high vulnerabilities
- [ ] No sensitive data in git history (check recent commits)
- [ ] Appropriate rate limiting for expensive operations

### Low (fix in follow-up)
- [ ] Security-relevant events logged
- [ ] Error messages appropriately generic for users

## Output

```markdown
## Security Review: [Component/Feature]

**Risk Level**: CRITICAL / HIGH / MEDIUM / LOW / CLEAN

### 🔴 CRITICAL
- [finding] — `src/path/file.ts:L42`
  Risk: [what could happen]
  Fix: [specific remediation]

### ✅ Passed Checks
- No hardcoded secrets found
- No eval/new Function usage
- execa calls use array arguments
- Dependencies: 0 critical vulnerabilities

### Recommendation
[READY TO RELEASE / FIX REQUIRED before release]
```

## Usage

```
/security-review                    # full audit
/security-review src/auth/          # audit specific module
/security-review before-release     # full pre-release audit
```
