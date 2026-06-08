---
name: ost-render
description: Test fixture for Check 43 — body section missing.
metadata:
  instruction_budget: "55"
  framework_dependency: "mycelium"
  identifier_exposure: "YES"
---

# OST Render (fixture)

This skill intentionally omits the `## Identifier exposure` body section to exercise Check 43's missing-body failure path. Frontmatter is valid but the body audit-trail is absent.

## When NOT to use

Cosmetic content only; no Identifier exposure section present.
