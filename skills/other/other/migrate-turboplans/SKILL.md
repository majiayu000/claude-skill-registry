---
name: migrate-turboplans
description: "Migrate legacy plan and shell files in .turbo/ to the current format with YAML frontmatter. Handles three formats: inline prompt plans (.turbo/prompt-plans/ or .turbo/prompts.md with prompts embedded in the index), shell-based prompt plans (.turbo/prompt-plans/ index + separate shell files in .turbo/plans/), and regular plans without frontmatter. Use when the user asks to \"migrate turboplans\", \"migrate turbo plans\", \"upgrade plan format\", \"add frontmatter to plans\", or \"convert old plans\"."
---

# Migrate Plans

## Task Tracking

Use `TaskCreate` to create a task for each step:

1. Scan and classify existing files
2. Migrate prompt plan indexes
3. Add frontmatter to regular plans
4. Clean up and report

## Step 1: Scan and Classify Existing Files

Scan for all three legacy formats:

- **Prompt plan indexes** — Glob `.turbo/prompt-plans/*.md`. Also check for `.turbo/prompts.md` (oldest legacy format). Parse each index to determine whether prompts are inline (contain `### Prompt` sections with code blocks) or reference separate shell files (contain `**Shell:**` fields).
- **Shell files** — Glob `.turbo/plans/*.md`. Read each file's first 5 lines. Files that already have YAML frontmatter with `type:` are already migrated. Files without frontmatter that contain `## Produces`, `## Consumes`, and `## Covers Spec Requirements` are unmigrated shells. Files without frontmatter that contain `## Pattern Survey` are expanded plans (previously filled-in shells).
- **Regular plans** — Files in `.turbo/plans/*.md` without frontmatter that are neither shells nor expanded plans.

Report what was found: number of indexes, shells, expanded plans, regular plans, and already-migrated files. If nothing needs migration, report and stop.

## Step 2: Migrate Prompt Plan Indexes

For each prompt plan index, parse:

- **Source** — spec path from the `Source:` field
- **Prompts** — each `## Prompt N:` entry with its Status, Depends on, and content

### Inline Prompts (Old Format)

Indexes where each prompt contains a `### Prompt` section with a code block of concrete instructions. No separate shell files exist for these prompts.

For each prompt entry:

1. Generate a shell slug: `<spec-slug>-NN-<title-slug>` from the spec filename and prompt number/title
2. Map the old status: `done` → `done`, `pending` → `ready` (these prompts already have concrete instructions, so they're equivalent to expanded plans), `in-progress` → `in-progress`
3. Map `Depends on: Prompt N` to `depends_on` using the generated slugs of the referenced prompts. `Depends on: none` → `depends_on: []`
4. Write a plan file at `.turbo/plans/<shell-slug>.md`:

````markdown
---
type: shell
status: <mapped status>
spec: <source spec path>
depends_on: <mapped depends_on list>
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

Indexes where each prompt references a separate shell file via a `**Shell:**` field.

For each prompt entry:

1. Read the referenced shell file
2. If the shell file already has YAML frontmatter, skip it
3. Add frontmatter by extracting from the index:
   - `type: shell`
   - `status` mapped from the index entry's Status field (`done` → `done`, `pending` → `draft` (shell files without expansion still need `/expand-plan-shell` to fill in concrete references), `in-progress` → `in-progress`)
   - `spec` from the index's Source field
   - `depends_on` mapped from the index entry's Depends on field, converting prompt numbers to shell file slugs (derive from the shell's filename without `.md`)

Write the updated shell file back with frontmatter prepended before the existing `# Plan:` heading.

For shells that have already been expanded (contain `## Pattern Survey`), use `status: ready` instead of `draft` regardless of what the index says.

## Step 3: Add Frontmatter to Regular Plans

For each file in `.turbo/plans/*.md` that has no YAML frontmatter and is not a shell, add `type: plan`, `status: done`. Existing plans without frontmatter predate the frontmatter convention and have already been implemented.

Prepend the frontmatter before the existing `# Plan:` heading.

## Step 4: Clean Up and Report

After all files are migrated:

1. Delete `.turbo/prompt-plans/` (the index files are no longer needed)
2. Delete `.turbo/prompts.md` if it exists (oldest legacy format)

Report a summary:

- Number of inline prompts converted to shell files
- Number of existing shells that received frontmatter
- Number of regular plans that received frontmatter
- Number of files already migrated (skipped)
- Files deleted

## Rules

- Never modify the spec files in `.turbo/specs/`.
- Never overwrite a file that already has valid YAML frontmatter with `type:`.
- Preserve all existing content when adding frontmatter. The migration is additive (frontmatter) and subtractive (index deletion), never content-destructive.
- If a shell file referenced by an index does not exist, report the mismatch and skip that entry.
- If the source spec path in an index does not resolve, still migrate the shells but note the missing spec in the report.
