---
name: zellij-driver
description: >
  Programmatic Zellij terminal workspace management for agentic workflows.
  Use when orchestrating parallel development tasks, creating tabs/panes,
  tracking developer intent, or managing terminal layouts. Triggers include:
  (1) Creating tabs with specific naming conventions,
  (2) Spawning multiple panes for parallel work,
  (3) Logging and retrieving developer intent/context,
  (4) Workspace layout organization for agent coordination,
  (5) Integration with iMi worktrees for branch-per-pane workflows.
---

# Zellij Driver (Perth)

## Overview

Perth (`znav`) is a Redis-backed Zellij pane manager that tracks developer intent and cognitive context across terminal sessions. It enables programmatic control of Zellij tabs and panes, making it ideal for orchestrating parallel agentic workflows.

**Core Philosophy:** Capture what you're working on, not just what you typed. Perth bridges the gap between terminal activity and developer intent, enabling AI agents to understand and resume work context.

## Core Capabilities

### 1. Tab and Pane Management

**Create Named Tabs:**
```bash
znav tab my-feature                    # Switch to or create tab
znav pane my-task --tab my-feature     # Create pane in specific tab
```

**Pane Operations:**
```bash
znav pane api-refactor                 # Create/open pane (auto-creates tab if needed)
znav pane info api-refactor            # Get pane metadata
znav list                              # Tree view of all sessions/tabs/panes
znav reconcile                         # Sync Redis state with Zellij layout
```

### 2. Intent Tracking (Perth v2.0)

Track what you're working on, not just commands:

**Log Intent Entries:**
```bash
# Simple checkpoint
znav pane log my-feature "Fixed authentication bug"

# Milestone with artifacts
znav pane log api-refactor "Completed REST API redesign" \
    --type milestone --artifacts src/api.rs docs/api.md

# Exploration session
znav pane log research "Investigated caching strategies" --type exploration

# Agent-generated entry
znav pane log my-feature "Completed task analysis" --source agent
```

**Entry Types:**
- `checkpoint` (default): Regular progress markers
- `milestone`: Major accomplishments worth highlighting
- `exploration`: Research or investigative work

**Entry Sources:**
- `manual` (default): Human-created entries
- `agent`: Created by AI during assisted workflow
- `automated`: System-generated from activity detection

### 3. History Retrieval

Multiple output formats for different use cases:

```bash
# Human-readable (default)
znav pane history my-feature

# JSON for programmatic access
znav pane history my-feature --format json

# Compact JSON for piping
znav pane history my-feature --format json-compact | jq '.entries[0]'

# Markdown export (Obsidian-compatible)
znav pane history my-feature --format markdown > session.md

# LLM-optimized context for agent integration (~1000 tokens)
znav pane history my-feature --format context
```

### 4. LLM-Powered Snapshots

Auto-generate intent summaries from recent work:

```bash
# Generate AI summary of recent activity
znav pane snapshot my-feature

# Requires LLM configuration and consent
znav config set llm.provider anthropic
znav config consent --grant
```

**Supported Providers:**
- `anthropic` (Claude) - default model: claude-sonnet-4-20250514
- `openai` (GPT) - default model: gpt-4o-mini
- `ollama` (local) - default model: llama3.2
- `none` - disabled

### 5. Configuration Management

```bash
znav config show                       # View all settings
znav config set redis_url redis://...  # Update Redis connection
znav config consent --grant            # Allow LLM data sharing
znav config consent --revoke           # Revoke LLM consent
```

## Agentic Workflow Patterns

### Pattern 1: Parallel PR Fixes

When implementing multiple fixes from a PR in parallel:

```bash
# 1. Create a tab for the fixes (with optional correlation ID)
znav tab "myapp(fixes)"

# 2. Create individual panes for each fix
znav pane fix-auth --tab "myapp(fixes)"
znav pane fix-errors --tab "myapp(fixes)"
znav pane fix-docs --tab "myapp(fixes)"

# 3. Each pane can be worked on by a separate agent
# Agent in fix-auth pane:
znav pane log fix-auth "Starting auth token refresh fix" --source agent
# ... agent does work ...
znav pane log fix-auth "Completed auth fix" --type milestone --source agent
```

