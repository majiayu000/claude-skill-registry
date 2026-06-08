---
name: ost-render
description: Test fixture for Check 43 — frontmatter missing identifier_exposure field.
metadata:
  instruction_budget: "55"
  framework_dependency: "mycelium"
---

# OST Render (fixture)

This skill intentionally omits `identifier_exposure` from its metadata frontmatter to exercise Check 43's missing-frontmatter failure path.

## Identifier exposure

Body section is present but frontmatter is missing.
