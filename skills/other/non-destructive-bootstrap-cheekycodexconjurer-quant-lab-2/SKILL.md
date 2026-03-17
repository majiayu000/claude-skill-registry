---
name: non_destructive_bootstrap
description: Install agent docs without overwriting or deleting existing content.
metadata:
  short-description: Idempotent bootstrap
---

## Purpose
Integrate templates safely into an existing repository.

## Steps
1. Follow the merge protocol for all changes.
2. Add missing files without renaming existing ones.
3. Update references in place using markers only.
4. Log changes in `ACTION_LOG.md` and `ACTION_LOG.jsonl`.

## Guardrails
- Never delete or rename by default.
- Use `.agent-docs/compat/` for conflicts.
