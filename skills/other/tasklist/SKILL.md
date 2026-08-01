---
name: tasklist
description: Maintain a project's canonical TASKS.md or an opted-in studio portfolio task register with permanent IDs, ownership, lifecycle dates, and source provenance. Use to list, add, update, complete, or cancel tasks, view tasks across registered projects, or import selected action items from project artifacts. Do not use for planning the work itself or silently turn every proposed action into a task.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# /as:tasklist — Canonical Project or Studio Task Register

Own exactly one resolved `TASKS.md`: either a project's register or an opted-in studio portfolio register. Give every action a permanent identity, explicit lifecycle, and traceable source. This skill manages actions; `/as:workplan` may define future work, but it is neither required nor invoked implicitly.

## Usage

```text
/as:tasklist list
/as:tasklist add Coordinate reflected ceiling plan with electrical — owner: Sam — due: 2026-08-03
/as:tasklist update T0012 owner: Priya due: 2026-08-07
/as:tasklist complete T0012
/as:tasklist cancel T0014 reason: superseded by T0018
/as:tasklist import meetings/YYYY-MM-DD-owner-review.md#A3
```

## Hard rules

1. **One canonical register.** Read and write only the register returned by canonical context resolution. Project mode uses the selected project's `TASKS.md`; portfolio task mode uses the studio-root `TASKS.md`. They are never simultaneously writable for the same studio.
2. **Permanent identity.** IDs use `T0001`, `T0002`, and so on. Never delete, reuse, or renumber an ID. Allocate `max(all parseable IDs) + 1`, including completed and cancelled rows; gaps stay gaps.
3. **Preserve history.** Updating or closing a task keeps its ID, source, created date, and earlier lifecycle events. Append a dated history entry; do not erase the prior state.
4. **No silent promotion.** A plan unit, meeting action, site follow-up, or decision consequence remains a proposal until the user selects it for import. Preview candidates before mutation.
5. **Provenance is exact.** In project mode, file sources are project-relative. In portfolio mode, store a studio-relative link beginning with the selected registered project path so the link resolves from the studio register. Every source includes a stable heading/item ID, or uses the canonical direct-instruction token `conversation:YYYY-MM-DD#instruction-N`. Never invent a file or persist an absolute machine path.
6. **No silent duplicates.** Normalize a source within the selected project, then compare Project ID (in portfolio mode), normalized source path, and exact source item together. For conversation instructions, compare Project ID when applicable plus the complete canonical token. That normalized provenance key is the deduplication key. If it already exists, show `link`, `update`, or `new` and wait for the user's choice.
7. **Malformed means blocked, not empty.** Preserve a malformed register byte-for-byte. Report the path and parse problem, and block every mutation until the user authorizes repair. Listing may report parseable content and the failure, but must not claim completeness.
8. **Harness neutral.** Cross-skill invocation, agents, git history, structured question tools, and `/as:workplan` are optional conveniences, never runtime requirements.

## Resolve canonical context

Resolve a typed target once before any operation. `/as:tasklist` with no arguments means `list`; do not require an argument and do not open a confirmation gate for a read-only list.

1. Run the shared resolver and follow `skills/project/references/context-resolution.md`. Its typed result and validated choices are authoritative; do not reimplement manifest or filesystem validation in prose.
2. If a project is resolved, read its Project ID. If an owning studio is also explicitly resolved, read `Task register` from `STUDIO.md` and confirm the project is a matching registered descendant:
   - `project` mode returns `project-register` at `<project-root>/TASKS.md`;
   - `portfolio` mode returns `portfolio-filter` at `<studio-root>/TASKS.md`, filtered to the Project ID.
   A standalone project with no owning studio uses project mode.
3. For `studio-picker`, select the sole choice or use one structured gate listing validated projects plus **All projects**. Do not ask the same question first in prose.
4. For `no-projects`, offer `/as:studio create-project`; for `no-context`, ask for a project/studio path or offer `/as:studio`; for `invalid`, stop. Never create a register at an inferred directory.

### All-project targets

- In project mode, **All projects** is a read-only merged view of each eligible project's `TASKS.md`. Validate each register independently, preserve local IDs, and display them as `<project-id>:<task-id>` (for example `2401:T0007`). Never persist the merged view or renumber a task.
- In portfolio mode, **All projects** is the unfiltered studio-root register. A selected project is a Project ID filter on that same file.
- An add/import from an all-project view must first select one eligible project. An update/complete/cancel in project mode must resolve one exact `<project-id>:TNNNN` and mutate only that project's register. A read-only merged view itself is never a mutation target.

## Register contract

Create `TASKS.md` only after a valid target has been resolved and the first mutation is previewed and confirmed. Project mode uses bundled `templates/tasks.md`; portfolio mode uses `templates/portfolio-tasks.md`. Resolve templates relative to this skill's own directory. If bundled-resource resolution is unavailable, reproduce the applicable schema rather than searching unrelated installed copies.

The task table has these required columns:

