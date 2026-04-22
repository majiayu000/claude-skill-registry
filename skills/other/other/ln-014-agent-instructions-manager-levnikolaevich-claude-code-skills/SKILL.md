---
name: ln-014-agent-instructions-manager
description: "Creates AGENTS.md canonical and CLAUDE.md/GEMINI.md/ANTIGRAVITY.md @AGENTS.md stubs; audits token budget, cache safety, import-pattern compliance. Use when instruction files need alignment."
license: MIT
---

> **Paths:** All file refs relative to skills repo root.

# Agent Instructions Manager

**Type:** L3 Worker
**Category:** 0XX Shared

Creates missing instruction files and audits all of them (AGENTS.md, CLAUDE.md, GEMINI.md, ANTIGRAVITY.md) for quality, consistency, and best practices. AGENTS.md is the single canonical source of content; CLAUDE.md, GEMINI.md, and ANTIGRAVITY.md are thin `@AGENTS.md` import stubs with bounded harness-specific deltas. This skill is the single owner of instruction-file creation and MCP Tool Preferences insertion or replacement.

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`, `shared/references/environment_worker_runtime_contract.md`, and `shared/references/worker_runtime_contract.md`
**MANDATORY READ:** Load `shared/references/mcp_tool_preferences.md`
**MANDATORY READ:** Load `shared/references/agent_instructions_writing_guide.md` — canonical rationale for the `@AGENTS.md` import pattern, size budgets, and anti-patterns. All audit checks below trace back to this guide.

## Input / Output

| Direction | Content |
|-----------|---------|
| **Input** | project context, `dry_run` flag, optional `runId`, optional `summaryArtifactPath` |
| **Output** | Structured summary envelope with `payload.status` = `completed` / `skipped` / `error`, plus created files, audit findings, and warnings in `changes` / `detail` |

If `summaryArtifactPath` is provided, write the same summary JSON there. If not provided, return the summary inline and remain fully standalone. If `runId` is not provided, generate a standalone `run_id` before emitting the summary envelope.

## Runtime

Runtime family: `environment-worker-runtime`

Phase profile:
1. `PHASE_0_CONFIG`
2. `PHASE_1_DISCOVER_FILES`
3. `PHASE_2_CREATE_MISSING_FILES`
4. `PHASE_3_TOKEN_BUDGET_AUDIT`
5. `PHASE_4_PROMPT_CACHE_SAFETY`
6. `PHASE_5_CONTENT_QUALITY`
7. `PHASE_6_IMPORT_PATTERN_COMPLIANCE`
8. `PHASE_7_WRITE_SUMMARY`
9. `PHASE_8_SELF_CHECK`

Runtime rules:
- emit `summary_kind=env-instructions`
- standalone runs generate their own `run_id` and write the default worker-family artifact path
- managed runs require both `runId` and `summaryArtifactPath` and must write the summary to the exact provided path
- always write the validated summary artifact before terminal outcome

## Output Contract

Always build a structured `env-instructions` summary envelope per:
- `shared/references/coordinator_summary_contract.md`
- `shared/references/environment_worker_runtime_contract.md`

Payload fields:
- `files_found`
- `files_created`
- `quality_findings`
- `token_budget`
- `prompt_cache_safety`
- `import_pattern_status`
- `status`

## When to Use

- After editing any instruction file
- After adding/removing MCP servers or hooks
- Before release or publishing
- When sessions degrade (context bloat symptoms)
- First-time project setup (instruction files missing)

## Phase 1: Discover Files

Locate instruction files in target project:

| Agent | Primary | Canonical source | Fallback |
|-------|---------|------------------|----------|
| Claude Code | `CLAUDE.md` | imports `AGENTS.md` via `@AGENTS.md` | `.claude/settings.local.json` |
| Codex / Cursor / Amp / Factory | `AGENTS.md` | canonical | `.codex/instructions.md` |
| Gemini CLI | `GEMINI.md` | imports `AGENTS.md` via `@AGENTS.md` | `AGENTS.md` (shared with Codex) |
| Google Antigravity | `ANTIGRAVITY.md` | imports `AGENTS.md` via `@AGENTS.md` | `AGENTS.md` (shared with Codex/Gemini/Claude) |

Report: which files exist (`found` / `missing`), which harnesses share `AGENTS.md` directly vs via import.

## Phase 1b: Plugin Conflict Check

**Skip condition:** No `enabledPlugins` in settings OR all plugins are `@levnikolaevich-skills-marketplace`.

1. Read `~/.claude/settings.json` → parse `enabledPlugins`
2. Filter: enabled=true AND publisher ≠ `levnikolaevich-skills-marketplace`
3. For each external plugin:
   - Resolve active install first: matching plugin or marketplace under `~/.claude/plugins/marketplaces/*`
   - Read active `skills-catalog/*/SKILL.md` descriptions from that install surface
   - Only if no active install is available, fall back to the latest cache snapshot under `~/.claude/plugins/cache/{publisher}/{plugin}/*/skills/*/SKILL.md`
   - Treat cache as forensic fallback only. Never count multiple cache snapshots as separate active conflicts.
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

   - Check for `hooks/session-start` directory in the active install surface first
4. Score: 2+ signal categories → CONFLICT. 1 → WARN. 0 → safe
5. CONFLICT: `"CONFLICT: {plugin} overlaps with ln-* pipeline ({signals}). Disable?"` → AskUserQuestion → if yes, set to `false` in settings.json
6. WARN: report, continue

## Phase 2: Create Missing Files

**Skip condition:** All files exist OR `dry_run == true` (report what would be created).

**Canonical model:** AGENTS.md is the single source of content. CLAUDE.md, GEMINI.md, and ANTIGRAVITY.md are `@AGENTS.md` import stubs with bounded harness-specific deltas. Create in this order so the stubs reference a file that already exists.

### Step 2a: Detect Project Context

| Field | Source | Fallback |
|-------|--------|----------|
| PROJECT_NAME | `package.json` → `name` | `basename(cwd)` |
| PROJECT_DESCRIPTION | `package.json` → `description` | `[TBD: Project description]` |
| DATE | current date (YYYY-MM-DD) | — |
| ENABLE_WORKFLOW_PRINCIPLES | Caller input (default `false`) | — |

### Step 2b: Create AGENTS.md (if missing) — canonical

1. **MANDATORY READ:** Load `skills-catalog/ln-111-root-docs-creator/references/templates/agents_md_template.md`
2. Replace `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`, `{{DATE}}`, and `{{DEV_COMMANDS_*}}` placeholders
3. If `ENABLE_WORKFLOW_PRINCIPLES=true`: replace `{{WORKFLOW_PRINCIPLES_BLOCK}}` with the full content of `skills-catalog/ln-111-root-docs-creator/references/templates/agents_md_workflow_principles.md`. Otherwise strip the placeholder line and its leading HTML comment.
4. Mark remaining `{{...}}` as `[TBD: placeholder_name]`
5. Write to target project root

### Step 2c: Create CLAUDE.md (if missing) — import stub

1. **MANDATORY READ:** Load `skills-catalog/ln-111-root-docs-creator/references/templates/claude_md_template.md`
2. Replace `{{PROJECT_NAME}}` only
3. Write to target project root
4. Verify the file contains exactly one `@AGENTS.md` line and is ≤50 lines total
5. Do NOT copy any content from AGENTS.md into CLAUDE.md — the `@` import handles it at session load time

### Step 2d: Create GEMINI.md (if missing) — import stub

1. **MANDATORY READ:** Load `skills-catalog/ln-111-root-docs-creator/references/templates/gemini_md_template.md`
2. Replace `{{PROJECT_NAME}}` only
3. Write to target project root
4. Verify the file contains exactly one `@AGENTS.md` line and is ≤50 lines total
5. Do NOT copy any content from AGENTS.md into GEMINI.md — the `@` import handles it at session load time

### Step 2d2: Create ANTIGRAVITY.md (if missing) — import stub

1. **MANDATORY READ:** Load `skills-catalog/ln-111-root-docs-creator/references/templates/antigravity_md_template.md`
2. Replace `{{PROJECT_NAME}}` only
3. Write to target project root
4. Verify the file contains exactly one `@AGENTS.md` line and is ≤50 lines total
5. Do NOT copy any content from AGENTS.md into ANTIGRAVITY.md — the `@` import handles it at session load time


### Step 2e: Report Creations

List each created file with its source (template `agents_md_template.md`, template `claude_md_template.md` stub, template `gemini_md_template.md` stub, template `antigravity_md_template.md` stub).

## Phase 3: Token Budget Audit

Line-count budgets align with the Anthropic official target (`<200 lines per CLAUDE.md file`) and the IFScale instruction-ceiling research. See `shared/references/agent_instructions_writing_guide.md` for the full rationale.

| Check | Pass | Warn | Fail |
|-------|------|------|------|
| AGENTS.md line count | ≤150 | 151-200 | >200 |
| CLAUDE.md line count (stub) | ≤20 | 21-50 | >50 |
| GEMINI.md line count (stub) | ≤20 | 21-50 | >50 |
| ANTIGRAVITY.md line count (stub) | ≤20 | 21-50 | >50 |
| User-added imperative count in AGENTS.md | ≤100 | 101-150 | >150 |

**Imperative counter:** lines matching `^\s*- ` inside rule sections, plus any line containing `MUST\|NEVER\|ALWAYS\|DO NOT`. Cite the IFScale benchmark (arxiv 2507.11538) in WARN / FAIL messages.

Report table per file with line count and imperative count (for AGENTS.md).

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
| 1 | Has build/test commands | Found `npm\|cargo\|pytest\|dotnet` commands in AGENTS.md | Missing — add essential commands |
| 2 | No abstract principles | No `"write quality code"`, `"follow best practices"` | Found vague instructions |
| 3 | No redundant docs | No API docs, no full architecture description | Found content discoverable from code |
| 4 | Has hard boundaries | Found `NEVER\|ALWAYS\|MUST\|DO NOT` rules in AGENTS.md | Missing explicit prohibitions |
| 5 | Compact Instructions section | `## Compact Instructions` present in AGENTS.md with preservation priorities | Missing — sessions lose decisions on /compact |
| 6 | MCP Tool Preferences | Canonical policy section in AGENTS.md matches `shared/references/mcp_tool_preferences.md` | Missing or outdated — agents use suboptimal tools |
| 7 | No tool output examples | No large code blocks or command outputs | Found — bloats every turn |

