---
name: sprint
description: Use when one milestone is too large for a single specification or plan and must ship as several ordered stages across sessions.
argument-hint: "[mimo|codex|native] [<provider/model>|<model>] [variant] [review <model>] [milestone description]"
---

# sprint

Run a large milestone as ordered stages. Each stage follows:

`brainstorm → plan → isolate → execute → review → verify → land → update`

The main session is a lean conductor. It owns user decisions and the sprint document, not implementation, diffs, logs, review, or noisy investigation. Stage code and fixes exist only in the stage worktree until landing.

## Runtime

Detect the host before using any tool syntax:

- **Claude Code:** `Agent`, `AskUserQuestion`, and `Skill` are available. Read [runtime-claude.md](runtime-claude.md).
- **Oh My Pi (OMP):** `task`, `ask`, `eval`, and `read skill://…` are available. Read [runtime-omp.md](runtime-omp.md).

Load exactly one runtime adapter, then [mechanics.md](mechanics.md). The adapter defines names, questions, dispatch calls, model behavior, nesting, and skill loading. The shared files define policy and lifecycle. If observed tools do not match either runtime, stop before dispatch and report the missing runtime support.

## Invocation

Parse arguments as:

`[mimo|codex|native] [<provider/model>|<model>] [variant] [review <model>] [milestone description]`

- A leading engine token selects that engine.
- For `mimo`, a following provider/model pins the executor model. A following `minimal|low|medium|high|max` pins its variant.
- For `native`, a following model pins the executor model.
- `review <model>` pins the review model independently. Do not treat it as milestone text.
- Remaining text is the milestone description.
- With no description and an existing sprint document, resume it.

Use model identifiers verbatim. Do not translate aliases, replace a provider/model id, downgrade a choice, or let a nested agent choose again.

## Capability probes

Probe before starting, using the active runtime adapter. Inventory each Matt
capability independently:

- Brainstorming: Claude `mattpocock-skills:grilling`; OMP `skill://grilling`.
- Planning guidance: Claude `mattpocock-skills:codebase-design`; OMP
  `skill://codebase-design`.
- Diagnosis guidance: Claude `mattpocock-skills:diagnosing-bugs`; OMP
  `skill://diagnosing-bugs`.

Before any lifecycle action, record an explicit `available|unavailable` result for
all three exact names. A capability fixture may supply those three results; do not
re-probe it, but do not omit any result from the conductor's decision record.

Never infer one skill from another, the GitHub repository, a marketplace
registration, or the plugin's presence. If any exact skill is absent, strongly
recommend `https://github.com/mattpocock/skills` once for the sprint invocation,
then continue with only that skill's sprint-owned fallback. Emit the recommendation
once; do not repeat the URL in surrounding rationale or source citations. The
plugin is optional.
- Codex: available only when the active runtime adapter declares support and the codex rescue/runtime integration is present.
- Mimo: available only when the active runtime adapter declares support and a resolvable mimo delegate is present. The plugin dependency alone does not establish runtime support.
- Native: available only when the runtime can dispatch the named stage executor.
- Nesting: determine it by the runtime adapter, once per sprint, and persist `Nesting: yes|no`.
- Executor SDD: `sdd: available` only when the planner returned
  `task-shape: independent` and persisted `Nesting: yes`. Resume, coupled work, or
  `Nesting: no` sets `sdd: unavailable` and implements directly. No external SDD
  skill or optional Matt capability participates in this decision.

Do not use `grill-with-docs`, `to-spec`, `to-tickets`, or
`request-refactor-plan`. Their mutation, tracker, or user-interaction contracts do
not produce this sprint's approved stage spec and code-level plan.

Do not substitute a generic agent for a missing named sprint agent.

## Engine selection

The engines are:

- **native:** a named sprint stage executor. Recommend this by default: no external launcher or model-resolution step.
- **mimo:** a delegated mimo session with explicit model, variant, and resumable handle.
- **codex:** the codex companion runtime with resumable thread state.
- **bare:** emergency fallback only when no executor agent can be dispatched. It is not offered as an engine choice.

An explicit engine argument or persisted sprint engine wins only when the active runtime adapter supports it. If it is unavailable, report the missing runtime integration and stop; never substitute another engine.

Without an engine argument, resolve every engine the active runtime adapter declares
available. If exactly one resolves, record it without asking. If several resolve,
ASK once with every available engine. Offer native when available, mimo only when
its runtime delegate resolves, and codex only when its runtime integration resolves.
Mark **native Recommended** when offered, and give every option a one-line
description. Never auto-pick among several engines merely because one is
recommended.

