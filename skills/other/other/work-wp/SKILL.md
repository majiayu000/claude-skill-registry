---
name: Execute WP
description: Execute a Work Package (WP) from an ideaâ€™s latest/work_packages.md (auto-picks next Queued, or runs a specific WP id)
argument-hint: "<IDEA_ID> [WP-####]   (examples: IDEA-0001-my-idea | IDEA-0001-my-idea WP-0002 | WP-0002)"
disable-model-invocation: true
---

# Work Package Execution Assistant (Idea-Scoped, Backlog-Driven)

Execute development iteratively using **Work Packages (WPs)** as the driver.

This command must NOT ask for a feature name or plan doc path up front â€” it must discover the next unit of work automatically from the idea-scoped WP board:

- `docs/forge/ideas/<IDEA_ID>/latest/work_packages.md`

Supports optional arguments:

- `/work-wp IDEA-0002-my-idea` â†’ run the next `Queued` WP for that idea
- `/work-wp IDEA-0002-my-idea WP-0002` â†’ run a specific WP for that idea
- `/work-wp WP-0002` â†’ best-effort: locate the WP by scanning all ideas (only if unique)

Use `$ARGUMENTS` for the optional IDEA_ID and/or WP id.

---

## Resolve IDEA_ID (required)

Before using any idea-scoped paths:

- If `$ARGUMENTS` starts with `IDEA-`, treat the first token as `IDEA_REF`.
- Call `vf.resolve_idea_id` with `idea_ref = IDEA_REF` and store `IDEA_ID`.
- Use `IDEA_ID` for all paths, YAML headers, and run log entries.

---

## Inputs (Auto)

### Canonical sources of truth (idea-scoped)

- `docs/forge/ideas/<IDEA_ID>/latest/work_packages.md` (near-term execution queue)
- `docs/forge/ideas/<IDEA_ID>/planning/` (per-WP plan docs; created if missing)
- `docs/forge/ideas/<IDEA_ID>/latest/tasks.md` (canonical task definitions; required)

### Optional context (read-only, if present)

- `docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md` (preferred; fallback to features.md if backlog missing)
- `docs/forge/ideas/<IDEA_ID>/latest/features.md` (fallback if backlog missing)
- `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (preferred; fallback to epics.md if backlog missing)
- `docs/forge/ideas/<IDEA_ID>/latest/epics.md` (fallback if backlog missing)
- `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md`
- `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md`
- `docs/forge/ideas/<IDEA_ID>/inputs/idea.md`

### Progress tracking (per-idea)

- `docs/forge/ideas/<IDEA_ID>/manifest.md` (status index; preferred for task/WP status)
- `docs/forge/ideas/<IDEA_ID>/run_log.md` (append-only run log)

---

## Step 0 â€” Safety & Repo Context

1) Read current repo state:

- `git status -sb`
- `git diff --stat`

2) If there are unrelated uncommitted changes:

- Ask the user to confirm whether to stash/commit before proceeding.
- Do NOT proceed blindly.

---

## Step 1 â€” Resolve IDEA_ID and target WP

### Accepted invocation forms

**Form A (recommended):** `$ARGUMENTS` starts with `IDEA-...`

- Parse:
  - `IDEA_REF = first token`
  - Optional `WP_ID = second token` if it matches `WP-####`
  - Resolve `IDEA_ID` by calling `vf.resolve_idea_id` with `idea_ref = IDEA_REF`

**Form B (best-effort):** `$ARGUMENTS` is only `WP-####`

- Scan all idea folders under `docs/forge/ideas/` for a `latest/work_packages.md` containing that WP id.
- If exactly one match is found, set `IDEA_ID` to that folder.
- If zero matches: STOP and report â€œWP not found in any idea.â€
- If multiple matches: STOP and list candidates; ask the user to rerun with explicit `IDEA_ID`.

If neither an IDEA_ID nor a WP_ID can be determined, STOP and ask the user to rerun.

---

## Step 1.1 â€” Confirm idea-scoped files exist

Expected paths:

