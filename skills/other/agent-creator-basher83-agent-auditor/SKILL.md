---
name: agent-creator
description: >
  This skill should be used when the user asks to "create an agent", "write a subagent", "generate
  agent definition", "add agent to plugin", "write agent frontmatter", "create autonomous agent",
  "build subagent", needs agent structure guidance, YAML frontmatter configuration, invocation
  criteria with examples, or wants to add specialized subagents to Claude Code plugins with proper
  capabilities lists and tool access definitions.
---

# Agent Creator

## Overview

Creates subagent definitions for Claude Code. Subagents are specialized assistants
that Claude can invoke for specific tasks.

**When to use:** User requests an agent, wants to add specialized subagent to plugin, or needs agent structure guidance.

**References:** Consult
`plugins/meta/claude-docs/skills/official-docs/reference/plugins-reference.md` and
`plugins/meta/claude-docs/skills/official-docs/reference/sub-agents.md` for specifications.

## CRITICAL: Two Types of Agents

Claude Code has **two distinct agent types** with **different requirements**:

### Plugin Agents (plugins/*/agents/)

**Purpose:** Agents distributed via plugins for team/community use

**Required frontmatter fields:**
- `description` (required) - What this agent specializes in
- `capabilities` (required) - Array of specific capabilities

**Location:** `plugins/<category>/<plugin-name>/agents/agent-name.md`

**Example:**
```markdown
---
description: Expert code reviewer validating security and quality
capabilities: ["vulnerability detection", "code quality review", "best practices"]
---
```

### User/Project Agents (.claude/agents/)

**Purpose:** Personal agents for individual workflows

**Required frontmatter fields:**
- `name` (required) - Agent identifier
- `description` (required) - When to invoke this agent
- `tools` (optional) - Comma-separated tool list
- `model` (optional) - Model alias (sonnet, opus, haiku)

**Location:** `.claude/agents/agent-name.md` or `~/.claude/agents/agent-name.md`

**Example:**
```markdown
---
name: code-reviewer
description: Expert code review. Use after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---
```

**Key difference:** User agents have `name` field and system prompt. Plugin agents have `capabilities` array and documentation.

## Agent Structure Requirements (Plugin Agents)

Every **plugin agent** MUST include:

1. **Frontmatter** with `description` and `capabilities` array
2. **Agent title** as h1
3. **Capabilities** section explaining what agent does
4. **When to Use** section with invocation criteria
5. **Context and Examples** with concrete scenarios
6. Located in `agents/agent-name.md` within plugin

## Creation Process

### Step 0: Determine Agent Type

**Ask the user:**
- Is this for a plugin (team/community distribution)?
- Or for personal use (.claude/agents/)?

**If personal use:** Use user agent format with `name`, `description`, system prompt. See `plugins/meta/claude-docs/skills/official-docs/reference/sub-agents.md` for examples.

**If plugin:** Continue with plugin agent format below.

### Step 1: Define Agent Purpose

Ask the user:

- What specialized task does this agent handle?
- What capabilities distinguish it from other agents?
- When should Claude invoke this vs doing work directly?

### Step 2: Determine Agent Name

Create descriptive kebab-case name:

- "security review" → `security-reviewer`
- "performance testing" → `performance-tester`
- "API documentation" → `api-documenter`

### Step 3: List Capabilities

Identify 3-5 specific capabilities:

- Concrete actions the agent performs
- Specialized knowledge it applies
- Outputs it generates

### Step 4: Structure the Agent

Use this template:

```markdown
---
description: One-line agent description
capabilities: ["capability-1", "capability-2", "capability-3"]
---

# Agent Name

Detailed description of agent's role and expertise.

## Capabilities

- **Capability 1**: What this enables
- **Capability 2**: What this enables
- **Capability 3**: What this enables

## When to Use This Agent

Claude should invoke when:
- Specific condition 1
- Specific condition 2
- Specific condition 3

## Context and Examples

**Example 1: Scenario Name**

User requests: "Help with X"
Agent provides: Specific assistance using capabilities

**Example 2: Another Scenario**

When Y happens, agent does Z.
```

### Step 5: Verify Against Official Docs

**For plugin agents:**
Check `plugins/meta/claude-docs/skills/official-docs/reference/plugins-reference.md` (requires `capabilities` array).

**For user agents:**
Check `plugins/meta/claude-docs/skills/official-docs/reference/sub-agents.md` (requires `name` field).

## Key Principles

- **Specialization**: Agents should have focused expertise
- **Clear Invocation**: Claude must know when to use this agent
- **Concrete Capabilities**: List specific things agent can do
- **Examples**: Show real scenarios where agent helps

## Examples

### Example 1: Security Reviewer Agent

User: "Create an agent for security reviews"

Process:

1. Purpose: Reviews code for security vulnerabilities
2. Name: `security-reviewer`
3. Capabilities: ["vulnerability detection", "security best practices", "threat modeling"]
4. Structure: Include when to invoke, examples of security issues
5. Create: `agents/security-reviewer.md`

Output: Agent that Claude invokes for security-related code review

### Example 2: Performance Tester Agent

User: "I need an agent for performance testing"

Process:

1. Purpose: Designs and analyzes performance tests
2. Name: `performance-tester`
3. Capabilities: ["load testing", "benchmark design", "performance analysis"]
4. Structure: When to use for optimization vs testing
5. Create: `agents/performance-tester.md`

Output: Agent that Claude invokes for performance concerns
