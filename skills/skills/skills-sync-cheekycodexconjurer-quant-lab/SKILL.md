---
name: skills_sync
description: Align Codex-native skills with documented skills safely.
metadata:
  short-description: Skills sync
---

## Purpose
Ensure `.codex/skills/` matches `.agent-docs/skills/`.

## Steps
1. Check for missing skills in either location.
2. Update `index.md` to list new skills.
3. Add missing entries using merge protocol.
4. Validate frontmatter and folder naming.
5. Update `.agent-docs/memory/SKILLS_STATUS.md`.

## Guardrails
- Avoid overwriting existing skill content.