- `docs/forge/ideas/<IDEA_ID>/latest/work_packages.md` (create if missing, but usually should exist)
- `docs/forge/ideas/<IDEA_ID>/latest/tasks.md` (required)
- `docs/forge/ideas/<IDEA_ID>/planning/` (create if missing)
- `docs/forge/ideas/<IDEA_ID>/manifest.md` (create if missing; best-effort)
- `docs/forge/ideas/<IDEA_ID>/run_log.md` (create if missing; best-effort)

If `latest/tasks.md` is missing, STOP and report the expected path.

---

## Step 2 â€” Select the Work Package (WP)

1) Open:

- `docs/forge/ideas/<IDEA_ID>/latest/work_packages.md`

2) Determine target WP:

- If `WP_ID` is provided, locate that WP section.
- Else select the FIRST WP whose status is `Queued`.

3) If no `Queued` WP exists:

- Report â€œNo queued WPs found for <IDEA_ID>.â€
- Suggest running `/into-wps <IDEA_ID>` to enqueue new WPs.
- STOP.

4) Extract from the WP section (best-effort):

- WP id and title
- Status
- Idea-ID (should match <IDEA_ID> if present)
- Release target (if present)
- Task list (TASK-### ids + titles, if present)
- Goal
- Dependencies (WPs and/or TASK ids, if present)
- Plan Doc path
- Verify commands

5) If WP status is `Blocked`:

- Do not change anything automatically.
- Show blockers and ask if user wants to unblock or pick another WP.
- STOP.

6) If a specific WP id was provided and its status is NOT `Queued`:

- Continue only if status is `In Progress` (resume allowed).
- Otherwise STOP and report current status.

---

## Step 3 â€” Auto-update WP status to In Progress

Edit `docs/forge/ideas/<IDEA_ID>/latest/work_packages.md`:

- If status is `Queued`, set it to `In Progress`.
- Add sub-bullets under the WP:
  - `- Started: <YYYY-MM-DD HH:MM> (local)`
  - `- Branch: <current-branch>`

Do this BEFORE any code changes.

Also update `docs/forge/ideas/<IDEA_ID>/manifest.md` (best-effort):

- If the manifest tracks WPs: set this WP status to `In Progress`.
- For each task in the WP: set task status to `In Progress` only if it was previously `Proposed`/`Queued`.

If you cannot write files directly, output the exact edits to apply.

---

## Step 4 â€” Ensure WP Plan Doc Exists (or Create It)

Planning and execution can be performed in one command for simplicity.

1) Determine the Plan Doc path:

- Prefer the explicit `Plan Doc:` field in the WP entry.
- If missing, derive a default under:
  - `docs/forge/ideas/<IDEA_ID>/planning/WPP-<NEXT>-WP-XXXX_<slug>.md`

2) If the plan doc does not exist, create it.

Plan doc requirements:

- Title: `WP-XXXX â€” <name>`
- Goal (from work_packages.md)
- `Idea-ID: <IDEA_ID>`
- Task IDs included (explicit list)
- Ordered execution steps (task order)
- â€œDone meansâ€¦â€ section with verification commands
- A checkbox list mirroring the tasks for this WP
- â€œNotes / Decisionsâ€ section for anything learned mid-execution

The Plan Doc must reference TASK ids exactly (IDs unchanged).

---

## Step 5 â€” Build the Task Queue (Backlog-Driven)

1) Load the canonical backlog:

- `docs/forge/ideas/<IDEA_ID>/latest/tasks.md`
- Prefer parsing the canonical YAML block.

2) For each TASK referenced by the WP, extract:

- Title
- Description
- Acceptance criteria
- Dependencies (if present)
- Release target, priority, estimate, tags (if present)

3) Order the task queue (best-effort):

- Respect explicit `dependencies` between tasks.
- If dependencies are unknown, use the order listed in the WP plan doc (if present).
- If both exist and conflict, prefer explicit task dependencies and note the conflict in the plan doc.

4) If the plan doc has its own checkbox list:

- Treat it as the local execution checklist for this WP.
- Keep it consistent with the canonical tasks and update it as you go.

If any referenced TASK id cannot be found in `tasks.md`:

