---
name: hammer
description: Automated implement-review-iterate loop using nested teams delegation. Use when delegating any task that should reach 10/10 quality without manual coordinator babysitting. Spawns a worker-leader that manages the full fix-review cycle autonomously, reporting back only when done or after max iterations. Invoke with "hammer", "hammertime", or "use hammer".
---

# Hammer

Automated quality loop. Delegates a worker-leader that hammers away at an implement-review-iterate cycle until the work reaches 10/10 or max iterations (10) are exhausted. The main coordinator only hears back when it's done.

## Architecture

```
Main Agent (you)
  |-- delegates --> Loop Coordinator (worker-leader, hasTools: true)
       |-- delegates --> Implementer (sub-worker, shares worktree)
       |   |-- implements, tests, commits
       |-- delegates --> Reviewer (sub-worker, shares worktree)
       |   |-- reviews code, writes review TICKET with score in frontmatter
       |-- reads review ticket frontmatter
       |   score < 10? --> new Implementer with changes_requested
       |   score = 10 + no changes? --> DONE, report back
```

## When to Use

- Delegating any task that should meet high quality standards
- Work that benefits from independent review (a different agent reviews than implements)
- When the coordinator should not be bothered with iteration details

## How to Use

### Step 1: Prepare the Task

Gather the full task description and all requirements. Be explicit and complete -- the loop coordinator passes these verbatim to its sub-workers.

### Step 1.b: Announce Hammertime

`read` the `./hammertime.png` image.

### Step 2: Delegate the Loop Coordinator

Read the loop coordinator prompt template at `references/loop-coordinator-prompt.md` (relative to this skill directory). Fill in the placeholders and delegate:

```
teams({ action: 'delegate', tasks: [{
  text: <filled loop coordinator prompt>,
  assignee: '<descriptive-name>',
  hasTools: true
}]})
```

`hasTools: true` gives the loop coordinator the `teams` tool so it can spawn implementer and reviewer sub-workers.

### Step 3: Wait

The loop coordinator manages everything internally:
- Spawns an implementer for the task
- Spawns a reviewer after implementation completes
- Reads the review ticket, checks the score
- Loops (up to 10 iterations) if score < 10
- Reports back via team_comment when done

### What Comes Back

The loop coordinator's final note contains:
- Final review score
- Number of iterations taken
- Review ticket ID (for the passing review)
- Summary of what was implemented

If max iterations are exhausted without reaching 10/10, it reports the best score achieved and the last review ticket so the main agent can decide what to do.

## Prompt Templates

All prompt templates live in `references/` relative to this skill directory:

- `references/loop-coordinator-prompt.md` -- the worker-leader prompt (fill in placeholders)
- `references/reviewer-prompt.md` -- used by the loop coordinator when spawning reviewers

Placeholders in the loop coordinator prompt:

| Placeholder | Description |
|---|---|
| `{{TASK_DESCRIPTION}}` | Full task with all requirements |
| `{{WORKING_DIRECTORY}}` | Absolute path to the working directory |
| `{{ADDITIONAL_CONTEXT}}` | Codebase conventions, related files, etc. |
| `{{MODEL_IMPLEMENTER}}` | (optional) Model for implementer workers |
| `{{MODEL_REVIEWER}}` | (optional) Model for reviewer workers |

## The Review Ticket Contract

The reviewer writes a tk ticket with structured YAML frontmatter. This is the contract between reviewer and loop coordinator -- no text parsing, just frontmatter fields:

```yaml
---
id: p-xxxx
status: closed
type: task
tags: [review, 4step]
score: 8
changes_requested:
  - "Missing null check in auth.ts:45"
  - "No test for token expiry edge case"
---
# Review: <task> (iteration 2)

## Suggest Fixing
...
## Possible Simplifications
...
```

The loop coordinator reads `.tickets/<id>.md` and checks:
- `score: 10` AND `changes_requested: []` --> done
- Anything else --> feed `changes_requested` back to a new implementer

## Key Design Decisions

- **Review as ticket**: Score and feedback in YAML frontmatter. No regex, no text parsing.
- **No GitHub**: Purely local. No PRs, no GitHub API.
- **Separate agents**: Implementer and reviewer are different agents for objectivity.
- **Cleanup cascade**: Worker-leader death kills all sub-workers automatically.
- **`hasTools` flag**: Teams extension feature that gives a worker the `teams` tool for sub-delegation. Default is `false`; only the loop coordinator needs `true`.
