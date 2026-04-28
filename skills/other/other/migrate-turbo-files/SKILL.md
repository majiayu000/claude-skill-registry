---
name: migrate-turbo-files
description: "Migrate legacy files in .turbo/ to current formats. Covers plans and shells (layout split, frontmatter normalization, prompt-plan index cleanup) and improvements.md (legacy `trivial`/`standard` Type values rewritten to `direct`/`plan`). Use when the user asks to \"migrate turbo files\", \"migrate turbo\", \"migrate turboplans\", \"migrate turbo plans\", \"upgrade plan format\", \"add frontmatter to plans\", \"convert old plans\", or \"migrate improvements\"."
---

# Migrate Turbo Files

Current layouts:

- Unexpanded shells live in `.turbo/shells/` with `spec:` and `depends_on:` frontmatter.
- Plans live in `.turbo/plans/` with `status:` (required) and optional `spec:` for provenance.
- `.turbo/improvements.md` entries use Type values `direct`, `investigate`, or `plan`. Legacy values `trivial` and `standard` map to `direct` and `plan` respectively.

This skill migrates legacy shapes to those layouts.

## Task Tracking

Use `TaskCreate` to create a task for each step:

1. Scan and classify existing files
2. Migrate prompt plan indexes
3. Process remaining files in `.turbo/plans/`
4. Normalize frontmatter on remaining plans
5. Migrate `improvements.md` Type values
6. Clean up and report

## Step 1: Scan and Classify Existing Files

Scan for all legacy shapes:

- **Prompt plan indexes** — Glob `.turbo/prompt-plans/*.md`. Also check for `.turbo/prompts.md` (oldest legacy format). Parse each index to determine whether prompts are inline (contain `### Prompt` sections with code blocks) or reference separate shell files (contain `**Shell:**` fields). Record the set of shell files each index references — Step 3 will skip these.
- **Files in `.turbo/plans/*.md`** — Read each file's first 20 lines and classify:
  - **Unexpanded shell** — has legacy `type: shell` frontmatter AND does not contain `## Pattern Survey`, OR has no frontmatter but contains `## Produces`, `## Consumes`, and `## Covers Spec Requirements` without `## Pattern Survey`. Target: `.turbo/shells/<filename>`.
  - **Expanded plan** — contains `## Pattern Survey` (with or without `<!-- Expanded from:` marker, with or without legacy `type: shell`). Target: stays in `.turbo/plans/`, frontmatter normalized.
  - **Regular plan** — no frontmatter or legacy `type: plan` frontmatter, not shell-shaped, no `## Pattern Survey`. Target: stays in `.turbo/plans/`, frontmatter normalized.
  - **Already-current plan** — has frontmatter with `status:` and no `type:`. Skip.
- **Files in `.turbo/shells/*.md`** — if they already have current frontmatter (no `type:`, no `status:`, just `spec:` and `depends_on:`), they're migrated. Otherwise, queue for normalization in Step 3.
- **`.turbo/improvements.md`** — read the file if it exists. Count entries whose `- **Type**:` line carries the legacy values `trivial` or `standard`. Queue these for rewriting in Step 5.

Report what was found: number of indexes, unexpanded shells in `.turbo/plans/`, expanded plans in `.turbo/plans/`, regular plans, already-current plans, already-current shells, and improvements entries with legacy Type values. If nothing needs migration, report and stop.

## Step 2: Migrate Prompt Plan Indexes

For each prompt plan index (including `.turbo/prompts.md` if present), parse:

- **Source** — spec path from the `Source:` field
- **Prompts** — each `## Prompt N:` entry with its Status, Depends on, and content

### Inline Prompts (Old Format)

Indexes where each prompt contains a `### Prompt` section with a code block of concrete instructions. These are equivalent to expanded plans, so migrate them to `.turbo/plans/`.

For each prompt entry:

1. Generate a slug: `<spec-slug>-NN-<title-slug>` from the spec filename and prompt number/title
2. If `.turbo/plans/<slug>.md` already exists with current frontmatter, skip this entry (collision)
3. Map the legacy status to a plan `status`: `done` → `done`, `pending` → `ready`, `in-progress` → `ready`
4. Write a plan at `.turbo/plans/<slug>.md`:

````markdown
---
status: <mapped status>
spec: <source spec path>
---

# Plan: <Prompt Title>

## Context

<The prompt's **Context** field content. If absent, use "Migrated from legacy prompt plan.">

## Implementation Steps

1. **Execute prompt instructions**
   - <The prompt's code block content, converted from a monolithic block into numbered sub-steps where natural boundaries exist. Preserve the concrete file references and instructions.>

## Verification

- Verify the implementation matches the prompt's requirements
- Run any test commands mentioned in the prompt
````

### Shell-Based Prompt Plans (Newer Format)

Indexes where each prompt references a separate shell file via a `**Shell:**` field. The referenced files may live in `.turbo/plans/` under the old layout. For each prompt entry:

