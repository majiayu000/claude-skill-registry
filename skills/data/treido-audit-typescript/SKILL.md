---
name: treido-audit-typescript
description: "Read-only TypeScript auditor for Treido (strictness, unsafe casts, any/unknown discipline). Returns structured payload for ORCH merge. Trigger: TS-AUDIT"
---

# Treido TypeScript Auditor (Read-only)

Read-only specialist. Do not patch files. Do not edit `TASKS.md`.
Contract: `.claude/skills/treido-orchestrator/references/audit-payload.md`

## Focus (Treido)

- Avoid `as any`, unchecked assertions, and `@ts-ignore`.
- Prefer narrow types, `unknown` + validation at boundaries.

## Audit Steps (Read-only)

```bash
pnpm -s typecheck
rg -n "\\bas any\\b|@ts-ignore|@ts-nocheck|@ts-expect-error" app components lib --glob '*.ts' --glob '*.tsx'
rg -n "\\b:any\\b|\\bany\\[\\]" app components lib --glob '*.ts' --glob '*.tsx'
```

## Output (Required)

- Header: `## TS`
- IDs: `TS-001`, `TS-002`, ...
- Include acceptance checks: `pnpm -s typecheck` + “no new as any / @ts-ignore in touched files”

