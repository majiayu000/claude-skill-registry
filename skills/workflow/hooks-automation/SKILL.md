---
name: hooks-automation
title: Hooks Automation
version: 2.0.0
category: development
description: Automated coordination, formatting, and learning from Claude Code operations using intelligent hooks with MCP integration
author: Claude Flow
tags:
  - hooks
  - automation
  - coordination
  - memory
  - neural-training
difficulty: intermediate
prerequisites:
  - Claude Flow CLI installed (npm install -g claude-flow@alpha)
  - Claude Code with hooks enabled
  - .claude/settings.json with hook configurations
tools_required:
  - npx claude-flow hook
  - mcp__claude-flow__*
related_skills:
  - sparc-methodology
  - swarm-orchestration
  - verification-quality
---

# Hooks Automation

## Behavioral Classification

**Type**: Autonomous Execution

This skill provides hooks that execute automatically in response to Claude Code operations. No interactive decisions required.

**Trigger Points**:
- Pre-operation: Validates and prepares before edits, commands, tasks
- Post-operation: Formats, analyzes, and trains after operations
- Session: Manages state across sessions
- MCP: Coordinates with swarm agents

---

## Overview

Intelligent automation system that coordinates, validates, and learns from Claude Code operations through hooks integrated with MCP tools and neural pattern training.

**Key Capabilities:**
- **Pre-Operation Hooks**: Validate, prepare, and auto-assign agents
- **Post-Operation Hooks**: Format, analyze, and train patterns
- **Session Management**: Persist state, restore context
- **Memory Coordination**: Synchronize knowledge across swarm agents
- **Git Integration**: Automated commit hooks with quality verification
- **Neural Training**: Continuous learning from successful patterns

---

## Quick Start

### Initialize Hooks System

```bash
# Initialize with default hooks configuration
npx claude-flow init --hooks
```

This creates:
- `.claude/settings.json` with pre-configured hooks
- Hook command documentation in `.claude/commands/hooks/`
- Default hook handlers for common operations

### Basic Hook Usage

```bash
# Pre-task hook (auto-spawns agents)
npx claude-flow hook pre-task --description "Implement authentication"

# Post-edit hook (auto-formats and stores in memory)
npx claude-flow hook post-edit --file "src/auth.js" --memory-key "auth/login"

# Session end hook (saves state and metrics)
npx claude-flow hook session-end --session-id "dev-session" --export-metrics
```

---

## Sub-Documentation

For detailed information, see the following files:

| Document | Contents |
|----------|----------|
| [Pre-Hooks](./pre-hooks.md) | pre-edit, pre-bash, pre-task, pre-search |
| [Post-Hooks](./post-hooks.md) | post-edit, post-bash, post-task, post-search |
| [MCP Integration](./mcp-integration.md) | MCP hooks, memory coordination, agent workflows |
| [Session Management](./session.md) | session-start, session-restore, session-end |
| [Configuration](./configuration.md) | Settings, git hooks, custom hooks |

---

## Available Hooks

### Pre-Operation Hooks
| Hook | Description |
|------|-------------|
| `pre-edit` | Validate and assign agents before file modifications |
| `pre-bash` | Check command safety and resource requirements |
| `pre-task` | Auto-spawn agents and prepare for complex tasks |
| `pre-search` | Prepare and optimize search operations |

### Post-Operation Hooks
| Hook | Description |
|------|-------------|
| `post-edit` | Auto-format, validate, and update memory |
| `post-bash` | Log execution and update metrics |
| `post-task` | Performance analysis and decision storage |
| `post-search` | Cache results and improve patterns |

### Session Hooks
| Hook | Description |
|------|-------------|
| `session-start` | Initialize new session |
| `session-restore` | Load previous session state |
| `session-end` | Cleanup and persist session state |
| `notify` | Custom notifications with swarm status |

### MCP Integration Hooks
| Hook | Description |
|------|-------------|
| `mcp-initialized` | Persist swarm configuration |
| `agent-spawned` | Update agent roster and memory |
| `task-orchestrated` | Monitor task progress |
| `neural-trained` | Save pattern improvements |

---

## Quick Reference

### Most Common Commands

```bash
# Pre-task preparation
npx claude-flow hook pre-task --description "Task description"

# Post-edit with memory storage
npx claude-flow hook post-edit --file "path/to/file" --memory-key "key"

# Session management
npx claude-flow hook session-start --session-id "my-session"
npx claude-flow hook session-end --session-id "my-session" --export-metrics

# Notifications
npx claude-flow hook notify --message "Task completed" --broadcast
```

### Hook Response Format

```json
{
  "continue": true,
  "reason": "All validations passed",
  "metadata": {
    "agent_assigned": "backend-dev",
    "syntax_valid": true
  }
}
```

---

## Benefits

- **Automatic Agent Assignment**: Right agent for every file type
- **Consistent Code Formatting**: Language-specific formatters
- **Continuous Learning**: Neural patterns improve over time
- **Cross-Session Memory**: Context persists between sessions
- **Performance Tracking**: Comprehensive metrics and analytics
- **Quality Gates**: Pre-commit validation and verification

---

## Performance Tips

1. **Keep Hooks Lightweight** - Target < 100ms execution time
2. **Use Async for Heavy Operations** - Don't block the main flow
3. **Cache Aggressively** - Store frequently accessed data
4. **Batch Related Operations** - Combine multiple actions
5. **Use Memory Wisely** - Set appropriate TTLs

---

## Related Skills

- `sparc-methodology` - Hooks enhance SPARC workflows
- `pair-programming` - Automated quality in pairing sessions
- `verification-quality` - Truth-score validation in hooks
- `swarm-advanced` - Multi-agent coordination via hooks

---

**Version**: 2.0.0
**Last Updated**: 2025-01-24