### Pattern 2: iMi Integration

Combine with iMi worktrees for branch-per-pane isolation:

```bash
# 1. Create worktrees with iMi
imi add fix auth-refresh
imi add fix error-handling
imi add fix api-docs

# 2. Create Zellij workspace matching worktrees
znav tab "myapp(fixes)"

# 3. Create panes and set working directories
znav pane fix-auth --tab "myapp(fixes)"
# Then in pane: cd ~/code/myapp/fix-auth-refresh/

znav pane fix-errors --tab "myapp(fixes)"
# Then in pane: cd ~/code/myapp/fix-error-handling/

znav pane fix-docs --tab "myapp(fixes)"
# Then in pane: cd ~/code/myapp/fix-api-docs/
```

### Pattern 3: Session Resumption

When returning to a pane, Perth displays the last intent:

```bash
# First session
znav pane my-feature
znav pane log my-feature "Implementing user authentication flow"
# ... work happens ...

# Later session (shows resume context)
znav pane my-feature
# Output: "Resuming: ● Implementing user authentication flow (2 hours ago)"
```

### Pattern 4: Agent Context Injection

Get condensed context for LLM prompts:

```bash
# Get ~1000 token context summary
CONTEXT=$(znav pane history my-feature --format context)

# Inject into agent prompt
echo "Continue this work session:\n$CONTEXT"
```

## Tab Naming Conventions

For agentic workflows, use consistent naming:

| Pattern | Example | Use Case |
|---------|---------|----------|
| `{repo}(fixes)` | `myapp(fixes)` | PR fix batch |
| `{repo}({branch})` | `myapp(feat-auth)` | Feature branch work |
| `{repo}({context})-{id}` | `myapp(fixes)-abc123` | Bloodbank correlation |
| `{task}` | `research-caching` | Exploration work |

## Current Limitations

**Not Yet Implemented (Sprint 5 backlog):**
- Batch pane creation (`znav pane batch --panes a,b,c`)
- Tab naming with correlation ID (`--correlation-id`)
- Bloodbank event publishing
- MCP tool exposure

**Zellij Version:**
- Requires Zellij >= 0.39.0

## Data Model

**IntentEntry:**
```json
{
  "id": "uuid",
  "timestamp": "2025-01-06T12:00:00Z",
  "summary": "What you were working on",
  "entry_type": "checkpoint|milestone|exploration",
  "source": "manual|agent|automated",
  "artifacts": ["file1.rs", "file2.ts"],
  "commands_run": 15,
  "goal_delta": "Progress description"
}
```

**PaneRecord:**
- Tracks session, tab, pane name, position
- Stores metadata for navigation
- Marks stale panes after reconciliation

## Redis Keyspace

Perth v2.0 uses the `perth:` keyspace:

```
perth:pane:{name}          # Pane metadata hash
perth:intent:{name}        # Intent history list (LPUSH/LRANGE)
```

Migration from v1.0 (`znav:`) keyspace:
```bash
znav migrate --dry-run     # Preview migration
znav migrate               # Execute migration
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `znav pane <name>` | Create/open pane |
| `znav pane --tab <tab> <name>` | Pane in specific tab |
| `znav pane log <name> "<summary>"` | Log intent entry |
| `znav pane history <name>` | View history |
| `znav pane history <name> --format context` | LLM-ready context |
| `znav pane snapshot <name>` | AI-generate summary |
| `znav pane info <name>` | Pane metadata |
| `znav tab <name>` | Switch/create tab |
| `znav list` | Tree view of workspace |
| `znav reconcile` | Sync state with layout |
| `znav config show` | View configuration |
| `znav config consent --grant` | Allow LLM sharing |

## Integration Points

**33GOD Ecosystem:**
- **iMi**: Worktree management for branch isolation
- **Bloodbank**: Event publishing for workflow triggers (planned)
- **Jelmore**: Session correlation tracking (planned)
- **Flume**: Task coordination across panes (planned)

**Claude Code:**
- Use `--format context` for prompt injection
- Use `--source agent` for agent-created entries
- Use `--format json` for programmatic processing
