---
name: authentication-best-practices
description: Use established authentication libraries rather than implementing from scratch Use when implementing security best practices. Security category skill.
metadata:
  category: Security
  priority: high
  is-built-in: true
  session-guardian-id: builtin_auth_best_practices
---

# Authentication Best Practices

Use established authentication libraries rather than implementing from scratch. Hash passwords with bcrypt, Argon2, or scrypt with appropriate cost factors. Implement rate limiting on login endpoints. Use secure session management with proper cookie flags (HttpOnly, Secure, SameSite). Support MFA for sensitive operations. Log authentication events for security monitoring.