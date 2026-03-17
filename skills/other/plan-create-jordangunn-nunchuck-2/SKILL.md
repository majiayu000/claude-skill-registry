---
name: plan-create
license: MIT
description: >
  Compile `.plan/active.yaml` into a schema-validated active plan directory under `.plan/active/`.
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
    - assets/plan-root-schema.json
    - assets/plan-subplan-schema.json
    - assets/plan-task-schema.json
    - assets/plan-discuss-artifact-schema.json
  keywords:
    - plan
    - create
    - scaffold
    - initialize
    - compile
---

# INSTRUCTIONS

1. Refer to `metadata.references`.
