---
name: bd-first-memory-migration
description: 'Consolidate fragmented agent-memory layers into one bd-canonical store, then GC/retire the rest. Triggers: "memory migration", "consolidate agent memory", "beads-first memory".'
skill_api_version: 1
practices:
- wiki-knowledge-surface
- pragmatic-programmer
hexagonal_role: driving-adapter
consumes:
- repo-context
produces:
- migration-report
- bd-memories
metadata:
  tier: knowledge
---

# bd-first-memory-migration

> Make `bd` the single source of truth for agent memory. Salvage the keepers, derive the caches, garbage-collect and retire the rest. Three phases, gated between destructive steps.

## The problem this solves

Agents accrete **multiple uncoordinated memory stores** — one per harness (Claude `MEMORY.md`, an `ao`/flywheel store, `.agents/learnings` piles, `bd` memories). None is canonical, so they drift, bloat, duplicate, and never get garbage-collected. This skill collapses them to **one bd-canonical substrate**; everything else becomes a derived cache or is retired.

**Not** a generic dedup tool. It is opinionated: `bd` wins, decay-ranked recall replaces grep, and stale low-utility memory is evicted to a cold archive (never silently deleted).

## When to use / when not

| Use it when | Skip it when |
|---|---|
| You have ≥2 memory stores and one is `bd` (or you'll adopt bd) | You only have one store and it's healthy |
| A store has stalled (e.g. 99% "provisional", never promoted/evicted) | You need cross-org memory federation (out of scope) |
| Disk pile of duplicated extracts (`-pend-*`, N× copies) | You want to *keep* every store independent |

## Quick start

```bash
# Phase 1 — AUDIT (read-only; produces the KEEP/DROP manifest + reversibility plan)
scripts/audit-scan   --target <box>          # inventory every layer
scripts/classify     --manifest out/manifest.json   # keepers vs junk (dry-run)
#   ⛔ GATE A: human reviews the manifest before anything is written

# Phase 2 — MIGRATE (salvage -> bd; stand up typed recall; unify writes)
scripts/import       --manifest out/manifest.json --dry-run   # then drop --dry-run
scripts/recall       --query "<topic>" --max-tokens 400       # decay-ranked
scripts/gen-memory-md                                          # regenerate the thin cache

# Phase 3 — GC / RETIRE (after rollback test green)
scripts/gc           --dry-run               # dedup + evict-to-archive
#   ⛔ GATE B: rollback test green before any destructive retire
scripts/retire       --dry-run               # decommission dead daemons + reclaim disk
```

## The three phases

| Phase | Goal | Destructive? | Gate |
|---|---|---|---|
| **1 — Audit** | Inventory all layers; classify keep vs junk; write reversibility plan | No (read-only) | ⛔ **Gate A** — review KEEP/DROP manifest |
| **2 — Migrate** | Salvage keepers → bd (typed + provenance); decay-ranked recall; unified write path; generated `MEMORY.md` | Writes to bd only | — |
| **3 — GC/Retire** | Utility scoring, scheduled GC/dedup, retire dead stores, reclaim disk | **Yes** | ⛔ **Gate B** — rollback test green; ⛔ **Gate C** — human go/no-go on the real box |

Full per-phase contract: [references/PHASES.md](references/PHASES.md).
Memory data model + type taxonomy: [references/DATA-MODEL.md](references/DATA-MODEL.md).
Reversibility/rollback contract: [references/ROLLBACK.md](references/ROLLBACK.md).
Worked examples: [references/EXAMPLES.md](references/EXAMPLES.md).
Acceptance scenarios: [references/audit.feature](references/audit.feature) (Phase 1) · [references/migrate.feature](references/migrate.feature) (Phase 2).

## Anti-patterns

| Don't | Do |
|---|---|
| Hard-delete a store before salvage is verified | Import-ledger confirms every keeper landed in bd *first* |
| Run destructive retire before rollback is proven | Gate B: rollback test green is a hard precondition |
| Burst bd writes during bulk salvage | **Pace writes** — bd auto-commits each write to Dolt; bursts OOM a memory-capped server |
| Silently truncate (top-N, sampling) | `log()` whatever was dropped — silent caps read as "covered everything" |
| Hand-edit the generated `MEMORY.md` | It is a read-only cache rebuilt from bd; edit the bd memory instead |
| Auto-fire the real destructive retire | Gate C: human go/no-go on the live box (pre-mortem first) |

## Guardrails (load-bearing)

- **Idempotent + reversible + backup-aware.** Every destructive step takes a backup and has a documented rollback (see ROLLBACK.md).
- **Dry-run first.** Every Phase-2/3 mutate path ships with a working `--dry-run`.
- **Pace bd/Dolt writes.** Bulk salvage of thousands of keepers will trip a memory-capped Dolt server if unpaced — sleep between writes, cap concurrency.
- **bd canonical, not br.** This skill targets `bd`; it does not migrate the tracker itself.

## See also

- `skills/beads/SKILL.md` — the bd issue/memory substrate this skill writes to
- `skills/harvest/SKILL.md` — promoting `.agents` knowledge (the *authored* keepers this skill salvages)
