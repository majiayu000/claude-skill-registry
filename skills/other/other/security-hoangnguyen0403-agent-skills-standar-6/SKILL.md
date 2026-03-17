---
name: Security
description: Security best practices for Angular (XSS, CSP, Route Guards).
metadata:
  labels: [angular, security, xss, csp]
  triggers:
    files: ['**/*.ts', '**/*.html']
    keywords: [DomSanitizer, innerHTML, bypassSecurityTrust, CSP]
---

# Security

## **Priority: P0 (CRITICAL)**

## Principles

- **XSS Prevention**: Angular sanitizes by default. Do NOT use `innerHTML` unless absolutely necessary.
- **Bypass Security**: Avoid `DomSanitizer.bypassSecurityTrust...` unless the content source is trusted.
- **Route Guards**: Protect all sensitive routes with `CanActivateFn`.

## Guidelines

- **CSP**: Configure Content Security Policy headers on the server.
- **HTTP**: Use Interceptors to attach secure tokens (HttpOnly cookies preferred over LocalStorage tokens).
- **Secrets**: NEVER store secrets (API keys) in Angular code.

## References

- [Security Best Practices](references/security-best-practices.md)

## Related Topics

common/security-standards | components
