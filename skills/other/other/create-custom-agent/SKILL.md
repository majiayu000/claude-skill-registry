---
name: create-custom-agent
description: Creates VS Code custom agent files (.agent.md) for specialized AI personas with tools, instructions, and handoffs. Use when scaffolding new custom agents, configuring agent workflows, or setting up agent-to-agent handoffs.
---

# Create Custom Agent

This skill helps you create VS Code custom agent files that define specialized AI personas for development tasks. Custom agents configure which tools are available, provide specialized instructions, and can chain together via handoffs.

## When to Use

- Creating a new custom agent from scratch
- Scaffolding an `.agent.md` file with proper frontmatter
- Setting up agent-to-agent handoffs for multi-step workflows
- Configuring tool restrictions for specialized roles (planner, reviewer, etc.)
- Creating workspace-shared or user-profile agents

## When Not to Use

- Creating instruction files (use `.instructions.md` instead)
- Creating reusable prompts (use `.prompt.md` instead)
- Modifying existing agents (edit the file directly)

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Agent name | Yes | Descriptive name for the agent (e.g., `planner`, `code-reviewer`) |
| Description | Yes | Brief description shown as placeholder text in chat |
| Purpose/Persona | Yes | What role the agent plays and how it should behave |
| Tools | Recommended | List of tools or tool sets the agent can use |
| Handoffs | Optional | Next-step agents to transition to after completing work |

## Workflow

### Step 1: Create the agent file

Create a file with `.agent.md` extension in the `agents/` directory:

```
agents/<agent-name>.agent.md
```

### Step 2: Add YAML frontmatter

Add the header with required and optional fields:

```yaml
---
name: <agent-name>
description: <brief description for chat placeholder>
tools:
  - <tool-name>
  - <tool-set-name>
---
```

#### Available frontmatter fields:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name (defaults to filename) |
| `description` | Yes | Placeholder text shown in chat input |
| `argument-hint` | No | Hint text guiding user interaction |
| `tools` | No | List of available tools/tool sets |
| `agents` | No | List of allowed subagents (`*` for all, `[]` for none) |
| `model` | No | AI model name or prioritized array of models |
| `handoffs` | No | List of next-step agent transitions |
| `user-invokable` | No | Show in agents dropdown (default: true) |
| `disable-model-invocation` | No | Prevent subagent invocation (default: false) |
| `target` | No | Target environment: `vscode` or `github-copilot` |
| `mcp-servers` | No | MCP server configs for GitHub Copilot target |

### Step 3: Configure tools

Specify which tools the agent can use:

```yaml
tools:
  - search              # Built-in tool
  - fetch               # Built-in tool
  - codebase            # Tool set
  - myServer/*          # All tools from MCP server
```

Common tool patterns:
- **Read-only agents**: `['search', 'fetch', 'codebase']`
- **Full editing agents**: `['*']` or specific editing tools
- **Specialized agents**: Cherry-pick specific tools

### Step 4: Add handoffs (optional)

Configure transitions to other agents:

```yaml
handoffs:
  - label: Start Implementation
    agent: implementation
    prompt: Implement the plan outlined above.
    send: false
    model: GPT-5.2 (copilot)
```

Handoff fields:
- `label`: Button text displayed to user
- `agent`: Target agent identifier
- `prompt`: Pre-filled prompt for target agent
- `send`: Auto-submit prompt (default: false)
- `model`: Optional model override for handoff

### Step 5: Write agent instructions (body)

Add the agent's behavior instructions in Markdown:

```markdown
You are a security-focused code reviewer. Your job is to:

1. Analyze code for security vulnerabilities
2. Check for common security anti-patterns
3. Suggest secure alternatives

## Guidelines

- Focus on OWASP Top 10 vulnerabilities
- Flag hardcoded secrets immediately
- Review authentication and authorization logic

## Reference other files

See [security guidelines](../security.md) for standards.
```

Tips for instructions:
- Use Markdown links to reference other files
- Reference tools with `#tool:<tool-name>` syntax
- Be specific about agent behavior and constraints

### Step 6: Validate the agent

Verify the agent loads correctly:

1. Open Command Palette (Ctrl+Shift+P)
2. Run "Chat: New Custom Agent" or check agents dropdown
3. Use "Diagnostics" view (right-click in Chat view) to check for errors

## Template

```markdown
---
name: <agent-name>
description: <brief description for chat placeholder>
argument-hint: <optional hint for user input>
tools:
  - <tool-1>
  - <tool-2>
handoffs:
  - label: <button-text>
    agent: <target-agent>
    prompt: <pre-filled-prompt>
    send: false
---

# <Agent Title>

<One paragraph describing the agent's persona and purpose.>

## Role

<Describe the agent's specialized role and expertise.>

## Guidelines

- <Guideline 1>
- <Guideline 2>
- <Guideline 3>

## Workflow

1. <Step 1>
2. <Step 2>
3. <Step 3>

## Constraints

- <Constraint 1>
- <Constraint 2>
```

## Example Agents

### Planning Agent

```markdown
---
name: planner
description: Generate an implementation plan
tools:
  - search
  - fetch
  - codebase
handoffs:
  - label: Start Implementation
    agent: implementation
    prompt: Implement the plan above.
---

# Planning Agent

You are a solution architect. Generate detailed implementation plans.

## Guidelines

- Analyze requirements thoroughly before planning
- Break work into discrete, testable steps
- Identify dependencies and risks
- Do NOT make code changes
```

### Code Review Agent

```markdown
---
name: code-reviewer
description: Review code for quality and security issues
tools:
  - search
  - codebase
---

# Code Review Agent

You are a senior engineer performing code review.

## Focus Areas

- Security vulnerabilities
- Performance concerns
- Code maintainability
- Test coverage gaps

## Output Format

Provide findings as:
1. **Critical**: Must fix before merge
2. **Warning**: Should address
3. **Suggestion**: Nice to have
```

## Validation Checklist

- [ ] File has `.agent.md` extension
- [ ] File is in `agents/` directory
- [ ] YAML frontmatter is valid (proper indentation, no syntax errors)
- [ ] Description is non-empty and descriptive
- [ ] Tools list contains only available tools
- [ ] Handoff agent names match existing agents
- [ ] Instructions are clear and actionable
- [ ] Agent appears in agents dropdown

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Agent not appearing in dropdown | Check file is in `agents/` directory with `.agent.md` extension |
| YAML syntax errors | Validate frontmatter indentation and quoting |
| Tools not working | Verify tool names exist; unavailable tools are ignored |
| Handoffs not showing | Target agent must exist; check agent identifier |
| Instructions too vague | Be specific about role, constraints, and workflow |
| Agent invoked as subagent unexpectedly | Set `disable-model-invocation: true` |
| Want agent only as subagent | Set `user-invokable: false` |

## References

- [VS Code Custom Agents Documentation](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Tools in Chat](https://code.visualstudio.com/docs/copilot/chat/chat-tools)
- [Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [Prompt Files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
