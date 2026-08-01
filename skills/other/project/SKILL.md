---
name: project
description: Create or maintain an Architecture Studio project — initialize its record bundle, remember sourced facts, capture or supersede decisions, inspect project status, or migrate a 1.x PROJECT.md. Use when the user says “set up the project,” “remember this,” “we decided,” asks about project context, or runs /as:project.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# /as:project — Project Setup and Memory

`/as:project` is the only project-memory interface. It owns current facts in `PROJECT.md` and durable reasoning in `decisions/*.md` without combining those record types or duplicating a decision index.

## Commands

```text
/as:project init
/as:project status
/as:project update
/as:project remember <information>
/as:project decisions
/as:project record-decision <choice>
/as:project supersede <number>
/as:project migrate
```

## Hard boundaries

1. `PROJECT.md` contains sourced current facts. Decision identity, status, rationale, and history live only in `decisions/*.md`.
2. `PROJECT.md` links to `decisions/` but has no Decisions table and never copies decision metadata.
3. Never write `STUDIO.md`. `/as:studio` alone owns the manifest.
4. Never create a nested project beneath an existing `PROJECT.md`.
5. Every durable mutation is previewed and requires affirmative confirmation.
6. Preserve malformed records. A parse failure means unknown, not absent or approved.
7. Use project-relative links; never persist machine-specific absolute paths.

## Resolve the project root

Run `${CLAUDE_PLUGIN_ROOT}/skills/project/scripts/resolve-context.sh` from the current or explicitly supplied directory and follow `references/context-resolution.md`. `PROJECT.md` is the only implicit project boundary. A nearer project inside a monorepo wins over outer repository metadata; typed-record directories, task/time files, Claude instructions, git roots, and the current directory never establish a project. Stop on `invalid`; use the validated picker for `studio-picker`; and never write before one exact project is resolved.

## `/as:project init`

1. If the current path resolves an existing `PROJECT.md`, show status and do not create a nested project.
2. If a `STUDIO.md` is resolved, route creation to `/as:studio create-project`. Do not mutate the studio manifest and do not call back recursively after `/as:studio` has begun its confirmed orchestration.
3. Outside a studio, ask whether to initialize a studio or create a standalone project. Standalone creation requires explicit confirmation.
4. Gather the project name, optional ID, and exact target. Normalize the directory to lowercase kebab-case, prefixing a supplied ID. When no ID is supplied, use the folder slug as the stable local ID. Reject unsafe names, separators, dot segments, control characters, existing files, and non-empty directories. Never silently suffix a project identity.
5. Preview the exact path and full bundle. State that no git repository, ALPA account, or cloud service will be created.
6. After confirmation, run `${CLAUDE_PLUGIN_ROOT}/skills/project/scripts/project-workspace.sh init <target> <name> <project-id> project` and verify every file and directory. Standalone projects always use a project-local task register; portfolio mode belongs to a studio.
7. Report the exact created path and `.claude/skills/` extension path. Explain that Claude Code should be started or restarted from the intended project directory if new project-only skills are not visible.

## `/as:project status`

Read `PROJECT.md`, scan `decisions/*.md` directly, and summarize known facts, record counts, decision statuses, open tasks, and recent dated records. If an owning `STUDIO.md` declares portfolio task mode, read open tasks for this Project ID from the studio-root register; otherwise read the project register. Report duplicate decision numbers or malformed files. Do not consult or create a decision index.

## Facts: `update` and `remember`

Every fact has a value, source, and date. Update an existing fact in place; append only genuinely new facts to the correct section. Git or the file-sharing system preserves history.

For `/as:project remember` or a natural memory request:

1. Read the exact input and relevant project records.
2. Classify each item as fact-like, decision-like, or mixed:
   - fact-like states a current, sourceable project condition;
   - decision-like expresses a choice, selection, rejection, approval, or rationale;
   - mixed contains separable facts and choices.
3. Preview grouped destinations. Facts show the `PROJECT.md` section, value, source, and date. Decisions show the proposed decision record.
4. Ask which grouped changes to apply. Confirmation of a source record is not authorization to promote every candidate.
5. Write only selected items, then re-read and verify.

When importing a selected item from minutes or a site report, require its exact project-relative path and stable item label. Read it and preserve its epistemic status. Reported, discussed, interpreted, proposed, or uncertain content cannot silently become a verified fact.

## Decisions

### `/as:project decisions`

Discover `decisions/*.md` independently. Report number, title, status, and path for each parseable record, plus duplicate numbers, missing/unrecognized statuses, and malformed files. Filenames and files are canonical; no `PROJECT.md` table participates.

### `/as:project record-decision`

1. Scan every decision filename. Allocate max parseable number + 1, zero-padded to four digits; never reuse a number because another record is malformed.
2. Capture one choice per record: context, at least two honestly stated options, status (`proposed` or `decided`), deciders, the call, consequences, and source links. Pull from conversation first and ask one grouped question only for missing pieces.
3. A proposed source item remains proposed unless the user affirmatively says the choice was made.
4. Preview the complete record and collision-free path. Wait for confirmation.
5. Write `decisions/NNNN-slug.md`, re-read it, and verify number, status, title, and backlinks. Do not update `PROJECT.md` with decision metadata.

### `/as:project supersede <number>`

1. Resolve exactly one parseable decided record. Stop on missing, ambiguous, malformed, or already-superseded records.
2. Allocate a replacement normally. Preview the complete new record and the old record’s single status change together.
3. After confirmation, create and verify the replacement first; only then change the old status to `superseded by NNNN` and verify both cross-links.
4. On a later failure, preserve the verified replacement, report the exact partial state, and offer recovery against those records. Never allocate another replacement number for recovery.

## `/as:project migrate`

Migration removes the legacy Decisions table only when it is lossless:

1. Read `PROJECT.md` and discover all decision files.
2. Parse every legacy table row conservatively and match it to exactly one decision file by number plus compatible identity/status.
3. Missing files, duplicate numbers, malformed rows, or status disagreements block mutation. Report exact rows and paths.
4. If every row is accounted for, preview replacing the entire legacy section/table with the stable `decisions/` link while preserving all unrelated content byte-for-byte.
5. After confirmation, run the helper migration, re-read `PROJECT.md`, and verify the table is gone, the link exists, and all decision files are unchanged.
6. A project already using the link-only contract reports “already migrated” without mutation.

## Typed record handoffs

- Minutes and site reports may propose selected facts or decisions; `/as:project` re-reads and confirms them.
- `/as:workplan` reads facts and decision files but writes only its plan.
- `/as:tasklist` owns task rows in the canonical project or portfolio `TASKS.md`; `/as:studio` alone owns the studio task-mode setting; `/as:timetracker` owns `TIMELOG.md`.
- Project registration state and archive belong to `/as:studio`, not `/as:project`.

## Collaboration and harness boundary

These are plain local files shared however the project already is. This local plugin creates no ALPA account or server. Cross-skill invocation and structured questions are enhancements; when unavailable, preserve completed work and print the exact follow-up command.
