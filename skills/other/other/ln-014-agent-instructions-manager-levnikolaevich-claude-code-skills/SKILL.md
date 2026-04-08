---
name: ln-014-agent-instructions-manager
description: "Creates missing instruction files (CLAUDE.md, AGENTS.md, GEMINI.md), audits token budget, prompt cache safety, cross-agent consistency. Use after setup or when instruction files need alignment."
license: MIT
---

> **Paths:** All file refs relative to skills repo root.

# Agent Instructions Manager

**Type:** L3 Worker
**Category:** 0XX Shared

Creates missing instruction files and audits all (CLAUDE.md, AGENTS.md, GEMINI.md) for quality, consistency, and best practices.

## Input / Output

| Direction | Content |
|-----------|---------|
| **Input** | project context, `dry_run` flag, optional `runId`, optional `summaryArtifactPath` |
| **Output** | Structured summary envelope with `payload.status` = `completed` / `skipped` / `error`, plus created files, audit findings, and warnings in `changes` / `detail` |

If `summaryArtifactPath` is provided, write the same summary JSON there. If not provided, return the summary inline and remain fully standalone. If `runId` is not provided, generate a standalone `run_id` before emitting the summary envelope.

## When to Use

- After editing any instruction file
- After adding/removing MCP servers or hooks
- Before release or publishing
- When sessions degrade (context bloat symptoms)
- First-time project setup (instruction files missing)

## Phase 1: Discover Files

Locate instruction files in target project:

| Agent | Primary | Fallback |
|-------|---------|----------|
| Claude | `CLAUDE.md` | `.claude/settings.local.json` |
| Codex | `AGENTS.md` | `.codex/instructions.md` |
| Gemini | `GEMINI.md` | `AGENTS.md` (shared with Codex) |

Report: which files exist (`found` / `missing`), which agents share files.

## Phase 1b: Plugin Conflict Check

**Skip condition:** No `enabledPlugins` in settings OR all plugins are `@levnikolaevich-skills-marketplace`.

1. Read `~/.claude/settings.json` → parse `enabledPlugins`
2. Filter: enabled=true AND publisher ≠ `levnikolaevich-skills-marketplace`
3. For each external plugin:
   - Locate cache: `~/.claude/plugins/cache/{publisher}/{plugin}/*/skills/*/SKILL.md`
   - Read each skill description (frontmatter `description:` field)
   - Match against conflict signal keywords:

| Signal | Keywords in description | Overlap with |
|--------|----------------------|--------|
| Orchestration | "orchestrat", "pipeline", "end-to-end", "lifecycle" | ln-1000 pipeline |
| Planning | "plan.*implement", "brainstorm", "design.*spec" | ln-300 task coordinator |
| Execution | "execut.*plan", "subagent.*task", "task-by-task" | ln-400/ln-401 executors |
| Code review | "code.review.*dispatch", "review.*quality.*spec" | ln-402/ln-310 |
| Quality gate | "quality.*gate", "verification.*complet", "test-driven.*always" | ln-500 quality gate |
| Debugging | "systematic.*debug", "root.*cause.*phase" | problem_solving.md |
| Git isolation | "worktree.*creat", "git.*isolat" | git_worktree_fallback.md |

   - Check for `hooks/session-start` directory (competing SessionStart injection)
4. Score: 2+ signal categories → CONFLICT. 1 → WARN. 0 → safe
5. CONFLICT: `"CONFLICT: {plugin} overlaps with ln-* pipeline ({signals}). Disable?"` → AskUserQuestion → if yes, set to `false` in settings.json
6. WARN: report, continue

## Phase 2: Create Missing Files

**Skip condition:** All files exist OR `dry_run == true` (report what would be created).

### Step 2a: Detect Project Context

| Field | Source | Fallback |
|-------|--------|----------|
| PROJECT_NAME | `package.json` → `name` | `basename(cwd)` |
| PROJECT_DESCRIPTION | `package.json` → `description` | `[TBD: Project description]` |
| DATE | current date (YYYY-MM-DD) | — |

### Step 2b: Create CLAUDE.md (if missing)

1. **MANDATORY READ:** Load `skills/ln-111-root-docs-creator/references/templates/claude_md_template.md`
2. Replace `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`, `{{DATE}}`
3. Mark remaining `{{...}}` as `[TBD: placeholder_name]`
4. Write to target project root

### Step 2c: Create AGENTS.md (if missing)

Source: target project's CLAUDE.md (just created or pre-existing).

| # | Transformation | Find | Replace |
|---|---------------|------|---------|
| 1 | Title | First H1 line | `# AGENTS.md` |
| 2 | SCOPE | `Guides in \`docs/\`` | `Detailed guides in \`docs/\`. Skill workflows in individual \`SKILL.md\` files. Public documentation in \`README.md\`.` |
| 3 | Agent name | `Claude Code` / `Claude` in intro line | `Codex` |
| 4 | DAG entry | `CLAUDE.md →` | `AGENTS.md →` |
| 5 | Add rule | After last Critical Rules row | Add: `\| **Code Comments 15-20%** \| Writing code \| WHY not WHAT. No historical notes. Task/ADR IDs as spec refs only \|` |

### Step 2d: Create GEMINI.md (if missing)

Source: target project's AGENTS.md (just created or pre-existing).

| # | Transformation | Find | Replace |
|---|---------------|------|---------|
| 1 | Title | First H1 line | `# GEMINI.md` |
| 2 | Agent name | `Codex` in intro line | `Gemini CLI` |
| 3 | DAG entry | `AGENTS.md →` | `GEMINI.md →` |
| 4 | Compact | `during /compact:` | `during context compression:` |
| 5 | Remove rule | `Code Comments` row | Delete row |

