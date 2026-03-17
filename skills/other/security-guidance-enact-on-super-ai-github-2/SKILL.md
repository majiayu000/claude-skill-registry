---
name: security-guidance
description: Security reminder hook that warns about potential security issues when editing files, including command injection, XSS, and unsafe code patterns
license: MIT
compatibility: opencode
---

# Security Guidance Skill

Security best practices and vulnerability detection for code development.

## What I Check

### Command Injection
- OS command injection from user input
- Unsafe use of `exec`, `spawn`, `subprocess`
- Shell metacharacters in interpolated strings

### Cross-Site Scripting (XSS)
- Unescaped user input in HTML/JSX
- `dangerouslySetInnerHTML` usage
- User-controlled URLs in anchors/iframes

### Authentication & Authorization
- Missing authentication checks
- Hardcoded credentials or API keys
- Session management issues
- Missing CSRF protection

### Data Validation
- Missing input validation and sanitization
- Type coercion vulnerabilities
- Array/object confusion attacks

### Cryptography
- Weak encryption algorithms
- Hardcoded encryption keys
- Missing signature verification
- Insecure random number generation

### Dependency Security
- Outdated packages with known vulnerabilities
- Unused dependencies
- Unsafe source configurations

## Security Checklist

### Before Writing Code
- Validate and sanitize all user input
- Use parameterized queries for database access
- Implement proper authentication and authorization
- Never trust client-side validation

### While Writing Code
- Use prepared statements for SQL
- Escape user-generated content
- Implement principle of least privilege
- Log security-relevant events

### After Writing Code
- Review for hardcoded secrets
- Check for exposed sensitive data
- Verify error handling doesn't leak information
- Test with malicious input

## Common Vulnerabilities

| Vulnerability | Description | Prevention |
|---------------|-------------|------------|
| SQL Injection | Malicious SQL via user input | Use prepared statements |
| XSS | Script injection via user content | Escape/encode output |
| CSRF | Unauthorized actions on behalf of users | Use CSRF tokens |
| Path Traversal | Access to files outside intended directory | Validate and sanitize paths |
| SSRF | Server makes requests to attacker-controlled URLs | Allowlist and validate URLs |

## When to Use Me

Invoke this skill whenever:
- Handling user input or data
- Implementing authentication/authorization
- Working with external systems/APIs
- Processing files or uploads
- Implementing cryptographic features

---

*Part of SuperAI GitHub - Centralized OpenCode Configuration*
