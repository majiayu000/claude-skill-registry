---
name: to-issues
description: Decompose a plan, PRD, or spec into independently-grabbable vertical-slice issues (markdown file by default, GitHub issues via flag). Trigger when the user wants implementation tickets, work decomposition, or to convert an implementation plan into parallelizable work. Takes a plan file and emits atomic vertical slices.
---

Break a plan into **tracer-bullet vertical slices**. Each slice cuts end-to-end through every layer (schema, API, UI, tests) and is independently demoable. Reject horizontal layer-slices — they create blocked queues.

## Emission Modes [LOCKED]

**Default (file mode):** Write to `<project-root>/docs/issues/<feature>-slices.md` as a numbered list of slices with the issue template per entry. Rerun-idempotent.

**Flag mode (`--emit-issue`):** After approval, create issues via `gh issue create` in dependency order so blocker references resolve to real numbers. Print URLs.

## Process

### 1. Gather context

Read the source plan or PRD. If user passes a GitHub issue: `gh issue view <number> --comments`. If a plan file path: `bat -P -p -n <path>`. Otherwise work from active conversation.

### 2. Explore (if not already primed)

If the codebase is unfamiliar, dispatch an Explore agent. Trace integration layers: schema → service → API → UI → tests.

### 3. Draft vertical slices

Each slice MUST:
- Cut through every relevant layer
- Be demoable or verifiable on its own
- Be either **AFK** (no human needed) or **HITL** (decision/review required) — prefer AFK
- Be small enough that one engineer ships it in <2 days

Reject any slice that is "schema only" or "wire up later" — those are queue-blockers.

### 4. Quiz the user

Present the slate via a clarifying-question protocol. Show per slice: title, AFK/HITL, blocked-by references, user-stories covered. Ask: granularity correct? dependency edges correct? merge/split needed? AFK/HITL labels honest?

### 5. Emit

**File mode:** Write the approved slice list to `docs/issues/<feature>-slices.md`. Reference blockers by slice index. Commit.

**Flag mode:** `gh issue create` per slice in topological order. Capture each new issue number; backfill `Blocked by` with real numbers.

## Issue Template

```
## Parent
#<parent-issue-number-or-PRD-path-or-omit>

## What to build
Concise end-to-end behavior description. Demoable outcome, not layer-by-layer mechanics.

## Acceptance criteria
- [ ] Observable criterion 1
- [ ] Observable criterion 2

## Blocked by
- #<issue-or-slice-number>   (or "None — start immediately")

## User stories covered
- US-1, US-3
```

## Slice Examples Across Stacks

- **Rust + Postgres API:** "Add `GET /accounts/{id}/balance` returning JSON; includes sqlx migration, handler, integration test against testcontainer Postgres." — one slice, all layers.
- **TypeScript + React frontend:** "Render account balance with optimistic refresh; includes Zod response schema, TanStack Query hook, component, Vitest test." — one slice, all layers.
- **CLI tool (any language):** "Add `--dry-run` flag to the migrate subcommand; includes flag parsing, no-op execution path, unit test." — one slice, all layers.
