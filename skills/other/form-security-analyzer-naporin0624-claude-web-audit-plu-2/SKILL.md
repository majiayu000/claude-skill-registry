---
name: form-security-analyzer
description: Static security analysis of HTML forms without sending any requests. Checks for CSRF tokens, insecure actions, missing validation, hidden field issues, and common security misconfigurations. Safe to run - no payloads sent. Use when user asks to "analyze form security", "check form for vulnerabilities", "static security check".
---

# Form Security Analyzer

Static analysis of HTML forms to find security issues. No requests sent - just code inspection. Safe and fast.

## Your Bounty Hunter Perspective

When analyzing a form, think:
- "Where's the money hiding in this form?"
- "What did the developer forget?"
- "How can I abuse this?"

## Quick Start

### Installation

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/form-security-analyzer
npm install
npm run build
```

### Run Analysis

```bash
# Analyze a single file
npx tsx ${CLAUDE_PLUGIN_ROOT}/skills/form-security-analyzer/src/index.ts path/to/file.html

# JSON output
npx tsx ${CLAUDE_PLUGIN_ROOT}/skills/form-security-analyzer/src/index.ts path/to/file.html --json
```

### Using Built Version

```bash
node ${CLAUDE_PLUGIN_ROOT}/skills/form-security-analyzer/dist/index.js path/to/file.html
```

## What It Checks

### Critical Issues ($$$)

| Check | What It Finds | Bounty Potential |
|-------|--------------|------------------|
| Missing CSRF Token | Forms without protection | $1K - $10K |
| HTTP Action URL | Credentials sent insecurely | $500 - $5K |
| Hidden sensitive data | API keys, tokens in hidden fields | $500 - $25K |

### High Issues

| Check | What It Finds | Bounty Potential |
|-------|--------------|------------------|
| State-changing GET | Destructive actions via link | $1K - $5K |
| Predictable IDs | Sequential/guessable object refs | $2K - $50K |

### Medium Issues

| Check | What It Finds | Bounty Potential |
|-------|--------------|------------------|
| No email validation | Missing type="email" | $500 - $2K |
| Autocomplete on passwords | Credential caching enabled | $100 - $500 |
| Inline JS handlers | XSS surface area | $500 - $2K |

### Low Issues

| Check | What It Finds | Bounty Potential |
|-------|--------------|------------------|
| Missing maxlength | Potential buffer/storage issues | $100 - $500 |

## Security Checks Detail

### 1. CSRF Protection
```html
<!-- BAD: No CSRF token -->
<form action="/transfer" method="POST">
  <input name="amount" />
  <button>Send</button>
</form>

<!-- GOOD: Has CSRF token -->
<form action="/transfer" method="POST">
  <input type="hidden" name="_csrf" value="abc123" />
  <input name="amount" />
  <button>Send</button>
</form>
```

### 2. Secure Action URL
```html
<!-- BAD: HTTP (credentials exposed) -->
<form action="http://example.com/login" method="POST">

<!-- GOOD: HTTPS -->
<form action="https://example.com/login" method="POST">
```

### 3. Input Validation
```html
<!-- BAD: No validation -->
<input name="email" />

<!-- GOOD: Proper validation -->
<input name="email" type="email" required pattern="[^@]+@[^@]+\.[^@]+" />
```

### 4. Password Security
```html
<!-- BAD: Autocomplete allows caching -->
<input type="password" name="password" />

<!-- GOOD: Prevent caching -->
<input type="password" name="password" autocomplete="new-password" />
```

### 5. Hidden Field Analysis
```html
<!-- BAD: Sensitive data exposed -->
<input type="hidden" name="user_id" value="12345" />
<input type="hidden" name="api_key" value="sk_live_xxx" />
<input type="hidden" name="admin" value="false" />

<!-- These are IDOR and privilege escalation opportunities! -->
```

### 6. Dangerous Patterns
```html
<!-- BAD: Inline handlers (XSS surface) -->
<form onsubmit="return validate()">

<!-- BAD: State-changing GET -->
<form action="/delete" method="GET">
```

## Output Format

```markdown
# Form Security Analysis: login.html

## Summary
| Severity | Count |
|----------|-------|
| Critical | 2 |
| High | 3 |
| Medium | 1 |
| Low | 1 |
| **Total** | **7** |

## Critical Issues [CRITICAL]

### 1. Missing CSRF Token
**Form**: #login-form
**Type**: missing-csrf
**Bounty Estimate**: $1,000 - $10,000
**OWASP**: A01 | **CWE**: CWE-352

No hidden CSRF token field found. Vulnerable to cross-site request forgery.

---

## Hunting Tips

Based on this analysis:
1. **Test CSRF**: Submit form #login-form from a different origin
2. **Test IDOR**: Change the hidden ID to access other users' data
3. **Run dynamic tests**: Use playwright-security-runner for actual exploitation
4. **Check CVEs**: Search for vulnerabilities in any detected frameworks
```

## Integration with Other Skills

After static analysis, use:
- `attack-methods-lookup` - Get attack payloads for found issues
- `cve-search` - Check if used libraries have known CVEs
- `playwright-security-runner` - Dynamic testing (with confirmation)

## Limitations

This is **static analysis only**:
- Cannot detect server-side issues
- Cannot verify if CSRF tokens are actually validated
- Cannot test actual exploitation

Use this as reconnaissance, then proceed to dynamic testing.

## Safety

This skill is 100% safe:
- Only reads HTML files
- No requests sent
- No payloads executed
- No data modified

Run freely without concerns.