### Step 2e: Report Creations

List each created file with its source (template / derived from CLAUDE.md / derived from AGENTS.md).

## Phase 3: Token Budget Audit

For each instruction file:

| Check | Pass | Warn | Fail |
|-------|------|------|------|
| Line count | ≤100 lines | 101-150 lines | >150 lines |
| Estimated tokens | ≤2,500 tokens | 2,501-3,500 | >3,500 |
| Sections count | ≤8 sections | 9-12 | >12 |

**Token estimation:** `wc -w {file}` × 1.3 (English average tokens/word ratio).

Report table per file with line count, word count, estimated tokens.

## Phase 4: Prompt Cache Safety

Check each file for content that breaks prefix-based prompt caching:

| # | Check | Pattern | Severity |
|---|-------|---------|----------|
| 1 | No timestamps | `grep -E '\d{4}-\d{2}-\d{2}.\d{2}:\d{2}'` | WARN |
| 2 | No dates in content | `grep -E '(January|February|March|today|yesterday|Last Updated:)'` except `**Last Updated:**` at file end | WARN |
| 3 | No dynamic counts | `grep -E '\d+ skills\|\d+ tools\|\d+ servers'` (hardcoded counts change) | WARN |
| 4 | No absolute paths | `grep -E '[A-Z]:\\|/home/|/Users/'` (machine-specific) | INFO |
| 5 | Stable structure | No conditional sections (`if X then include Y`) | INFO |

## Phase 5: Content Quality

| # | Check | Pass | Fail |
|---|-------|------|------|
| 1 | Has build/test commands | Found `npm\|cargo\|pytest\|dotnet` commands | Missing — add essential commands |
| 2 | No abstract principles | No `"write quality code"`, `"follow best practices"` | Found vague instructions |
| 3 | No redundant docs | No API docs, no full architecture description | Found content discoverable from code |
| 4 | Has hard boundaries | Found `NEVER\|ALWAYS\|MUST\|DO NOT` rules | Missing explicit prohibitions |
| 5 | Compact Instructions section | `## Compact Instructions` present with preservation priorities | Missing — sessions lose decisions on /compact |
| 6 | MCP Tool Preferences | Table mapping built-in → MCP tools | Missing — agents use suboptimal tools |
| 7 | No tool output examples | No large code blocks or command outputs | Found — bloats every turn |

### Phase 5b: Auto-fix Fixable Issues

For each FAIL in Phase 5, attempt auto-fix before reporting:

**Before any auto-fix insertion:**
1. Verify insertion point exists (exact heading found at specific line)
2. If ambiguous (heading not found) — WARN and skip (report as manual fix needed)
3. After insertion — verify no duplicate `## Compact Instructions` or `## MCP Tool Preferences` sections exist in the file


| # | Issue | Fix | Skip when |
|---|-------|-----|----------|
| 5 | Missing Compact Instructions | Insert `## Compact Instructions` section before `## Navigation` | `dry_run: true` |
| 6 | Missing MCP Tool Preferences | Insert table from hex-line output-style template | `dry_run: true` or hex-line not registered |
| 1 | Missing build/test commands | WARN only (project-specific, cannot auto-generate) | -- |
| 2 | Abstract principles found | WARN only (requires human judgment) | -- |

**Compact Instructions template** (insert before `## Navigation` or after last rules section):

```markdown
## Compact Instructions

Preserve during /compact: [Critical Rules], [MCP Tool Preferences table],
[Navigation table], [language/communication rules], [hard boundaries (NEVER/ALWAYS)].
Drop examples and explanations first.
```

Adapt per agent: GEMINI.md uses "context compression" instead of "/compact".

## Phase 6: Cross-Agent Consistency

Compare content across all found instruction files:

| Check | Pass | Fail |
|-------|------|------|
| MCP Tool Preferences | Same table in all files | Inconsistent content across files |
| Critical Rules | Same core rules | Divergent rules |
| Build/test commands | Same commands | Different or missing |
| Structural sections | Same section order | Inconsistent structure |

**Sync action:** For each inconsistency, show diff and suggest which file is source of truth (usually CLAUDE.md).

## Phase 7: Report

```
Agent Instructions Manager:

Created:  (omit section if nothing created)
- CLAUDE.md (from template, context from package.json)
- AGENTS.md (derived from CLAUDE.md)

Audit:
| File       | Lines | ~Tokens | Cache-safe | Quality | Issues |
|------------|-------|---------|------------|---------|--------|
| CLAUDE.md  | 80    | 2,100   | OK         | 7/7     | Compact Instructions added |
| AGENTS.md  | 77    | 2,000   | OK         | 7/7     | OK |
| GEMINI.md  | 75    | 1,950   | OK         | 7/7     | OK |

Cross-agent: OK (or N inconsistencies listed)

Recommendations:
1. Run /init (ln-100) for full context-aware CLAUDE.md with project-specific rules
```

## Definition of Done

- [ ] All instruction files discovered
- [ ] Missing files created (CLAUDE.md from template, AGENTS/GEMINI derived)
- [ ] Token budget within limits (≤2,500 tokens each)
- [ ] No prompt cache breakers found (or reported as WARN)
- [ ] Content quality checks passed (or issues reported)
- [ ] Auto-fixable issues resolved (Compact Instructions, MCP Tool Preferences) or reported if dry_run
- [ ] Cross-agent consistency verified
- [ ] Report generated with creation log and actionable recommendations
- [ ] No conflicting external plugins detected (or user confirmed keep)

**Critical Rule: Non-destructive file edits.** Auto-fix inserts sections at verified positions only. Never rewrite the entire instruction file. Preserve all existing content outside the inserted section.

**Version:** 2.2.0
**Last Updated:** 2026-03-25
