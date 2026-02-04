---
name: technical-implementation
description: "Orchestrate implementation of plans using agent-based TDD workflow with per-task review and approval gate (auto mode available). Use when: (1) Implementing a plan from docs/workflow/planning/{topic}.md, (2) User says 'implement', 'build', or 'code this' with a plan available, (3) Ad hoc coding that should follow TDD and quality standards, (4) Bug fixes or features benefiting from structured implementation. Dispatches executor and reviewer agents per task, commits after review approval."
---

# Technical Implementation

Orchestrate implementation by dispatching **executor** and **reviewer** agents per task. Each agent invocation starts fresh — flat context, no accumulated state.

- **Executor** (`.claude/agents/implementation-task-executor.md`) — implements one task via strict TDD
- **Reviewer** (`.claude/agents/implementation-task-reviewer.md`) — independently verifies the task (opus)

The orchestrator owns: plan reading, task extraction, agent invocation, git operations, tracking, task gates.

## Purpose in the Workflow

This skill can be used:
- **Sequentially**: To execute a plan created by technical-planning
- **Standalone** (Contract entry): To execute any plan that follows plan-format conventions

Either way: dispatch agents per task — executor implements via TDD, reviewer verifies independently.

### What This Skill Needs

- **Plan content** (required) - Phases, tasks, and acceptance criteria to execute
- **Plan format** (required) - How to parse tasks (from plan frontmatter)
- **Specification content** (optional) - For context when task rationale is unclear
- **Environment setup** (optional) - First-time setup instructions

**Before proceeding**, verify all required inputs are available and unambiguous. If anything is missing or unclear, **STOP** — do not proceed until resolved.

- **No plan provided?**
  > "I need an implementation plan to execute. Could you point me to the plan file (e.g., `docs/workflow/planning/{topic}.md`)?"

- **Plan has no `format` field in frontmatter?**
  > "The plan at {path} doesn't specify an output format in its frontmatter. Which format does this plan use?"

- **Plan status is not `concluded`?**
  > "The plan at {path} has status '{status}' — it hasn't completed the review process. Should I proceed anyway, or should the plan be reviewed first?"

If no specification is available, the plan becomes the sole authority for design decisions.

---

## Resuming After Context Refresh

Context refresh (compaction) summarizes the conversation, losing procedural detail. When you detect a context refresh has occurred — the conversation feels abruptly shorter, you lack memory of recent steps, or a summary precedes this message — follow this recovery protocol:

1. **Re-read this skill file completely.** Do not rely on your summary of it. The full process, steps, and rules must be reloaded.
2. **Check task progress in the plan** — use the plan adapter's instructions to read the plan's current state. Also read the implementation tracking file and any other working documents for additional context.
3. **Check `task_gate_mode`** in the tracking file — if `auto`, the user previously opted out of per-task gates for this session.
4. **Check git state.** Run `git status` and `git log --oneline -10` to see recent commits. Commit messages follow a conventional pattern that reveals what was completed.
5. **Announce your position** to the user before continuing: what step you believe you're at, what's been completed, and what comes next. Wait for confirmation.

Do not guess at progress or continue from memory. The files on disk and git history are authoritative — your recollection is not.

---

## Orchestrator Hard Rules

1. **No autonomous decisions on spec deviations** — when the executor reports a blocker or spec deviation, present to user and STOP. Never resolve on the user's behalf.
2. **All git operations are the orchestrator's responsibility** — agents never commit, stage, or interact with git.

---

## Step 1: Environment Setup

Run setup commands EXACTLY as written, one step at a time.
Do NOT modify commands based on other project documentation (CLAUDE.md, etc.).
Do NOT parallelize steps — execute each command sequentially.
Complete ALL setup steps before proceeding.

Load **[environment-setup.md](references/environment-setup.md)** and follow its instructions.

#### If `docs/workflow/environment-setup.md` states "No special setup required"

→ Proceed to **Step 2**.

#### If setup instructions exist

Follow them. Complete ALL steps before proceeding.

→ Proceed to **Step 2**.

#### If no setup file exists

Ask:

> "No environment setup document found. Are there any setup instructions I should follow before implementing?"

