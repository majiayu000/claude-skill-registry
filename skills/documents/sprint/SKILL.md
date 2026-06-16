---
name: sprint
description: Use when one milestone is too large for a single spec or plan and needs several brainstorm-and-plan rounds before it ships — a long, multistage effort spanning sessions where the coding is handed off to an executor (codex or mimo) while you stay the conductor. Triggers on "long multistage project", "many brainstorms and plans", "milestone with multiple stages", "resume where I left off", "delegate implementation to codex or mimo".
argument-hint: "[mimo|codex] [<provider/model>] [variant] [milestone description]"
---

# sprint

## Overview

A milestone too big for one spec-and-plan is run as a **sprint**: a series of stages, each one `brainstorm a spec → write a plan → hand the coding to the executor`. One living doc tracks the stages so you can stop and resume across sessions.

**Core principle:** the main context stays a **lean conductor** — only the sprint doc, current stage, decisions, open questions. Every technical step (executor, review, verify, land) runs in a worktree via a subagent, so diffs and logs never reach it.

**You are the foreman. The executor digs.**

## When to Use

- A milestone needs **multiple** brainstorm/plan rounds, not one spec → done.
- Long, multistage work **spanning sessions**; you resume "what stage am I on".
- You delegate implementation to an **executor** (codex or mimo) while steering design.

**Not for:** a single-spec feature; one small task (`codex:rescue` directly).

## Invocation arguments

Raw slash-command arguments: `$ARGUMENTS`

