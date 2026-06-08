---
name: ost-render
description: Test fixture for Check 43 — invalid identifier_exposure value.
metadata:
  instruction_budget: "55"
  framework_dependency: "mycelium"
  identifier_exposure: "BOGUS"
---

# OST Render (fixture)

This skill intentionally uses a non-canonical `identifier_exposure` value to exercise Check 43's invalid-value failure path.

## Identifier exposure

Body section is present but the frontmatter value is not YES/NONE/MIXED.
