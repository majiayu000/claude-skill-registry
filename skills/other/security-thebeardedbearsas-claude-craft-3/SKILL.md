---
name: security
description: Security best practices, OWASP Top 10, and secure coding guidelines
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebSearch
model: opus
triggers:
  files:
    - "**/auth/**"
    - "**/security/**"
    - "**/*Auth*"
    - "**/*Security*"
    - "**/.env*"
  keywords:
    - security
    - authentication
    - authorization
    - OWASP
    - injection
    - XSS
    - CSRF
    - encryption
    - password
    - token
    - JWT
    - OAuth
---

# Sécurité

This skill provides guidelines and best practices.

See ../../rules/11-security.md for detailed documentation.
