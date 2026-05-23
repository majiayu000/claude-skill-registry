---
id: 010
title: Add esper:yolo skill for automated phase implementation
status: done
type: feature
priority: 2
phase: 001-polish-and-publish
branch: feature/phase-1
created: 2026-02-18
shipped_at: 2026-02-18
pr: merged-to-main
---

# Add esper:yolo skill for automated phase implementation

## Context

The current workflow requires manual intervention between each plan: run `/esper:build`, then `/esper:commit`, then `/esper:ship`, then repeat for the next plan. For phases with many small plans, this is repetitive. YOLO mode automates the full loop — implement every pending plan in the current phase sequentially, committing at milestones, and opening the phase PR when all are done.

This is aligned with the constitution's "vibe coding toolkit for Claude Code power users" goal. It does NOT violate the "one AI, one plan, one PR at a time" principle — plans are still processed one at a time; there is just no pause between them. No multi-agent orchestration; one Claude Code session working sequentially.

The auto-commit-at-milestones approach is the key differentiator from simply calling `/esper:build` in a loop: YOLO commits after each logical Approach step group so the git history stays readable even for long sessions.

Existing patterns to follow:
- `skills/esper-build/SKILL.md` — plan selection, branch creation, activation, implementation, verification, Progress update
- `skills/esper-ship/SKILL.md` — archiving, pushing, phase PR logic (Step 4–7)
- All feature plans share branch `feature/phase-1`, so branch already exists after the first plan

## Approach

1. Create `skills/esper-yolo/SKILL.md` with the following steps:

**Step 1 — Check setup**
- Verify `.esper/esper.json` exists; stop if not
- If there is already an active plan in `.esper/plans/active/`, read its title and ask: "Include it as the first plan in YOLO, or skip it and only run pending plans?"
  - Include: add it to the front of the queue (don't move it — it's already active)
  - Skip: leave it active, only run pending plans after it

**Step 2 — Load phase queue**
- Read all `.md` files in `.esper/plans/pending/` where `phase:` matches `current_phase` from `esper.json`
- Sort by `priority` (ascending), then `id` (ascending)
- If queue is empty and no active plan is included: print "No pending plans for this phase." and stop
- Show the ordered list: `#<id> — <title> (p<priority>)`

**Step 3 — Confirm YOLO**
- Use `AskUserQuestion` to confirm: "YOLO mode will implement N plans automatically, committing at milestones, and open the phase PR when done. Proceed?"
- If declined: stop gracefully

**Step 4 — For each plan in queue (loop)**

  **4a. Branch**
  - Read `branch:` from plan frontmatter (all feature plans share `feature/<current_phase>`)
  - If branch doesn't exist: `git checkout -b <branch>`
  - If branch exists: `git checkout <branch>`
  - If checkout fails: stop the entire YOLO run and report error

  **4b. Activate**
  - If this plan is not already active (i.e., it was pending): move from `pending/` → `active/`, set `status: active`
  - If already in `active/` (the pre-existing active plan from Step 1): skip the move

  **4c. Read context**
  - Read the active plan file (full content), `.esper/CONSTITUTION.md`, and `.esper/phases/<current_phase>.md`

  **4d. Implement with milestone commits**
  - Follow the plan's **Approach** section step by step
  - After each logical group of Approach steps is complete (e.g., after creating a file, after wiring up a module, after writing tests), run a milestone commit **without pausing for user approval**:
    ```
    feat: <what was just implemented>

    Plan: #<id> — <title> (milestone)
    ```
  - Stage only files related to the current plan's changes (`git add <specific files>`)
  - Keep the plan file as a living document — update Approach/Files to change if something unexpected is found
  - Do NOT add features beyond what the plan describes

  **4e. Verify**
  - Run verification steps from the plan's **Verification** section
  - Run `commands.test`, `commands.lint`, `commands.typecheck` from `esper.json` (skip if empty)
  - If any verification fails: **STOP the entire YOLO run**. Report which plan failed and what went wrong. Do NOT proceed to the next plan. The user must fix and re-run.

  **4f. Update Progress**
  - Add or update `## Progress` section in the active plan file

  **4g. Archive**
  - Move plan from `active/` → `done/`, update `status: done`, `shipped_at: <today>`
  - Commit the archive:
    ```
    chore: archive plan #<id> — <title>
    ```
  - Stage: `git add .esper/plans/done/<filename> .esper/plans/active/<filename>`

  **4h. Continue to next plan** (back to 4a)

**Step 5 — Push**
- After all plans are archived: `git push -u origin <branch>`
- If push fails: report the error; do not open PR

**Step 6 — Open phase PR**
- Use the same logic as `esper:ship` Step 7:
  - Read all plans where `phase:` matches `current_phase`
  - If any plans remain in `pending/` or `active/` (i.e., not all phase plans are done): print how many remain and skip PR
  - If all phase plans are in `done/`:
    - Collect all feature-type plans for the PR body
    - Open the phase PR targeting `main` with title, phase goal, shipped plans list, and acceptance criteria from the phase file
    - Print the PR URL
    - Update each feature plan's `pr:` field in `done/` with the PR URL

**Step 7 — Done**
- Report: total plans shipped, PR URL (or "N plans remain, no PR opened yet")
- Suggest `/esper:backlog` if plans from other phases exist

## Files to change

- `skills/esper-yolo/SKILL.md` (create — new skill implementing the steps above)

## Verification

- Run: manual (install via `node bin/cli.js`, confirm `esper-yolo` appears in `~/.claude/skills/`)
- Expected: skill is discoverable as `/esper:yolo`; on a project with 3 pending feature plans it implements them in priority order, commits at milestones, archives each, and opens the phase PR
- Edge cases:
  - No pending plans → graceful stop, clear message
  - Verification fails mid-run → stop immediately, do not proceed to next plan; leave the failed plan in `active/` so the user can fix and re-run (or use `/esper:continue`)
  - Branch already exists (common — all phase features share a branch) → checkout, don't error
  - Mix of fix and feature plans in pending → YOLO only processes the current phase; fix-type plans with a different branch would require a branch switch; skip them and note to user (or warn and ask)
  - Active plan already exists when YOLO starts → ask user to include or skip (Step 1)

## Progress

- Created `skills/esper-yolo/SKILL.md` with 7-step workflow: check setup → load queue → confirm → implement loop (branch, activate, read, implement+commit, verify, progress, archive) → push → phase PR → done
- Auto-commit on milestone design: stages specific files only, no `git add -A`, commit message format `feat: ... Plan: #id — title (milestone)`
- Fail-loudly on verification: stops entire run, leaves failed plan active for `/esper:continue` recovery
- Phase PR logic mirrors `esper:ship` Step 7 exactly
- Modified: skills/esper-yolo/SKILL.md (created)
- Verification: passed — `node bin/cli.js` shows `+ esper-yolo`, skill installed at `~/.claude/skills/esper-yolo/SKILL.md`, discoverable as `/esper:yolo`
