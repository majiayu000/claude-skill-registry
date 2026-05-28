---
name: Execute Feature
description: Execute one feature (FEAT-XXX) at a time using docs/forge/ideas/<IDEA_ID>/latest/tasks.md as the source of truth. Creates a short workspace checklist and tracks progress so reruns continue automatically.
argument-hint: "<IDEA_ID> [FEAT-XXX]   (examples: IDEA-0001-my-idea | IDEA-0001-my-idea FEAT-003 | FEAT-003)"
disable-model-invocation: true
---

# Feature Execution Assistant (Idea-Scoped, Tasks-Driven)

Execute development iteratively using **Features (FEAT-XXX)** as the unit of work.

This command must NOT depend on `latest/work_packages.md`.
The canonical source of truth is the **feature-grouped tasks** in:

- `docs/forge/ideas/<IDEA_ID>/latest/tasks.md`

Supports optional arguments:

- `/work-feat IDEA-0002-my-idea` -> auto-pick the next not-yet-completed FEAT from tasks.md using the progress tracker
- `/work-feat IDEA-0002-my-idea FEAT-003` -> execute a specific feature
- `/work-feat FEAT-003` -> best-effort: locate the FEAT by scanning idea tasks (only if unique)

Use `$ARGUMENTS` for IDEA_ID and/or FEAT id.

---

## Resolve IDEA_ID (required)

Before using any idea-scoped paths:

- If `$ARGUMENTS` starts with `IDEA-`, treat the first token as `IDEA_REF`.
- Call `vf.resolve_idea_id` with `idea_ref = IDEA_REF` and store `IDEA_ID`.
- Use `IDEA_ID` for all paths, YAML headers, and run log entries.

---

## Inputs (Auto)

### Canonical sources of truth (idea-scoped)

- `docs/forge/ideas/<IDEA_ID>/latest/tasks.md` (required; feature-grouped task definitions)
- `docs/forge/ideas/<IDEA_ID>/latest/existing_solution_map.md` (context for existing code, update when necessary)
- `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md` (broader project context)

### Optional context

- `docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md` (fallback to features.md if missing)
- `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (fallback to epics.md if missing)
- `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md`
- `docs/forge/ideas/<IDEA_ID>/latest/existing_solution_map.md`
- `docs/forge/ideas/<IDEA_ID>/latest/codebase_context.md`
- `docs/forge/ideas/<IDEA_ID>/inputs/idea.md`

### Execution tracking (small, per-idea)

- `docs/forge/ideas/<IDEA_ID>/latest/feature_execution_progress.md` (create if missing; append-only)
- `docs/forge/ideas/<IDEA_ID>/planning/` (workspace checklists live here)
- `docs/forge/ideas/<IDEA_ID>/manifest.md` (optional best-effort)
- `docs/forge/ideas/<IDEA_ID>/run_log.md` (append-only)

---

## Step 0 - Safety & Repo Context

1) Read current repo state:
- `git status -sb`
- `git diff --stat`

2) If there are unrelated uncommitted changes:
- Ask the user to confirm whether to stash/commit before proceeding.
- Do NOT proceed blindly.

---

## Step 1 - Determine target FEAT

### Accepted invocation forms

**Form A:** `$ARGUMENTS` starts with `IDEA-...`
- Parse:
  - `IDEA_REF = first token`
  - Optional `FEAT_ID = second token` if it matches `FEAT-\d{3}`
  - Resolve `IDEA_ID` using `vf.resolve_idea_id`

**Form B:** `$ARGUMENTS` is only `FEAT-XXX`
- Scan all idea folders under `docs/forge/ideas/` for a `latest/tasks.md` containing that FEAT header.
- If exactly one match is found, set `IDEA_ID` accordingly.
- If zero matches: STOP and report "FEAT not found in any idea."
- If multiple matches: STOP and list candidates; ask the user to rerun with explicit `IDEA_ID`.

If no `FEAT_ID` was provided:
- Auto-select the next FEAT not marked complete in `latest/feature_execution_progress.md`.

### IMPORTANT: Do not scan the entire tasks.md
When selecting or executing a feature:
- Use targeted search within `latest/tasks.md` to locate the FEAT section header (e.g., `FEAT-003:` or `## FEAT-003`).
- Extract ONLY the tasks under that FEAT section.

