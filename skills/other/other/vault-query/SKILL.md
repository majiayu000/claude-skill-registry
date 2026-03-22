---
name: vault-query
description: Search and analyze the vault knowledge base. Query learnings by type, status, tags, or pattern-key. Show promotion candidates and recurring patterns.
user-invocable: true
argument-hint: "<query | stats | promotions | recent | by-tag <tag>>"
context: fork
agent: researcher
allowed-tools:
  - Read
  - Glob
  - Grep
model: sonnet
---

# Vault Query

Search and analyze the vault knowledge base from the CLI.

## Subcommands

Parse `$ARGUMENTS` to determine which subcommand to run:

### `stats`
Count learnings by status and type, show promotion candidates:
1. `Glob` for `vault/learnings/*.md`
2. Read each file's frontmatter
3. Aggregate counts by `type` (learning/error/feature), `status`, `area`, and `project`
4. List any entries with `recurrence-count >= 3` as promotion candidates
5. Output a summary table

### `promotions`
List learnings eligible for promotion:
1. `Grep` for `recurrence-count:` in `vault/learnings/*.md`
2. Read files where `recurrence-count >= 3`
3. For each, show: id, title, recurrence-count, first-seen, last-seen, pattern-key
4. Sort by recurrence-count descending

### `recent` (or `recent N`)
Show the last N learnings (default 10):
1. `Glob` for `vault/learnings/*.md`
2. Sort by filename (date-based naming gives chronological order)
3. Read the last N files
4. Show: id, type, title, status, tags

### `by-tag <tag>`
Filter learnings by tag:
1. `Grep` for the tag in `vault/learnings/*.md` frontmatter `tags:` lines
2. Read matching files
3. Show: id, type, title, status

### Free-form query
For any other `$ARGUMENTS`, treat it as a search query:
1. `Grep` for the query in `vault/learnings/*.md` (both frontmatter and body)
2. Also search `vault/shared/**/*.md`
3. Read matching files and present relevant excerpts
4. Highlight matching `pattern-key`, `tags`, and section content

## Output Format

Use concise tables for structured output. Example:

```
| ID | Type | Title | Status | Tags |
|----|------|-------|--------|------|
| LRN-20250310-001 | learning | Claude CLI env stripping | resolved | [cli, env, spawn] |
```

For stats, use summary format:
```
Vault Stats:
  Learnings: 12 (8 resolved, 3 new, 1 promoted)
  Errors: 5 (4 resolved, 1 investigating)
  Features: 3 (1 built, 2 requested)
  Promotion candidates: 2
```
