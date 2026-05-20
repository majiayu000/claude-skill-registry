---
name: security
description: Security guidelines and OWASP Top 10. Use when reviewing security, implementing authentication or authorization, hardening code, or discussing vulnerabilities.
triggers:
  files: ["**/auth/**", "**/identity/**", "**/security/**", "**/middleware/**", "*.security.*", "*Auth*.*", "*Security*.*"]
  keywords: ["security", "auth", "authentication", "authorization", "OWASP", "injection", "XSS", "CSRF", "JWT", "password", "vulnerability", "encryption", "hashing", "bcrypt", "token", "session", "RBAC", "permissions", "CORS", "HSTS", "CSP", "SQL injection", "SSRF", "rate limit"]
auto_suggest: true
---

# Security

This skill provides universal security guidelines and OWASP Top 10 best practices applicable to any technology stack.

See @REFERENCE.md for detailed documentation.

## Quick Reference

- **Validation**: Always server-side, never trust client input
- **Queries**: Parameterized only (no SQL concatenation)
- **Passwords**: Hash with bcrypt/Argon2 (never MD5/SHA1)
- **Secrets**: Environment variables or vault (never in code)
- **Headers**: CSP, X-Frame-Options, HSTS, nosniff
