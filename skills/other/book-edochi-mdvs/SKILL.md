---
name: book
description: mdBook documentation conventions. Apply when writing, editing, or reviewing pages in book/src/. Covers content rules, example verification, tone, and structure.
---

# mdBook Documentation Conventions

## Location

The book lives in `book/` at the repo root. `book/src/SUMMARY.md` is the source of truth for page structure — always check it before adding or moving pages.

## Running example

All pages use `example_kb/` (the Prismatiq Lab fixture) for examples. Never use a hypothetical vault. Refer to the fixture's characters, fields, and edge cases by name when illustrating concepts.

Key reference: `example_kb/.plan.md` documents every file, field, and edge case in the fixture.

## Content rules

### Every command output must be real

1. Run the command against `example_kb` before writing.
2. Capture the actual output.
3. Paste it into the book. Trim if long, but never invent lines.
4. If a command's output changes (new fields, format tweaks), re-run and update the book.

### Every code block must be copy-pasteable

- Shell examples must work if the reader clones the repo and runs them from the repo root.
- Use `example_kb` as the path argument, not `.` or a made-up directory.
- Quote arguments correctly for common shells (bash/zsh).

### Accuracy over completeness

- Check `docs/spec/commands/` for the authoritative behavior, flags, and error conditions.
- Rewrite for users — the specs are for implementors. Drop internal details (Arrow types, struct names, pipeline steps).
- If unsure whether a behavior is correct, run it and verify before writing.

## Tone

- **User-facing.** The reader has never seen the codebase. No internal architecture, no struct names, no module paths.
- **Direct.** Lead with what the command does, not how it works internally.
- **Concise.** Short paragraphs, bullet points, tables. Long prose blocks lose readers.
- **No emojis** unless explicitly requested.

## Page structure

### Command pages (`commands/*.md`)

```markdown
# command-name

<One-sentence description of what the command does.>

## Usage

\`\`\`bash
mdvs <command> [args] [flags]
\`\`\`

## Flags

<Table: flag, default, description>

## What it does

<Brief explanation — 2-4 paragraphs max. What the user needs to know, not how it works internally.>

## Examples

<2-4 examples with real output from example_kb. Start simple, build to complex.>
```

### Concept pages

Lead with the "what" and "why", then illustrate with `example_kb` fields. Use tables for type rules, widening matrix, etc. Keep it in one page — don't split tightly coupled concepts across files.

### The search guide

The most example-heavy page. Must cover:
- Scalar filters (string, number, boolean)
- Array containment (`array_has`, `= ANY()`)
- Array length
- Nested object bracket access
- Field names with special characters (space, quotes)
- Combined filters

Every query must be runnable against `example_kb`. See `scripts/test_array_queries.rs` for tested patterns.

## Workflow for writing a new page

1. Read the relevant spec in `docs/spec/commands/` (if it exists).
2. Read `example_kb/.plan.md` to pick appropriate examples.
3. Run all commands you plan to show. Capture output.
4. Write the page.
5. Build the book (`mdbook build book/`) and check rendering.

## Workflow for editing an existing page

1. Read the current page.
2. Re-run any commands whose output may have changed.
3. Edit the page. Update output blocks if stale.
4. Build the book and check rendering.

## Updating example_kb

If a page needs an edge case that `example_kb` doesn't have:
1. Discuss with the user — new content must fit the Prismatiq Lab story.
2. Add the file/field to `example_kb/`.
3. Update `example_kb/.plan.md` with the new edge case.
4. Re-run `mdvs update example_kb` and `mdvs build example_kb --force`.
5. Then write the book content.
