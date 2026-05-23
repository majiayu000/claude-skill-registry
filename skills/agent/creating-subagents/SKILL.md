---
name: creating-subagents
description: Guide for creating custom Claude Code subagents (Task tool agents). Use when building specialized autonomous agents for specific domains or workflows. Covers agent definition, frontmatter options, tool restrictions, and spawning patterns.
allowed-tools: ["Read", "Write", "Bash", "Glob"]
---

# Creating Subagents

Build specialized AI agents for Claude Code that handle domain-specific tasks with custom configurations, tools, and system prompts.

## Quick Reference

| Element | Requirement |
|---------|-------------|
| Location | `.claude/agents/` (project) or `~/.claude/agents/` (user) |
| Filename | `agent-name.md` |
| Name | Lowercase, hyphens only (e.g., `code-reviewer`) |
| Required Fields | `name`, `description` |
| Optional Fields | `tools`, `model`, `permissionMode`, `skills`, `hooks` |

## What Are Subagents?

Subagents are specialized AI assistants that Claude Code delegates tasks to. They provide:

- **Separate Context** - Own context window, prevents main conversation pollution
- **Custom Tools** - Restricted or expanded tool access
- **Specialized Prompts** - Domain-specific instructions and expertise
- **Flexible Models** - Can use different models (opus, sonnet, haiku)

When Claude encounters a task matching a subagent's expertise, it spawns the subagent via the **Task tool**, which works independently and returns results.

## Built-in vs Custom Agents

### Built-in Agents

Claude Code includes several built-in agents:

| Agent | Model | Mode | Purpose |
|-------|-------|------|---------|
| **Explore** | Haiku | Read-only | Fast codebase search and analysis |
| **Plan** | Inherits | Read-only | Research for plan mode |
| **General-purpose** | Inherits | Read/Write | Complex multi-step tasks |
| **Bash** | Inherits | Commands | Running terminal commands in separate context |
| **statusline-setup** | Sonnet | Config | Configuring status line via `/statusline` |
| **Claude Code Guide** | Haiku | Read-only | Answering questions about Claude Code features |

### When to Create Custom Agents

Create custom agents when you need:

- **Domain expertise** - Security audit, database migration, API design
- **Workflow automation** - Test runner, deployment, documentation
- **Tool restrictions** - Read-only reviewers, sandboxed explorers
- **Team consistency** - Shared agents for common workflows

## Agent Definition Structure

Agents are Markdown files with YAML frontmatter:

```markdown
---
name: agent-name
description: When this agent should be invoked
tools: Tool1, Tool2, Tool3
model: sonnet
permissionMode: default
skills: skill1, skill2
---

System prompt content here.

Detailed instructions for the agent's behavior,
expertise area, and approach to problem-solving.
```

## Frontmatter Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Unique identifier (lowercase, hyphens) |
| `description` | Yes | string | When to invoke (include "PROACTIVELY" for auto-use) |
| `tools` | No | string | Comma-separated tool list (allowlist). Omit to inherit all tools |
| `disallowedTools` | No | string | Comma-separated tools to deny (denylist), removed from inherited list |
| `model` | No | string | `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | No | string | Permission handling mode |
| `skills` | No | string | Skills to load into subagent's context at startup |
| `hooks` | No | object | Agent-scoped hooks (2.1.0+) |

**Note on `skills`:** The full skill content is injected into the subagent, not just made available for invocation. Subagents don't inherit skills from the parent conversation.

### Model Options

| Value | Description |
|-------|-------------|
| `sonnet` | Default. Balanced capability and speed |
| `opus` | Most capable. Use for complex reasoning |
| `haiku` | Fastest. Use for simple, quick tasks |
| `inherit` | Use main conversation's model |

### Permission Modes

Subagents inherit permission context from the main conversation but can override the mode.

| Mode | Description |
|------|-------------|
| `default` | Standard permission checking with prompts |
| `acceptEdits` | Auto-accept file edits |
| `dontAsk` | Auto-deny permission prompts (explicitly allowed tools still work) |
| `bypassPermissions` | Skip all permission checks (**use with caution**) |
| `plan` | Plan mode (read-only exploration) |

**Important:** If the parent uses `bypassPermissions`, this takes precedence and cannot be overridden by subagents.

## Critical Constraint

**Subagents cannot spawn other subagents.** This prevents infinite nesting. Design your agents to be self-contained.

## Hooks in Agent Frontmatter (2.1.0+)

Agents can define hooks scoped to their lifecycle. These hooks are:
- **Lifecycle-scoped** - Only active while the agent executes
- **Auto-cleanup** - Removed when the agent finishes
- **Portable** - Packaged with the agent for distribution

```yaml
---
name: secure-agent
description: Security-focused agent with audit logging
hooks:
  PreToolUse:
    - matcher: "Bash|Write|Edit"
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/audit-log.sh"
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/agent-complete.sh"
---
```

Supported hook events in agent frontmatter:
- `PreToolUse` - Before tool execution
- `PostToolUse` - After tool completion
- `Stop` - When agent finishes

### Conditional Rules with Hooks

For dynamic control over tool usage, use `PreToolUse` hooks to validate operations. This is useful when you need to allow some operations of a tool while blocking others.

**Example: Read-only database agent**

```yaml
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

The validation script reads JSON from stdin, extracts the command, and exits with code 2 to block:

