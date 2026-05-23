---
name: plan:findings:create
description: Retroactively create findings for a plan by reviewing completed phases. Use when findings weren't recorded during implementation and need to be extracted after the fact.
allowed-tools: Bash(git log:*), Bash(git diff:*), Bash(git show:*)
---

# Plan Findings Create Skill

Retroactively extract findings from completed plan phases when findings weren't recorded during implementation.

## Process

1. **Identify the target plan:**

   - If the user provides a plan number (e.g., `/plan:findings:create 0018`), use that plan directly
   - If no number is provided, scan for in-progress plans:
     - Look for `plans/*/task-list.md` files (exclude `plans/archive/`)
     - Check which plans have completed tasks but no `findings/` directory (or sparse findings)
     - If one plan qualifies, use it
     - If multiple plans qualify, list them and ask the user to choose
     - If no plans qualify, check `plans/archive/` and offer those

2. **Gather implementation context:**

   Read the plan's state to understand what was done:
   - Read `implementation-plan.md` for the intended approach
   - Read `task-list.md` to identify completed phases and tasks
   - Read `.plan-state.json` for:
     - `commits` array — commit SHAs from completed phases
     - `last_session_notes` — notes about what happened
     - `current_task` — where work stopped
   - Read task files in `tasks/` for what was planned vs. what may have changed

3. **Review commits for each completed phase:**

   For each commit SHA in `.plan-state.json`:
   - Run `git log --format='%H %s' <sha>` to get the commit message
   - Run `git diff <sha>~1..<sha> --stat` to see what files changed
   - Run `git diff <sha>~1..<sha>` to review the actual changes
   - Compare changes against what the task files specified

   If no commits are recorded but tasks are checked off:
   - Use `git log --oneline` to find likely commits by message pattern (`feat(plan-NNNN)`)
   - Review those commits instead

4. **Identify findings by comparing plan vs. reality:**

   For each completed task/phase, look for:

   - **Diversions:** Code that differs from what the task file specified. Why did the approach change?
   - **Discoveries:** Unexpected behavior encountered. New understanding of how the code works.
   - **Plan errors:** Tasks that assumed something incorrect. Missing steps that had to be improvised.
   - **TODOs:** Comments with `TODO`, `FIXME`, `HACK`, or `WORKAROUND` in the committed code.
   - **Cleanup items:** Code that works but could be improved. Temporary scaffolding left in place.
   - **Notes:** Important context that future work should know about.

   Also search the committed code:
   - Grep for `TODO`, `FIXME`, `HACK`, `WORKAROUND`, `XXX` in changed files
   - Look for commented-out code or temporary implementations
   - Check test files for `#[ignore]` or `@skip` markers

5. **Present findings to the user:**
   ```
   **Plan:** `plans/NNNN-feature-name/`
   **Phases reviewed:** N completed phases (M commits)
   **Findings identified:** K total

   | # | Finding | Type | Phase/Task | Source |
   |---|---------|------|------------|--------|
   | 1 | [Short title] | diversion | Phase 2 / Task 2.1 | Commit abc1234 |
   | 2 | [Short title] | todo | Phase 3 / Task 3.2 | TODO in src/foo.rs:42 |
   | 3 | [Short title] | discovery | Phase 1 / Task 1.3 | Commit def5678 |

   Should I write these as finding files in `plans/NNNN-name/findings/`?
   You can adjust, add, or remove findings before I write them.
   ```

6. **Wait for user approval** before writing findings.

7. **Write finding files:**

   - Create `plans/NNNN-name/findings/` directory if it doesn't exist
   - Write each finding as an individual markdown file
   - Use descriptive filenames: `findings/todo-cleanup-unused-helpers.md`
   - Follow the standard finding format:

     ```markdown
     # Finding: Short Title

     **Type:** discovery | diversion | plan-error | note | todo | cleanup
     **Task:** 2.1
     **Date:** YYYY-MM-DD
     **Source:** Commit abc1234 | TODO in src/foo.rs:42 | Observed during review

     ## Details
     [What was found/changed/wrong]

     ## Impact
     [How this affects the current plan or future work]

     ## Action Items
     - [ ] Concrete next step (if any)
     ```

8. **Report results:**
   ```
   **Findings written:** N files in `plans/NNNN-name/findings/`

   - findings/diversion-changed-routing-approach.md
   - findings/todo-cleanup-unused-helpers.md
   - findings/discovery-diamond-attachment-behavior.md

   Run `/plan:findings:resume NNNN` to triage these into issues and research.
   ```

## When to Use This Skill

- A plan has completed phases but no `findings/` directory
- You finished implementing and forgot to record findings along the way
- You want to do a retrospective review of what changed vs. what was planned
- Before archiving a plan, to capture learnings

## Example Output

---

**Plan:** `plans/0018-lr-rl-remaining-fixes/`
**Phases reviewed:** 3 completed phases (3 commits)
**Findings identified:** 4 total

| # | Finding | Type | Phase/Task | Source |
|---|---------|------|------------|--------|
| 1 | Router needed separate LR/RL backward path | diversion | Phase 2 / Task 2.1 | Commit 9b85567 |
| 2 | `render_edge` has TODO for multi-segment labels | todo | Phase 3 / Task 3.2 | TODO in src/render/edge.rs:187 |
| 3 | Plan assumed waypoints always ordered top-to-bottom | plan-error | Phase 2 / Task 2.3 | Commit 7b7e7f0 |
| 4 | Diamond attachment points need rank-aware sorting | discovery | Phase 1 / Task 1.2 | Commit 0d66d6c |

Should I write these as finding files in `plans/0018-lr-rl-remaining-fixes/findings/`?

---
