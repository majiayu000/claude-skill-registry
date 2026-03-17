---
name: plan-exec
license: MIT
description: >
  Execute tasks in the active plan under `.plan/active/`. Writes concrete Output
  and Handoff for each task and archives the plan once terminal.
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
    - 07_INSTRUCTIONS.md
    - 08_PROCEDURE.md
    - 09_PROCEDURE.md
  scripts:
    - scripts/skill.sh
    - scripts/skill.ps1
  assets:
    - assets/plan-root-schema.json
    - assets/plan-subplan-schema.json
    - assets/plan-task-schema.json
    - assets/plan-archive-receipt-schema.json
  keywords:
    - plan
    - execute
    - implement
    - work
    - task
---

# INSTRUCTIONS

1. Refer to `metadata.references`.