Checks #1–#6 evaluate AGENTS.md only because CLAUDE.md / GEMINI.md / ANTIGRAVITY.md inherit that content via the `@AGENTS.md` import. Checks on the deltas themselves live in Phase 6.

### Phase 5b: Auto-fix Fixable Issues

For each FAIL in Phase 5, attempt auto-fix before reporting:

**Before any auto-fix insertion:**
1. Verify insertion point exists (exact heading found at specific line)
2. If ambiguous (heading not found) — WARN and skip (report as manual fix needed)
3. After insertion — verify no duplicate `## Compact Instructions` or `## MCP Tool Preferences` sections exist in the file


| # | Issue | Fix | Skip when |
|---|-------|-----|----------|
| 5 | Missing Compact Instructions | Insert `## Compact Instructions` section before `## Navigation` in AGENTS.md | `dry_run: true` |
| 6 | Missing or outdated MCP Tool Preferences | Insert or replace section in AGENTS.md from `shared/references/mcp_tool_preferences.md` | `dry_run: true` |
| 1 | Missing build/test commands | WARN only (project-specific, cannot auto-generate) | -- |
| 2 | Abstract principles found | WARN only (requires human judgment) | -- |

**Compact Instructions template** (insert in AGENTS.md before `## Navigation` or after last rules section):

