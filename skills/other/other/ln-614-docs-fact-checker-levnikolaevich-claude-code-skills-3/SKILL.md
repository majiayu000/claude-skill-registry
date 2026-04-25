---
name: ln-614-docs-fact-checker
description: "Verifies claims in .md files (paths, versions, counts, configs, endpoints) against codebase, cross-checks contradictions. Use when auditing docs accuracy."
license: MIT
---

> **Paths:** This is a Codex-native adapter. Load canonical files relative to the skills repo root.

# ln-614-docs-fact-checker Codex Adapter

## Mandatory Read

**MANDATORY READ:** Load `skills-catalog/ln-614-docs-fact-checker/SKILL.md`.

## Workflow

1. Load the canonical skill file listed above.
2. Follow the canonical skill exactly.
3. Treat this adapter as discovery metadata only; do not duplicate or override canonical instructions.

## Definition of Done

- [ ] Canonical skill loaded
- [ ] Canonical workflow followed
- [ ] Result reported per canonical skill contract

**Version:** 1.0.0
**Last Updated:** 2026-04-24
