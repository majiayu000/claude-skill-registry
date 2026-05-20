---
name: mpm-init
description: Initialize or update project for Claude Code and MPM
user-invocable: true
version: "1.0.0"
category: mpm-command
tags: [mpm-command, system, pm-required, setup]
---

# /mpm-init

Initialize or intelligently update project for Claude Code and Claude MPM.

## Usage

```
/mpm-init [update|context|resume|catchup] [options]
```

## Core Modes

### Project Setup

```
/mpm-init                      # Auto-detect: offer update or create
/mpm-init update               # Quick update (30-day git activity)
/mpm-init --update             # Full documentation refresh
/mpm-init --force              # Force recreate from scratch
```

**Delegates to Agentic Coder Optimizer agent** for:
- CLAUDE.md creation/update (with priority rankings 🔴🟡🟢⚪)
- AST analysis and code structure docs
- Single-path workflows (ONE way to do ANYTHING)
- Tool configuration, memory system, gitignore management

**Smart Update Mode:** Auto-detects existing CLAUDE.md and offers update vs recreate.

### Context Analysis

```
/mpm-init context [--days N]   # Intelligent git history analysis (default: 7 days)
/mpm-init catchup              # Quick commit history (last 25 commits, no analysis)
```

**context:** Delegates to Research agent for deep analysis of:
- Active work streams (from commit patterns)
- Intent and motivation (from messages)
- Risks and blockers
- Recommended next actions

**catchup:** Direct CLI execution, instant output.

### Resume from Logs

```
/mpm-init resume [--list] [--session-id ID]
```

Reads stop event logs from `.claude-mpm/resume-logs/` and `.claude-mpm/responses/` showing:
- What was being worked on
- Tasks completed, files modified
- Next steps, stop reason, token usage
- Git context (branch, status)

## Key Options

**Configuration:**
- `--project-type TYPE`: web, api, cli, library
- `--framework NAME`: react, django, fastapi, etc.
- `--ast-analysis` / `--no-ast-analysis`: Enable/disable code analysis
- `--comprehensive` / `--minimal`: Full setup vs CLAUDE.md only

**Organization:**
- `--organize`: Organize misplaced files
- `--preserve-custom`: Keep custom sections (default)
- `--review`: Review without changes

## What Gets Created

**New Projects:**
- ✅ CLAUDE.md (priority-ranked instructions)
- ✅ Single-path workflows (make build/test/deploy)
- ✅ Tool configs (linting, formatting, testing)
- ✅ Memory system (.claude-mpm/memories/)
- ✅ DEVELOPER.md, CODE_STRUCTURE.md (with AST)
- ✅ .gitignore updates (auto-adds .claude-mpm/)

**Updates:**
- ✅ Smart merging (preserves custom sections)
- ✅ Automatic archival (docs/_archive/)
- ✅ Change tracking

## Examples

```bash
# Quick start
/mpm-init                      # Auto-detect mode

# Quick update (lightweight)
/mpm-init update               # 30-day activity report

# Resume work
/mpm-init context --days 14    # Analyze last 2 weeks
/mpm-init resume               # Show latest session from logs
/mpm-init catchup              # Quick commit history

# Full configuration
/mpm-init --project-type web --framework react --comprehensive
```

## Implementation Notes

**Delegation patterns:**
- **Project init/update:** → Agentic Coder Optimizer agent
- **context:** → PM → Research agent (structured analysis)
- **catchup:** → Direct CLI (git log wrapper)
- **resume:** → PM (reads logs, no delegation)

**Token budgets:**
- context analysis: 10-30s processing time
- resume display: ~10-20k tokens
- catchup: instant, minimal tokens

See docs/commands/init.md for comprehensive documentation.
