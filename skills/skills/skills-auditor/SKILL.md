---
name: skills_auditor
description: Detect incorrectly installed skills and report issues.
metadata:
  short-description: Skills audit
---

## Purpose
Find broken or missing Codex-native skills.

## Steps
1. Validate `.codex/skills/*/SKILL.md` frontmatter and folder names.
2. Compare `.codex/skills/` with `.agent-docs/skills/`.
3. Record findings in `.agent-docs/memory/SKILLS_STATUS.md`.

## Guardrails
- Propose fixes via merge protocol, do not overwrite blindly.
