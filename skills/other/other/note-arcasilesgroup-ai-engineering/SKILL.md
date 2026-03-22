---
name: note
description: Use when a debugging session, research, or investigation yields non-obvious findings worth preserving for future sessions.
effort: medium
argument-hint: "find [query]|<slug>"
---



# Note

## Purpose

Knowledge management for technical discoveries. Captures debugging insights, non-obvious behaviors, and integration gotchas that would cost 30+ minutes to re-discover. Notes persist across sessions and are searchable.

## Trigger

- Command: `/ai-note <slug>` (create/update) or `/ai-note find [query]` (search)
- Context: discovery during debugging, research, or investigation that should be preserved.

## When to Use

- Discovery cost exceeds 30 minutes of investigation
- Non-obvious behavior that contradicts documentation or expectations
- Debugging insight that required multiple attempts to isolate
- Integration gotcha between tools, libraries, or services
- Workaround for a known issue with no upstream fix

## When NOT to Use

- **Architecture decisions** -- use `decision-store.json` via `/ai-governance`
- **Incident analysis** -- use `/ai-postmortem`
- **Customer issues** -- use `/ai-support`

## Procedure

### Mode: find

1. **Search notes** -- scan `.ai-engineering/notes/*.md` for files matching the query in filename, title, or content.
2. **Rank results** -- sort by relevance (title match > content match > date).
3. **Present** -- list matching notes with title, date, and first-line summary.

### Mode: create/update (by slug)

1. **Check existing** -- look for `.ai-engineering/notes/{slug}.md`. If found, load for update.
2. **Gather context** -- from the current session, extract:
   - What problem was being solved
   - What was tried and failed
   - What actually worked and why
3. **Write note** -- create/update at `.ai-engineering/notes/{slug}.md` using template:

```markdown
# {Title}

**Discovery Date**: YYYY-MM-DD
**Context**: {What triggered this investigation}
**Spec**: {spec-NNN if applicable, otherwise "N/A"}

## Problem

{What was expected vs what happened}

## Findings

{The non-obvious insight -- be specific, include versions/configs}

## Code Examples

{Minimal reproduction or working solution}

## Pitfalls

{What looks right but is wrong -- save future-you from the same trap}

## Related

- {Links to docs, issues, PRs, other notes}
```

4. **Validate** -- ensure Problem and Findings sections are non-empty. A note without findings is not a note.

## Decision: Save or Skip

| Signal | Action |
|--------|--------|
| Took 30+ min to figure out | Save |
| Contradicts official docs | Save |
| Required reading source code to understand | Save |
| Workaround for upstream bug | Save |
| Standard usage documented in README | Skip |
| One-off configuration for this machine | Skip |

## Quick Reference

```
/ai-note find ruff          # search notes mentioning ruff
/ai-note find               # list all notes
/ai-note gitleaks-staged    # create/update note with slug "gitleaks-staged"
```

## Storage

- Location: `.ai-engineering/notes/{slug}.md`
- Naming: kebab-case slugs, descriptive, max 50 chars
- Index: notes are flat files, searched by content -- no separate index needed

$ARGUMENTS
