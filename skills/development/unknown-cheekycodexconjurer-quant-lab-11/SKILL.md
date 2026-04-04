---
name: size_guard
description: Enforce line budgets and rotate or split large context files.
metadata:
  short-description: Line budget guard
---

## Purpose
Keep context-heavy files within line limits for fast loading.

## Steps
1. Read `.agent-docs/memory/LINE_BUDGETS.yaml`.
2. Rotate or split files that exceed budgets.
3. Update indexes to reference new parts.
4. Record the action in the Action Log.

## Guardrails
- Preserve history by archiving before splitting.
