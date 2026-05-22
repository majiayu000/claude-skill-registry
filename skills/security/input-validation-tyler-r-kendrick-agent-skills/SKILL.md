---
name: input-validation
description: |
    Use when implementing input validation and output encoding to prevent injection attacks. Covers validation strategies, context-specific output encoding, parameterized queries, and defense-in-depth approaches across all languages and frameworks.
    USE FOR: input validation, output encoding, XSS prevention, SQL injection prevention, command injection prevention, parameterized queries, sanitization, allowlisting, content security policy
    DO NOT USE FOR: authentication validation (use authentication), API rate limiting (use api-security), cryptographic validation (use cryptography)
license: MIT
metadata:
  displayName: "Input Validation & Output Encoding"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "OWASP Input Validation Cheat Sheet"
    url: "https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html"
  - title: "OWASP Cross-Site Scripting Prevention Cheat Sheet"
    url: "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html"
  - title: "OWASP SQL Injection Prevention Cheat Sheet"
    url: "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"
---

# Input Validation & Output Encoding

## Overview

Input validation and output encoding form a **defense-in-depth** strategy against injection attacks. Neither is sufficient on its own:

- **Input validation** ensures that data conforms to expected formats before processing. It reduces the attack surface but cannot account for every output context.
- **Output encoding** ensures that data is rendered safely in its target context (HTML, SQL, JavaScript, etc.). It neutralizes malicious content but should not be the only line of defense.

Always apply both: validate all input as early as possible, and encode all output as late as possible — immediately before it is rendered or interpreted in its target context.

## Input Validation Strategy

### Allowlist vs. Denylist

- **Always prefer allowlist (positive) validation.** Define what is permitted and reject everything else. Allowlists are explicit, predictable, and far harder to bypass.
- **Denylist (negative) validation is fragile.** Blocking known-bad patterns always misses novel attack vectors, encoding tricks, and edge cases.

### Principles

1. **Validate as early as possible** — at the API boundary, form handler, or deserialization layer before data enters business logic.
2. **Normalize before validating** — decode, trim, and canonicalize input before applying validation rules. Attackers exploit double-encoding and Unicode normalization differences to bypass checks.
3. **Use typed validation** — parse inputs into their expected types (integers, dates, enums) rather than treating everything as strings. Type coercion eliminates entire classes of injection.
4. **Validate on the server side** — client-side validation improves UX but provides zero security. All validation must be enforced server-side.

## Validation by Data Type

| Data Type     | Validation Rule                                           | Example                                                  |
|---------------|-----------------------------------------------------------|----------------------------------------------------------|
| Strings       | Max length, allowed character set, regex pattern          | Username: `^[a-zA-Z0-9_]{3,30}$`                        |
| Numbers       | Type check, min/max range, integer vs. float              | Age: integer, 0-150                                      |
| Emails        | RFC 5322 format validation + DNS MX record check          | `user@example.com` — verify domain has MX records        |
| URLs          | Scheme allowlist (https only), reject internal/private IPs | Allow `https://` only; block `file://`, `javascript:`, RFC 1918 ranges |
| File uploads  | MIME type check (magic bytes, not extension), max size, rename to random, virus scan | Accept `image/png` up to 5MB; rename to UUID; scan with ClamAV |
| Dates         | Strict format parsing (ISO 8601), valid range check       | `2024-01-15` — reject `0000-00-00`, far-future dates    |

## Output Encoding

Output encoding must be **context-specific**. The correct encoding depends entirely on where the data is being rendered.

| Context            | Encoding Method                  | Example                                                    |
|--------------------|----------------------------------|------------------------------------------------------------|
| HTML body          | HTML entity encode               | `<script>` becomes `&lt;script&gt;`                        |
| HTML attributes    | HTML attribute encode            | `" onclick="alert(1)` becomes `&quot; onclick=&quot;alert(1)` |
| JavaScript         | JavaScript encode / `JSON.stringify()` | Embed user data only via `JSON.stringify()` into a variable assignment |
| URL parameters     | URL encode (percent-encoding)    | `param=hello world` becomes `param=hello%20world`          |
| CSS                | CSS hex encode                   | `</style>` becomes `\003c\002fstyle\003e`                  |
| SQL                | **Parameterized queries ONLY**   | Never encode manually for SQL — always use prepared statements |

