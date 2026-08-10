---
name: ai-coding-agents-tasks
description: "Designs background task systems for coding-agent runtimes. Use when implementing task lists, worker tasks, background execution, cancellation, or teammate task coordination."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# AI Coding Agents Tasks

Use this skill to design or review how a coding-agent runtime represents work as tasks: local agent tasks, shell tasks, remote tasks, teammate tasks, background execution, task lists, and task coordination.

This skill is about runtime task systems, not product backlog planning.

## ASCII Flow

```text
work request
  |
  v
task model
  type + owner + status + inputs + blockers + cancellation semantics
  |
  v
task store
  local task list | background task | remote task | teammate task
  |
  v
scheduling
  claim -> run -> progress events -> complete | fail | blocked | release
  |
  v
UI/session reflection
  background badge, task detail, foregrounding, retry, escalation
```

## Quick Reference

| Question | Read | Outcome |
|----------|------|---------|
| What task types should a coding-agent runtime support? | [`references/task-types-and-lifecycle.md`](references/task-types-and-lifecycle.md) | Task families, statuses, background eligibility, and host ownership |
| How should task lists and teammate routing work? | [`references/task-list-coordination-and-teammate-routing.md`](references/task-list-coordination-and-teammate-routing.md) | File-watched task lists, claiming, blockers, teammate routing, and response loops |
| How do Anthropic-hosted routines (schedule / API / GitHub) behave? | [`references/claude-code-routines.md`](references/claude-code-routines.md) | Trigger types, `/fire` endpoint, beta header, cap-drop behaviour, fresh-session model, comparison with Actions / n8n / cron |
| How do I trigger agents from webhooks, queues, or schedules at scale? | [`references/webhook-and-queue-triggers.md`](references/webhook-and-queue-triggers.md) | Shape A — SQS / Streams / Kafka / EventBridge, idempotency, dedup, DLQ, provider rate-limit slots |
| How do I make agent runs durable across crashes and multi-step? | [`references/durable-trigger-integration.md`](references/durable-trigger-integration.md) | Temporal / Inngest / Restate / Step Functions, agent-as-activity, sagas, signals, replay |
| Where do I actually host the trigger + agent (Vercel, Fly, CF, Render)? | [`../software-paas-hosting/references/agent-hosting-matrix.md`](../software-paas-hosting/references/agent-hosting-matrix.md) | Per-shape PaaS stacks + reference architectures |
| How do I statically validate a recipe blueprint YAML? | [`scripts/recipe_scanner.py`](scripts/recipe_scanner.py) | stdlib-only validator: required fields, parameter types, extension risk gates, placeholder detection |
| How does OpenAI Codex model cloud tasks, apply/diff, and agent graphs? | [`references/openai-codex-cloud-tasks-and-agent-graph.md`](references/openai-codex-cloud-tasks-and-agent-graph.md) | Task CLI lifecycle, best-of-N attempts, partial apply states, environment filters, and persisted parent-child topology |

## When To Use

- Design background work for a coding-agent CLI or runtime
- Add task lists, worker tasks, or background execution surfaces
- Decide how local, remote, and teammate tasks should differ
- Model cancellation, claiming, blocking, and foreground/background transitions
- Coordinate work between a lead session and worker tasks

## Use Other Skills

| Need | Use Instead |
|------|-------------|
| Multi-agent planning and ownership contracts | [`../agents-swarm-orchestration/SKILL.md`](../agents-swarm-orchestration/SKILL.md) |
| Terminal UI and task dialogs | [`../ai-coding-agents-terminal-ui/SKILL.md`](../ai-coding-agents-terminal-ui/SKILL.md) |
| Session resume and transcript persistence | [`../ai-coding-agents-sessions/SKILL.md`](../ai-coding-agents-sessions/SKILL.md) |
| Prompt-cache economics when spawning subagent tasks | [`../ai-coding-agents-sessions/references/resume-path-decision-tree.md`](../ai-coding-agents-sessions/references/resume-path-decision-tree.md) — blank vs. forked subagent startup, cache-prefix economics; also [`../ai-coding-agents-sessions/references/context-forking.md`](../ai-coding-agents-sessions/references/context-forking.md) |
| Tool-call permission gating, approval modes, and policy inheritance for subagents | [`../ai-coding-agents-permissions/SKILL.md`](../ai-coding-agents-permissions/SKILL.md) |

