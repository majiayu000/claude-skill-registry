---
name: detecting-security-vulnerabilities
description: Scans code for security vulnerabilities and unsafe patterns. Use when the user asks about security, mentions OWASP, credentials, secrets, XSS, SQL injection, or wants to audit code for threats.
---

# Security Lint & Threat Detector

## When to use this skill

- User asks to scan code for security issues
- User mentions OWASP vulnerabilities
- User wants to find leaked credentials or secrets
- User asks about XSS, SQL injection, or CSRF risks
- User wants to audit code before deployment

## Workflow

- [ ] Identify files to scan (changed or full codebase)
- [ ] Run automated security scanners
- [ ] Perform pattern-based detection
- [ ] Categorize findings by severity
- [ ] Provide remediation suggestions
- [ ] Generate security report

## Instructions

### Step 1: Identify Scan Scope

For changed files:

```bash
git diff --cached --name-only --diff-filter=ACMR | grep -E '\.(js|jsx|ts|tsx|py|rb|php|java|go)$'
```

For full codebase:

```bash
find src -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \)
```

### Step 2: Run Security Scanners

**JavaScript/TypeScript — npm audit:**

```bash
npm audit --json
```

**JavaScript/TypeScript — Snyk (if available):**

```bash
npx snyk test --json
```

**ESLint security plugin:**

```bash
npx eslint --plugin security --rule 'security/*: error' <files>
```

**Semgrep (multi-language):**

```bash
npx @semgrep/semgrep --config=auto --json .
```

**Gitleaks (secrets detection):**

```bash
gitleaks detect --source . --report-format json
```

### Step 3: Pattern-Based Detection

Scan for these high-risk patterns:

#### Credential Leakage

| Pattern            | Risk     | Regex                                                                 |
| ------------------ | -------- | --------------------------------------------------------------------- |
| API keys           | Critical | `['"]?(api[_-]?key\|apikey)['"]?\s*[:=]\s*['"][a-zA-Z0-9]{16,}['"]`   |
| AWS keys           | Critical | `AKIA[0-9A-Z]{16}`                                                    |
| Private keys       | Critical | `-----BEGIN (RSA\|DSA\|EC\|OPENSSH) PRIVATE KEY-----`                 |
| Passwords          | High     | `['"]?(password\|passwd\|pwd)['"]?\s*[:=]\s*['"][^'"]{4,}['"]`        |
| Tokens             | High     | `['"]?(token\|secret\|auth)['"]?\s*[:=]\s*['"][a-zA-Z0-9_-]{20,}['"]` |
| Connection strings | High     | `(mongodb\|postgres\|mysql):\/\/[^:]+:[^@]+@`                         |

```bash
grep -rn --include="*.{ts,js,tsx,jsx,json,env}" -E "AKIA[0-9A-Z]{16}" .
grep -rn --include="*.{ts,js,tsx,jsx}" -E "(api[_-]?key|apikey)\s*[:=]\s*['\"][^'\"]{16,}['\"]" .
```

#### Unsafe Code Patterns

| Pattern                   | Risk     | Detection                  |
| ------------------------- | -------- | -------------------------- |
| `eval()`                  | Critical | Direct code execution      |
| `dangerouslySetInnerHTML` | High     | XSS vulnerability in React |
| `v-html`                  | High     | XSS vulnerability in Vue   |
| `innerHTML` assignment    | High     | DOM-based XSS              |
| `document.write`          | High     | DOM manipulation risk      |
| `new Function()`          | High     | Dynamic code execution     |
| `child_process.exec`      | High     | Command injection risk     |
| `sql` + string concat     | Critical | SQL injection              |
| `http://` URLs            | Medium   | Insecure transport         |

```bash
grep -rn --include="*.{ts,js,tsx,jsx}" -E "\beval\s*\(" .
grep -rn --include="*.tsx" "dangerouslySetInnerHTML" .
grep -rn --include="*.vue" "v-html" .
grep -rn --include="*.{ts,js}" -E "\.exec\s*\(.*\$\{" .
```

#### OWASP Top 10 Checks