**STOP.** Wait for user response.

Save their instructions to `docs/workflow/environment-setup.md` (or "No special setup required." if none needed). Commit.

→ Proceed to **Step 2**.

---

## Step 2: Read Plan + Load Plan Adapter

1. Read the plan from the provided location (typically `docs/workflow/planning/{topic}.md`)
2. Plans can be stored in various formats. The `format` field in the plan's frontmatter identifies which format this plan uses.
3. Load the format's per-concern adapter files from `.claude/skills/technical-planning/references/output-formats/{format}/`:
   - **reading.md** — how to read tasks from the plan
   - **updating.md** — how to write progress to the plan
4. If no `format` field exists, ask the user which format the plan uses.
5. These adapter files apply during Step 5 (task loop).

→ Proceed to **Step 3**.

---

## Step 3: Project Skills Discovery

#### If `.claude/skills/` does not exist or is empty

```
No project skills found. Proceeding without project-specific conventions.
```

→ Proceed to **Step 4**.

#### If project skills exist

Scan `.claude/skills/` for project-specific skill directories. Present findings:

> Found these project skills that may be relevant to implementation:
> - `{skill-name}` — {brief description}
> - `{skill-name}` — {brief description}
> - ...
>
> Which of these should I pass to the implementation agents? (all / list / none)

**STOP.** Wait for user to confirm which skills are relevant.

Store the selected skill paths — they will be persisted to the tracking file in Step 4.

→ Proceed to **Step 4**.

---

## Step 4: Initialize Implementation Tracking

#### If `docs/workflow/implementation/{topic}.md` already exists

Reset `task_gate_mode` to `gated` in the tracking file before proceeding (fresh session = fresh gate).

If `project_skills` is populated in the tracking file, present for confirmation:

> "Previous session used these project skills:
> - `{skill-name}` — {path}
> - ...
>
> · · ·
>
> - **`y`/`yes`** — Keep these, proceed
> - **`c`/`change`** — Add or remove skills"

**STOP.** Wait for user choice.

- **`y`/`yes`**: Proceed with the persisted paths.
- **`change`**: Re-run discovery (Step 3), update `project_skills` in the tracking file.

→ Proceed to **Step 5**.

#### If no tracking file exists

Create `docs/workflow/implementation/{topic}.md`:

```yaml
---
topic: {topic}
plan: ../planning/{topic}.md
format: {format from plan}
status: in-progress
task_gate_mode: gated
project_skills: []
current_phase: 1
current_task: ~
completed_phases: []
completed_tasks: []
started: YYYY-MM-DD  # Use today's actual date
updated: YYYY-MM-DD  # Use today's actual date
completed: ~
---

# Implementation: {Topic Name}

Implementation started.
```

After creating the file, populate `project_skills` with the paths confirmed in Step 3 (empty array if none).

Commit: `impl({topic}): start implementation`

→ Proceed to **Step 5**.

---

## Step 5: Task Loop

Load **[steps/task-loop.md](references/steps/task-loop.md)** and follow its instructions as written.

→ After the loop completes, proceed to **Step 6**.

---

## Step 6: Mark Implementation Complete

Update the tracking file (`docs/workflow/implementation/{topic}.md`):
- Set `status: completed`
- Set `completed: YYYY-MM-DD` (use today's actual date)
- Update `updated` date

Commit: `impl({topic}): complete implementation`

---

## References

- **[environment-setup.md](references/environment-setup.md)** — Environment setup before implementation
- **[steps/task-loop.md](references/steps/task-loop.md)** — Task execution loop, task gates, tracking, commits
- **[steps/invoke-executor.md](references/steps/invoke-executor.md)** — How to invoke the executor agent
- **[steps/invoke-reviewer.md](references/steps/invoke-reviewer.md)** — How to invoke the reviewer agent
- **[task-normalisation.md](references/task-normalisation.md)** — Normalised task shape for agent invocation
- **[tdd-workflow.md](references/tdd-workflow.md)** — TDD cycle (passed to executor agent)
- **[code-quality.md](references/code-quality.md)** — Quality standards (passed to executor agent)
