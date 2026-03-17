---
name: 124-java-secure-coding
description: Use when you need to apply Java secure coding best practices — including validating untrusted inputs, defending against injection attacks with parameterized queries, minimizing attack surface via least privilege, applying strong cryptographic algorithms, handling exceptions securely without exposing sensitive data, managing secrets at runtime, avoiding unsafe deserialization, and encoding output to prevent XSS. Part of the skills-for-java project
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Java Secure coding guidelines

Identify and apply Java secure coding practices to reduce vulnerabilities, protect sensitive data, and harden application behaviour against common attack vectors.

**Core areas:** Input validation with type, length, format, and range checks; SQL/OS/LDAP injection defence via `PreparedStatement` and parameterized APIs; attack surface minimisation through least-privilege permissions and removal of unused features; strong cryptographic algorithms for hashing (passwords with BCrypt/Argon2), encryption (AES-GCM), and digital signatures while avoiding deprecated ciphers (MD5, SHA-1, DES); secure exception handling that logs diagnostic details internally while exposing only generic messages to clients; secrets management by loading credentials from environment variables or secret managers — never hardcoded; safe deserialization with strict allow-lists and preference for explicit DTOs over native Java serialization; output encoding to prevent XSS in rendered content.

**Prerequisites:** Run `./mvnw compile` before applying any changes. If compilation fails, **stop immediately** — do not proceed until the project is in a valid state.

**Multi-step scope:** Step 1 validates the project compiles. Step 2 categorizes security issues by severity (CRITICAL, HIGH, MEDIUM, LOW) and area (input validation, injection, cryptography, secrets, serialization, XSS, exception handling). Step 3 adds comprehensive input validation — type, length, format, and range — to all entry points handling untrusted data. Step 4 replaces string-concatenated queries with `PreparedStatement` or ORM parameterized equivalents to eliminate injection vectors. Step 5 audits permissions and exposed surfaces to enforce least-privilege and remove unused endpoints, libraries, and accounts. Step 6 replaces weak or deprecated cryptographic algorithms with current standards (AES-GCM, BCrypt/Argon2, SHA-256+). Step 7 sanitizes exception messages and error responses so no stack traces or internal details reach clients; aligns logging to record full diagnostics internally. Step 8 removes hardcoded secrets and replaces them with runtime secret sources (env vars, Vault, cloud secret managers). Step 9 removes or replaces unsafe Java native deserialization with JSON/XML DTO binding; adds type allow-lists where deserialization is unavoidable. Step 10 adds output encoding at all render points to prevent XSS. Step 11 runs `./mvnw clean verify` to confirm all tests pass after changes.

**Before applying changes:** Read the reference for detailed good/bad examples, constraints, and safeguards for each secure coding pattern.

## Reference

For detailed guidance, examples, and constraints, see [references/124-java-secure-coding.md](references/124-java-secure-coding.md).
