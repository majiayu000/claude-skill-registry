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

Zero-config goal-to-tasks engine. AI handles discovery and content; `script.py` handles mechanics.

**Script**: `~/.claude/skills/prd-taskmaster-v2/script.py` (all commands output JSON)

## When to Use

Activate: PRD, product requirements, taskmaster, task-driven development, "I want to build X", any goal.
Skip: API docs, test specs, project timelines, PDF creation.

## Phase 0: Setup Gate

Read the phase file and follow it:
```
Read ~/.claude/skills/prd-taskmaster-v2/phases/SETUP.md
```

Verify TaskMaster is installed, initialized, and the AI pipeline works.
Default to `claude-code` provider (zero API key for Claude Max users).

**Gate: TaskMaster installed, project initialized, provider configured. Proceed to Preflight.**

## Phase 1: Zero-Config Preflight

Run preflight and auto-detect everything. Ask zero setup questions.

```bash
python3 ~/.claude/skills/prd-taskmaster-v2/script.py preflight
```

**From preflight JSON, determine the state:**

| Condition | Action |
|-----------|--------|
| `prd_path` exists + `task_count > 0` | Ask: execute tasks / update PRD / new PRD / review |
| `taskmaster_method == "none"` | Return to Phase 0 — setup incomplete |
| `has_taskmaster` but no PRD | Proceed to Discovery |
| `has_crash_state` | Offer: resume from crash point or start fresh |

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
2. Phase 0 runs FIRST — verify TaskMaster before anything else
3. Default to `claude-code` provider — zero API key for Claude Max users
4. Discovery via superpowers:brainstorming — one question at a time, adaptive
5. Domain-agnostic — works for any goal (app, pentest, business, anything)
6. Use TaskMaster's native `analyze-complexity` and `expand_task` — no custom enrichment
7. Validate PRDs catch placeholders — mustache, TBD, TODO patterns fail validation
8. Handoff recommends ONE mode — present best fit, not 4 equal choices
9. Phase files must be Read explicitly — they are not auto-loaded