| OWASP | Vulnerability             | What to look for                            |
| ----- | ------------------------- | ------------------------------------------- |
| A01   | Broken Access Control     | Missing auth checks, direct object refs     |
| A02   | Cryptographic Failures    | Weak algorithms (MD5, SHA1), hardcoded keys |
| A03   | Injection                 | SQL/NoSQL/Command injection patterns        |
| A04   | Insecure Design           | Missing rate limiting, no input validation  |
| A05   | Security Misconfiguration | CORS \*, debug modes, default creds         |
| A06   | Vulnerable Components     | Outdated dependencies                       |
| A07   | Auth Failures             | Weak password rules, session issues         |
| A08   | Data Integrity            | Unsafe deserialization, unverified updates  |
| A09   | Logging Failures          | Sensitive data in logs, missing audit       |
| A10   | SSRF                      | Unvalidated URL fetches                     |

### Step 4: Categorize Findings

**Severity levels:**

| Level    | Examples                            | Action           |
| -------- | ----------------------------------- | ---------------- |
| Critical | Exposed secrets, RCE, SQL injection | Block deployment |
| High     | XSS, CSRF, auth bypass              | Fix before merge |
| Medium   | Insecure cookies, weak crypto       | Fix in sprint    |
| Low      | Info disclosure, best practices     | Track for later  |

### Step 5: Generate Report

Format findings clearly:

````markdown
## Security Scan Report

### Critical (2)

#### 1. Hardcoded API Key

- **File**: src/api/client.ts:42
- **Pattern**: `apiKey = "sk_live_..."`
- **Risk**: Credential exposure in source control
- **Fix**: Move to environment variable

```typescript
// Before
const apiKey = "sk_live_abc123...";

// After
const apiKey = process.env.API_KEY;
```
````

#### 2. SQL Injection Risk

- **File**: src/db/users.ts:23
- **Pattern**: String concatenation in query
- **Risk**: SQL injection allows data theft
- **Fix**: Use parameterized queries

```typescript
// Before
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// After
db.query("SELECT * FROM users WHERE id = $1", [userId]);
```

### High (1)

#### 1. XSS via dangerouslySetInnerHTML

- **File**: src/components/Article.tsx:15
- **Risk**: User content rendered as HTML
- **Fix**: Sanitize with DOMPurify

```tsx
import DOMPurify from "dompurify";
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(content) }} />;
```

### Summary

| Severity | Count |
| -------- | ----- |
| Critical | 2     |
| High     | 1     |
| Medium   | 3     |
| Low      | 5     |

````

## Common Remediation Patterns

**Environment variables for secrets:**
```typescript
// Use dotenv or platform env
const secret = process.env.SECRET_KEY;
if (!secret) throw new Error('SECRET_KEY required');
````

**Parameterized queries:**

```typescript
// Prisma (safe by default)
await prisma.user.findUnique({ where: { id: userId } });

// Raw SQL with parameters
await db.query("SELECT * FROM users WHERE id = $1", [userId]);
```

**XSS prevention:**

```typescript
// React - avoid dangerouslySetInnerHTML
// If needed, sanitize first
import DOMPurify from "dompurify";
const clean = DOMPurify.sanitize(userContent);
```

**CSRF protection:**

```typescript
// Use CSRF tokens in forms
<input type="hidden" name="_csrf" value={csrfToken} />

// Validate on server
if (req.body._csrf !== req.session.csrfToken) {
  throw new Error('CSRF validation failed');
}
```

**Secure headers:**

```typescript
// Next.js next.config.js
const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "X-XSS-Protection", value: "1; mode=block" },
  {
    key: "Strict-Transport-Security",
    value: "max-age=31536000; includeSubDomains",
  },
];
```

## Validation

Before completing:

- [ ] All critical issues addressed
- [ ] High severity issues have remediation plan
- [ ] No secrets in committed code
- [ ] Dependencies updated for known CVEs
- [ ] Security headers configured

## Error Handling

- **Scanner not installed**: Run `npm install -g <tool>` or use npx.
- **Too many results**: Filter by severity or scope to changed files.
- **False positives**: Review context before reporting; exclude test fixtures.
- **Unsure about severity**: Default to higher severity; security errs on caution.

## Resources

- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Semgrep Rules](https://semgrep.dev/explore)
- [Snyk Vulnerability DB](https://snyk.io/vuln/)