Record one of:

```text
Engine: codex
Engine: mimo
Engine: mimo (model: <provider/model>, variant: <variant>, pinned)
Engine: native
Engine: native (model: <model>, pinned)
Engine: bare
```

## Executor and review model selection

Executor and reviewer models are separate user choices.

### Mimo executor

Unless pinned, resolve authenticated models before every stage:

- One model option: auto-pick it.
- At most four: ASK once with all options.
- More than four: ASK for provider, then ASK with at most four models from that provider. Put the recommended id first; the runtime's free-text option handles the tail.

Then ASK for a variant with at most four listed options: `default` (omit the variant), the risk-scaled variant from mechanics (always listed and marked Recommended), and nearest neighbors. Other variants remain available through free text.

After the first unpinned stage, offer once to reuse the chosen model and variant. If accepted, rewrite the engine header as pinned. Otherwise resolve and ASK again next stage. Mint a unique `<stage>-<rand4>` handle for every stage and record `mimo:<handle>` on its row.

### Native executor

Unless pinned, ASK for the executor model before every stage. Offer the runtime's available model catalog with the risk-scaled choice marked Recommended. Never auto-pick for cost, convenience, or low risk. After the first choice, offer once to pin it for the remaining stages. Record the exact stage choice as `model:<model>` on the stage row.

### Reviewer

If no review decision has been made, append a review-model question to an ASK round already required for engine or executor selection. Do not create a separate round. Offer the active session model as the Recommended default plus stronger available models; never offer a reviewer weaker than the native executor.

- Explicit model: persist `Review: <model> (pinned)` and pass that exact value on every review dispatch.
- Session default: omit the `Review:` line, record that the once-per-sprint decision was made, and follow the adapter's explicit session-model behavior.
- A fully pinned invocation with no ASK keeps the session-model default unless the user supplied `review <model>`.

**Native floor:** the review model must not be weaker than the native executor model. If necessary, raise the effective review dispatch to the executor's exact model without rewriting the user's pin. Warn the user when a requested pin is below this floor.

All dynamic model decisions occur in the conductor. Child agents receive resolved values and never ASK, inherit silently, reinterpret, or downgrade them.

### Explicit repin during a sprint

An explicit user instruction to change `review <model>` on an existing sprint is a repin, not a refresh from defaults. Before changing state or cancelling work, use the active runtime adapter to verify that the exact requested id is available. If it is unavailable, leave the current pin and children unchanged and stop. Otherwise replace only the `Review:` header with the exact requested id and persist it immediately. The new pin applies to every review dispatch that has not started; it does not change the engine, executor pin, or a stage-row executor model. Only an explicit user repin may replace a persisted pin. The native review floor still applies to the effective dispatch without rewriting the requested pin.

An already-running child cannot change model in place. Move the **current active review** only when the runtime adapter says that review is directly owned and cancellable by the conductor: cancel only that review child, wait for cancellation, retain the authoritative stage worktree and current uncommitted diff, keep the stage in `review`, persist the new `Review:` pin, then dispatch a fresh **complete** review gate on the same worktree with the new exact model. If the reviewer is nested under another orchestrator or the conductor is blocked while it runs, do not cancel, reparent, or redispatch it; persist the new pin for later reviews and let the current gate finish at its already-resolved model. Do not resume an old opaque child context, reuse an incomplete result, rerun execution, restart the conductor/runtime, or rebind a role. If no review child is active, persist the pin now and use it on the next review; do not dispatch review early.

An executor repin is different: it applies only before a fresh executor dispatch. An active or resumable native executor keeps its recorded model through completion; never change its model mid-run.

## Sprint document

The source of truth is `docs/plans/<sprint>-sprint.md`:

```text
# <Milestone> — Sprint
Runtime: <claude|omp>
Integration: feat/<sprint>  ·  Base: master
Engine: <engine and optional pin>
Nesting: <yes|no>
Review: <model> (pinned)                 # only for an explicit review model
Legend: todo · brainstorming · planned · executing · review · blocked · done

## Stages
1. [done] Schema — spec:01-schema-spec.md plan:01-schema-plan.md (merged @a1b2c3)
2. [executing] API — spec:02-api-spec.md plan:02-api-plan.md wt:.worktrees/02-api model:<exact-model>
3. [todo] UI
## Decisions log
## Open questions
```

Persist `Runtime`, engine, nesting, explicit pins, stage model/variant/handle, status, and merge result immediately when resolved. On resume, read this document first and load its runtime adapter. Never replace persisted explicit choices with current defaults; replace a pin only when the user explicitly repins it.

