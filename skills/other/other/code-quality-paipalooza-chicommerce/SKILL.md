---
name: code-quality
description: Coding style standards, security guidelines, and accessibility requirements. Use when (1) Writing new code, (2) Reviewing code for style/security, (3) Implementing UI/UX features, (4) Addressing security concerns, (5) Ensuring accessibility compliance. Covers naming conventions, formatting, security best practices (no secrets/PII), accessibility standards (semantic HTML, keyboard nav), and responsive design.
---

# Code Quality Standards

## Coding Style

* **Naming:** camelCase for vars/functions; PascalCase for classes/types
* **Formatting:** 4-space indentation; target ≤80 chars (wrap thoughtfully)
* **Comments:** Meaningful, current; delete stale comments
* **Security:** Never log secrets/PII; validate inputs; least privilege by default
* **Errors/Logs:** Explicit error types; structured logs by level; actionable messages

## Accessibility & UX Quality

* Favor semantic roles/labels; keyboard nav and focus order must work
* Include responsive checks at **375, 768, 1024, 1440** with notes/screenshots
* Use deterministic test IDs; avoid brittle CSS/XPath

## Security & Compliance Guardrails

* No real credentials in code, tests, or screenshots
* Use test accounts/fixtures; redact secrets
* Follow least-privilege and input validation
* Document threat considerations in PR when relevant

## Reference Files

See `references/coding-style.md` for detailed style guide, formatting rules, comment standards.

See `references/security-checklist.md` for security validation checklist, threat modeling, PII handling.

See `references/accessibility-standards.md` for WCAG compliance, semantic HTML patterns, keyboard nav testing.