```markdown
## Compact Instructions

Preserve during /compact: [Critical Rules], [MCP Tool Preferences table],
[Navigation table], [language/communication rules], [hard boundaries (NEVER/ALWAYS)].
Drop examples and explanations first.
```

Because CLAUDE.md, GEMINI.md, and ANTIGRAVITY.md `@AGENTS.md`, the preservation list propagates to all of them. The harness-specific terminology (`/compact` vs context compression) lives in each stub's delta.

## Phase 6: Import Pattern Compliance

AGENTS.md is the canonical source per `DOC_ROLE` metadata. CLAUDE.md, GEMINI.md, and ANTIGRAVITY.md must be thin `@AGENTS.md` import stubs with bounded harness-specific deltas.

| # | Check | Pass | Fail |
|---|-------|------|------|
| 1 | CLAUDE.md has `@AGENTS.md` import | Exactly one `@AGENTS.md` line present | Missing or multiple — FAIL |
| 2 | GEMINI.md has `@AGENTS.md` import | Exactly one `@AGENTS.md` line present | Missing or multiple — FAIL |
| 3 | CLAUDE.md delta bounded | Total file ≤50 lines | >50 lines — FAIL with drift report |
| 4 | GEMINI.md delta bounded | Total file ≤50 lines | >50 lines — FAIL with drift report |
| 5 | No content duplication | No section or rule from AGENTS.md reappears in CLAUDE.md / GEMINI.md | Duplicate found — FAIL, name the specific overlapping lines |