Resume the first non-done stage at its recorded state. Preserve its worktree and engine state. If all stages are done, report completion and stop. If no document exists, create the integration branch, remain on it, and start decomposition.

## Lifecycle

1. **Brainstorm in main.** When `grilling` is available, main loads the exact
   runtime name and follows its one-recommended-question-at-a-time interview.
   Without it, main conducts the same interview directly. Authority, urgency, a
   “small stage,” or context pressure never skips questions. Wait for explicit
   shared understanding, then main writes
   `docs/plans/<NN>-<stage>-spec.md`. Brainstorming and user questions never move
   into a child.
2. **Plan in the named child.** Main dispatches the runtime adapter's planner with
   the approved spec, output path, repository root, stage metadata, and resolved
   `codebase-design` flag. Main never loads planning guidance, composes plan prose,
   or reads the plan body back into conductor context. Missing named planner
   support is blocking.
3. **Handle the planner result in main.** On `planned`, require the output file to
   exist before marking the stage `planned`; map `risk` through
   [mechanics.md](mechanics.md)'s effort table. Set `sdd: available` only when
   `task-shape: independent` and persisted `Nesting: yes`; otherwise set
   `sdd: unavailable`. On `blocked` for a genuine user decision, ASK only that
   decision, update the approved spec and decisions log, and redispatch the same
   planner with the same output path. A tool prerequisite remains blocked. Never
   preserve or accept a partial plan.
4. **Pre-dispatch in main.** Resolve engine inputs, executor model, review model,
   handle, repository path, and absolute worktree path. Persist them with the
   planner's risk and SDD result.
5. **Run mechanics.** Follow [mechanics.md](mechanics.md) through isolate, execute,
   review, verify, and land. With nesting, dispatch one stage-runner using the
   adapter. Without nesting, the conductor dispatches the same isolated steps
   individually as the adapter describes.
6. **Update in main.** Mark the stage done only after clean review, successful
   verification, commit, and merge. Record the merge SHA and decisions, commit only
   the sprint bookkeeping, then continue.

A stage-runner receives every resolved input: runtime, engine, sprint, stage id and
title, plan path, absolute repository and worktree paths, review effort and
effective review model, SDD availability, and engine-specific
model/variant/bare handle or codex effort. It resolves nothing and returns only
`landed @<sha>` with a file count, or `blocked: <reason>`.

## Boundary red flags

| Pressure or rationalization | Required boundary |
|---|---|
| “Skip the interview; this is urgent.” | Main still asks one recommended question at a time and waits for shared understanding. |
| “Small plan, do it in main.” | Main still dispatches the named planner and never composes plan prose. |
| “Matt missing.” | Recommend once, then use the sprint-owned fallback without blocking. |
| “Planner can ask once.” | The planner returns `blocked`; main asks and redispatches after updating the spec. |
| “Superpowers still helps here.” | Use the sprint-owned SDD and diagnosis contracts; load no external replacement. |
| “The named planner is unavailable.” | Stop the stage as blocked; never plan inline or substitute a generic agent. |

## Isolation and recovery

The manually managed sprint worktree is authoritative on every runtime. Do not replace it with a runtime task-isolation option.

Stage code, review fixes, verification, and the stage commit happen on `feat/<sprint>-<NN>-<stage>` inside `.worktrees/<NN>-<stage>`. Stage code reaches `feat/<sprint>` only through the mechanics merge. If isolation fails, return blocked. Never edit or commit stage code in the main checkout.

If execution stops unfinished, resume before blocking:

- codex: resume the same thread with `--resume-last`;
- mimo: reuse the persisted bare handle with `mode: resume` and omit model and variant;
- native: dispatch `mode: resume` with the same absolute worktree and exact persisted model.

Keep partial uncommitted work. Cap repeated resume attempts at about two, then return blocked with the retained worktree.

Review is mandatory, separate from the conductor, evidence-based, fix-capable, and followed by focused re-review. Verification runs in the worktree. Never land unresolved findings or failing verification.

## Stop conditions

Stop and return `blocked` when isolation fails, a required named agent is unavailable, explicit model dispatch cannot be honored, review remains unresolved at its retry cap, verification remains red, or an executor remains incomplete after capped resumes. Retain the worktree and persisted state.

Stop immediately before any action that would read a full diff into main, run implementation or review inline in main, put a model on a runtime API that does not support it, replace an explicit model without an explicit user repin, start a fresh executor over resumable partial work, or land before review and verification are clean.