If tasks.md format varies, adapt by finding a stable "feature header" pattern used in the file and extracting the block until the next feature header.

---

## Step 2 - Confirm required files exist

Required:
- `docs/forge/ideas/<IDEA_ID>/latest/tasks.md`

Create if missing:
- `docs/forge/ideas/<IDEA_ID>/latest/feature_execution_progress.md`
- `docs/forge/ideas/<IDEA_ID>/planning/`

If `latest/tasks.md` is missing, STOP and report the expected path.

---

## Step 3 - Build the Feature Workspace Checklist (short)

Create (or update) a checklist doc for this feature:

- `docs/forge/ideas/<IDEA_ID>/planning/FEC-<FEAT_ID>-workspace-checklist.md`

Checklist requirements (keep it short):
- Title: `<FEAT_ID> - <feature title>`
- Idea-ID and Run-ID
- A checkbox list of the tasks in this feature (TASK-### ids + titles)
- For each task: 1-2 bullets:
  - key files expected to change (from existing_solution_map if available; otherwise best-effort)
  - verify command(s) (best-effort)
- "Notes / Decisions" section (append-only)

Do NOT create long plan docs. This is a working checklist.

---

## Step 4 - Mark Feature as In Progress (progress tracker)

Update `docs/forge/ideas/<IDEA_ID>/latest/feature_execution_progress.md`:
- If this FEAT is not present, add an entry:
  - `FEAT-XXX - In Progress - <timestamp> - run <RUN_ID> - checklist: planning/FEC-FEAT-XXX-workspace-checklist.md`
- If already present and In Progress, treat as resume.

---

## Step 5 - Execute Tasks One at a Time (Iterative Loop)

For each TASK in the feature's section (in dependency order if stated; otherwise file order):

### 5.1 - Preparation
- Use `existing_solution_map.md` if present to prefer extension of existing code.
- Do minimal, focused changes.
- Keep commits small; include `TASK-###` in commit messages.

### 5.2 - Implement
- Implement the smallest change meeting acceptance criteria.
- Avoid parallel implementations; extend existing components where possible.

### 5.3 - Verify
- Run the most relevant verification (unit tests/lint/smoke).
- If failing: attempt focused fix; re-run.

### 5.4 - Update checklist
In `planning/FEC-...-workspace-checklist.md`:
- Check off the task only after verification passes.
- Add 1-3 bullets:
  - files changed
  - commands run
  - anything learned

### 5.5 - If blocked
- Record blocker under that task in the checklist
- Update progress tracker to `Blocked` for this FEAT
- STOP

---

## Step 6 - Feature-level Close Out

After all tasks are checked:
1) Run a feature-level verification (best-effort):
   - run the main test suite subset relevant to changed areas
2) If passes:
   - Update progress tracker: `FEAT-XXX - Done - <timestamp> - run <RUN_ID>`
3) If fails:
   - Keep FEAT as In Progress
   - Record failure summary in checklist and STOP

---

## Step 7 - End-of-Run Summary (Always)

Print a concise summary:
- Feature executed: FEAT-XXX
- Tasks done vs remaining
- Verification commands run + result
- Key files touched
- Next recommended feature (next not-done FEAT)

---

## Required tool calls (MCP helpers)

- `vf.start_run` (idea_id=<IDEA_ID>, label="work-feat")
- `vf.write` to create/update:
  - `planning/FEC-<FEAT_ID>-workspace-checklist.md`
  - `latest/feature_execution_progress.md`
  - run snapshots under `runs/<RUN_ID>/...` (best-effort)
- `vf.append_log` with stage `execute.feature` and outputs

---

## Non-negotiable Rules

- Source of truth is `latest/tasks.md`.
- Execute exactly one feature per invocation.
- Do not read the full tasks.md; extract only the FEAT section being executed.
- Prefer extending existing code over creating parallel subsystems (use existing_solution_map when available).
- Only mark tasks done after verification passes.

