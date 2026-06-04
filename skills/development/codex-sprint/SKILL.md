---
name: codex-sprint
description: Use when one milestone is too large for a single spec or plan and needs several brainstorm-and-plan rounds before it ships — a long, multistage effort spanning sessions where the coding should be handed off to codex while you stay the conductor. Triggers on "long multistage project", "many brainstorms and plans", "milestone with multiple stages", "resume where I left off", "delegate implementation to codex".
---

# codex-sprint

## Overview

A milestone too big for one spec-and-plan is run as a **sprint**: a series of stages, each one `brainstorm a spec → write a plan → hand the coding to codex`. One living doc tracks the stages so you can stop and resume across sessions.

**Core principle:** the main context stays a **lean conductor** — only the sprint doc, current stage, decisions, open questions. Every technical step (codex, review, verify, land) runs in a worktree via a subagent, so diffs and logs never reach it.

**You are the foreman. Codex digs.**

## When to Use

- A milestone needs **multiple** brainstorm/plan rounds, not one spec → done.
- Long, multistage work **spanning sessions**; you resume "what stage am I on".
- You delegate implementation to **codex** while steering design.

**Not for:** a single-spec feature; one small task (`codex:rescue` directly).

## Capability Probes (run FIRST, every invocation)

Probe; never assume. Adapt, and tell the user to install whatever's missing.

| Capability | Probe | If absent |
|---|---|---|
| superpowers | `superpowers:brainstorming` in skills list? | bare brainstorm + plan; **recommend installing superpowers** |
| codex | `codex:rescue` in skills list? | run a `general-purpose` subagent in the worktree; **recommend the codex plugin** |
| codex SDD | `fd -t d subagent-driven-development ~/.codex/skills ~/.claude/plugins/marketplaces/openai-codex 2>/dev/null` | hand codex the whole plan |

## Starting a Sprint

1. `mkdir -p docs/plans`.
2. Create the integration branch and stay on it the whole sprint: `git switch -c feat/<sprint>`.
3. Brainstorm the **decomposition** with the user → ordered stages → write the sprint doc. Then run stages one at a time.

## The Sprint Doc

Source of truth at `docs/plans/<sprint>-sprint.md`. Re-invoking the skill reads it and resumes at the first non-done stage. Slugs: **`<sprint>`** = milestone slug (e.g. `auth`); **`<NN>-<stage>`** = per-stage prefix (e.g. `01-schema`).

```
# <Milestone> — Sprint
Integration: feat/<sprint>  ·  Base: master
Legend: todo · brainstorming · planned · executing · review · blocked · done

## Stages
1. [done]      Schema — spec:01-schema-spec.md plan:01-schema-plan.md (merged @a1b2c3)
2. [executing] API    — spec:02-api-spec.md plan:02-api-plan.md wt:.worktrees/02-api
3. [todo]      UI
## Decisions log
## Open questions
```

Per-stage files: `docs/plans/<NN>-<stage>-spec.md` and `-plan.md` (superpowers convention).

**Resuming:** read the doc → resume at the **first non-done stage** (at its current status). None left → sprint complete, report and stop. No doc → start a sprint.

## Per-Stage Lifecycle

Steps **1–2 are interactive, in the main context**. Steps **3–7 run in a worktree via a subagent**. Step **8 is back in the main context**. **Before running steps 3–7, open `mechanics.md` (this skill directory) — it holds the exact commands and shell variables (`$WT`, `$BR`, `$S`).**

1. **Brainstorm** (main) → `superpowers:brainstorming` (or bare) → `docs/plans/<NN>-<stage>-spec.md`.
2. **Plan** (main) → `superpowers:writing-plans` (or bare) → `docs/plans/<NN>-<stage>-plan.md`.
3. **Isolate** → create the worktree off the integration branch.
4. **Execute** → codex implements the plan, write-enabled, **in the worktree**; effort by risk. If codex stalls/stops mid-plan, **resume the same thread** (`task --resume-last`, what `codex:rescue --resume` wraps) — never re-run fresh (mechanics §4).
5. **Review** → headless `/code-review --fix` **in the worktree**; loop unresolved items back to step 4.
6. **Verify** → repo test/build **in the worktree**; on failure, loop back to step 4.
7. **Commit & land** → commit the worktree changes (codex/review leave them uncommitted), merge the branch into the integration branch, remove the worktree.
8. **Update doc** (main) → stage → `done` + merge SHA; append decisions/questions; commit the doc; next stage.

**Dispatch model:** per stage the conductor spawns **one** `general-purpose` stage-runner subagent that executes steps 3–7 from the repo root and returns a **terse** report: `landed @sha` / `blocked: <reason>` / files-touched count. The conductor runs only steps 1–2 and 8 — never the Mechanics commands. **No diffs or logs reach the conductor.**

## Common Mistakes

| Mistake | Fix |
|---|---|
| codex or review run in the main repo, not a worktree | Always `--cwd "$WT"` / a `(cd "$WT" && …)` subshell; both mutate files. |
| One giant spec/plan for the whole milestone | The anti-pattern this skill replaces. Decompose into stages. |
| Merging/removing the worktree before committing | codex and `--fix` leave changes uncommitted — commit first (mechanics §7). |
| Marking a stage `done` before it merged + passed verify | `done` = merged **and** green. |
| codex stopped/stalled mid-stage → reported `blocked` or re-ran a fresh `task` | Resume the **same** thread first: `task --resume-last` (mechanics §4). Fresh loses codex's context and may clobber the partial edits. |

## Red Flags — STOP

- About to read a full diff in the main context → dispatch a subagent instead.
- About to start coding yourself → that's codex's job; delegate.
- codex stopped before finishing and about to launch a fresh `task` (or report `blocked`) → resume the existing thread first (`--resume-last`, mechanics §4).
- No sprint doc yet but already brainstorming a stage → create the branch + doc and decompose first.
