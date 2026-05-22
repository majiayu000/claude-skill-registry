---
name: agent-creator
description: Guide for creating effective Claude Code agents. This skill should be used when users want to create a new agent (or update an existing agent) that configures Claude with specialized system prompts, tool restrictions, model selection, and MCP/skill integrations.
---

# Agent Creator

This skill provides guidance for creating effective Claude Code agents.

## About Agents

Agents are Markdown files with YAML frontmatter that configure Claude Code with specialized behavior. They can be used in two ways:

1. **Main Agent** (`claude --agent name`) - Starts Claude Code as this persona
2. **Subagent** (Task tool) - Spawns a focused worker that reports back

Unlike skills (which inject knowledge into context), agents fundamentally change *who Claude is* for that session - the system prompt, available tools, and even the model.

### When to Create an Agent

| Use Case | Create Agent? | Alternative |
|----------|---------------|-------------|
| Specialized persona with restricted tools | Yes | - |
| Domain expert needing specific MCPs/skills | Yes | - |
| Cost optimization (haiku for simple tasks) | Yes | - |
| Orchestrator that delegates to sub-agents | Yes | - |
| Adding domain knowledge to context | No | Create a skill |
| One-off task instructions | No | Direct prompting |
| Reusable scripts/assets | No | Create a skill |

### Agent vs Skill Decision

- **Agent**: Changes *who* Claude is (persona, tools, model)
- **Skill**: Changes *what* Claude knows (knowledge, procedures, scripts)

Agents can load skills. Skills cannot become agents.

## Agent Anatomy

### File Location

Agents are stored as `.md` files in:

- `~/.claude/agents/` - User-level (global, all projects)
- `.claude/agents/` - Project-level (repo-specific, higher precedence)

### Required Structure

```markdown
---
name: agent-name
description: "When to use this agent. Be specific about triggers."
---

System prompt content goes here.
```

### All Configuration Options

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Unique ID (lowercase, hyphens only) |
| `description` | Yes | string | When/why to invoke this agent |
| `tools` | No | list | Restrict to specific tools only |
| `model` | No | string | `haiku`, `sonnet`, `opus`, or omit to inherit |
| `permissionMode` | No | string | `default`, `acceptEdits`, `plan`, `bypassPermissions` |
| `skills` | No | list | Auto-load specific skills |

### Tool Restriction

Omitting `tools` grants all available tools. Specifying it creates a whitelist:

```yaml
tools:
  - Read
  - Grep
  - Glob
```

Common tools: `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`, `Task`, `WebSearch`, `WebFetch`, `TodoWrite`

See `references/tool-catalog.md` for the complete catalog with use cases.

## Agent Creation Process

### Step 1: Define the Agent's Purpose

Before writing, answer:

1. **What is this agent's specialty?** (one clear focus)
2. **When should it be invoked?** (specific triggers)
3. **What tools does it need?** (minimum viable set)
4. **What model fits the task?** (haiku=fast/cheap, sonnet=balanced, opus=complex)
5. **What MCPs or skills should it load?**

### Step 2: Initialize the Agent

Run the initialization script to scaffold the agent file:

```bash
python ~/.claude/skills/agent-creator/scripts/init_agent.py <agent-name> [--path <directory>]
```

Default path is `~/.claude/agents/` (user-level). Use `.claude/agents/` for project-level.

### Step 3: Write the System Prompt

The system prompt (Markdown body after frontmatter) defines the agent's behavior. Follow Opus 4.5 prompting best practices from `references/opus-prompting.md`.

#### System Prompt Structure

```markdown
---
name: example-agent
description: "..."
---

[Role statement - who this agent is]

## Capabilities
[What this agent can do]

## Guidelines
[How to approach tasks]

## Workflow
[Step-by-step process if applicable]
```

#### Writing Style

- Use **imperative form**: "Analyze the code" not "You should analyze the code"
- Be **explicit and specific**: State exactly what to do
- Add **context for why**: Explain reasoning behind guidelines
- Include **concrete examples**: Show expected behavior
- Keep it **focused**: One clear specialty, not a generalist

### Step 4: Configure Tools and Model

Match tools to the agent's purpose:

| Agent Type | Recommended Tools | Model |
|------------|-------------------|-------|
| Researcher | Read, Grep, Glob, WebSearch, WebFetch | sonnet |
| Code Reviewer | Read, Grep, Glob, Bash | sonnet |
| Writer/Editor | Read, Write, Edit | sonnet |
| Quick Search | Grep, Glob, Read | haiku |
| Complex Analysis | Read, Grep, Glob, Task | opus |
| Orchestrator | Task, Read, TodoWrite | opus |

### Step 5: Add MCP/Skill Integrations

For agents that need external capabilities:

```yaml
skills:
  - ui-styling
  - docs-seeker
```

Reference skills in the system prompt:

```markdown
## Available Skills

Use the `ui-styling` skill for shadcn components and Tailwind.
Use the `docs-seeker` skill for finding library documentation.
```

For MCP tools, mention them explicitly in the system prompt so the agent knows they're available.

### Step 6: Test and Iterate

1. **Test as main agent**: `claude --agent your-agent`
2. **Test as subagent**: Use Task tool to spawn it
3. **Verify tool restrictions**: Ensure it only uses allowed tools
4. **Check persona consistency**: Does it maintain character?
5. **Validate triggers**: Does the description accurately predict usage?

## Opus 4.5 Prompting Guidelines

Claude Opus 4.5 has specific characteristics that affect agent design. See `references/opus-prompting.md` for full details.

### Key Points

1. **Dial back aggressive language** - Replace "CRITICAL/MUST" with normal phrasing
2. **Avoid "think"** - Use "consider", "evaluate", "reflect" when extended thinking is off
3. **Be explicit about action** - "Implement changes" vs "suggest changes"
4. **Include anti-over-engineering guidance** - Opus tends to add unnecessary abstractions
5. **Examples matter** - Opus follows examples precisely, ensure they're correct
6. **Parallel tool calling** - Explicitly encourage when tools are independent

### Anti-Over-Engineering Snippet

Include this in agents that write code:

```markdown
Avoid over-engineering. Only make changes directly requested or clearly necessary.
Keep solutions simple and focused. Do not add features, refactor code, or make
improvements beyond what was asked.
```

## Agent Patterns

See `references/agent-patterns.md` for common archetypes:

- **Researcher** - Read-only exploration and analysis
- **Specialist** - Domain expert with focused tools
- **Reviewer** - Code/content review without editing
- **Builder** - Focused creation with write access
- **Orchestrator** - Delegates to sub-agents
- **Quick Responder** - Fast, cheap responses with haiku

## Validation Checklist

Before finalizing an agent:

- [ ] Name is lowercase with hyphens only
- [ ] Description clearly states when to use the agent
- [ ] Tools are minimal but sufficient for the task
- [ ] Model matches complexity needs (haiku/sonnet/opus)
- [ ] System prompt uses imperative form
- [ ] No "CRITICAL/MUST" aggressive language
- [ ] Includes anti-over-engineering guidance if writes code
- [ ] Examples in prompt are accurate and helpful
- [ ] Tested as both main agent and subagent
