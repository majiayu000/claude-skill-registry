---
name: speci5.implement
description: "Implement a story's tasks and acceptance criteria from .spec/features/. Reads plan.md tasks and story.md acceptance criteria, then implements them using worktree isolation. Supports two modes: default (single agent, sequential) and sub-agent (parallel agents per task). WHEN: /implement, implement story, build story, execute plan, implement tasks, code the story, develop story, run implementation, implement feature. DO NOT USE FOR: brainstorming ideas (use brainstorm), writing specs (use specify), creating plans (use plan), checking implementation (use check)."
argument-hint: "<path-to-story-folder> [--mode default|sub-agent]  e.g. .spec/features/user-auth/login-with-email --mode sub-agent"
---

# Implement

Read a story's plan and acceptance criteria, then implement all tasks using worktree-isolated agents.

## Triggers

Activate this skill when the user wants to:
- Implement a planned story
- Execute the tasks in a `plan.md`
- Build out a feature story end-to-end
- Run implementation against a spec

## Hard Gate

Do NOT modify `story.md`, `feature.md`, or create new spec/idea files. This skill ONLY writes source code (and updates `plan.md` checkboxes on completion).

## Arguments

Parse the user's arguments:

- **Story path** (required): path to the story folder, e.g. `.spec/features/user-auth/login-with-email`
- **`--mode`** (optional, default: `default`): implementation mode
  - `default` — one agent implements all tasks sequentially in a single worktree
  - `sub-agent` — one agent per task, all running in parallel, each in their own worktree

If no story path is given, check if the user mentioned one in the conversation, or ask for it.

## Steps

### 1. Read the spec

Load these files from the story folder:
- `story.md` — acceptance criteria and context
- `plan.md` — ordered task checklist

If `plan.md` doesn't exist, tell the user to run `/speci5.plan` first and stop.

Extract:
- The list of **unchecked tasks** from `plan.md` (`- [ ] ...`)
- The **acceptance criteria** from `story.md`

If all tasks are already checked, report that the story appears complete and offer to run `/speci5.check` to verify.

### 2. Confirm before implementing

Show the user:
- Story title and number of tasks to implement
- Mode that will be used
- A brief summary of what will happen

Then proceed (no need to wait for explicit confirmation unless something looks wrong).

### 3. Implement

Dispatch to the appropriate mode.

---

#### Mode: `default` (single agent, sequential)

Spawn **one** Agent with `isolation: "worktree"` containing the full implementation prompt.

The agent should:
1. Read `story.md` and `plan.md`
2. Implement each unchecked task in order
3. After all tasks are done, verify acceptance criteria by reading/running relevant code
4. Update `plan.md` checkboxes for completed tasks
5. Commit all changes with a clear message referencing the story

**Agent prompt template:**
```
You are implementing the story at: <story-path>

## Your goal
Implement all unchecked tasks in plan.md, satisfying the acceptance criteria in story.md.

## Files to read first
- <story-path>/story.md
- <story-path>/plan.md

## Instructions
1. Read both files above.
2. For each unchecked task (- [ ]) in plan.md, implement it. Work through them in order — earlier tasks often set up foundations for later ones.
3. Follow existing code conventions: check nearby files for naming patterns, import styles, test structure.
4. After implementing all tasks, verify against each acceptance criterion in story.md. Do a quick sanity check — read the key files you wrote and confirm they address the criteria.
5. Update plan.md: mark completed tasks as - [x].
6. Commit all changes with message: "feat: implement <story-title>\n\nImplemented via speci5.implement"

## Constraints
- Do NOT modify story.md or feature.md.
- Do NOT add code beyond what the tasks require (YAGNI).
- If a task is ambiguous, use the acceptance criteria to guide your interpretation.
- If you hit a genuine blocker (missing dependency, unclear spec), note it in plan.md and skip that task rather than guessing.
```

---

#### Mode: `sub-agent` (parallel agents per task)

Spawn **one Agent per unchecked task**, all in the **same turn** (parallel), each with `isolation: "worktree"`.

Each agent gets a focused prompt for its single task.

**Per-task agent prompt template:**
```
You are implementing a single task from the story at: <story-path>

## Story context
Read <story-path>/story.md for acceptance criteria and overall context.
Read <story-path>/plan.md for the full task list — understand where your task fits.

## Your task
<task-text>

## Instructions
1. Read story.md and plan.md.
2. Implement ONLY the task listed above. Do not implement other tasks.
3. Follow existing code conventions in the project.
4. Write focused, minimal code — only what is needed for this task.
5. Commit your changes with message: "feat(<story-slug>): <task-text-summary>"

## Constraints
- Do NOT modify story.md, feature.md, or plan.md.
- Do NOT implement tasks other than the one assigned to you.
- If this task depends on something that doesn't exist yet (e.g., a function another agent is creating), implement it yourself or stub it clearly.
```

After all agents complete:
1. Collect the branch names returned from each agent's worktree
2. Merge all branches into the current branch (resolve conflicts conservatively — prefer additive merges)
3. Update `plan.md`: mark all successfully implemented tasks as `- [x]`
4. Commit the merge and plan update

> **Note on sub-agent mode:** Because each agent works in isolation, tasks that depend on each other's output may need stubs or may produce minor conflicts. The merge step should reconcile these. If conflicts are complex, prefer sequential (`default`) mode.

### 4. Report results

After implementation completes, print a summary:

```
## Implementation Complete: <Story Title>

Mode: <default|sub-agent>
Tasks implemented: X/Y

### Completed
- ✅ Task description

### Skipped / Blocked
- ⚠️ Task description — reason

### Next step
Run `/speci5.check .spec/features/<feature>/<story>` to verify the implementation against acceptance criteria.
```

If in sub-agent mode, also note any merge conflicts that were resolved or left for the user.

## Output Format

See [output template](./assets/output.md).