Parse them as `[mimo|codex] [<provider/model>] [variant] [milestone description]` (empty when the skill was triggered by description match rather than `/sprint` — then read intent from the user's message):

- A leading `mimo` or `codex` token → the **engine** (see [Engine selection](#engine-selection)).
- A `<provider/model>` token (contains `/`, mimo only) → **pin** that model for the whole sprint; a following `minimal|low|medium|high|max` token → the pinned **variant**. A pin records `Engine: mimo (model: …, variant: …, pinned)` and skips per-stage model resolution.
- Remaining text → the **milestone description** that seeds the decomposition brainstorm. No description **and** an existing sprint doc → resume at the first non-done stage.

## Capability Probes (run FIRST, every invocation)

Probe; never assume. Adapt, and tell the user to install whatever's missing.

| Capability | Probe | If absent |
|---|---|---|
| superpowers | `superpowers:brainstorming` in skills list? | bare brainstorm + plan; **recommend installing superpowers** |
| executor: codex | `codex:rescue` in skills list? | not required — codex is optional; mimo is the dependency-guaranteed default |
| executor: mimo | `mimo-code:mimo-delegate` available? (hard dependency — should always be true) | if absent, the dependency failed to install — tell the user to reinstall sprint |
| codex SDD | *(only if engine=codex)* `fd -t d subagent-driven-development ~/.codex/skills ~/.claude/plugins/marketplaces/openai-codex 2>/dev/null` | hand codex the whole plan |
| mimo model | *(only if engine=mimo, unless pinned)* dispatch `mimo-code:mimo-resolve` | **ASK the user** unless `options` has exactly one model (then auto-pick) — one provider ≠ one option |
| **nesting** | dispatch a one-shot `general-purpose` probe subagent, prompt: *"Reply with exactly one word: `Agent` if you have a Task/Agent subagent-dispatch tool, else `NONE`."* | reports `Agent`/`Task` → `Nesting: yes`; `NONE` → `Nesting: no`. Selects the **orchestration mode** (see Dispatch). Run **once per sprint**, persist in the header. (CLI grants subagents `Agent` → yes; Claude Desktop withholds it → no.) |

## Starting a Sprint

1. `mkdir -p docs/plans`.
2. Create the integration branch and stay on it the whole sprint: `git switch -c feat/<sprint>`.
3. **Select the engine** (see below).
4. Brainstorm the **decomposition** with the user → ordered stages → write the sprint doc (record the engine in its header). Then run stages one at a time.

### Engine selection

The executor is **codex** or **mimo**. mimo is the dependency-guaranteed default; codex is optional (probe `codex:rescue`).

- **Explicit arg wins.** `/sprint mimo` or `/sprint codex` picks the engine directly. If codex is requested but absent → tell the user to install the codex plugin (or explicitly opt into bare execution), then stop.
- **No arg:** if codex is present (probe) → `AskUserQuestion` (mimo vs codex). If codex is absent → **mimo** (the only guaranteed engine), no question.

Record the engine in the sprint-doc header. **The model is stored in the header ONLY when pinned:**

- `Engine: codex`
- `Engine: mimo` — resolve the model **every stage** (the conductor dispatches `mimo-resolve` and ASKs/auto-picks per stage).
- `Engine: mimo (model: <provider/model>, variant: <v>, pinned)` — **only** on an explicit user pin like `/sprint mimo <provider/model> [variant]`; reuse the pinned model+variant every stage.
- `Engine: bare` — last-resort fallback when neither executor is available (the stage-runner implements stages itself, mechanics §4c). Normally unreachable since mimo is a hard dependency; recorded so a resumed bare sprint still has a recognizable header.

## The Sprint Doc

Source of truth at `docs/plans/<sprint>-sprint.md`. Re-invoking the skill reads it and resumes at the first non-done stage. Slugs: **`<sprint>`** = milestone slug (e.g. `auth`); **`<NN>-<stage>`** = per-stage prefix (e.g. `01-schema`).

```
# <Milestone> — Sprint
Integration: feat/<sprint>  ·  Base: master
Engine: mimo
Nesting: yes
Legend: todo · brainstorming · planned · executing · review · blocked · done

## Stages
1. [done]      Schema — spec:01-schema-spec.md plan:01-schema-plan.md (merged @a1b2c3)
2. [executing] API    — spec:02-api-spec.md plan:02-api-plan.md wt:.worktrees/02-api mimo:api-7f3a
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
4. **Execute** → the executor (codex or mimo — see mechanics §4) implements the plan, write-enabled, **in the worktree**; effort/model chosen per engine. If it stalls/stops mid-plan, **resume the same session** — never re-run fresh: codex resumes via `task --resume-last` (what `codex:rescue --resume` wraps); mimo resumes by re-dispatching `mimo-delegate` with the recorded `mimo:<handle>` (mechanics §4).
5. **Review** → in a **subagent** that cds into the worktree, invoke the **vendored `code-review` skill** (`<high|xhigh|max> --fix`, effort by stage risk) via the Skill tool — not the GitHub-PR `/code-review` plugin, not `ultra` (mechanics §5); loop unresolved items back to step 4.
6. **Verify** → repo test/build **in the worktree**; on failure, loop back to step 4.
7. **Commit & land** → commit the worktree changes (the executor/review leave them uncommitted), merge the branch into the integration branch, remove the worktree.
8. **Update doc** (main) → stage → `done` + merge SHA; append decisions/questions; commit the doc; next stage.

**Conductor pre-dispatch (engine=mimo, unless pinned):** before the stage executes (i.e. before dispatching the stage-runner in nested mode, or the executor in flat mode), the conductor dispatches `mimo-resolve` to gather the authenticated `options`, then **selects model+variant by this rule:** `options` has **exactly one** model → auto-pick it (asking is pointless); `options` has **more than one** → **ASK the user** (`AskUserQuestion` when ≤4 models, else print the grouped list and have them name an id). **One authenticated provider offering several models is still "more than one" → ASK; never collapse a provider to a single auto-pick.** The proactive output style, a "low-risk"/"mechanical"/"bounded"/"trivial" stage, saving cost, or "not wanting to interrupt" are **not** reasons to skip the ASK — the user delegated execution to mimo but still chooses the model unless they pinned one. ASK the variant the same way (offer a "default" that omits `--variant`). Then generate a unique per-stage handle `<stage>-<rand4>` and record `mimo:<handle>` on the stage line. A **pinned** sprint (`Engine: mimo (… pinned)`) is the *only* thing that skips the resolve+ASK: it reuses the pinned model+variant every stage (still minting a fresh handle per stage). For `Engine: codex` there's no model resolution.

**Dispatch (by `Nesting:` mode):** steps 3–7 always run in subagents — diffs/logs never reach the conductor. HOW they're dispatched depends on the `Nesting:` header (set by the nesting probe):

- **`Nesting: yes` (nested):** the conductor spawns **one** `sprint:stage-runner` subagent that runs steps 3–7 from the repo root and dispatches the executor (§4) and review (§5) as **nested** subagents, returning a **terse** report (`landed @sha` / `blocked: <reason>` / files count). The stage-runner carries the **`Agent` tool** and has **no model** (inherits main).
- **`Nesting: no` (flat — Claude Desktop & any runtime that withholds `Agent` from subagents):** a subagent can't dispatch subagents, so the **conductor orchestrates the stage itself**, dispatching each isolated step directly (all `main → subagent`, one level — allowed everywhere). Per stage:
  1. **Isolate** — conductor runs the `git worktree add` plumbing (mechanics §3). *(git only, no diffs.)*
  2. **Execute** — dispatch the executor subagent, **foreground**: mimo → `mimo-code:mimo-delegate` (sonnet); codex → a worktree subagent running the codex CLI; bare → a `general-purpose` worktree subagent (mechanics §4). Resume loop as usual.
  3. **Review** — dispatch a `general-purpose` review subagent (**no model override** → inherits main) that invokes the vendored `code-review` skill `--fix` in the worktree (mechanics §5). Loop unresolved items to 2.
  4. **Verify** — dispatch a `general-purpose` subagent to run the repo test/build in the worktree (keeps test output out of main). Loop failures to 2 (mechanics §6).
  5. **Land** — conductor runs the commit + `git merge --no-ff` + worktree-remove plumbing (mechanics §7). *(git only, no diffs.)*
  Even here the conductor **never reads diffs/logs and never runs or monitors the executor** — execute/review/verify each return only a terse report; the only Bash it runs is the git plumbing in 1 and 5 (the same kind it already runs for the integration branch and the step-8 doc commit).

**Model policy (both modes):** the mimo executor (`mimo-code:mimo-delegate`) is **sonnet**; the **review subagent inherits the main/session model** — never put a `model` override on it, because the review is the quality gate and must run at the main context's model. (In nested mode the `sprint:stage-runner` also has no model, so the review it dispatches inherits main too.) A verify subagent may be `sonnet`. The conductor runs only steps 1–2, the pre-dispatch resolve, the `Nesting: no` git plumbing (isolate/land), and step 8 — and **never runs or monitors the executor** (no launcher calls, no PID/NDJSON/output polling). **No diffs or logs reach the conductor.**

**Isolation invariant (non-negotiable):** stage **code** never touches the main checkout. Every edit, review fix, and the stage commit happen on the **stage branch `$BR` inside the worktree `$WT`**. Stage code reaches the integration branch **only** through the §7 `git merge --no-ff "$BR"`. The stage-runner must **never** edit stage code in the main tree and **never** `git commit` stage code onto the integration or base branch directly — even when it seems faster, even if the worktree step was skipped, even for a "one-line" change. The *only* thing committed directly to the integration branch is the conductor's step-8 sprint-doc bookkeeping. If step 3 can't isolate (integration branch missing, dirty main tree, `git worktree add` fails), **report `blocked` and stop** — never fall back to working in the main tree.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Executor or review run in the main repo, not a worktree | codex: `--cwd "$WT"`. mimo: launched with the worktree as cwd. Review: the nested subagent cds into `$WT` first. All mutate files. |
| Committing stage code straight onto the current/integration branch (no worktree, no stage branch) | Violates the isolation invariant. Stage code is committed on `$BR` in `$WT` and only reaches the integration branch via §7 `merge --no-ff`. Can't isolate → `blocked`, never commit in the main tree. |
| Review run inline or as a `claude -p` subprocess instead of a subagent | Step 5 is **mandatory in a nested Agent/Task subagent** (mechanics §5) — keeps diffs/fixes out of the stage-runner's context. |
| One giant spec/plan for the whole milestone | The anti-pattern this skill replaces. Decompose into stages. |
| *(nested mode)* Dispatching the stage-runner as `general-purpose` | It lacks the `Agent` tool, so it can't dispatch the executor/review subagents. In `Nesting: yes` mode use `sprint:stage-runner` (has `Agent`, inherits the main model). |
| Using `sprint:stage-runner` when `Nesting: no` | On Desktop (and any runtime that withholds `Agent` from subagents) the stage-runner can't dispatch its nested executor/review — it dies the same way. With `Nesting: no` the **conductor** orchestrates flat (isolate → executor subagent → review subagent → verify subagent → land); never hand the whole stage to one subagent. |
| Running the nesting probe per stage, or assuming a runtime | Probe **once** per sprint, record `Nesting:` in the header, reuse it. Don't hardcode yes/no — CLI and Desktop differ. |
| `fd`-searching for a `/code-review` command | That finds the `claude-plugins-official` **PR** plugin (reviews a GitHub PR via `gh pr comment`, and spawns its own agents — both wrong here). Invoke the **vendored** `code-review` skill via the Skill tool (`<effort> --fix`, in the worktree), and never `ultra` (the only multi-agent/cloud variant). |
| Conductor running or monitoring the executor — calling the launcher, polling mimo's PID / NDJSON / output files | That's the executor subagent's job (`mimo-delegate`, foreground) — nested under the stage-runner when `Nesting: yes`, dispatched directly by the conductor when `Nesting: no`. Either way the conductor only awaits a terse report and never touches executor machinery. A subagent that "keeps yielding" is **not** a licence to take over monitoring in main. |
| Auto-picking the mimo model because the stage is "low-risk"/"mechanical" or to avoid interrupting | The user chose the engine, not the model. Auto-pick **only** when `options` has exactly one model; several models (even all from one authenticated provider) → **ASK**. Proactivity and "right-sizing cost" never override this — only an explicit user pin does. |
| Merging/removing the worktree before committing | The executor and `--fix` leave changes uncommitted — commit first (mechanics §7). |
| Marking a stage `done` before it merged + passed verify | `done` = merged **and** green. |
| Executor stopped/stalled mid-stage → reported `blocked` or re-ran fresh | Resume the **same** session first: codex `task --resume-last`; mimo re-dispatch `mimo-delegate` with the recorded handle (mechanics §4). Fresh loses the executor's context and may clobber the partial edits. |

## Red Flags — STOP

- About to read a full diff in the main context → dispatch a subagent instead.
- About to start coding yourself → that's the executor's job; delegate.
- About to `git add`/`commit` in the main tree or onto the integration/base branch (stage code) → STOP. Stage code commits only on `$BR` inside `$WT`; it reaches the integration branch via §7 `merge --no-ff`. (Only the conductor's doc commit in step 8 goes on the integration branch.)
- About to read mimo's NDJSON/PID or the launcher's output in the main context, or poll a "detached" executor → STOP. The executor runs inside a `mimo-delegate` subagent (foreground); the conductor only awaits a terse report.
- `Nesting: no` and about to hand the whole stage to one `sprint:stage-runner` → STOP. That subagent can't dispatch its nested executor/review on this runtime; orchestrate the stage flat from the conductor (mechanics §0).
- Executor stopped before finishing and about to launch a fresh session (or report `blocked`) → resume the existing session first: codex `--resume-last`; mimo re-dispatch with the recorded handle (mechanics §4).
- No sprint doc yet but already brainstorming a stage → create the branch + doc and decompose first.
