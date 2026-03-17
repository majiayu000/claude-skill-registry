---
name: code-quality
description: Coding standards for new/reviewed code, UI/UX, security, accessibility.
---

# Code Quality Standards

## Coding Style
* Naming: camelCase (vars/funcs), PascalCase (classes/types)
* Format: 4-space indent; ≤80 chars
* Comments: Meaningful, current
* Security: No secrets/PII; validate inputs; least privilege
* Errors: Explicit types; structured logs

## Accessibility & UX
* Semantic roles; keyboard nav
* Responsive checks: 375, 768, 1024, 1440
* Deterministic test IDs

## Security Guardrails
* No real credentials
* Test accounts/fixtures
* Least-privilege validation
* Document threats in PRs

## References
`references/coding-style.md`
`references/security-checklist.md`
`references/accessibility-standards.md`