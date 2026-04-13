---
name: prd-taskmaster-v2
description: >-
  Zero-config goal-to-tasks engine. Takes any goal (software, pentest, business, learning),
  runs adaptive discovery via brainstorming, generates a validated spec, parses into TaskMaster
  tasks, and hands off to execution. Use when user says "PRD", "product requirements",
  "I want to build", or wants task-driven development.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Skill
  - AskUserQuestion
  - WebSearch
---

# prd-taskmaster-v2

Zero-config goal-to-tasks engine. AI handles discovery and content; `script.py` and the `prd-taskmaster` MCP handle mechanics.

**Script**: `~/.claude/skills/prd-taskmaster-v2/script.py` (all commands output JSON)
**MCP**: `mcp__prd-taskmaster__*` tools (see `mcp_server/README.md` for registration)

## Tool Preference — MCP First, CLI Fallback

This skill is designed to run against **two MCP servers in tandem**:

| Operation domain | Preferred | Fallback |
|---|---|---|
| Skill mechanics (preflight, validate-prd, detect-capabilities, backup-prd, log-progress) | `mcp__prd-taskmaster__*` | `python3 script.py <subcommand>` |
| TaskMaster operations (parse_prd, analyze_complexity, expand_task, list, next, set_status) | `mcp__task-master-ai__*` | `task-master <subcommand>` |

Prefer MCP whenever both servers are registered — structured data, lower token cost, first-class error handling. Fall back to CLI only when a given MCP is not available in the current session. Detection is done via `validate-setup` in Phase 0.

## When to Use

Activate: PRD, product requirements, taskmaster, task-driven development, "I want to build X", any goal.
Skip: API docs, test specs, project timelines, PDF creation.

## Phase 0: Setup Gate

Read the phase file and follow it:
```
Read ~/.claude/skills/prd-taskmaster-v2/phases/SETUP.md
```

One-shot diagnostic (preferred):
- **MCP**: `mcp__prd-taskmaster__validate_setup()`
- **CLI**: `python3 script.py validate-setup`

Returns 6 structured checks with per-failure fix commands. Default provider is `claude-code` + `sonnet` (zero API key for Claude Max users).

**Gate: `validate-setup` reports `ready: true` with 0 critical failures. Proceed to Preflight.**

## Phase 1: Zero-Config Preflight

Run preflight and auto-detect everything. Ask zero setup questions.

- **MCP**: `mcp__prd-taskmaster__preflight(cwd=".")`
- **CLI**: `python3 script.py preflight`

**From preflight JSON, determine the state:**

| Condition | Action |
|-----------|--------|
| `prd_path` exists + `task_count > 0` | Ask: execute tasks / update PRD / new PRD / review |
| `prd_path` exists + `task_count == 0` | Ask: parse existing PRD / replace with new PRD / review then decide. `backup-prd` before replacing. |
| `taskmaster_method == "none"` | Return to Phase 0 — setup incomplete |
| `has_taskmaster` but no PRD | Proceed to Discovery |
| `has_crash_state` | Offer: resume from crash point or start fresh |

**Autonomous mode:** if invoked via `/pentest-wtf`, `/ralph-loop`, or with auto-approval active and no human to answer, choose sensible defaults without blocking: backup-and-replace for stale PRDs, fresh for missing crash state, proceed to Discovery with self-brainstorm. See `phases/DISCOVER.md` for the autonomous discovery path.

**Gate: TaskMaster detected and environment ready. Proceed to Discovery.**

## Phase 2: Discovery

Read the phase file and follow it:
```
Read ~/.claude/skills/prd-taskmaster-v2/phases/DISCOVER.md
```

Progressive, adaptive, domain-agnostic discovery via superpowers:brainstorming.

**Gate: Discovery complete and user approved design. Proceed to Generate.**

## Phase 3: Generate & Validate

Read the phase file and follow it:
```
Read ~/.claude/skills/prd-taskmaster-v2/phases/GENERATE.md
```

Generate spec, validate quality, parse tasks. Uses TaskMaster's native tools:
- **`analyze-complexity`**: Replaces custom enrich-tasks — TaskMaster classifies task complexity natively
- **`expand_task`**: Decomposes each task into verifiable subtasks with optional research

**Gate: PRD validated GOOD+ and tasks parsed with subtasks. Proceed to Handoff.**

## Phase 4: Handoff

Read the phase file and follow it:
```
Read ~/.claude/skills/prd-taskmaster-v2/phases/HANDOFF.md
```

Detect capabilities, recommend ONE execution mode, hand off.

**Gate: User chose mode and handoff complete.**

## Script Commands Reference

| Command | Purpose |
|---------|---------|
| `preflight` | Detect environment state |
| `detect-taskmaster` | Find MCP or CLI taskmaster |
| `detect-capabilities` | Scan for available skills/tools/plugins |
| `load-template --type comprehensive\|minimal` | Load PRD template |
| `validate-prd --input <path>` | Quality checks + placeholder detection |
| `calc-tasks --requirements <count>` | Recommended task count |
| `backup-prd --input <path>` | Timestamped backup |
| `gen-test-tasks --total <count>` | Generate USER-TEST task specs |
| `gen-scripts --output-dir <dir>` | Create tracking scripts |
| `log-progress --task-id T --title "..."` | Append to progress.md |
| `init-taskmaster --method cli\|mcp` | Initialize taskmaster project |
| `read-state` | Read crash recovery state |

## Context

**In the pipeline:** atlas-start → **prd-taskmaster-v2** → atlas-plan → atlas-loop → atlas-sync
**Standalone:** Works on its own. Takes any goal, produces spec + tasks.
**Produces:** prd.md + tasks.json (in .taskmaster/)
**Can invoke next:** atlas-plan (for planning), then execution mode of choice

## Critical Rules

1. Zero setup questions — detect everything, ask only discovery questions
2. Phase 0 runs FIRST — use `validate-setup` to verify environment before anything else
3. Default to `claude-code` provider — zero API key for Claude Max users
4. Discovery via superpowers:brainstorming — one question at a time, adaptive; autonomous self-brainstorm if no user present
5. Domain-agnostic — works for any goal (app, pentest, business, anything)
6. Use TaskMaster's native `analyze-complexity` and `expand_task` — no custom enrichment
7. **Prefer `mcp__prd-taskmaster__*` and `mcp__task-master-ai__*` tools over CLI subprocess** when registered — structured data, lower token cost
8. Validate PRDs catch placeholders — mustache, TBD, TODO patterns fail validation
9. Handoff recommends ONE mode — Mode C (free ralph-loop) by default, Mode D only if atlas-loop + atlas-cdd actually detected
10. Phase files must be Read explicitly — they are not auto-loaded
