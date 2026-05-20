---
name: rule-effectiveness
description: Analyze which rules are actively used vs inert. Detect coverage gaps. Recommend pruning to reduce token consumption.
---

# Rule Effectiveness Analysis

Analyze the effectiveness of `.claude/rules/` in the current project by cross-referencing rule globs against actual file activity from git history.

## Step 1: Collect rules inventory

Read all `.md` files in `.claude/rules/`. For each:
1. Extract `globs:` value from YAML frontmatter
2. Count lines of content (excluding frontmatter)
3. Record filename and glob pattern

If a rule has no `globs:` or `paths:` frontmatter, classify as **always-loaded** (loads every session regardless of files touched).

Rules with `globs:` load eagerly at session start. Rules with `paths:` + `alwaysApply: false` load lazily (only when a matching file is touched). Note: `paths:` must be unquoted CSV — YAML arrays and quoted strings fail silently.

## Step 2: Collect file activity from git history

Run: `git log --name-only --pretty=format:'' --since='3 months ago'` (or configurable period).

Parse output to build:
- **session_files**: group files by commit date (approximate 1 day = 1 session)
- **total_sessions**: count distinct dates with commits
- **all_files_touched**: unique set of all files modified

If fewer than 5 sessions available, warn that results may not be representative and extend to `--since='6 months ago'`.

## Step 3: Cross-reference rules vs activity

For each rule with a glob pattern:
1. Match glob against **all_files_touched** using bash glob expansion or fnmatch logic
2. Calculate:
   - `matched_files`: count of unique files that match the glob
   - `match_rate`: % of sessions where at least 1 file matched the glob
   - `token_cost`: lines of rule content (proxy for context consumption)

For the project overall:
- `covered_files`: files that match at least 1 rule glob
- `uncovered_files`: files touched but matching no rule
- `file_coverage`: covered / total

## Step 4: Classify rules

| Classification | Criteria | Action |
|---------------|----------|--------|
| **Active** | match_rate > 50% | Keep — rule loads in most sessions and covers real files |
| **Occasional** | match_rate 10-50% | Evaluate — may be worth keeping for specific workflows (deploys, migrations) |
| **Inert** | match_rate < 10% | Candidate for removal — consumes tokens without matching real files |
| **Always-loaded** | globs: `**/*` or no globs | Evaluate content — is it generic enough to justify always loading? |
| **Overbroad** | globs: `**/*` but content is stack-specific | Should have narrower globs to avoid loading in wrong contexts |

## Step 5: Detect coverage gaps

From **uncovered_files**, group by directory prefix. Report directories with >5 uncovered files:

```
SIN COBERTURA:
  src/utils/     — 12 files touched, no rule covers this path
  scripts/       — 8 files touched, no rule covers this path
  migrations/    — 5 files touched, no rule covers this path
```

For each gap, suggest:
- If directory maps to an existing stack (e.g., `migrations/` → supabase), recommend adding stack rule
- If directory is project-specific, recommend creating a custom rule

## Step 6: Token optimization analysis

Calculate approximate token impact:
- **Always-loaded rules**: sum of all lines (loaded every session)
- **Active rules**: weighted by match_rate × lines
- **Inert rules**: full line count = wasted tokens

```
TOKEN BUDGET:
  Always loaded:  _common.md (35 lines) + agents.md (52 lines) + memory.md (18 lines) = 105 lines/session
  Active rules:   backend.md (33 lines × 95%) + testing.md (30 lines × 78%) = ~55 lines avg/session
  Inert rules:    ios.md (34 lines × 0%) = 34 lines WASTED per session when loaded

  POTENTIAL SAVINGS: Remove ios.md → save ~34 lines of context per session
```

## Step 7: Generate report

```
═══ RULE EFFECTIVENESS — {{project}} ═══
Period: last {{N}} months ({{total_sessions}} sessions)
Rules: {{rule_count}} files, {{total_lines}} lines

── ACTIVE (keep) ──
  {{rule.md}}     — {{match_rate}}% match, {{matched_files}} files, {{lines}} lines
  ...

── OCCASIONAL (evaluate) ──
  {{rule.md}}     — {{match_rate}}% match, {{matched_files}} files
  ...

── INERT (candidates for removal) ──
  {{rule.md}}     — {{match_rate}}% match, {{matched_files}} files ← {{reason}}
  ...

── ALWAYS-LOADED ({{total_lines}} lines/session) ──
  {{rule.md}}     — {{lines}} lines, globs: **/*
  ...

── COVERAGE ──
  Files covered by rules:   {{covered}}/{{total}} ({{coverage}}%)
  Gaps: {{gap_dirs}}

── TOKEN OPTIMIZATION ──
  Current avg load:    ~{{current}} lines/session
  After pruning inert: ~{{pruned}} lines/session
  Potential savings:   ~{{savings}} lines/session ({{pct}}% reduction)

── RECOMMENDATIONS ──
1. {{action}} — {{reason}}
2. ...
```

## Step 8: Offer automated fixes

For each recommendation, offer to execute:
- **Remove inert rule**: `rm .claude/rules/{{file}}` (with confirmation)
- **Narrow glob**: edit frontmatter to restrict to actual file patterns
- **Add missing rule**: create `.claude/rules/{{name}}.md` with suggested globs
- **Split overbroad rule**: extract stack-specific content to narrower-glob rule

Only execute with user confirmation. Show diff before applying.