## Default Workflow

1. **Model task types explicitly.** Local shell, local agent, remote agent, teammate, workflow, and monitor-style tasks should not be one untyped blob.
2. **Keep task state in the host store.** Status, ownership, backgrounding, and timestamps belong to runtime state, not just UI widgets.
3. **Define background eligibility.** Only running or pending tasks that are actually backgrounded should appear in background-task surfaces.
4. **Use claiming for shared task lists.** External or teammate task lists need explicit claim and release behavior.
5. **Respect blockers and ownership.** Pending tasks with unresolved blockers or owners are not available for automatic pickup.
6. **Differentiate abort from kill.** Interrupting current work is not the same as terminating the worker or task object.
7. **Stabilize task-list identity.** Task list IDs should resolve from explicit context first and use monotonic high-water-mark rules so resets do not accidentally reuse old IDs.
8. **Serialize shared mutations.** Host-owned task stores need lock or backoff semantics when multiple workers can touch the same list.
9. **Test concurrency edges.** Verify double claim, failed submission after claim, blocked task ordering, background/foreground transitions, and remote-task cancellation.

## Host Rules

- Task type and task state should be typed separately from UI rendering.
- Background task indicators should only show truly backgrounded running or pending work.
- Claiming must be atomic enough to avoid duplicate workers taking the same task.
- Lead and teammate navigation should stay separate from generic task-list execution.
- Cancellation semantics must distinguish “stop this turn” from “kill this task.”
- Task-list identity should be host-owned and sanitized before it becomes a filesystem or external synchronization key.

## Build Order

1. Define typed task families and lifecycle states.
2. Put task state in a host-owned store with timestamps and ownership.
3. Add background eligibility and foreground transition rules.
4. Add claiming and release semantics for shared task lists.
5. Add task-list identity resolution and collision-resistant non-reuse rules.
6. Add blocker resolution, retry logic, and serialized shared mutations.
7. Add teammate and remote-task routing with explicit cancellation behavior.

## Core Invariants

- Task type and lifecycle state are runtime data, not UI decoration.
- Claiming shared work must be explicit and collision-resistant.
- Background visibility should reflect real background execution, not intent.
- Abort and kill are different actions with different guarantees.
- Lead-session navigation and teammate-task routing are not generic queue operations.
- Task-list IDs must not be reused casually after reset or crash.

## Failure Modes

