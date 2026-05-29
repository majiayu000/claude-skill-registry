---
name: Make WPs
description: Queue next Work Package(s) from an ideaâ€™s backlog (tasks â†’ work_packages.md), without modifying tasks.md
argument-hint: "<IDEA_ID> [N|MVP|V1|Full|Later|EPIC-###|FEAT-###|WP-####] ...  (examples: IDEA-0003_my-idea 2 | IDEA-0003_my-idea MVP | IDEA-0003_my-idea EPIC-003)"
disable-model-invocation: true
---

# VibeForge â€” Queue Next Work Packages from Backlog (Tasks â†’ WPs)

Generate and enqueue the next Work Package(s) in the per-idea board:

- `docs/forge/ideas/<IDEA_ID>/latest/work_packages.md`

From the canonical backlog:

- `docs/forge/ideas/<IDEA_ID>/latest/tasks.md`

This command ONLY selects tasks and appends WP entries; it must never modify the backlog tasks.

---

## Invocation

Call with an idea folder id first:

- `/into-wps <IDEA_ID> [filters...]`

Examples:

- `/into-wps IDEA-0003_my-idea` â†’ enqueue 1 WP (default)
- `/into-wps IDEA-0003_my-idea 3` â†’ enqueue up to 3 new WPs
- `/into-wps IDEA-0003_my-idea MVP` â†’ only queue tasks with `release_target: MVP`
- `/into-wps IDEA-0003_my-idea EPIC-003` â†’ only queue tasks under an epic
- `/into-wps IDEA-0003_my-idea FEAT-014` â†’ only queue tasks under a feature
- `/into-wps IDEA-0003_my-idea WP-0007` â†’ force-create next WP id starting at WP-0007 (rare)

Argument parsing rules (best-effort):

- `$1` = IDEA_REF (required)
- Remaining tokens in `$ARGUMENTS` may include:
  - a count `N` (integer)
  - a release filter `MVP|V1|Full|Later`
  - `EPIC-###` and/or `FEAT-###` filters
  - a forced starting id `WP-####`

If IDEA_REF is missing, STOP and ask the user to provide it.

---

## Resolve IDEA_ID (required)

Before using any paths, resolve the idea folder:

- Call `vf.resolve_idea_id` with `idea_ref = $1`
- Store the returned `idea_id` as `IDEA_ID`
- Use `IDEA_ID` for all paths, YAML headers, and run log entries

---

## Inputs (Auto)

Per-idea WP board (target):

- `docs/forge/ideas/<IDEA_ID>/latest/work_packages.md` (create if missing)

Idea backlog (canonical):

- `docs/forge/ideas/<IDEA_ID>/latest/tasks.md` (required)

## Optional Inputs (Auto if present)

For better titles/context (do not derive tasks from these):

- `docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md` (preferred; fallback to features.md if backlog missing)
- `docs/forge/ideas/<IDEA_ID>/latest/features.md` (fallback if backlog missing)
- `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (preferred; fallback to epics.md if backlog missing)
- `docs/forge/ideas/<IDEA_ID>/latest/epics.md` (fallback if backlog missing)
- `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md`

---

## Output (Auto)

Append WP entries into:

- `docs/forge/ideas/<IDEA_ID>/latest/work_packages.md`

No other files are modified by this command.

If you cannot write to the file directly, output the exact text block(s) that should be appended.

---

## Step 0 â€” Read context and compute queue state

1) Open `docs/forge/ideas/<IDEA_ID>/latest/work_packages.md` and parse existing WPs:

- WP ids
- Status (`Queued`, `In Progress`, `Blocked`, `Done`, etc.)
- Referenced Task IDs (`TASK-###`) if present
- Any explicit dependencies and verify commands

If the file does not exist, treat as empty and create it with a minimal header:

```md
# Work Packages â€” <IDEA_ID>

(append new WPs below)
```

2) Compute:

- Next WP id = (max existing WP number + 1), unless a forced starting id is provided
- Task IDs already referenced by any existing WP (any status) to avoid duplicates

3) If there are already 4+ WPs with status `Queued`, STOP and report:

- â€œQueue is already full; execute or plan queued WPs first.â€
- List the currently queued WP ids.

---

## Step 1 â€” Read and index the backlog (tasks.md)

1) Open `docs/forge/ideas/<IDEA_ID>/latest/tasks.md`.
2) Parse the canonical YAML block at the top (preferred). If missing, fall back to parsing the Markdown rendering.
3) Build an in-memory list of tasks with fields (best-effort):

- `task_id` (TASK-001)
- `feature_id` (FEAT-014)
- `epic_id` (EPIC-003)
- `title`
- `description`
- `release_target` (MVP/V1/Full/Later)
- `priority` (P0/P1/P2)
- `estimate` (S/M/L)
- `dependencies` (task ids, if present)
- `tags` (backend/frontend/infra/qa/etc., if present)

