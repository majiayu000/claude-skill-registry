---
name: timetracker
description: Reconstruct daily or weekly project work from dated plans, decisions, meetings, site reports, tasks, and other artifacts, then append user-confirmed manual entries to TIMELOG.md. Use for "log my time," "what did I work on," daily timesheets, or weekly time reconstruction. Never infer hours, start/stop times, billing status, or completeness from activity signals.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# /as:timetracker — Evidence-Based Manual Time Tracking

Reconstruct defensible work descriptions from project evidence, ask the user for every duration, preview the proposed rows, and append confirmed entries to one project-level `TIMELOG.md`.

## Usage

```text
/as:timetracker today
/as:timetracker yesterday
/as:timetracker this week
/as:timetracker 2026-07-13 through 2026-07-17
/as:timetracker correct E0012: this was 1.5 hours, not 2.0
```

## Hard rules

1. **Evidence suggests descriptions, never duration.** Never infer hours, start or stop times, billing status, billable category, or completeness from artifact counts, commit counts, timestamp spans, modification times, task status, or meeting duration.
2. **Every duration comes from the user.** Candidate rows always show a blank Hours field. Require a positive user-supplied decimal duration for every selected row before preview or append.
3. **Preview before mutation.** Show the exact rows, including IDs, dates, decimal hours, descriptions, sources, and any correction reference. Append only after explicit confirmation.
4. **Append only.** Never edit, delete, reorder, renumber, or reuse an existing entry. Corrections are new rows that reference the original entry.
5. **Keep permanent identity.** IDs use `E0001`, `E0002`, and so on. Allocate the next ID as the highest parseable existing E-number plus one, including corrective entries.
6. **Cite the trail.** Store project-relative Markdown source links. Preserve all distinct relevant sources when several artifacts support one description.
7. **Do not equate activity with a complete timesheet.** Report the paths and evidence channels inspected. A quiet or unreadable source means unknown, not no work.
8. **Preserve malformed logs.** If `TIMELOG.md` cannot be parsed reliably, report the problem and stop before mutation. Do not silently replace or repair it.

## Resolve the project root

Before discovery or logging, resolve one project root:

1. Search upward from the current directory for the nearest `PROJECT.md` or established project marker, in this shared order: `meetings/`, `site-reports/`, `decisions/`, `plans/`, `docs/plans/`, `TASKS.md`, `TIMELOG.md`, `CLAUDE.md`, `AGENTS.md`, `.claude/`, `.codex/`.
2. When git is available, treat `git rev-parse --show-toplevel` as the outer search boundary, not the automatic winner. A nearer marker inside a monorepo takes precedence.
3. Prefer an existing `PROJECT.md` over other markers at the same level. If genuinely conflicting candidates remain, show both project-relative candidates and ask one target question.
4. If no marker or git root exists, use the current directory and state that assumption.

Resolve the root once. `TIMELOG.md`, discovery, and all persisted source links use this root. Git is optional; the workflow must still operate when the project is not a repository or git history is unavailable.

## Step 1 — Resolve the requested period

Interpret a day, week, or explicit inclusive date range in the user's local time. Show the resolved dates before discovery. If the request omits a period, ask for one rather than assuming.

## Step 2 — Read the existing log

Read `<project-root>/TIMELOG.md` when it exists. Otherwise prepare to create it from the bundled template after the user confirms the first append.

Validate existing rows before continuing:

- Each entry has one unique `E0001`-style ID, work date, positive decimal hours, description, and at least one source link.
- A corrective entry identifies the original as `Corrects E####` and does not change that original row.
- Previously used IDs remain permanent even if a row is disputed.

Build an index of normalized project-relative source paths and any headings or stable item IDs already cited. Use it to detect evidence that may already have been logged.

## Step 3 — Discover candidate evidence

Search only within the requested period and relevant project root. Inspect:

- `plans/*.md` and `docs/plans/*.md`
- `decisions/*.md`
- `meetings/*.md`
- `site-reports/*.md`
- `TASKS.md`
- `PROJECT.md`
- Other project artifacts with explicit created, event, work, completed, or updated dates

Use this evidence hierarchy for the candidate work date:

1. **High confidence — explicit artifact date.** Prefer a semantic date inside the artifact: meeting or visit date, work date, created date, completed date, or an explicitly recorded updated date.
2. **Supporting evidence — git history.** When available, use commits to discover or corroborate work in the period. A commit date never overrides a different explicit artifact event date and never supplies elapsed time.
3. **Low confidence — filesystem modification time.** Use mtime only when no explicit date or useful git evidence exists. Label the candidate `low confidence — filesystem mtime` and ask the user whether it belongs in the period.

An artifact publication or edit date may differ from when the described work occurred. Prefer the most semantically relevant explicit date and make ambiguity visible.

Report every search path inspected and every path that could not be parsed. Do not collapse parse failure into “no evidence.”

## Step 4 — Build and deduplicate candidates

Create concise descriptions of observable work, not claims about effort or completion. Group evidence into one candidate when sources describe the same work event, topic, task ID, plan unit, meeting action, or decision. Preserve all supporting source links in the grouped candidate.

Do not merge merely because artifacts share a date. Keep distinct work as distinct candidates. Do not split one linked activity into multiple rows to inflate detail.

Compare candidates with the existing source index:

- Exclude or clearly flag a source already represented by an entry in `TIMELOG.md`.
- Show the existing E-ID beside the candidate.
- If the user performed additional work related to that source, require an explicit new description and new duration. Reusing a source is never proof of additional time.

Present the draft with blank durations:

| Select | Work date | Draft description | Hours | Confidence | Sources | Existing entry |
|---|---|---|---:|---|---|---|
| [ ] | YYYY-MM-DD | ... | _(required)_ | explicit artifact date | source path + item | — |

Ask the user which candidates to log, how many hours belong to each selected row, and any description changes. Meeting duration may appear in the source, but must never prefill Hours.

## Step 5 — Validate user-supplied entries

For every selected candidate:

- Require a work date in `YYYY-MM-DD` within the requested period, unless the user explicitly corrects the period.
- Require a finite positive decimal number of hours supplied or explicitly confirmed by the user.
- Require a specific work description and one or more project-relative sources.
- Reject blank, zero, negative, inferred, or merely suggested durations.
- Do not convert a meeting's scheduled length, timestamps, commit span, or filesystem activity into hours.

Ask for missing values; do not append a partial row.

## Step 6 — Preview and append

Allocate sequential permanent IDs and show the exact Markdown rows to be appended. Ask for explicit confirmation. On confirmation:

1. Create `TIMELOG.md` from `templates/timelog.md` if it does not exist.
2. Append the confirmed rows to the end of the Entries table in ID order.
3. Do not change any pre-existing row or infer that the resulting log is a complete accounting of the period.
4. Report the appended IDs and the inspected evidence paths.

If confirmation changes any field, render a new preview before writing.

## Correcting an entry

For `/as:timetracker correct E####`:

1. Read and show the original row.
2. Ask for the corrected work date, decimal hours, description, and reason, deriving nothing beyond unchanged fields the user explicitly confirms.
3. Allocate a new permanent E-ID.
4. Preview a new row whose Correction field says `Corrects E#### — {reason}`.
5. Append it after confirmation. Never edit or delete E####.

The original and correction remain in the audit trail. Do not calculate net billing or totals unless the user separately specifies the accounting rule.

## Bundled template

Resolve `templates/timelog.md` relative to the loaded `skills/timetracker/SKILL.md` when the harness exposes that location. On Claude Code, `${CLAUDE_PLUGIN_ROOT}/skills/timetracker/templates/timelog.md` is the fallback. If the bundled resource cannot be resolved, create the exact table contract documented below rather than searching unrelated filesystem locations.

Required entry columns, in order:

```text
ID | Work date | Hours | Description | Sources | Correction
```

Use `—` when an appended entry is not a correction. This skill is harness-neutral: structured questions, git, subagents, and other named tools are optional enhancements, not runtime requirements.

## Cross-skill handoffs

- `/as:workplan`, `/as:project`, `/as:meeting-minutes`, `/as:site-visit-report`, and `/as:tasklist` own their respective source records. `/as:timetracker` reads and links them; it never rewrites them.
- A candidate description that reveals missing future work can be handed to `/as:tasklist`, but time logging does not create a task automatically.
- A work description is not a durable project fact or decision. Use `/as:project remember` or `/as:project record-decision` explicitly when promotion is warranted.