- Multiple workers claiming the same task.
- Submission failing after claim without releasing ownership.
- Blocked tasks being scheduled as if they were runnable.
- Background indicators showing tasks that are not actually executing.
- Cancellation stopping the current turn but leaving the task object running indefinitely.
- Task-list resets reusing old IDs and colliding with stale watcher or worker state.
- A background task silently auto-denying an unapproved tool call and stalling in a read-only loop instead of surfacing the pending-permission state to the owning session (see [Background-Subagent Task Semantics](#background-subagent-task-semantics-claude-code-2026-0607)).

## Minimal Viable Version

- One typed task model with statuses and ownership.
- One host-owned task store.
- One background-task filter based on real state.
- One atomic-enough claim and release path.
- One host-owned task-list ID strategy that survives restart and reset.
- One clear distinction between aborting work and killing a task.

## What Strong Implementations Add

- File-watched or externally synchronized task lists.
- Teammate routing and lead-session coordination flows.
- Debounced watcher updates and stable callbacks.
- Lockfile or backoff discipline for concurrent task-list mutation.
- Explicit blocker resolution, retry, and escalation transitions.
- Remote-task and workflow-task families beyond local shell or local agent tasks.
- **Typed recipe blueprints** with declared parameters, pinned extensions, and static validation at load time.
- **Capability-narrowed subagents** whose extension envelope is a strict subset of the lead's.
- **Sub-recipe composition** as a distinct task relationship, with cascading cancellation and blocker semantics.

## Known Traps

- Treating tasks as chat affordances only and never defining the runtime lifecycle, owner, blocker, or cancellation semantics behind them.
- Assuming claim operations are atomic without any collision handling, lock discipline, or stale-owner recovery.
- Letting UI sorting logic decide runnable order instead of blocker-aware runtime rules.
- Reusing task-list identities after reset or branch changes and accidentally reconnecting stale background work.
- Collapsing abort, cancel, stop, and kill into one action even though they imply different process and state cleanup behavior.
- Treating a subagent-spawn primitive that was merely renamed (e.g. Claude Code's `Task` → `Agent`) as two distinct task families instead of checking whether it is the same primitive under an old name.

## Common Anti-Patterns

- Treating tasks as plain strings or chat messages instead of typed runtime objects.
- Using badge counts without a real background-task model.
- Assuming claim is just “set owner if empty” with no collision handling.
- Reusing task-list identifiers after reset because “the old list is gone.”
- Conflating abort, cancel, stop, and kill into one button.
- Letting UI sorting logic decide runnable order instead of blocker-aware runtime rules.

## Task Sizing Heuristic (OpenAI / Codex, 2026-05)

Source: [*How OpenAI uses Codex*](https://cdn.openai.com/pdf/6a2631dc-783e-479b-b1a4-af0cfbd38630/how-openai-uses-codex.pdf), p. 11 — internal-usage report.

- **Calibration point:** a well-scoped Codex task is one that *"would take you or a teammate about an hour to complete or a few hundred lines of code to implement."* This is the largest scoped unit OpenAI's own teams reliably run unattended in May 2026.
- **Pattern — sizing gate:** before queueing a task, ask "could a teammate do this in roughly an hour given the same prompt?" If no, break it down. If yes, dispatch.
- **Anti-pattern — multi-day asks framed as one task.** "Migrate the auth subsystem to OAuth 2.1" is not a task; it is a project. Decompose into sized tasks each gated by an Ask-Mode plan before dispatch (see [`../ai-coding-agents/SKILL.md#openai-internal-practice-codex-2026-05`](../ai-coding-agents/SKILL.md#openai-internal-practice-codex-2026-05)).
- **Forecast hook:** "as models improve, expect the size of the tasks it can take on to increase" (OpenAI). Re-baseline this heuristic every two minor model releases; do not treat the hour/few-hundred-LOC figure as a permanent ceiling.
- **Task queue as backlog:** the corollary to the sizing rule — small tasks dispatched freely become a working backlog rather than a planning burden. No obligation to produce a full PR per task; tangential and partial work is legitimate queue content.

## Claude Code Routines (2026-04)

Claude Code Routines is a research-preview scheduling layer that lets Claude Code run without a local session. Distinguish three trigger classes; pick the narrowest one that fits:

| Trigger class | Runtime | Persistence | Use when |
|---------------|---------|-------------|----------|
| **Routines** (Anthropic cloud) | Cloud-hosted Claude Code workers | Schedule, API call, or GitHub event fires the job with the laptop closed | You need cadence-driven or webhook-driven work (PR babysitting, nightly repo sweeps, scheduled reports) |
| **`/loop`** (session-bound) | Current local session | Dies with the session; runs while the session is open | You want a repeating task during an active working session (poll deploy, retry until green) |
| **Desktop scheduled tasks** | Local machine | Tied to this machine staying awake | Machine-local automation where cloud access is not acceptable |

Routines are task-shaped: a Routine creates tasks in the host runtime under a scheduler-owned task family. Apply the same typing, claiming, blocker, and cancellation rules as other task types — schedule triggers do not earn special cases.

Caveats (verified 2026-07-11 — still research preview, not GA; re-check before treating this as a stable contract):
- Daily run caps per plan (Pro: 5/day; Max: 15/day; Team/Enterprise: 25/day; overage billing available on metered plans). One-off (non-scheduled) fires draw down normal session usage instead and do **not** count against the daily cap — model it as a separate counter. Source: https://code.claude.com/docs/en/routines, https://claude.com/blog/introducing-routines-in-claude-code. Design for throttling and idempotent handlers regardless of tier.
- Each Routine invocation is a fresh session — depends on `AGENTS.md` / `CLAUDE.md` for context, not transcript memory.
- Treat Routine-spawned tasks as remote-task lifecycle, not local-agent lifecycle, for cancellation and ownership purposes.
- GitHub-event runs are capped per routine per hour; events beyond the cap are **dropped, not queued**.

Source: Matt Abrams, *Claude Code Routines* tutorial (2026-04-20); https://code.claude.com/docs/en/routines (re-verified 2026-07-11).

## Background-Subagent Task Semantics (Claude Code, 2026-06/07)

Claude Code's own subagent-task model changed enough in the last two months that the "task vs. subagent" naming and the background-permission contract in this skill's design rules need a concrete, dated anchor. Treat these as the reference implementation of the abstract rules above ("Differentiate abort from kill," "background eligibility"), not as a Claude-Code-only detail.

- **Naming collapse (v2.1.63):** the tool historically called `Task` for spawning subagents was renamed `Agent`. Legacy `Task(...)` references in settings and agent definitions still resolve as an alias; some SDK surfaces still report `Task` in an initial tools list while emitting `Agent` in tool-use blocks. When auditing an existing runtime, do not assume "Task" and "Agent" are different task families — check whether it is the same subagent-spawn primitive under an old name before modeling two families.
- **Background-by-default (v2.1.198, 2026-07-01):** subagent spawns run in the background by default rather than opt-in; the lead session keeps working and is notified on completion or when input is needed via a Notification hook (`agent_needs_input` / `agent_completed`). Design implication: "background" is no longer a rare, explicitly-requested task state — it is the default task shape, so background-task surfaces must be a first-class, always-visible part of the UI, not a rare drawer.
- **Permission-prompt routing fix (v2.1.186, 2026-06-22):** before this release, a background subagent that hit an unapproved tool call **silently auto-denied** the call and could stall in a read-only loop with no visible error — a textbook version of this skill's "background indicators showing tasks that are not actually executing" failure mode. Since v2.1.186, the permission prompt now **surfaces into the parent/lead session**, labeled with the subagent's name, and the lead can approve or deny inline while the subagent keeps running. Model this explicitly: a background task's "waiting on a tool permission" moment is a distinct pending-input sub-state that must route to the owning session, not a state that gets swallowed and reported as generic progress.
- **Fork-mode override:** the `CLAUDE_CODE_FORK_SUBAGENT` environment variable forces every subagent spawn into the background and removes the runtime's ability to force a specific spawn to the foreground (the `background` frontmatter field and any per-call foreground request are ignored). Treat this as a host-wide policy switch on background eligibility, not a per-task property — a runtime that lets individual task requests silently override a host-wide fork-mode policy has a policy-enforcement bug, not a feature.

Known trap to add to your own review checklist: a runtime that treats "background subagent needs a permission" as a silent, unrecoverable failure — rather than routing it to the owning session as a first-class pending state — reproduces a bug Anthropic had to ship a dedicated fix for. Verify current behavior against `code.claude.com/docs/en/sub-agents` before depending on exact version gates; permission-routing and background-default behavior are active areas of change.

## Cross-Platform Patterns (Goose)

Goose models task creation around **recipes**: declarative YAML units that replace ad-hoc free-text task spawning. Three patterns worth importing into the task runtime model.

### Recipes as typed task blueprints

A Goose recipe is a validated YAML file with `version / title / description / instructions / author / extensions / activities / prompt / parameters` (typed: `{key, input_type, requirement, description, default}`). Tasks spawn *from* a recipe, not from a free-form user string. Parameters are declared, activities are listed, required extensions are pinned.

- **Pattern:** when a task type is well-defined and reusable, promote it to a typed blueprint. Runtime validates the blueprint at load time (see `recipe-scanner`-style static checks), binds typed parameters, and spawns the task with a pinned extension manifest.
- **Anti-pattern:** treating every task as a free-text prompt and relying on prompt craft to make them repeatable. That collapses reuse, versioning, and validation into transcript memory.
- **Recipe:** ship a validator that checks YAML syntax, required fields, extension references (do the declared extensions actually exist?), and security gates (is this recipe allowed to spawn network-touching tools?). Goose's `recipe-scanner/` crate is a working reference.

### Capability-narrowed subagents

When a lead session spawns parallel subagents (code review lane, docs lane, file-processing lane), each subagent should carry its *own* extension manifest — typically a subset of the lead's. Goose models this explicitly; the subagent inherits no more capability than its recipe declares.

- **Pattern:** subagent spawn = recipe + parameters + capability-narrowed extension list. The narrower capability envelope is enforced at task-creation time, not at tool-call time.
- **Anti-pattern:** subagents inheriting the lead's full tool belt by default. That turns "delegate code review" into "let a sub-process touch anything the lead could touch" and defeats parallel-lane isolation.
- **Recipe:** in your task typing, add an `extensions: Vec<ExtensionRef>` field to the subagent-task family. Refuse to spawn if the subagent's declared extensions are not a subset of the lead's envelope.

### Sub-recipes — composable task blueprints

A Goose recipe can invoke another recipe as a step, not just call a tool. Sub-recipes let complex workflows compose from validated pieces instead of giant monolithic prompts.

- **Pattern:** model sub-recipe calls as a distinct task relationship ("spawned-by-recipe-step"), separate from lead→worker (delegation) and from tool calls (invocation). Ownership, cancellation, and blocker semantics follow the recipe tree.
- **Anti-pattern:** inlining sub-recipes into the parent's prompt text. That loses the validation, capability-narrowing, and telemetry attribution benefits of the recipe boundary.
- **Recipe:** give sub-recipe tasks a distinct lifecycle state (`pending-subrecipe`, `running-subrecipe`, `completed-subrecipe`) and a parent-recipe pointer. Cancellation of the parent should cascade; a failed sub-recipe should be a first-class blocker on the parent.

## Goal-Mode Loops (Codex `/goal`, Goose `/goal`, and analogues, 2026-05)

Codex exposes a `/goal` command and Goose (v1.36.0+) ships its own `/goal` loop — two first-party implementations of the same pattern: act → score → check goal → continue or terminate. The same loop shape can be built on top of any agent runtime (Claude Code subagent, custom SDK harness, scheduled Routine). Two failure modes dominate when the loop is wired to a vague target:

- **Early give-up.** Score function is unsatisfiable in the obvious direction → agent halts after a few minutes claiming "good enough."
- **Infinite flail.** Score function never converges → agent rewrites the same files indefinitely, burning tokens with no progress.

Both modes share the same root cause: the *check goal* step is underspecified. Fixes below are first-party patterns from Chris Hayduk (OpenAI, 2026-05-11).

### Pattern — Quantitative goal + constraints

Replace qualitative goals with a measurable target plus an explicit constraint set. The agent terminates when target ≥ threshold AND no constraint is violated.

- **Anti-pattern:** "Make the code better." / "Improve this paper."
- **Pattern:** "Reduce runtime of code in `specific_file.py` by 20% without causing regressions in existing unit and integration tests."

Required fields for any goal-mode prompt:

1. **Target metric** — runtime, accuracy, line count, lint score, completed-items count.
2. **Direction + magnitude** — "reduce by 20%", "raise above 0.85", "down to ≤ 50 lines".
3. **Constraint set** — tests that must keep passing, files that must not change, APIs that must not break.
4. **Termination signal** — exact command or file state the agent can read to confirm it is done.

### Pattern — Checklist-as-score (qualitative → quantitative)

When the real goal is qualitative (formatting compliance, style guide adherence, doc completeness), convert it to a binary checklist:

1. Extract the qualitative spec into a markdown checklist with N items (Hayduk's NeurIPS→ICML conversion produced 200+ items from a LaTeX style file).
2. Instruct the agent: "Goal complete when all N of N items are checked off."
3. Each item can itself be vague — the model reasons about per-item completion better than per-goal completion.
4. Have the agent mutate the checklist file as it works, so progress is persisted and inspectable.

Why this works: a fuzzy "is the paper formatted correctly?" decision becomes N narrow "is rule K satisfied?" decisions, each of which the model can self-check with reasonable reliability.

### Pattern — Tight feedback loop

The goal-mode loop is bounded by per-iteration scoring time. Drop scoring cost without compromising signal:

- For ML/training tasks: smaller model + subsampled dataset (Hayduk: NanoFold dataset cut scoring from days to minutes for protein-structure architecture search).
- For codebases: scoped test subset that exercises the affected path, not full suite.
- For builds: incremental builds, not clean rebuilds.

This is the same minification principle as dev-loop test speedups, applied to the *evaluation* step of an RL-style agent loop instead of to verification.

### When bare goal-mode is not enough

Goal-mode is a ralph-style loop: same prompt repeats with the goal-state read back each iteration. Ralph loops scale test-time compute effectively — Anthropic's BrowseComp data (linked from [Watts, 2026-05-07](https://x.com/jarrodwatts/status/2052372045829382430)) shows Sonnet 4.6 spending ~10× tokens yielded ~10 percentage points higher score. But a bare ralph loop hits three ceilings:

1. **Ambiguity bottleneck.** Each iteration's output is the next iteration's input. One underspecified decision early in the run direction-shifts everything downstream. No amount of token spend rescues a run whose target was vague. Fix: invest in a pre-loop interview/clarification phase (20–50 clarifying questions) that forces the human to decide upfront. See [`../dev-workflow-planning/SKILL.md#pre-loop-setup-phase-both-variants`](../dev-workflow-planning/SKILL.md) and `superpowers:brainstorming`.

2. **Single-context-window bottleneck.** Even with token budget headroom, a single agent's context window accumulates clutter and the model starts "deluding itself" (Watts, citing Boris Cherny). Separate context windows beat one big window. Fix: orchestrator + implementer + reviewer triad — fresh subagent context per task, reviewer judges work without implementer biases. See [`../agents-swarm-orchestration/SKILL.md`](../agents-swarm-orchestration/SKILL.md).

3. **Cross-context memory bottleneck.** Multi-day runs cross compaction boundaries; without filesystem-backed memory, new context windows lose the chain. Fix: filesystem-backed journaling per the Watts 4-file (bounded product) or Hayduk 3-file (exploratory) pattern. See [`../dev-workflow-planning/SKILL.md#long-horizon-agent-journaling`](../dev-workflow-planning/SKILL.md).

Goal-mode + ralph loop alone is the right primitive for short-horizon quantitative goals (Hayduk's NeurIPS→ICML, runtime-by-20% optimizations). For multi-day product building it is necessary but not sufficient — pair it with interview-led setup, multi-agent execution, and cross-context memory or accept that the run will drift.

### Anti-pattern — Letting compaction carry multi-day state

Goal-mode runs that last hours or days exceed the practical window of in-memory transcript compaction. Force state to the filesystem instead. See [Long-Horizon Agent Journaling](../dev-workflow-planning/SKILL.md#long-horizon-agent-journaling-3-file-pattern) in `dev-workflow-planning` for the canonical 3-file (`PLAN.md` / `EXPERIMENTS.md` / `EXPERIMENT_NOTES.md`) pattern.

### Recipe — Wiring a goal-mode task

1. Convert user intent → quantitative goal + constraint set. If qualitative, build the checklist first as a planning step.
2. Stand up the cheapest scoring command that still discriminates progress; record it in the task definition.
3. Seed `PLAN.md` with the initial approach. Mount `EXPERIMENTS.md` + `EXPERIMENT_NOTES.md` as the agent's persistent scratchpad.
4. Spawn the goal-mode task with a hard wall-clock cap and an iteration cap; both should be generous but finite.
5. On termination, check the *real* score (not the agent's self-reported claim) before accepting the result.

Source: Chris Hayduk, *Using Codex Goals Effectively* (2026-05-11). Generalizable beyond Codex — the same pattern works for Claude Code subagents driving toward a measurable target.

## Navigation

### References

- [`references/task-types-and-lifecycle.md`](references/task-types-and-lifecycle.md) — Task families, statuses, and background visibility rules
- [`references/task-list-coordination-and-teammate-routing.md`](references/task-list-coordination-and-teammate-routing.md) — File-watched task lists, claiming, blockers, and teammate routing
- [`references/claude-code-routines.md`](references/claude-code-routines.md) — Scheduled/triggered routines: schedule (cron), API `/fire`, and GitHub-event triggers; prompt-authoring rules, limits, and creation paths
- [`references/durable-trigger-integration.md`](references/durable-trigger-integration.md) — Durable trigger integration for reliable triggered runs
- [`references/webhook-and-queue-triggers.md`](references/webhook-and-queue-triggers.md) — Webhook- and queue-driven task triggers, including per-event budgets
- [`references/openai-codex-cloud-tasks-and-agent-graph.md`](references/openai-codex-cloud-tasks-and-agent-graph.md) — OpenAI Codex cloud task lifecycle, apply/diff result states, environment filters, and persisted task topology

### Scripts

- [`scripts/recipe_scanner.py`](scripts/recipe_scanner.py) — stdlib-only static validator for recipe blueprint YAML files

### Data

- [`data/sources.json`](data/sources.json) — Primary documentation and source references for coding-agent task runtime guidance

### Related Skills

- [`../agents-swarm-orchestration/SKILL.md`](../agents-swarm-orchestration/SKILL.md)
- [`../ai-coding-agents-terminal-ui/SKILL.md`](../ai-coding-agents-terminal-ui/SKILL.md)
- [`../ai-coding-agents-sessions/SKILL.md`](../ai-coding-agents-sessions/SKILL.md)
- [`../ai-agents/references/autonomous-loop-patterns.md`](../ai-agents/references/autonomous-loop-patterns.md) — when a trigger should drive an autonomous *loop* (iterate until a goal/acceptance criterion is met), not a single run
- [`../agents-hooks/references/budget-and-loop-hooks.md`](../agents-hooks/references/budget-and-loop-hooks.md) — budget, iteration-cap, stagnation, and kill-switch enforcement for scheduled/triggered runs and always-on bots

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- The patterns here are grounded in a local April 2026 `claude_code` snapshot, current primary runtime docs, and a 2026-07-11 web re-verification pass (Task→Agent rename, background-by-default default, and background-permission-prompt routing — see [Background-Subagent Task Semantics](#background-subagent-task-semantics-claude-code-2026-0607)). Re-check current task type names, subagent or handoff affordances, session persistence rules, and backgrounding behavior before depending on exact runtime details — this cluster changes fast.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