4) Apply optional filters from remaining args:

- Release filter: MVP/V1/Full/Later
- Epic filter: EPIC-###
- Feature filter: FEAT-###

If the backlog file is missing, STOP and report the expected path.

---

## Step 2 â€” Find eligible candidate tasks

Eligible tasks are tasks that:

- exist in `tasks.md`
- are NOT already referenced by any existing WP
- are not obviously blocked by missing dependencies (best-effort)

Preference order (unless filters override):

1) `release_target: MVP` first, then V1, then Full, then Later
2) Within a release target:
   - priority P0 â†’ P1 â†’ P2
   - group by `epic_id` then `feature_id`
   - smaller estimates first (S then M then L), unless dependency chains require ordering

Dependency-aware selection (best-effort):

- If a task lists dependencies that are not already in any WP (any status) and not included in the current WP batch, treat it as blocked and skip.
- If dependencies are missing/unknown, be conservative: pick fewer tasks per WP.

If no eligible tasks are found, STOP and report why.

---

## Step 3 â€” Form appropriately sized Work Packages (WP batching heuristics)

Goal: small, focused WPs.

Default WP sizing targets:

- 3â€“8 tasks per WP (bias toward smaller counts unless tasks are tiny)
- Total effort per WP ~ 1â€“3 days (best-effort)
  - Heuristic points: S=1, M=2, L=4; aim for 4â€“8 points per WP

Batching heuristics (priority order):

1) Keep WPs within the same `feature_id` when possible.
2) If a feature is too large, allow spanning within the same `epic_id`, but keep it tight.
3) Prefer related tasks only if they share the same epic/feature (IDs alone are not a guarantee).
4) Avoid mixing unrelated tags (e.g., deep infra + UI polish) unless tasks are explicitly coupled.
5) Stop early if you hit a task that clearly depends on missing prerequisites.
6) If uncertain, create smaller WPs.

When a count `N` is provided:

- Repeat batching up to N times, removing selected tasks from the candidate pool each time.

---

## Step 4 â€” Draft WP metadata

For each WP batch selected:

1) WP Title (short, readable):

- Prefer: `<EPIC title> â€” <Feature title> (slice)` if `features_backlog.md`/`epics_backlog.md` are available (fallback to `features.md`/`epics.md` if backlog missing)
- Otherwise: derive from dominant `feature_id`/`epic_id` + common tags
- Keep it human-scannable

2) Goal sentence:

- Outcome-oriented: what completing the WP enables.

3) WP Task list:

- List included Task IDs and task titles.

4) Plan Doc path (reference only; created later by a planning command):

- `docs/forge/ideas/<IDEA_ID>/planning/WPP-0001-WP-XXXX_TASK-AAA-BBB_<short_slug>.md`
  - `WPP-0001` is an incrementing plan-doc id local to the idea (best-effort).
  - `TASK-AAA-BBB` = numeric range (min/max) of included tasks
  - Slug: short + stable (e.g., `orchestration_api_slice`, `ui_control_panel_basics`)

5) Status:

- `Queued`

6) Dependencies (best-effort):

- If tasks depend on other tasks not already covered by any WP (any status) and not included in this WP, list them at WP level.
- Otherwise: `None`

7) Verify commands (best-effort defaults):

- Default: `pytest`
- If clearly frontend-only: include `npm test` or minimal build if known
- If unclear: keep only `pytest`

8) Traceability:

- Include `Idea-ID: <IDEA_ID>` in the WP entry so WPs are traceable back to the idea.

---

## Step 5 â€” Append to work_packages.md

Append each new WP section at the end.

Recommended WP entry format:

```md
## WP-XXXX â€” <Title>

- Status: Queued
- Idea-ID: <IDEA_ID>
- Release: MVP|V1|Full|Later
- Tasks:
  - TASK-001 â€” <title>
  - TASK-002 â€” <title>
- Goal: <goal sentence>
- Dependencies: None | WP-XXXX | TASK-YYY
- Plan Doc: docs/forge/ideas/<IDEA_ID>/planning/WPP-0001-WP-XXXX_TASK-AAA-BBB_<slug>.md
- Verify: pytest (and any extras)
```

---

## Step 6 â€” Output next actions

Print:

- New WP id(s) and tasks selected
- Plan Doc path(s)
- Suggested next step (e.g., â€œRun your WP planning command for WP-XXXXâ€)

---

## Non-negotiable Rules

- Never modify or rewrite the canonical backlog in `docs/forge/ideas/<IDEA_ID>/latest/tasks.md`.
- Never enqueue tasks already referenced by any existing WP (any status).
- Keep WPs small and focused; default to 1 WP if no count is provided.
- Do NOT mark tasks complete here.
- Prefer conservative batching when dependencies are unclear.
- Do not invent tasks; only select tasks that exist in `tasks.md`.