**Drift resolution rule:** AGENTS.md is the canonical source. For each inconsistency:
- (a) If content is missing from AGENTS.md but present in CLAUDE.md / GEMINI.md → move it to AGENTS.md, then remove from the stub.
- (b) If CLAUDE.md / GEMINI.md duplicate AGENTS.md content → replace with a single `@AGENTS.md` import line.
- (c) If the stub delta exceeds 50 lines → split genuinely harness-specific content into `.claude/rules/*.md` (for Claude) or modular `@imports` (for Gemini); everything else moves to AGENTS.md.

**Do not** "suggest which file is source of truth" based on content volume — AGENTS.md is always the source.

If `.hex-skills/environment_state.json` reports `agents.codex.discovery_violation=true`, emit a WARN that Codex skill discovery is drifted and duplicate skill counts from stale cache must not be used as evidence during instruction audits until `ln-013-config-syncer` repairs the mapping.

If `.hex-skills/environment_state.json` reports `agents.codex.permissions_default_ready=false`, emit a WARN that Codex CLI startup permissions are drifted from the managed default and instruction audits must not assume full-access startup semantics until `ln-013-config-syncer` repairs `~/.codex/config.toml`.

## Phase 7: Report

```
Agent Instructions Manager:

Created:  (omit section if nothing created)
- AGENTS.md (from template, context from package.json)
- CLAUDE.md (import stub)
- GEMINI.md (import stub)

Audit:
| File       | Lines | Imperatives | Cache-safe | Quality | Import pattern | Issues |
|------------|-------|-------------|------------|---------|----------------|--------|
| AGENTS.md  | 118   | 47          | OK         | 7/7     | n/a            | OK |
| CLAUDE.md  | 13    | 0           | OK         | 7/7     | OK             | OK |
| GEMINI.md  | 12    | 0           | OK         | 7/7     | OK             | OK |

Import pattern: OK (or N drift issues listed)

Recommendations:
1. Run /init (ln-100) for full context-aware AGENTS.md with project-specific rules
```

**Cross-agent note:** Codex CLI 0.120 (2026-04-11) now supports `SessionStart` hook with `/clear` vs fresh/resume distinction, matching Claude Code behavior.

## Definition of Done

- [ ] All instruction files discovered
- [ ] Missing files created (AGENTS.md from template first; CLAUDE.md and GEMINI.md as `@AGENTS.md` import stubs second)
- [ ] Token budget within limits: AGENTS.md ≤200 lines, CLAUDE.md and GEMINI.md each ≤50 lines, AGENTS.md imperative count ≤150
- [ ] No prompt cache breakers found (or reported as WARN)
- [ ] Content quality checks passed on AGENTS.md (or issues reported)
- [ ] Auto-fixable issues resolved in AGENTS.md (Compact Instructions, MCP Tool Preferences) or reported if dry_run
- [ ] Import pattern compliance verified: CLAUDE.md and GEMINI.md each contain exactly one `@AGENTS.md` line and no duplicated AGENTS.md content
- [ ] Report generated with creation log, drift findings, and actionable recommendations
- [ ] No conflicting external plugins detected (or user confirmed keep)
- [ ] Structured summary returned
- [ ] Summary artifact written to the managed or standalone runtime path

**Critical Rule: Non-destructive file edits.** Auto-fix inserts sections at verified positions only. Never rewrite the entire instruction file. Preserve all existing content outside the inserted section.

**Version:** 2.2.0
**Last Updated:** 2026-03-25
