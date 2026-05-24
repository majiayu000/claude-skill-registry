---
name: treido-orchestrator
description: "Orchestrates Treido work end-to-end (parallel specialist audits, single-writer plan, execute, verify/test). Uses a bundle matrix to spawn auditors. Trigger: ORCH"
---

# Treido Orchestrator (Single Writer)

This skill coordinates a predictable workflow:

- **Phase 1 (Parallel)**: specialist auditors (read-only) return structured payloads
- **Phase 2 (Single-writer)**: merge audits + write a prioritized plan in `TASKS.md`
- **Phase 3 (Single-writer)**: implement tasks in 1–3 file batches
- **Phase 4 (Single-writer)**: run verification gates
- **Phase 5 (Single-writer)**: run the smallest relevant tests

## Non-Negotiables

- **Single-writer rule**:
  - Auditors + verifier are read-only (no patches, no `TASKS.md` edits).
  - Orchestrator is the sole writer for `audit/*` and `TASKS.md`.
  - Code changes happen in the implementer lane (still one writer per batch).
- **Small batches**: execute as 1–3 file rounds; run gates after each round.
- **Rails first**: no secrets/PII in logs, next-intl for user strings, Tailwind v4 tokens only, cached-server rules, no scope creep.

## Bundle Matrix (Intent → Auditors)

| User intent (examples) | Bundle | Auditors spawned |
|---|---|---|
| “fix styling”, “UI looks off”, “mobile styling” | UI | Next.js + TW4 + SHADCN |
| “backend issue”, “server action broken”, “webhook” | Backend | Next.js + Supabase + TypeScript |
| “database”, “RLS”, “schema/policies” | Supabase | Supabase + TypeScript |
| “full audit”, “what’s wrong” | Full | All: Next.js + TW4 + SHADCN + Supabase + TypeScript |

Preferred auditor skill names (new system):

- `treido-audit-nextjs`
- `treido-audit-tw4`
- `treido-audit-shadcn`
- `treido-audit-supabase`
- `treido-audit-typescript`

Fallbacks (if a new auditor skill doesn’t exist yet):

- Next.js: `nextjs-structure` (or `treido-frontend` for boundary scans)
- TW4: `treido-tailwind-v4`
- SHADCN: `treido-shadcn`
- Supabase: `treido-supabase-mcp`
- TypeScript: `treido-audit` (TS-focused scan) + `pnpm -s typecheck`

## Phase 1 — Specialist Audits (Parallel, Read-only)

1. Select a bundle from the matrix (or accept an explicit override like `ORCH:UI`, `ORCH:FULL`).
2. Spawn auditors in parallel. Each auditor must return **only** the structured payload contract:
   - Contract: `.codex/skills/treido-orchestrator/references/audit-payload.md`
3. Validate the payloads are mergeable (each starts with `## <AUDITOR>` and includes the required sections).

### Auditor Prompt Template (copy/paste)

Send each auditor this message (customize scope/context):

```md
You are an audit-only specialist. Read-only: do not patch files, do not edit TASKS.md.

Goal/context: <1–2 sentences>
Scope hints: <routes/files if known>

Return ONLY a Markdown section that follows:
.codex/skills/treido-orchestrator/references/audit-payload.md

No preamble. Start with `## <AUDITOR_NAME>`.
```

## Phase 1.5 — Merge Audits (Single Writer)

1. Create a shared audit artifact under `audit/`:
   - `audit/YYYY-MM-DD_<short-context>.md`
2. Merge auditor sections verbatim (no rewrites beyond formatting), ordered by bundle.
3. Ensure no secrets/PII are written into audit artifacts.

## Phase 2 — Plan (Write `TASKS.md`)

1. Convert findings into tasks with clear priority and acceptance criteria.
2. Keep tasks small (≤ 1 day) and executable in 1–3 file rounds.
3. Prefer these owners (new system), otherwise use existing owners:
   - `treido-impl-frontend` (fallback: `treido-frontend`)
   - `treido-impl-backend` (fallback: `treido-backend`)
   - `treido-verify` (fallback: `treido-audit`)
4. Respect `TASKS.md` “Ready ≤15” rules.

Task block (recommended):

```md
### Priority 1 (Critical)
- [ ] <ID>: <task summary>
  - Owner: <skill>
  - Verify: `<commands>`
  - Files: <paths>
```

## Phase 3 — Execute (Single Writer)

1. Pick the smallest set of Priority 1 tasks that fit into a 1–3 file batch.
2. Implement using the owner lane conventions (frontend vs backend).
3. Avoid unrelated refactors; defer follow-ups into `TASKS.md`.

## Phase 4 — Verify / QA

Always:

```bash
pnpm -s typecheck
pnpm -s lint
pnpm -s styles:gate
```

## Phase 5 — Tests (Risk-based)

- UI-only: consider `pnpm -s test:unit` (and/or Storybook spot-check if used)
- Auth/payments/checkout/webhooks: `REUSE_EXISTING_SERVER=true pnpm -s test:e2e:smoke`
- Database/RLS: run Supabase advisors + regenerate types (via MCP lane) when applicable

## References (load only if needed)

- SSOT: `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/DESIGN.md`
- Audit payload contract: `.codex/skills/treido-orchestrator/references/audit-payload.md`
- Existing lanes (fallbacks): `.codex/skills/treido-frontend/SKILL.md`, `.codex/skills/treido-backend/SKILL.md`, `.codex/skills/treido-supabase-mcp/SKILL.md`, `.codex/skills/treido-audit/SKILL.md`
