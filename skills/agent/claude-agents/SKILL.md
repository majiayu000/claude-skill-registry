---
name: claude-agents
description: Guide for creating custom agents for Claude Code. Use when creating specialized agents, configuring agent tools.
---

# Claude Code Agents

Guide for creating custom agents that provide specialized behaviors and tool access for specific tasks.

## When to Use This Skill

Activate this skill when:
- Creating custom agent types for specific workflows
- Defining agent behaviors and tool permissions
- Configuring agent capabilities
- Understanding agent vs skill differences
- Implementing domain-specific agents

## What Are Agents?

Agents are specialized Claude instances with:
- **Specific tool access**: Limited or specialized tool sets
- **Defined behaviors**: Pre-configured instructions and constraints
- **Task focus**: Optimized for particular workflows
- **Autonomous operation**: Can execute multi-step tasks independently

## Agents vs Skills

| Feature | Agents | Skills |
|---------|--------|--------|
| **Activation** | Explicitly launched via Task tool | Auto-activated based on context |
| **Tool Access** | Configurable, can be restricted | Inherit from parent context |
| **State** | Independent, isolated | Share parent context |
| **Use Case** | Complex multi-step tasks | Knowledge and guidelines |
| **Persistence** | Single execution | Always available when loaded |

## Agent File Structure

### Location

Agents are defined in markdown files located in:
- Plugin: `<plugin-root>/agents/`
- User-level: `.claude/agents/`

### File Naming

- Use kebab-case: `code-reviewer.md`
- File name becomes the agent type
- Be descriptive about the agent's purpose

## Basic Agent Format

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Grep, Glob
model: sonnet
---

You are a code reviewer. Analyze code for quality, security, and best practices.

## Workflow

1. **Find files**: Glob to locate target files
2. **Read code**: Examine contents
3. **Check patterns**: Grep for anti-patterns
4. **Report**: Provide prioritized feedback

## Guidelines

- **Specific**: Reference file:line locations
- **Actionable**: Suggest concrete fixes
- **Prioritized**: Critical issues first
```

## Agent Writing Style

Effective agents use direct, imperative language:

### Opening Statement

- **Do**: "You are a [role]. Your role is to [primary function]."
- **Don't**: "I am a specialized [role] focused on..."

### Workflow Steps

- **Do**: Numbered steps with specific commands
- **Don't**: Bullet lists describing capabilities

### Guidelines Section

- **Do**: Single-word bold labels with brief explanations
- **Don't**: Verbose explanations of best practices

## Agent Configuration

### YAML Frontmatter

Required and optional fields:

```markdown
---
name: agent-name                    # Required: kebab-case identifier
description: Brief description      # Required: What this agent does
tools:                             # Optional: Tool allowlist
  - Read
  - Write
  - Bash
model: sonnet                      # Optional: Model to use (sonnet, opus, haiku)
max_iterations: 10                 # Optional: Maximum task iterations
timeout: 300                       # Optional: Timeout in seconds
---
```

### Tool Allowlist

Restrict agent to specific tools:

- Can read files
- Can search code
- Can find files
- Cannot use Write, Edit, Bash, etc.

Example:

```markdown
---
tools: Read, Grep, Glob     
---
```




**No tool restrictions** (access to all tools):

```markdown
---
# Omit tools field entirely
---
```

### Model Selection

Choose appropriate model for the task:

```markdown
---
model: haiku        # Fast, cost-effective for simple tasks
# model: sonnet     # Balanced (default)
# model: opus       # Most capable for complex tasks
---
```

## Common Agent Patterns

### Read-Only Analysis Agent

For security scans, code reviews, or audits. Restricted to Read, Grep, Glob.

See: `templates/read-only-analyzer.md`

### Write-Capable Agent

For generating tests, documentation, or code. Includes Write tool.

See: `templates/write-capable-agent.md`

### Full-Access Agent

For refactoring, migrations, or complex modifications. Omit tools field entirely for no restrictions.

See: `templates/full-access-agent.md`

### MCP-Enabled Agent

For browser automation, external APIs, or specialized MCP server tools. Mix core tools with MCP tools.

See: `templates/mcp-agent.md`

## Agent Plugin Configuration

### In plugin.json

```json
{
  "agents": [
    "./agents/code-reviewer.md",
    "./agents/test-generator.md",
    "./agents/security-analyzer.md"
  ]
}
```

### Directory-Based Loading

```json
{
  "agents": "./agents"
}
```

Loads all `.md` files in `agents/` directory.

## Invoking Agents

Agents are launched via the Task tool:

```python
# In parent Claude conversation
Task(
    subagent_type="code-reviewer",
    description="Review authentication module",
    prompt="""
    Review the authentication module for:
    - Security vulnerabilities
    - Error handling
    - Input validation
    - Best practices
    """
)
```

## Agent Communication

### Input to Agent

- Task description
- Detailed prompt
- Access to conversation history (if configured)

### Output from Agent

- Final report/result
- No ongoing dialogue
- One-time execution

## Best Practices

### Clear Purpose

Each agent should have a specific, well-defined purpose:

```markdown
---
name: migration-helper
description: Assists with database schema migrations
---

