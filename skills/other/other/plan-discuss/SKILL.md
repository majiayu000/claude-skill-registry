---
name: plan-discuss
license: MIT
description: >
  Shape and stabilize plan intent idempotently into `.plan/active.yaml`
  until `plan-create` is invoked.
metadata:
  author: Jordan Godau
  version: 0.1.0
  references:
    - 00_ROUTER.md
    - 01_SUMMARY.md
    - 02_TRIGGERS.md
    - 03_ALWAYS.md
    - 04_NEVER.md
    - 05_PROCEDURE.md
    - 06_FAILURES.md
  scripts:
    - scripts/skill.sh
    - scripts/skill.ps1
  assets:
    - assets/plan-discuss-artifact-schema.json
  keywords:
    - plan
    - discuss
    - clarify
    - intent
    - idempotent
---

# INSTRUCTIONS

1. Refer to `metadata.references`.
