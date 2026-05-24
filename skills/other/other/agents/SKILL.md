---
name: agents
description: List all available agents (core + expert)
user-invocable: true
---

# Available Agents

List all agents available in Director Mode Lite.

---

## Core Agents

### code-reviewer
**Purpose:** Code quality, security, best practices review.
**Triggers:** "review", "check code", before commits

### debugger
**Purpose:** Systematic debugging for errors.
**Triggers:** Errors, test failures, "bug", "debug"

### doc-writer
**Purpose:** Documentation creation and maintenance.
**Triggers:** New features, "document", "README"

---

## Expert Agents

### claude-md-expert
CLAUDE.md design patterns and best practices.

### mcp-expert
MCP configuration and troubleshooting.

### agents-expert
Custom agent creation and configuration.

### skills-expert
Custom skill/command creation.

### hooks-expert
Automation hooks and triggers.

---

## How Agents Work

1. **Auto-activate** based on context
2. **Follow specific methodologies**
3. **Provide structured output**
4. **Can be explicitly invoked**

---

## Using Agents

```
"Use code-reviewer to check src/auth/"
"I need the debugger - tests are failing"
"Have doc-writer update the API docs"
```

---

## Creating Custom Agents

```markdown
---
name: my-agent
description: What this agent does
tools: Read, Grep, Glob, Bash
---

# Agent Name

## When to Activate
## Process
## Output Format
```

Save to `.claude/agents/my-agent.md`
