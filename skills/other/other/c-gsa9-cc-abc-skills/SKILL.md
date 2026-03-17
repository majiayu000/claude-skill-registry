---
name: c
description: "ONLY when user explicitly types /c. Never auto-trigger on execute, run, or implement."
---

# /c - Execute Plan via Subagents

Execute blueprint.md by dispatching phases to subagents. Main thread orchestrates only.

**Designed for fresh session** — no prior context needed. blueprint.md contains everything.

**Execution model:** All-or-nothing. A git checkpoint is created before any phase runs. If anything fails, the user resets to the checkpoint — no partial recovery, no resume.

## Orchestrator Rules

Main thread is a **lightweight dispatcher**:
- Reads blueprint.md ONCE at start
- Stores only: phase numbers, dependencies, parallel groups, titles
- Dispatches subagents via Task tool (general-purpose)
- Reports 1-line progress per phase

Main thread **NEVER**:
- Executes tasks directly
- Reads files beyond blueprint.md
- Accumulates subagent details in its own context

## Execution Flow

```
1. CHECKPOINT
   - Run: git add -A && git commit -m "checkpoint before run" && git push
   - Store the commit hash (git rev-parse HEAD)
   - This commits everything including blueprint.md — the safety net

2. LOAD
   - Read blueprint.md, verify marker <!-- @blueprint: /b ... -->
   - Parse phases overview table (deps, groups, titles)

3. EXECUTE LOOP
   While phases remain:
   a. Find ready phases (deps satisfied, not done)
   b. Batch by parallel group:
      - All ready in same group → ONE message with MULTIPLE Task calls (parallel)
      - NEVER mix different groups in parallel
   c. Dispatch subagent(s) — one Task call per phase
   d. On ANY failure: STOP, jump to FAILURE
   e. Log: "✓ Phase N: [title]"

4. ON SUCCESS
   - Delete blueprint.md
   - Run: git add -A && git commit -m "run complete: [Goal field from blueprint.md]" && git push
   - Store the final commit hash
   - Report: "Run complete. N/N phases succeeded. Committed & pushed: <short-hash>"

5. ON FAILURE — see Failure Protocol below
```

## Failure Detection

A phase has failed when:
- The Task tool itself errors (agent crash, timeout)
- The subagent explicitly reports it could not complete a task

## Failure Protocol

On any failure:

```
╔══════════════════════════════════════════════════════════════════╗
║  PLAN FAILED — RESET TO CHECKPOINT RECOMMENDED                 ║
║                                                                 ║
║  Checkpoint: <hash> (committed at start of this session)        ║
║                                                                 ║
║  To recover:                                                    ║
║    git reset --hard <hash>                                      ║
║    git push --force                                             ║
║                                                                 ║
║  This discards ALL changes from this run and restores           ║
║  the codebase with blueprint.md intact for a clean re-run.      ║
╠══════════════════════════════════════════════════════════════════╣
║  Failed: Phase N — [error summary]                              ║
║  Completed before failure: Phases X, Y, Z                       ║
║  Not started: Phases A, B, C                                    ║
╚══════════════════════════════════════════════════════════════════╝
```

**Do NOT suggest partial recovery, resuming, or fixing in place.** Propose the reset. If the user wants to keep partial changes, that's their call.

## Subagent Dispatch

Each subagent receives ONLY:

**First parallel group** — full context:
```markdown
# Context
Goal: [1-2 sentences from blueprint.md Goal field]
Rationale: [from blueprint.md Rationale section]
Working directory: [absolute path]

# Your Assignment: Phase N
[EXACT phase section copied from blueprint.md]

# Instructions
1. Read the Reference files FIRST — understand patterns before writing code
2. Execute all tasks in order
3. RESPECT Guardrails — these are hard constraints, not suggestions
4. Stay within Modifies scope — do not touch files outside it
5. On failure: stop immediately, return error details
6. Return 1-2 sentence summary of what was done
```

**Later parallel groups** — lighter context:
```markdown
# Context
Goal: [1-2 sentences from blueprint.md Goal field]
Working directory: [absolute path]
Follow patterns in CLAUDE.md and Reference files.

# Dependencies
[Verbatim dependency notes from blueprint.md, e.g.:]
- Depends: 2 (creates lib/core.py)

# Your Assignment: Phase N
[EXACT phase section copied from blueprint.md]

# Instructions
1. Read the Reference files FIRST — understand patterns before writing code
2. Execute all tasks in order
3. RESPECT Guardrails — these are hard constraints, not suggestions
4. Stay within Modifies scope — do not touch files outside it
5. On failure: stop immediately, return error details
6. Return 1-2 sentence summary of what was done
```

## Progress Output

```
/c

Checkpoint created: abc1234
Loading blueprint.md... N phases, M parallel groups

Group A:
  ✓ Phase 1: [title]

Group B (parallel):
  ✓ Phase 2: [title]
  ✓ Phase 3: [title]
Group C:
  ✓ Phase 4: [title]

Run complete. N/N phases succeeded. Committed & pushed: abc1235
```

## Constraints

- NEVER modify blueprint.md during execution
- NEVER execute tasks directly — always delegate via Task tool
- Minimal orchestrator context — 1 line per completed phase
- Same parallel group only — never cross-group parallel
- Fail-fast: stop on first failure, recommend checkpoint reset
- On success: delete blueprint.md, commit and push
- All-or-nothing: no resume, no partial recovery