1. Read the referenced file at its original path. If missing, report the mismatch and skip
2. Classify as unexpanded (no `## Pattern Survey`) or expanded (has `## Pattern Survey`)
3. Determine target:
   - **Unexpanded** → `.turbo/shells/<filename>`, frontmatter carries `spec:` and `depends_on:`
   - **Expanded** → `.turbo/plans/<filename>`, frontmatter carries `status:` and `spec:`
4. Build frontmatter:
   - `spec` from the index's Source field
   - For unexpanded only: `depends_on` mapped from the index entry's Depends on field, converting prompt numbers to shell file slugs
   - For expanded only: `status` mapped from the index entry's Status field (`done` → `done`, `pending` → `ready`, `in-progress` → `ready`)
5. If the target already exists with current frontmatter, skip
6. Write the file to the target path with the new frontmatter prepended before the existing `# Plan:` heading (replacing any legacy frontmatter). Delete the original at `.turbo/plans/<filename>`.

## Step 3: Process Remaining Files in `.turbo/plans/`

Handles files in `.turbo/plans/` that were not recorded in Step 1 as referenced by a prompt-plan index. Skip index-referenced files even if Step 2 couldn't process them (missing source, collision, target-already-current) — they belong to Step 2's accounting and should not be reprocessed here as unexpanded shells.

For each unexpanded shell:

1. Build frontmatter: `spec:` inferred from the spec slug embedded in the filename (`<spec-slug>-NN-<title>.md`) when a matching `.turbo/specs/<spec-slug>.md` exists (otherwise omit), `depends_on: []`
2. Write to `.turbo/shells/<filename>` with the new frontmatter prepended before the `# Plan:` heading (replacing any legacy frontmatter)
3. Delete the original at `.turbo/plans/<filename>`

For each expanded plan:

1. Build frontmatter: `status: ready` (default), or `status: done` if legacy frontmatter had `status: done`, plus `spec:` inferred from the filename when a matching spec exists
2. Rewrite the file in place with the normalized frontmatter (dropping legacy `type:`, `depends_on:`, and any other fields)

For each file in `.turbo/shells/*.md` that needs normalization (queued from Step 1):

1. Keep `spec:` and `depends_on:` if present, synthesize defaults if not (`depends_on: []`)
2. Drop any legacy `type:` or `status:` fields
3. Rewrite the file in place with the normalized frontmatter

Create `.turbo/shells/` if it does not exist. If a file at a shell target path already exists, report the collision and skip.

## Step 4: Normalize Frontmatter on Remaining Plans

For regular plans in `.turbo/plans/` that were not handled by Steps 2 or 3:

- If the file has no frontmatter, prepend `status: done` (plans without frontmatter predate the convention and have already been implemented)
- If the file has legacy `type: plan` frontmatter, drop `type:` and normalize `status:` to `done` if already `done`, otherwise `ready`. If no `status:` is present, set `status: done`.

The `status: done` default here differs from Step 3's `ready` default for expanded plans. Reasoning: regular plans without frontmatter are old enough that they're assumed implemented; expanded plans may have been expanded but never implemented, so `ready` is the safer default.

## Step 5: Migrate `improvements.md` Type Values

For each entry queued in Step 1, rewrite its `- **Type**:` line in place:

- `- **Type**: trivial` → `- **Type**: direct`
- `- **Type**: standard` → `- **Type**: plan`

`investigate` is unchanged. Preserve all other entry content (Category, Where, Why, Noted, summary). If `improvements.md` does not exist or no entries carry legacy values, skip this step.

## Step 6: Clean Up and Report

After all files are migrated:

1. Delete `.turbo/prompt-plans/` (the index files are no longer needed)
2. Delete `.turbo/prompts.md` if it exists (oldest legacy format)

Report a summary:

- Number of inline prompts converted to plans under `.turbo/plans/`
- Number of shells migrated from prompt-plan indexes to `.turbo/shells/`
- Number of expanded plans migrated from prompt-plan indexes to `.turbo/plans/`
- Number of unexpanded shells relocated from `.turbo/plans/` to `.turbo/shells/`
- Number of expanded plans normalized in place in `.turbo/plans/`
- Number of shells normalized in place in `.turbo/shells/`
- Number of regular plans that received frontmatter
- Number of improvements entries with rewritten Type values
- Number of files already migrated (skipped)
- Files deleted (indexes and relocated source files)

## Rules

- Treat `.turbo/specs/` as read-only.
- Skip any target path that already has valid current frontmatter.
- Preserve all existing body content when adding or normalizing frontmatter. The migration is additive, structural (directory moves), and subtractive (legacy index deletion), never content-destructive.
- If a shell file referenced by an index does not exist, report the mismatch and skip that entry.
- If the source spec path in an index does not resolve, still migrate the files but note the missing spec in the report.
- Omit `type:` from all migrated files; the directory is the type signal.
- Reserve `depends_on:` for shells; plans omit it.
- Use `ready` as the baseline status for migrated expanded plans; `draft` is reserved for refinement-stage artifacts.
- For `improvements.md`, only the Type value changes. Leave summaries, categories, file paths, rationales, and dates untouched.