```bash
#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

**Hook exit codes:**
- `0` - Allow operation
- `2` - Block operation (with message to stderr)

## Creating an Agent

### Via /agents Command (Recommended)

```
/agents
```

Interactive interface to:
- **View** all available subagents (built-in, user, project, plugin)
- **Create** new subagents with guided setup or Claude generation
- **Edit** existing subagent configuration and tool access
- **Delete** custom subagents
- **See active** subagents when duplicates exist (higher priority wins)

**Generate with Claude:** Select "Generate with Claude" and describe your subagent. Claude generates the system prompt and configuration. Press `e` to open in your editor.

### Via File Creation

```bash
# Project agent
mkdir -p .claude/agents
cat > .claude/agents/test-runner.md << 'EOF'
---
name: test-runner
description: Run tests and fix failures. Use PROACTIVELY after code changes.
tools: Bash, Read, Glob, Grep, Edit
---

You are a test automation expert.

When invoked:
1. Identify test files related to changes
2. Run appropriate test suite
3. Analyze failures
4. Fix issues while preserving test intent
5. Re-run to verify fixes

Test frameworks to check:
- Jest/Vitest for TypeScript/JavaScript
- pytest for Python
- go test for Go
- cargo test for Rust

Always run tests before reporting completion.
EOF
```

### Via CLI Flag

```bash
claude --agents '{
  "test-runner": {
    "description": "Run tests and fix failures",
    "prompt": "You are a test automation expert...",
    "tools": ["Bash", "Read", "Glob", "Grep", "Edit"],
    "model": "sonnet"
  }
}'
```

## Using Agents

### Automatic Delegation

Claude automatically delegates based on:
- Task matching `description` field
- Current context and available tools
- Phrases like "PROACTIVELY" or "MUST BE USED"

### Explicit Invocation

```
> Use the code-reviewer agent to check my changes
> Have the security-audit agent scan for vulnerabilities
> Ask the database-migration agent to create the schema
```

### Chaining Agents

```
> First use test-runner to find failures, then have debugger fix them
```

### Resuming Agents

Agents can be resumed to continue previous work:

```
> Resume agent abc123 and continue the analysis
```

Each execution gets a unique `agentId` stored in `agent-{agentId}.jsonl`.

## Tool Restrictions

### Read-Only Agent

```yaml
tools: Read, Glob, Grep
```

### Execution-Safe Agent

```yaml
tools: Bash, Read, Glob, Grep
```

**Note:** Bash in this context is still full Bash. For truly safe execution, use hooks to validate commands.

### Write-Capable Agent

```yaml
tools: Read, Write, Edit, Bash, Glob, Grep
```

### Inherit All Tools

Omit the `tools` field entirely to inherit all tools from main thread, including MCP tools.

## Workflow: Creating a Custom Agent

### Prerequisites
- [ ] Identify the domain/expertise area
- [ ] Determine required tools
- [ ] Plan the system prompt

### Steps

1. **Define the agent**
   - [ ] Choose descriptive name (lowercase, hyphens)
   - [ ] Write clear description with trigger phrases
   - [ ] Select minimum necessary tools
   - [ ] Choose appropriate model

2. **Write system prompt**
   - [ ] Define role and expertise
   - [ ] List step-by-step process
   - [ ] Include constraints and best practices
   - [ ] Add output format expectations

3. **Configure location**
   - [ ] Project (`.claude/agents/`) for team sharing
   - [ ] User (`~/.claude/agents/`) for personal use

4. **Test**
   - [ ] Invoke explicitly: "Use the X agent to..."
   - [ ] Check `/agents` menu for registration
   - [ ] Verify tool restrictions work

### Validation
- [ ] Name is lowercase with hyphens
- [ ] Description explains when to use
- [ ] Tools are minimum necessary
- [ ] System prompt is clear and actionable

## Priority Order

When agent names conflict, higher priority wins:

| Priority | Location | Scope |
|----------|----------|-------|
| 1 (highest) | `--agents` CLI flag | Current session only |
| 2 | `.claude/agents/` | Current project |
| 3 | `~/.claude/agents/` | All your projects |
| 4 (lowest) | Plugin's `agents/` directory | Where plugin is enabled |

**Project agents** (`.claude/agents/`) are ideal for team sharing - check them into version control.

**User agents** (`~/.claude/agents/`) are personal agents available in all your projects.

**CLI agents** exist only for that session - useful for quick testing or automation scripts.

## Disabling Specific Subagents

Disable built-in or custom subagents using permission rules or CLI flags.

### Via settings.json

```json
{
  "permissions": {
    "deny": ["Task(Explore)", "Task(Plan)"]
  }
}
```

### Via CLI

```bash
claude --disallowedTools "Task(Explore)"
```

### Permission Rule Syntax

| Pattern | Effect |
|---------|--------|
| `Task(Explore)` | Disable built-in Explore agent |
| `Task(Plan)` | Disable built-in Plan agent |
| `Task(code-reviewer)` | Disable custom code-reviewer agent |
| `Task(*)` | Disable all subagents |

### Use Cases

- **Security** - Prevent delegation to agents with write access
- **Workflow control** - Force specific agents for certain tasks
- **Debugging** - Isolate main thread behavior without subagents
- **Cost management** - Disable expensive opus-based agents

### Example: Read-Only Mode

Disable all write-capable agents for safe exploration:

```json
{
  "permissions": {
    "deny": ["Task(general-purpose)", "Task(code-reviewer)"],
    "allow": ["Task(Explore)"]
  }
}
```

## Reference Files

| File | Contents |
|------|----------|
| [DEFINITION.md](./DEFINITION.md) | Complete frontmatter reference and file structure |
| [EXAMPLES.md](./EXAMPLES.md) | Real-world agent examples |
| [PATTERNS.md](./PATTERNS.md) | Best practices and composition patterns |
