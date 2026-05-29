---
name: mcp-optimizer
description: Use when optimizing MCP server usage to reduce token overhead. Helps select appropriate servers based on task type.
---

# MCP Optimizer Skill

## Purpose

Optimize MCP server usage to reduce token overhead. Each MCP server consumes tokens for tool definitions - this skill helps select only the servers needed for the current task.

## Token Impact Reference

| Server              | Approximate Tokens | Use Cases                                   |
| ------------------- | ------------------ | ------------------------------------------- |
| playwright          | ~5K                | UI testing, screenshots, browser automation |
| memory              | ~2K                | Context persistence, session continuity     |
| sequential-thinking | ~1K                | Complex reasoning, multi-step problems      |
| github              | ~3K                | PR management, issue tracking               |
| filesystem          | ~2K                | Enhanced file operations                    |
| **Total**           | **~13K**           | All servers loaded                          |

## Task-Based Server Recommendations

### Backend Development

**Recommended servers:** memory, sequential-thinking
**Token savings:** ~8K (60%)

Tasks: CQRS commands, entity development, data migrations

### Frontend Development

**Recommended servers:** memory, playwright, sequential-thinking
**Token savings:** ~5K (38%)

Tasks: Component development, UI testing, form validation

### PR/Issue Workflow

**Recommended servers:** memory, github
**Token savings:** ~8K (60%)

Tasks: Create PRs, fix issues, code review

### Debugging

**Recommended servers:** memory, sequential-thinking, playwright
**Token savings:** ~5K (38%)

Tasks: Bug diagnosis, root cause analysis, behavior verification

### Code Review

**Recommended servers:** memory, github
**Token savings:** ~8K (60%)

Tasks: Review changes, check patterns, verify compliance

### Architecture/Planning

**Recommended servers:** memory, sequential-thinking
**Token savings:** ~8K (60%)

Tasks: Design decisions, impact analysis, dependency mapping

## Optimization Strategies

### 1. Session Cleanup

Use `/clear` command after completing major tasks to reset context:

```
/clear
```

This removes accumulated tool outputs and conversation history while preserving essential context.

### 2. MAX_MCP_OUTPUT_TOKENS

Set environment variable to limit MCP tool output size:

```bash
export MAX_MCP_OUTPUT_TOKENS=25000
```

This prevents large tool outputs from consuming excessive context.

### 3. Selective Tool Usage

When a task doesn't need specific MCP capabilities:

- **Skip Playwright** for backend-only work
- **Skip GitHub** when not doing PR/issue work
- **Keep Memory** for session continuity (always recommended)
- **Keep Sequential-Thinking** for complex reasoning

### 4. Deferred Tool Discovery

For large result sets, use filtering before full retrieval:

```
# Instead of getting all, filter first
mcp__memory__search_nodes({ query: "specific-term" })

# Then open only relevant nodes
mcp__memory__open_nodes({ names: ["specific-entity"] })
```

## Server Configuration Guide

The MCP server configuration is in `.mcp.json`:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@package/name"],
      "description": "Purpose description"
    }
  }
}
```

### To Temporarily Disable a Server

Comment out or remove from `.mcp.json`, then restart Claude Code.

### Task-Specific Configurations

Consider creating task-specific MCP configurations:

```
.mcp.json              # Full configuration (default)
.mcp.backend.json      # Backend-focused (memory, sequential-thinking)
.mcp.frontend.json     # Frontend-focused (memory, playwright)
.mcp.pr-workflow.json  # PR workflow (memory, github)
```

## Token Budget Planning

For 200K context window:

| Usage                  | Tokens | Percentage |
| ---------------------- | ------ | ---------- |
| MCP Tools (all)        | ~13K   | 6.5%       |
| CLAUDE.md              | ~15K   | 7.5%       |
| Skills (loaded)        | ~5K    | 2.5%       |
| Instructions           | ~3K    | 1.5%       |
| **Available for work** | ~164K  | 82%        |

With optimization (backend-only):

| Usage                  | Tokens | Percentage |
| ---------------------- | ------ | ---------- |
| MCP Tools (optimized)  | ~3K    | 1.5%       |
| CLAUDE.md              | ~15K   | 7.5%       |
| Skills (loaded)        | ~5K    | 2.5%       |
| Instructions           | ~3K    | 1.5%       |
| **Available for work** | ~174K  | 87%        |

**Net gain: 10K tokens (5% improvement)**

## Best Practices

1. **Start minimal** - Enable only needed servers at session start
2. **Add as needed** - Enable additional servers when task requires
3. **Clear regularly** - Use `/clear` after major task completion
4. **Monitor usage** - Watch token indicator during complex sessions
5. **Store context** - Use Memory MCP before clearing to preserve learnings

## Verification Checklist

Before starting a session, consider:

```
[ ] What type of task am I doing?
[ ] Which MCP servers are needed?
[ ] Can I disable unused servers?
[ ] Should I clear previous context?
[ ] Is Memory MCP preserving important context?
```
