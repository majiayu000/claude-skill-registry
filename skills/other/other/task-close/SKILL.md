---
name: task-close
license: MIT
description: >
  Close a task by setting state to closed, recording close_reason and closed_at.
  Recomputes intent hash and clears `.tasks/.active` if it pointed to this task.
metadata:
  author: Jordan Godau
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
  keywords:
    - task
    - close
    - complete
    - finish
    - done
    - abandon
---

# INSTRUCTIONS

1. Refer to `metadata.references`.
