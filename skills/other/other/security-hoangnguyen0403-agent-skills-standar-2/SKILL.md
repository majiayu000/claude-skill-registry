---
name: PHP Security
description: PHP security standards for database access, password handling, and input validation.
metadata:
  labels: [php, security, pdo, hashing]
  triggers:
    files: ['**/*.php']
    keywords: [pdo, password_hash, htmlentities, filter_var]
---

# PHP Security

## **Priority: P0 (CRITICAL)**

## Structure

```text
src/
└── Security/
    ├── Validators/
    └── Auth/
```

## Implementation Guidelines

- **Prepared Statements**: Use PDO exclusively. Never concatenate SQL.
- **Type Binding**: Apply `bindParam()` with PDO constants.
- **Password Hashing**: Use `password_hash()` with `PASSWORD_ARGON2ID`.
- **Verify Securely**: Use `password_verify()` for all authentication.
- **XSS Escaping**: Apply `htmlentities($data, ENT_QUOTES, 'UTF-8')` to all user output.
- **Input Filtering**: Use `filter_var()` for types (email, URL, int).
- **CSRF Protection**: Require tokens for all state-changing requests.

## Anti-Patterns

- **Raw SQL**: **No Concat**: Never build queries with string concatenation.
- **Weak Hashing**: **No MD5/SHA1**: Use modern algorithms only.
- **Trusting $\_GET**: **No Raw Input**: Always validate external data.
- **Error Exposure**: **No Production Errors**: Log errors; don't display them.

## References

- [Secure Implementation Patterns](references/implementation.md)
