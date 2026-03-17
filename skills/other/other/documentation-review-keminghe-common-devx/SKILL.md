---
name: documentation-review
description: |
  Review and correct documentation for consistency, correctness, and drift.
  Documentation edits only (txt, md, mdx, rst) - no functional code changes.
  Triggers: "review docs", "check documentation", "doc review", "fix docs".
license: MIT
metadata:
  author: KemingHe
  version: "2.0.0"
---

# Documentation Review

Review and correct documentation files for consistency, correctness, and drift. Documentation edits only - no functional code changes.

**Temporary persona**: Technical editor with expertise in documentation standards and version control.

## When to Use This Skill

- Before committing documentation changes
- Auditing docs for staleness or drift
- Reviewing PRs (GitHub) / MRs (GitLab) with documentation updates
- Checking consistency across related files

## Process

### Step 1: Identify Scope

Determine files to review:

- Single file, directory, or pattern
- Related files (e.g., SKILL.md + README + assets)

### Step 2: Apply Checklist

| Dimension | Check For |
| :--- | :--- |
| **Consistency** | Version sync (frontmatter/footer), naming patterns, terminology |
| **Correctness** | Valid YAML/markdown, working links, accurate paths |
| **Completeness** | Required sections present, no unfilled placeholders |
| **Freshness** | Last Updated date, version numbers, changelog entries |
| **Characters** | QWERTY-only everywhere; no smart quotes, emojis, or special Unicode; no em-dashes or em-dash substitutes (`--`, ` -- `) in prose; use ` - ` for clause separation (exception: `↑`) |
| **Inline formatting** | `_underscore_` italics only; colon outside bold label markers (`**Topic**:`) |
| **Linter** | Check IDE/editor linter errors when available |
| **Output quality** | Soft-wrapped bullets or prose; sentences broken across hard newlines; orphaned `(optional)` labels in populated sections; unfilled `[placeholder]` text; terminology inconsistency; KISS/DRY violations |

### Step 3: Check Linter Errors

When linter tooling is available (IDE, markdownlint, etc.):

- Run linter on files in scope
- Include linter errors in findings table
- Distinguish between new errors (introduced by changes) and pre-existing

Common markdown linter catches:

- Missing language specifier on fenced code blocks
- Inconsistent list indentation
- Trailing whitespace or missing final newline
- Invalid link references

### Step 4: Report Findings

Present issues in structured table:

```markdown
| Issue | Location | Current | Fix Needed |
| :--- | :--- | :--- | :--- |
| [issue type] | Line X | `[current]` | [action] |
```

Summarize with:

- Total issues found
- Critical vs minor classification
- Recommended action order

## Common Misses

- **Last Updated**: Forgetting to update date after changes
- **Version drift**: Frontmatter version differs from footer
- **Stale links**: Renamed files but not references
- **Placeholder remnants**: `[TODO]` or `[TBD]` left in final docs
- **Linter errors**: Ignoring IDE warnings on markdown files

## General Doc Constraints

Apply to all generated output. If a discovered template deviates from any rule (e.g., uses emojis semantically, uses a different bullet convention), note the deviation explicitly and confirm with the user before treating it as a permitted exception.

- **Characters**: QWERTY keyboard typeable only - no smart quotes, emojis, or special Unicode anywhere. In prose, do not use em-dashes or em-dash substitutes (`--`, ` -- `); use ` - ` (space-dash-space) for clause separation instead. Exception: `↑` for ToC navigation.
- **Inline formatting**: Use `_underscore_` for italics, not `*single-star*`. Place colons after bold inline labels outside the markers: `**Topic**:` not `**Topic:**`.
- **Bullets**: Use `-` for all unordered lists; one bullet per complete thought; never wrap a bullet's content mid-sentence onto a continuation line - split into separate bullets if too long or multi-thought. Nested sub-bullets for component grouping are permitted. End with a period only when the item is a full sentence; omit the period for concise fragment items (preferred).
- **Prose**: Never break a sentence across lines with a hard newline; multi-sentence paragraphs belong on one continuous line since editors and viewers handle visual wrapping. Exception: commit message bodies use one sentence per line for `git log` readability.
- **Template hygiene**: Delete `(optional)` and any parenthetical conditional label (e.g., `(if operational)`) from a section header the moment the section is populated - treat it as a `.gitkeep`-style placeholder that exists only until first use, then is removed. Omit the entire section (header and body) when unused. Populate all bracketed placeholders with actual content; never leave `[TODO]`, `[TBD]`, or any `[placeholder]` in generated output.
- **Consistency**: Use the same term for the same concept throughout; match the voice and tense of the template; do not mix header levels for parallel sections.
- **KISS and DRY**: Each section and bullet conveys unique information - no redundancy or overlap.

> General Doc Constraints v1.1.0 - KemingHe/common-devx

## Skill Constraints

- **Documentation only**: Edit txt, md, mdx, rst files - no functional code changes
- **Structured output**: Always use table format for findings
- **Prioritized**: Critical issues (broken links, wrong versions) before style issues
- **Linter-aware**: Check and report linter errors when tooling is available