| Field | Contract |
|---|---|
| ID | Permanent `TNNNN` identifier |
| Description | One observable action |
| Owner | Named person, role, or `Unassigned` |
| Due | `YYYY-MM-DD` or `—` |
| Status | `open`, `in-progress`, `blocked`, `completed`, or `cancelled` |
| Created | `YYYY-MM-DD` |
| Updated | `YYYY-MM-DD` |
| Completed | `YYYY-MM-DD` or `—` |
| Cancelled | `YYYY-MM-DD` or `—` |
| Source | Canonically relative Markdown link with an exact heading/stable item ID, or `conversation:YYYY-MM-DD#instruction-N` |
| Related | Optional plan-unit or decision link, otherwise `—` |

The portfolio schema adds `Project ID` immediately after `ID`. Every value must match one eligible active or on-hold project in the current studio manifest. File links are relative to the studio register and begin with that project's registered path; validation also confirms they remain within that project. Portfolio task IDs remain permanent across the studio; project-filtered views never change them.

Lifecycle history lives under `## History`, one append-only bullet per change:

```markdown
- 2026-07-21 — T0007 created as `open` from source item `meetings/YYYY-MM-DD-owner-review.md#A3`.
- 2026-07-23 — T0007 owner changed from Sam to Priya; status changed from `open` to `in-progress`.
- 2026-07-28 — T0007 completed.
```

Treat missing required columns, duplicate IDs, invalid IDs or statuses, unparseable required dates, or a task row whose Source is neither a valid project-relative item link nor a valid canonical conversation token as malformed. Do not normalize or rewrite such a file without authorization.

## Operations

### List

1. Resolve the target, then read and validate the entire canonical register or every register in a read-only merged view.
2. Show tasks grouped by project when more than one project is visible, then by status, preserving ID order. Apply user filters for project, owner, due date, or status when supplied.
3. In a project-mode merged view, qualify each ID as `<project-id>:<task-id>` and label missing or malformed registers independently; one malformed project must not make another project appear empty.
4. Report malformed content explicitly. Listing is read-only.

### Add

1. Require one resolved project identity even when writing the portfolio register. Parse the requested description, owner, due date, source, and optional related link. Ask only for missing information that materially changes the task; `Unassigned`, `—`, and the current date are valid explicit defaults. For a direct instruction with no file source, allocate the next unused `conversation:YYYY-MM-DD#instruction-N` token for that date and show it in the preview.
2. Validate the full register and run the normalized source-path plus source-item duplicate check.
3. Preview the exact proposed row. Wait for confirmation.
4. Allocate the next monotonic ID, append the row, and append its creation history event.

### Update

1. Require an existing task ID and show its current values.
2. Preview field changes. Do not change ID, Created, Source, Completed, or Cancelled through a routine update.
3. On confirmation, change only selected mutable fields, set Updated to today, and append a history event naming old and new values.
4. Updating a completed or cancelled task preserves its closure date and history. Reopening is a separate explicitly confirmed lifecycle change; never clear historical closure dates.

### Complete

1. Show the selected task and preview `Status: completed`, `Updated: today`, and `Completed: today`.
2. On confirmation, preserve all identity and provenance fields, apply those values, and append a completion history event.
3. If already completed, report it without rewriting. A cancelled task requires explicit reopen approval before completion.

### Cancel

1. Require a short cancellation reason and show the selected task.
2. Preview `Status: cancelled`, `Updated: today`, and `Cancelled: today`.
3. On confirmation, preserve all identity and provenance fields and append the reason to the cancellation history event.
4. If already cancelled, report it without rewriting. Never delete the row.

## Confirmed import

Imports may read any user-specified artifact. Common sources are `plans/`, `meetings/`, `site-reports/`, and `decisions/`, but none is required.

1. Read the named source and identify candidate actions without changing `TASKS.md`.
2. Label candidates by their existing stable item ID. If the source has no stable item ID, propose one or cite the nearest heading plus an unambiguous item label; do not fabricate a false anchor.
3. Preview description, owner, due date, normalized source path/item, and optional plan-unit or decision link for every candidate.
4. Ask the user to select individual candidates. “Import all” is allowed only when the preview is visible and the user explicitly confirms it.
5. Before appending each selected candidate, compare the normalized project-relative source path plus exact source item against every task, regardless of status.
6. For a match, show the existing ID and offer:
   - **link** — keep the existing task and report its ID;
   - **update** — preview authorized mutable-field changes to that task;
   - **new** — create a distinct task only after the user confirms why it is separate.
7. Validate again, allocate IDs monotonically, append only confirmed rows, and record an import history event for each.

If direct invocation of another skill is unavailable, preserve the source and print the exact `/as:tasklist import <path>#<item>` command. Never claim an import occurred without reading the resulting `TASKS.md`.

## Repair boundary

When `TASKS.md` is malformed:

1. Stop all add, update, complete, cancel, and import mutations.
2. Report each detectable problem and retain the original file.
3. Offer a repair preview that shows every proposed change.
4. Repair only after explicit authorization. Prefer the smallest correction; never renumber IDs, delete rows, or infer missing lifecycle facts.
5. If a required fact cannot be recovered, keep the original row in a clearly labeled quarantine section and ask the user how to resolve it.

## Completion response

After a mutation, re-read the canonical register and report the project identity, affected permanent IDs, resulting statuses, and source links relative to the owning project or studio as appropriate. After a read-only operation, state that no files changed.
