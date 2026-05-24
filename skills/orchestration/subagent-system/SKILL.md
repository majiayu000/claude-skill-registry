---
name: Subagent System
description: Create and manage specialized Claude Code subagents for task-specific workflows. Use when delegating work to specialized agents, configuring agent permissions, or understanding subagent architecture and best practices.
---

# Subagent System

## When to Use

- Creating specialized subagents for task-specific work
- Delegating work to pre-configured agents
- Managing subagent tool permissions and scope
- Understanding when to use agent delegation vs. direct work

## What Are Subagents?

Pre-configured AI personalities that Claude Code can delegate tasks to. Each:
- Has specific purpose and expertise area
- Uses separate context window (prevents pollution)
- Can be configured with specific tools
- Includes custom system prompt

Benefits:
- **Context preservation** — Each operates in own context, keeping main conversation focused
- **Specialized expertise** — Fine-tuned instructions for specific domains
- **Reusability** — Use across projects and share with team
- **Flexible permissions** — Different tool access levels per agent

## Creating Subagents

### File Locations

| Type | Location | Scope |
|------|----------|-------|
| **Project subagents** | `.claude/agents/` | Current project only |
| **User subagents** | `~/.claude/agents/` | All projects |

Project-level subagents take precedence over user-level when names conflict.

### File Format

Each subagent is a Markdown file with YAML frontmatter:

```markdown
---
name: your-sub-agent-name
description: When this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all if omitted
model: sonnet  # Optional - specify model or 'inherit'
---

Your subagent's system prompt goes here. Multiple paragraphs.
Include role, capabilities, approach, best practices, constraints.
```

### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase + hyphens) |
| `description` | Yes | Natural language purpose description |
| `tools` | No | Comma-separated tools (inherits all if omitted) |
| `model` | No | Model alias (`sonnet`, `opus`, `haiku`) or `'inherit'` |

## Using Subagents Effectively

### Automatic Delegation
Claude Code proactively delegates based on:
- Task description in your request
- `description` field in subagent configuration
- Current context and available tools

To encourage proactive use, include "use PROACTIVELY" or "MUST BE USED" in description.

### Explicit Invocation
Request specific subagents by name:
```
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my recent changes
```

## Management

### Using `/agents` Command (Recommended)
Interactive menu for:
- View all available subagents
- Create new subagents with guided setup
- Edit existing custom subagents
- Delete custom subagents
- Manage tool permissions

### Direct File Management
```bash
mkdir -p .claude/agents
cat > .claude/agents/test-runner.md << 'EOF'
---
name: test-runner
description: Use proactively to run tests and fix failures
---

You are a test automation expert. When you see code changes, proactively run the appropriate tests. If tests fail, analyze failures and fix them.
EOF
```

## Best Practices

- **Start with Claude-generated agents**, then customize
- **Design focused subagents** with single, clear responsibility
- **Write detailed prompts** with specific instructions, examples, constraints
- **Limit tool access** to only necessary tools
- **Version control** project subagents for team collaboration

## Performance Notes

- **Context efficiency**: Agents preserve main context, enabling longer sessions
- **Latency**: Subagents start with clean slate, may add latency gathering context
