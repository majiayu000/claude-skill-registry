---
name: phx:work
description: Use after /phx:plan to systematically implement features, or with --continue to resume interrupted work. Executes plan tasks with progress tracking and verification after each step.
effort: high
argument-hint: <path to plan file>
---

# Work

Execute tasks from a plan file with checkpoint tracking and verification.

## Usage

```
/phx:work .claude/plans/user-auth/plan.md
/phx:work .claude/plans/user-auth/plan.md --from P2-T3
/phx:work --skip-blockers
/phx:work  # Resumes most recent plan
```

## Arguments

- `<plan-file>` -- Path to plan file (optional, auto-detects recent)
- `--from <task-id>` -- Resume from specific task (e.g., `P2-T3`)
- `--skip-blockers` -- Continue past blocked tasks
- `--continue` -- Resume IN_PROGRESS plan from checkboxes

## Iron Laws (NON-NEGOTIABLE)

1. **NEVER auto-proceed** to /phx:review or any next workflow
   phase -- always ask the user what to do next
2. **AUTO-CONTINUE between plan phases** -- when Phase N completes,
   immediately start Phase N+1. Do NOT stop or ask for permission
   between phases. Only stop at BLOCKERS or when ALL phases are done.
3. **Plan checkboxes ARE the state** -- `[x]` = done, `[ ]` = pending.
   No separate JSON state files. Resume by reading the plan.
4. **Verify after EVERY task** -- never skip verification
5. **Max 3 retries then BLOCKER** -- don't keep retrying forever
6. **Stage specific files** -- never use `git add -A` or `git add .`
7. **Read scratchpad BEFORE implementing** -- scratchpad has dead-ends
   and decisions that prevent rework. Step 2 is not optional.
8. **Clarify ambiguous tasks** -- ask the user rather than guessing
   when a plan task's intent is unclear

## Step 1: Research Decision

For plans with >3 tasks, ask the user:

> This plan has {count} remaining tasks across {count} phases.
>
> 1. **Start working** -- Begin immediately (familiar patterns)
> 2. **Quick research** -- Read source files first (~10 min)
> 3. **Extensive research** -- Web search + docs (~30 min)

Skip for plans with 3 or fewer simple tasks -- just start.

> **Split warning**: Plans with >10 tasks risk 2-3 context
> compactions. Suggest splitting via `/phx:plan` if not already.

## Step 2: Check Context (MANDATORY)

Read scratchpad and compound docs before writing any code.
Skipping this causes rework — scratchpad captures dead-ends
and decisions from planning that prevent taking wrong paths.

```bash
# Read full scratchpad — it's short and has critical context
cat .claude/plans/{slug}/scratchpad.md 2>/dev/null
# Check compound docs for solved patterns
grep -rl "KEYWORD" .claude/solutions/ 2>/dev/null
```

Apply findings: skip dead-ends, follow decisions, reuse patterns.
If a task's intent is ambiguous, ask the user before implementing
rather than guessing — corrections are expensive.

## Step 3: Load, Create Task List, and Resume

Read plan file, count `[x]` (completed) vs `[ ]` (remaining).
Find first unchecked task by `[Pn-Tm]` ID.

**Create Claude Code tasks** from ALL unchecked plan items using
`TaskCreate`. This gives real-time progress visibility in the UI:

```
For each unchecked `- [ ] [Pn-Tm] Description`:
  TaskCreate({
    subject: "[Pn-Tm] Description",
    description: "Full task details from plan",
    activeForm: "Implementing: Description"
  })
```

Already-checked items (`[x]`): skip, don't create tasks for them.
Set up `blockedBy` dependencies between phases (Phase 2 tasks
blocked by Phase 1 tasks).

With `--from P2-T3`: Skip to that specific task.

See `${CLAUDE_SKILL_DIR}/references/resume-strategies.md` for all resume modes.

## Step 4: Execute Tasks

For each unchecked task (`- [ ] [Pn-Tm][agent] Description`):

1. **Start task**: `TaskUpdate({taskId, status: "in_progress"})`
2. **Route** by `[agent]` annotation (see `${CLAUDE_SKILL_DIR}/references/execution-guide.md`)
3. **Implement** the task
4. **Verify**: `mix format` + `mix compile --warnings-as-errors`
   (at phase end, also run `mix test <affected>` — see tiers below)
5. **Complete task**: Mark checkbox `[x]` on pass, **append
   implementation note** inline, AND
   `TaskUpdate({taskId, status: "completed"})`. Example:
   `- [x] [P1-T3] Add user schema — citext for email, composite index on [user_id, status]`
   This survives context compaction; the plan is re-read on resume.
6. **On failure**: retry up to 3 times, then create BLOCKER
   and write DEAD-END to scratchpad (see error-recovery.md)

**Parallel groups**: Tasks under `### Parallel:` header spawn
as background subagents. See `${CLAUDE_SKILL_DIR}/references/execution-guide.md`
for spawning pattern, prompt template, and checkpoint flow.

**Verification tiers** (scoped to minimize redundant runs):

- Per-task: `mix compile --warnings-as-errors` only
  (format is checked by PostToolUse hook automatically)
- Per-phase: `mix compile --warnings-as-errors` + `mix test <affected_files>` + `mix credo --strict`
  (scope tests: `mix test test/path/to_affected_test.exs` — NOT full suite)
- Per-feature (Tidewave): behavioral smoke test via `project_eval`
  (create record, fetch, verify -- see execution-guide.md)
- Final gate: `mix test` (full suite — run ONCE at the end, not per-phase)

**Token efficiency**: Do NOT narrate each verification step. Execute
tool calls directly without "Let me now run..." preamble. Only narrate
when explaining a non-obvious decision or reporting a failure.

> **Linter note**: The PostToolUse hook checks formatting but does
> NOT modify files. Run `mix format` explicitly during verification
> steps or before committing.

## Step 5: Completion

Summarize results with `AskUserQuestion`:

> Implementation complete! {done}/{total} tasks finished.
> {count} files modified across {count} phases.

Options: 1. **Run review** (`/phx:review`) (Recommended),
2. **Get a briefing** (`/phx:brief` — understand what was built),
3. **Commit changes** (`/commit`), 4. **Continue manually**.

With blockers: list them, offer **Replan** (`/phx:plan`),
**Review first** (`/phx:review`), or **Handle myself**.

**If blockers remain**, auto-write HANDOFF to scratchpad:

```markdown
### [HH:MM] HANDOFF: {plan name}
Status: {done}/{total} tasks. Blockers: {list}.
Next: {first unchecked task ID and description}.
Key decisions: {brief list from this session}.
```

This gives a fresh session context beyond just checkboxes.

**NEVER** auto-start /phx:review or any other phase.

## Step 6: Check for Additional Plans

After completion, check for other pending plans:

```bash
ls .claude/plans/*/plan.md 2>/dev/null
```

If pending plans exist, inform the user. Do NOT auto-start.

## Integration

```text
/phx:plan → /phx:work (YOU ARE HERE) → /phx:review → /phx:compound
                 ↑ ASK USER before each transition
```

## References

- `${CLAUDE_SKILL_DIR}/references/execution-guide.md` -- Task routing, parallel execution, verification
- `${CLAUDE_SKILL_DIR}/references/resume-strategies.md` -- Resume modes and state persistence
- `${CLAUDE_SKILL_DIR}/references/file-formats.md` -- Plan and progress file formats
- `${CLAUDE_SKILL_DIR}/references/error-recovery.md` -- Error handling and blockers
- `${CLAUDE_SKILL_DIR}/references/harness-patterns.md` -- Critic-refiner pattern for debugging loops
