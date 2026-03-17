---
name: task-create
license: MIT
description: >
  Create a new task directory with 00_TASK.md from template.
  Sets initial epistemic_state to candidate and lifecycle_state to inactive.
  Computes created_at via deterministic time script.
metadata:
  author: Jordan Godau
  version: 0.1.0
  references:
    - 00_INSTRUCTIONS.md
    - 01_INTENT.md
    - 02_PROCEDURE.md
    - 03_OUTPUTS.md
  scripts:
    - create.py
  keywords:
    - task
    - create
    - new
    - initialize
    - init
    - start
    - begin
---
