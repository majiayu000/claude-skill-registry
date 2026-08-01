---
name: meeting-minutes
description: Turn a meeting transcript, notes, or conversation into collision-safe, source-linked minutes in meetings/YYYY-MM-DD-slug.md. Use for project meeting records, attendance, discussion, stated information, decisions, action candidates, and open questions. Saving minutes never changes PROJECT.md, decisions/, or TASKS.md; promote only user-selected items afterward.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# /as:meeting-minutes — Typed Project Meeting Records

Create an auditable record of what occurred in a meeting without silently turning discussion into project facts, durable decisions, or assigned tasks.

## Usage

```text
/as:meeting-minutes from notes/owner-meeting.md
/as:meeting-minutes turn this transcript into minutes
/as:meeting-minutes revise meetings/2026-07-21-design-team.md
```

## Hard rules

1. **Minutes are an event record.** They record the meeting; they do not become the authority for current project facts, durable rationale, or task status.
2. **Save before promotion.** Complete and save the minutes before offering any follow-up. Saving must not create or modify `PROJECT.md`, `decisions/*.md`, or `TASKS.md`.
3. **Promote item by item.** Show separately labeled candidates and require the user to select each fact, decision, or task. A general request to save minutes is not promotion approval.
4. **Preserve epistemic status.** Discussion, stated information, confirmed decisions, proposed decisions, proposed tasks, and open questions remain separate. Do not upgrade a statement or proposal based on confident wording.
5. **Preserve dates and provenance.** Record the meeting's event date, the artifact creation date, and every source/input reference. Do not replace an event date with a transcript, file, commit, or modification timestamp.
6. **Never overwrite implicitly.** A filename collision creates a deterministic numeric suffix. Update an existing record only when the user explicitly requests a revision of that record.
7. **Use portable links.** Store project-relative Markdown paths, optionally with a heading or item label. Never persist machine-specific absolute paths.
8. **Do not fabricate gaps.** Unknown attendees, dates, owners, due dates, or outcomes stay `Unknown` or `Not recorded`. Ask only when a missing value materially changes the record.

## Step 1 — Resolve the project root

Run the shared resolver and follow `skills/project/references/context-resolution.md`. Resolve exactly one validated project before reading sources or choosing a target. A `studio-picker` result requires one structured project-selection gate; do not ask first in prose. Stop on `invalid`, `no-projects`, or `no-context`. Resolve all inputs, the meeting target, and links relative to the selected project.

## Step 2 — Establish the source and dates

Read the supplied transcript, notes, agenda, files, and relevant conversation. Preserve each source as a project-relative reference. If the source exists only in conversation, record `Current conversation (not separately archived)`; do not invent a file.

Determine independently:

- **Event date:** when the meeting occurred. Prefer an explicit date in the source or user request. Because it defines the canonical filename, ask when it is unavailable rather than substituting another timestamp.
- **Created date:** the calendar date on which these minutes are written.
- **Source date:** when a source identifies its own date. Preserve it alongside that source when it differs from the event date.

Never infer the event date from filesystem mtime or artifact creation time. Preserve conflicting dates as a visible limitation rather than silently choosing one.

## Step 3 — Structure the record

Extract only what the source supports and assign stable labels within the meeting:

- `S1`, `S2` — stated information: claims, updates, or representations made by a participant; not automatically verified project facts.
- `CD1`, `CD2` — confirmed decisions: choices the source clearly records as made. Confirmation in minutes still does not create a durable `/as:project record-decision` record.
- `PD1`, `PD2` — proposed decisions: options, recommendations, or choices still awaiting authorization.
- `T1`, `T2` — proposed tasks: actions discussed or assigned in the meeting. They are not canonical tasks until selected and added through `/as:tasklist`.
- `Q1`, `Q2` — open questions.

Keep ordinary discussion in a chronological or topic-based summary without promoting it to one of these sections. Attribute stated information and consequential discussion to a participant when the source supports attribution. Preserve `Unknown` rather than guessing.

A task candidate may include a proposed owner and due date, but label missing values `Unassigned` and `No due date`. Do not treat them as approved merely because the transcript uses imperative language.

## Step 4 — Write collision-safe minutes

Use:

```text
meetings/YYYY-MM-DD-<descriptive-slug>.md
```

Use the event date in the filename. If the event date is unknown, ask for it before writing because the canonical path requires a date.

Resolve and show the exact project-relative target. If it already exists:

- When the user explicitly asked to revise that exact record, preserve the original event date, **Created** date, and sources; set **Updated** to today and add a concise revision note.
- Otherwise preserve the existing file and choose the next available suffix: `-02`, `-03`, and so on. Check the suffixed path before writing. Never overwrite merely because the title and date match.

Resolve the bundled template relative to the loaded `skills/meeting-minutes/SKILL.md` when the harness exposes that path. On Claude Code, `${CLAUDE_PLUGIN_ROOT}/skills/meeting-minutes/templates/meeting-minutes.md` is the fallback. If bundled resources are unavailable, reproduce every section listed in Step 3 plus meeting metadata, attendance, agenda, sources, discussion, and limitations.

Write the minutes completely. Confirm the saved path. At this point, stop all mutation and verify that `PROJECT.md`, `decisions/`, and `TASKS.md` were not changed by the save operation.

## Step 5 — Preview optional promotions

After saving, present three separate candidate lists:

1. **Potential project facts:** selected `S#` items that may warrant verification and entry through `/as:project remember`.
2. **Durable decisions:** `CD#` or `PD#` items worth recording through `/as:project record-decision`, preserving whether each is decided or proposed.
3. **Canonical tasks:** `T#` items that may be imported through `/as:tasklist`.

Do not characterize every item as promotion-worthy. Explain that no downstream record has changed. Ask the user to select exact labels, for example `S2, CD1, T1`, or choose none. “Promote the useful items,” “continue,” or approval of the minutes as a whole is not item-level selection; ask for exact labels.

Before handing off a selected item, search the owning record for the same project-relative meeting link and item label. If a match exists, show it and offer link/update/new as appropriate; never silently duplicate it.

Each handoff must preserve a backlink to `meetings/YYYY-MM-DD-slug.md#<item-heading-or-label>` and must carry only selected items. Do not promote unselected siblings.

## Step 6 — Hand off without hard dependencies

When direct skill invocation is supported, invoke the owning skill once per selected record type and pass the saved meeting path plus exact labels. The destination skill owns its confirmation and mutation rules.

When direct invocation is unavailable, leave the minutes intact and print copyable commands in this exact form, substituting the actual path and selected labels:

```text
/as:project remember selected stated information S2 from meetings/2026-07-21-design-team.md; verify it as a project fact and preserve the source backlink
/as:project record-decision selected item CD1 from meetings/2026-07-21-design-team.md; preserve its decided status and source backlink
/as:tasklist import selected items T1, T3 from meetings/2026-07-21-design-team.md; preview duplicates and changes before writing
```

Print only the commands for item types the user selected. If nothing is selected, finish with the meeting record only.

## Professional boundary

Internal minutes that only document discussion do not require the professional disclaimer. Avoid converting participant statements into findings about code compliance, zoning compliance, occupancy, life safety, structural or MEP adequacy, concealed conditions, or environmental risk.

If the minutes include such analysis or any output the user might submit to a client or authority, append the canonical block below at the very end of the artifact. If uncertain whether the output will be submitted, include it.

> **Disclaimer:** This is an AI-generated analysis for preliminary planning purposes. All findings must be verified by a licensed professional before use in design, permitting, or regulatory submissions.

<!-- architecture-studio:requires-disclaimer -->