# Database Migration Agent

Specialized in creating and validating database migrations.
```

### Appropriate Tool Access

Only grant necessary tools:

```markdown
---
# Analysis agent - read-only
tools: Read, Grep, Glob
---
```

```markdown
---
# Implementation agent - can modify
tools: Read, Write, Edit, Glob, Grep
---
```

### Model Selection

Match model to task complexity:

- **haiku**: Simple, repetitive tasks
- **sonnet**: Standard tasks (default)
- **opus**: Complex reasoning required

### Iteration Limits

Set appropriate limits for task complexity:

```markdown
---
max_iterations: 5   # Simple, focused task
# max_iterations: 20  # Complex, multi-step workflow
---
```

### Clear Instructions

Provide explicit behavior guidelines:

```markdown
# Testing Agent

## Mandatory Requirements

- Generate tests for ALL public methods
- Achieve minimum 80% code coverage
- Include edge cases and error scenarios
- Use project's testing framework conventions

## Constraints

- Do not modify source code
- Follow existing test file naming patterns
- Use appropriate assertions
```

## Security Considerations

### Tool Restrictions

Limit dangerous operations:

```markdown
---
# Don't give Bash access to untrusted agents
tools:
  - Read
  - Write  # Safer than arbitrary shell commands
---
```

### Input Validation

Validate agent inputs:

```markdown
# Deployment Agent

Before deploying:
1. Verify target environment is valid
2. Check deployment permissions
3. Validate configuration
4. Confirm destructive operations
```

### Sensitive Data

Never hardcode:
- Credentials
- API keys
- Private URLs
- Access tokens

## Agent Examples

For complete, production-ready agent templates:

- `templates/basic-agent.md` - Official minimal example
- `templates/read-only-analyzer.md` - Security analyzer pattern
- `templates/write-capable-agent.md` - Test generator pattern
- `templates/full-access-agent.md` - Refactoring pattern (no tool restrictions)
- `templates/mcp-agent.md` - Browser testing with MCP tools

## Troubleshooting

### Agent Not Found

- Verify agent file location matches plugin.json
- Check file naming (kebab-case, .md extension)
- Ensure plugin is properly installed

### Tool Access Denied

- Check tools allowlist in frontmatter
- Verify tool names match exactly
- Ensure parent context permits delegation

### Unexpected Behavior

- Review agent instructions for clarity
- Check model selection appropriateness
- Verify iteration limits aren't too restrictive
- Test with verbose output

## References

Templates directory:
- `templates/basic-agent.md` - Official minimal example
- `templates/read-only-analyzer.md` - Security analysis pattern
- `templates/write-capable-agent.md` - Test generation pattern
- `templates/full-access-agent.md` - Refactoring pattern (no tool restrictions)
- `templates/mcp-agent.md` - MCP tools pattern (browser automation)

Documentation:
- Claude Code Agents: https://code.claude.com/docs/en/agents
- Task Tool: https://code.claude.com/docs/en/tools/task
