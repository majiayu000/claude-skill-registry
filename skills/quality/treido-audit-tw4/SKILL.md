---
name: treido-audit-tw4
description: "Read-only Tailwind v4 auditor for Treido (tokens + forbidden patterns). Returns structured payload for ORCH merge. Trigger: TW4-AUDIT"
---

# Treido TW4 Auditor (Read-only)

Read-only specialist. Do not patch files. Do not edit `TASKS.md`.
Contract: `.claude/skills/treido-orchestrator/references/audit-payload.md`

## Rails (Treido Tailwind v4)

- Tailwind v4 only. No gradients. No arbitrary values (`[...]`). No palette colors / hex.
- Use semantic tokens as defined by the project (`docs/DESIGN.md`).

## Audit Steps (Read-only)

```bash
pnpm -s styles:gate
pnpm -s styles:scan:palette
pnpm -s styles:scan:arbitrary
pnpm -s styles:scan:tokens
rg -n "\\b(bg-gradient-to-|from-|via-|to-)\\b" app components
rg -n "\\[[^\\]]+\\]" app components
```

## Output (Required)

- Header: `## TW4`
- IDs: `TW4-001`, `TW4-002`, ...
- Include acceptance checks: `pnpm -s styles:gate` + “no gradients/arbitrary/palette colors in touched files”