> **Critical:** HTML entity encoding does NOT protect against XSS in JavaScript or URL contexts. Each context requires its own encoding function.

## Injection Prevention

| Attack              | Root Cause                         | Prevention                                                       |
|---------------------|------------------------------------|------------------------------------------------------------------|
| SQL injection       | String concatenation in SQL queries | Parameterized queries / prepared statements                      |
| XSS (Cross-Site Scripting) | Unencoded user data in HTML output | Context-specific output encoding; Content Security Policy (CSP) |
| Command injection   | String concatenation in shell commands | Avoid shell execution; use language APIs with argument arrays   |
| Path traversal      | Unvalidated file paths from user input | Canonicalize paths; validate against an allowed base directory  |
| LDAP injection      | Unescaped user input in LDAP queries | LDAP-specific escaping functions; parameterized LDAP queries    |
| XML injection       | Inline construction of XML from user data | Use XML serialization libraries; disable external entities (XXE) |

## Framework-Specific Helpers

Modern frameworks provide built-in protections. Understand what your framework does automatically and where gaps remain.

| Framework   | Built-in Protection                                                        |
|-------------|----------------------------------------------------------------------------|
| React       | JSX auto-escapes embedded expressions by default; beware `dangerouslySetInnerHTML` |
| Angular     | Template expressions are auto-sanitized; beware `bypassSecurityTrust*` methods |
| ASP.NET     | Razor views auto-encode output by default; beware `Html.Raw()`            |
| Django      | Template engine auto-escapes variables by default; beware `|safe` filter and `mark_safe()` |
| Spring      | Thymeleaf auto-encodes with `th:text`; beware `th:utext` (unescaped)     |

> **Warning:** Every framework that auto-encodes also provides an escape hatch for raw output. Audit all uses of these escape hatches during code review.

## Parameterized Queries

Parameterized queries (prepared statements) are the **only reliable defense** against SQL injection. Never construct SQL by concatenating user input.

### SQL — Prepared Statement

```sql
-- Correct: parameterized query
SELECT * FROM users WHERE email = @Email AND status = @Status;

-- WRONG: string concatenation
SELECT * FROM users WHERE email = '" + email + "' AND status = '" + status + "';
```

### ORM — Entity Framework (C#)

```csharp
// Correct: LINQ query — parameterized automatically
var user = context.Users
    .Where(u => u.Email == email && u.Status == status)
    .FirstOrDefault();
```

### ORM — SQLAlchemy (Python)

```python
# Correct: ORM query — parameterized automatically
user = session.query(User).filter(
    User.email == email,
    User.status == status
).first()
```

### Note on Stored Procedures

Stored procedures are **not inherently safe** from SQL injection. If a stored procedure uses dynamic SQL internally (e.g., `EXEC` or `sp_executesql` with concatenation), it is still vulnerable. Always use parameterized inputs within stored procedures as well.

## Best Practices

- **Validate all input on the server side** — never rely on client-side validation for security.
- **Use allowlist validation** — define what is permitted and reject everything else; denylist approaches are inherently incomplete.
- **Normalize input before validation** — canonicalize Unicode, decode URL encoding, and trim whitespace before applying validation rules.
- **Encode output for its specific context** — HTML, JavaScript, URL, CSS, and SQL each require different encoding; there is no universal encoder.
- **Use parameterized queries for all database access** — never concatenate user input into SQL, regardless of prior validation.
- **Avoid shell execution with user input** — use language-native APIs with argument arrays instead of constructing shell command strings.
- **Deploy Content Security Policy (CSP) headers** — CSP provides an additional layer of defense against XSS even when encoding is missed.
- **Audit framework escape hatches** — review all uses of `dangerouslySetInnerHTML`, `Html.Raw()`, `|safe`, `th:utext`, and similar raw-output functions during code review.
