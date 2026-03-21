---
name: ln-014-agent-instructions-auditor
description: "Audits CLAUDE.md, AGENTS.md, GEMINI.md for token budget, prompt cache safety, compact instructions, and cross-agent consistency. Use after editing instruction files or before release."
license: MIT
---

> **Paths:** All file refs relative to skills repo root.

# Agent Instructions Auditor

**Type:** L3 Worker
**Category:** 0XX Shared

Audits instruction files (CLAUDE.md, AGENTS.md, GEMINI.md) across all three agents for quality, consistency, and best practices.

## When to Use

- After editing any instruction file
- After adding/removing MCP servers or hooks
- Before release or publishing
- When sessions degrade (context bloat symptoms)

## Phase 1: Discover Files

Locate instruction files in target project:

| Agent | Primary | Fallback |
|-------|---------|----------|
| Claude | `CLAUDE.md` | `.claude/settings.local.json` |
| Codex | `AGENTS.md` | `.codex/instructions.md` |
| Gemini | `GEMINI.md` | `AGENTS.md` (shared with Codex) |

Report: which files exist, which agents share files.

## Phase 2: Token Budget Audit

For each instruction file:

| Check | Pass | Warn | Fail |
|-------|------|------|------|
| Line count | ≤100 lines | 101-150 lines | >150 lines |
| Estimated tokens | ≤2,500 tokens | 2,501-3,500 | >3,500 |
| Sections count | ≤8 sections | 9-12 | >12 |

**Token estimation:** `wc -w {file}` × 1.3 (English average tokens/word ratio).

Report table per file with line count, word count, estimated tokens.

## Phase 3: Prompt Cache Safety

Check each file for content that breaks prefix-based prompt caching:

| # | Check | Pattern | Severity |
|---|-------|---------|----------|
| 1 | No timestamps | `grep -E '\d{4}-\d{2}-\d{2}.\d{2}:\d{2}'` | WARN |
| 2 | No dates in content | `grep -E '(January|February|March|today|yesterday|Last Updated:)'` except `**Last Updated:**` at file end | WARN |
| 3 | No dynamic counts | `grep -E '\d+ skills\|\d+ tools\|\d+ servers'` (hardcoded counts change) | WARN |
| 4 | No absolute paths | `grep -E '[A-Z]:\\|/home/|/Users/'` (machine-specific) | INFO |
| 5 | Stable structure | No conditional sections (`if X then include Y`) | INFO |

## Phase 4: Content Quality

| # | Check | Pass | Fail |
|---|-------|------|------|
| 1 | Has build/test commands | Found `npm\|cargo\|pytest\|dotnet` commands | Missing — add essential commands |
| 2 | No abstract principles | No `"write quality code"`, `"follow best practices"` | Found vague instructions |
| 3 | No redundant docs | No API docs, no full architecture description | Found content discoverable from code |
| 4 | Has hard boundaries | Found `NEVER\|ALWAYS\|MUST\|DO NOT` rules | Missing explicit prohibitions |
| 5 | Compact Instructions section | `## Compact Instructions` present with preservation priorities | Missing — sessions lose decisions on /compact |
| 6 | MCP Tool Preferences | Table mapping built-in → MCP tools | Missing — agents use suboptimal tools |
| 7 | No tool output examples | No large code blocks or command outputs | Found — bloats every turn |

## Phase 5: Cross-Agent Consistency

Compare content across all found instruction files:

| Check | Pass | Fail |
|-------|------|------|
| MCP Tool Preferences | Same table in all files | Missing in some files |
| Critical Rules | Same core rules | Divergent rules |
| Build/test commands | Same commands | Different or missing |
| Structural sections | Same section order | Inconsistent structure |

**Sync action:** For each inconsistency, show diff and suggest which file is source of truth (usually CLAUDE.md).

## Phase 6: Report

```
Agent Instructions Audit:
| File       | Lines | ~Tokens | Cache-safe | Quality | Issues |
|------------|-------|---------|------------|---------|--------|
| CLAUDE.md  | 80    | 2,100   | ✅          | 6/7     | Missing Compact Instructions |
| AGENTS.md  | 77    | 2,000   | ✅          | 7/7     | OK |
| GEMINI.md  | —     | —       | —          | —       | File not found |

Cross-agent: 1 inconsistency (GEMINI.md missing)

Recommendations:
1. Create GEMINI.md (copy from AGENTS.md, adjust agent-specific sections)
2. Add ## Compact Instructions to CLAUDE.md
```

## Definition of Done

- [ ] All instruction files discovered and audited
- [ ] Token budget within limits (≤2,500 tokens each)
- [ ] No prompt cache breakers found (or reported as WARN)
- [ ] Content quality checks passed (or issues reported)
- [ ] Cross-agent consistency verified
- [ ] Report generated with actionable recommendations

**Version:** 1.0.0
**Last Updated:** 2026-03-20