- Record a blocker in the plan doc and STOP (do not guess task definitions).

---

## Step 6 â€” Execute One Task at a Time (Iterative Loop)

For each task in the ordered queue:

### 6.1 â€” Preparation

- Identify relevant context:
  - feature/epic context (if `features_backlog.md`/`epics_backlog.md` exist; fallback to `features.md`/`epics.md` if backlog missing)
  - concept constraints/invariants (if `concept_summary.md` exists)
- Only update documentation if the change introduces NEW decisions or changes existing intent.

### 6.2 â€” Implement

- Make the smallest change that satisfies the taskâ€™s acceptance criteria.
- Keep modifications focused and reviewable.
- Prefer small commits; include TASK id(s) in commit messages.

### 6.3 â€” Verify (task-level)

- Run the most relevant verification for the task (unit tests, lint, minimal smoke if applicable).
- Capture key outputs (pass/fail + short error summary if fail).

### 6.4 â€” Update WP Plan Doc checkbox

- Mark the TASK item as complete in the WP plan doc ONLY after task-level verification passes.
- Add 1â€“3 sub-bullets:
  - key files changed
  - commands run to verify

### 6.5 â€” Update manifest (task status)

Update `docs/forge/ideas/<IDEA_ID>/manifest.md` (best-effort):

- Set task status to `Done` only when acceptance criteria are met AND task-level verification passed.
- Record `last_updated` and (optionally) `commit` reference(s).

### 6.6 â€” If blocked or failing

- If the task fails verification:
  - attempt a focused fix
  - re-run verification
- If still blocked:
  - record blocker in the WP plan doc under the task
  - proceed to Step 8 (Blocked handling)
  - STOP further execution

---

## Step 7 â€” WP-level Verification + Close Out

After all tasks in the WP are checked off in the plan doc:

1) Run the WP Verify commands from `latest/work_packages.md` (fallback: `pytest` if none listed).
2) If verification PASSES:
   - Update `docs/forge/ideas/<IDEA_ID>/latest/work_packages.md`:
     - set WP status to `Done`
     - add:
       - `- Verified: <commands>`
       - `- Completed: <YYYY-MM-DD HH:MM> (local)`
       - `- Commits: <short hashes or PR link if applicable>`
   - Update `docs/forge/ideas/<IDEA_ID>/manifest.md`:
     - ensure all tasks in the WP are marked `Done`
     - mark the WP record as `Done` (if WPs are tracked)
3) If verification FAILS:
   - do NOT mark WP as Done
   - keep WP status as `In Progress`
   - write a short failure summary under the WP (errors + next steps)
   - STOP

---

## Step 8 â€” Blocked Handling (Auto)

If execution is blocked:

1) Update `docs/forge/ideas/<IDEA_ID>/latest/work_packages.md`:

- set WP status to `Blocked`
- add:
  - `- Blocker: <short description>`
  - `- What is needed: <next action>`

2) Update `docs/forge/ideas/<IDEA_ID>/manifest.md` (best-effort):

- set WP status to `Blocked` (if WPs are tracked)
- set blocked task(s) status to `Blocked`
- record blocker notes

3) Propose the next Queued WP (if any) as the next iteration.

---

## Step 9 â€” End-of-Run Summary (Always)

Print a concise summary:

- WP executed (explicitly show WP id)
- Tasks completed (and which remain)
- Verification commands run + result
- Files/areas touched
- Next recommended WP (next Queued) OR blocker details if blocked

---

## Non-negotiable Rules

- Always use the idea-scoped `latest/work_packages.md` to select work (unless a WP id is provided).
- If a WP id is provided (e.g. `/work-wp WP-0040`), execute ONLY that WP (do not switch).
- Always use the idea-scoped `tasks.md` as canonical task definitions:
  - `docs/forge/ideas/<IDEA_ID>/latest/tasks.md`
- Automatically update WP status (Queued â†’ In Progress â†’ Done/Blocked) as part of this command.
- Only mark tasks `Done` after verification passes.
- Ask the user only when absolutely required (destructive conflict, ambiguous blocker, missing decision).

---

