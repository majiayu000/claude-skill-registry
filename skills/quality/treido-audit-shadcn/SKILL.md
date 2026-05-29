---
name: treido-audit-shadcn
description: "Read-only shadcn/ui auditor for Treido (primitives boundary + composition). Returns structured payload for ORCH merge. Trigger: SHADCN-AUDIT"
---

# Treido shadcn Auditor (Read-only)

Read-only specialist. Do not patch files. Do not edit `TASKS.md`.
Contract: `.claude/skills/treido-orchestrator/references/audit-payload.md`

## Focus (Treido)

- `components/ui/*` are primitives only: no app logic, no data fetching, no imports from `app/**`.
- Prefer composition in `components/shared/*` or route-private `app/[locale]/**/_components/*`.

## Audit Steps (Read-only)

```bash
rg -n "from ['\"]@/app/|from ['\"]\\.{1,2}/.*app/" components/ui
rg -n "\\b(supabase|stripe)\\b" components/ui
rg -n "\"use client\"" components/ui
rg -n "\\b(useEffect|useState|useMemo|createContext)\\b" components/ui
```

## Output (Required)

- Header: `## SHADCN`
- IDs: `SHADCN-001`, `SHADCN-002`, ...
- Include acceptance checks: “no app/** imports in components/ui/*”

