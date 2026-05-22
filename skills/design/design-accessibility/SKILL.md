---
name: design-accessibility
description: "WCAG and ARIA best practices for web UIs. Extends platform-frontend with accessibility-specific rules. Use when building any user-facing interface."
---

# Principles

- Use semantic HTML first — ARIA is a last resort, not a first tool
- Proper heading hierarchy — one h1 per page, never skip levels
- Alt text on all meaningful images
- Maintain 4.5:1 minimum color contrast ratio
- Use `<button>` for actions, `<a>` for navigation — never a styled `<div>`

# Rules

See `rules/` for detailed patterns.
