---
name: secure-coding
description: Implementing OWASP Proactive Controls (Input Validation, Output Encoding, AuthZ/AuthN).
role: ops-security, eng-backend
triggers:
  - secure code
  - input validation
  - output encoding
  - owasp
  - prevent xss
  - prevent sql injection
---

# secure-coding Skill

This skill guides the implementation of security controls *during* development (Shift Left).

## 1. Input Validation (Defense)
> "Never trust input."

- **Syntactic Validation**: Is it an email? Is it a number? (Use Zod/Pydantic).
- **Semantic Validation**: Is `start_date` before `end_date`? Is `transfer_amount` > 0?
- **Allow-list**: Only accept known bad characters (e.g., `[a-zA-Z0-9]`). Block everything else.

## 2. Output Encoding (Defense)
> "Context matters."

- **HTML Context**: Escape `<` -> `&lt;`. (Prevent XSS).
- **SQL Context**: Use Parameterized Queries. (Prevent SQLi).
- **JSON Context**: Ensure valid JSON structure.

## 3. Authentication & Authorization
- **NIST Guidelines**:
  - Passwords: Min 12 chars, no complexity rules, check against pwned passwords.
  - MFA: Required for admin/privileged actions.
  - Sessions: Absolute timeout (e.g., 12 hours) + Idle timeout (e.g., 30 mins).
- **Authorization**:
  - **Broken**: `if (user.isAdmin)` (Client-side check).
  - **Fixed**: `if (ctx.user.hasPermission('delete:user'))` (Server-side check).

## 4. Cryptography
- **At Rest**: Use AES-256-GCM (Authenticated Encryption).
- **In Transit**: TLS 1.3 only.
- **Hashing**: Argon2id or bcrypt (work factor > 12).
- **Secrets**: Never hardcode. Use `process.env`.
