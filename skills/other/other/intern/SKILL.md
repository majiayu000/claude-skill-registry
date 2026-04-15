---
name: intern
description: Use when the user asks to reflect on recent sessions, analyze repeated mistakes, or review prompting and agent patterns for improvement.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write, Task
argument-hint: "[--days N]"
---

# Intern — Session Analyst

Analyze recent Claude Code sessions. Find what went wrong, what went well, and what to change. Write a review report with concrete improvements.

A single suboptimal conversation is worth learning from — don't require cross-session recurrence. Findings are valuable when actionable and specific: a quoted message, a named file, a concrete proposal. Vague observations ("communication could be improved") are worthless.

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--days N` | 1 | How many days of sessions to analyze |

## Session Discovery

Session transcripts are JSONL files in two locations:
- `~/.claude/projects/*/`
- `~/.ccs/shared/context-groups/*/projects/*/`

Filter to `*.jsonl` files with mtime within the `--days` window, >2 lines, mtime >60s old (still-open sessions may be incomplete). Exclude `subagents/` directories.

## Analyst Teammates

Sessions are large. Dispatch analysis to teammates to preserve main context fidelity.

The analyst prompt lives at `${CLAUDE_SKILL_DIR}/agents/analyst.md`. Read the prompt file, prepend session file paths, and spawn as a teammate.

Batch by size: sessions with messageCount >50 get their own teammate; smaller ones batch up to 3 per teammate. Spawn all in parallel.

## Synthesis

Merge findings pointing to the same root cause across sessions — note affected sessions and elevate severity when patterns recur.

Before proposing rules or CLAUDE.md changes, read existing `.claude/rules/*.md`, project `CLAUDE.md`, and `~/.claude/CLAUDE.md`. If a proposal contradicts an existing rule, flag the contradiction rather than proposing either side.

For each actionable finding, draft the concrete change: full rule text, specific skill edit, exact CLAUDE.md addition. Rank by impact.

## Review Report

Write to `.intern/{timestamp}.md` (e.g., `.intern/2026-03-06T23-00.md`).

Sections (omit empty ones):

- **Header** — date range, session count, quality summary
- **Findings** — ranked by impact; each with severity, evidence, proposed action
- **Proposed Changes** — copy-pasteable rules, skill tweaks, CLAUDE.md edits, user tips; grouped by type
- **What Went Well** — success patterns worth reinforcing
- **Contradictions** — proposals that conflict with existing rules

## Constraints

- Redact API keys, passwords, and tokens from evidence quotes
- Note skipped/malformed sessions in the report
