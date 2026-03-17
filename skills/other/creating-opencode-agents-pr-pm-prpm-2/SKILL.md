---
name: creating-opencode-agents
description: Use when creating OpenCode agents - provides markdown format with YAML frontmatter, mode/tools/permission configuration, and best practices for specialized AI assistants
---

# Creating OpenCode Agents

Expert guidance for creating OpenCode AI agents with proper configuration, tools, and permissions.

## When to Use

**Use when:**
- User asks to create an OpenCode agent
- Need specialized AI assistant for specific tasks
- Building domain-focused development tools
- Configuring agent tools and permissions

**Don't use for:**
- OpenCode plugins (use creating-opencode-plugins skill)
- OpenCode slash commands (different format)
- Generic AI prompts (not OpenCode-specific)

## Quick Reference

### File Location
- **Project**: `.opencode/agent/<name>.md`
- **Global**: `~/.config/opencode/agent/<name>.md`

### Minimal Agent Structure
```markdown
---
description: Brief explanation of the agent's purpose
mode: all
---

System prompt content here...
```

### Required Fields
- **`description`** (string): Brief explanation of the agent's purpose (REQUIRED)

### Optional Fields
| Field | Type | Description |
|-------|------|-------------|
| `mode` | `primary` \| `subagent` \| `all` | How agent can be used (default: `all`) |
| `model` | string | Override model (e.g., `anthropic/claude-sonnet-4-20250514`) |
| `temperature` | number | Response randomness 0.0-1.0 |
| `prompt` | string | Path to prompt file: `{file:./path/to/prompt.txt}` |
| `maxSteps` | number | Maximum iterations (unlimited if unset) |
| `tools` | object | Enable/disable tools with boolean values |
| `permission` | object | Tool access: `ask`, `allow`, or `deny` |
| `disable` | boolean | Deactivate the agent |

### Agent Modes
- **`primary`**: Main assistant for direct interaction, switchable via Tab key
- **`subagent`**: Specialized assistant invoked by primary agents or `@mentions`
- **`all`**: Default; usable in both contexts

## Common Patterns

### Code Reviewer (Read-Only)
```markdown
---
description: Reviews code for best practices and security
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
  write: false
  edit: false
  bash: false
  read: true
  grep: true
  glob: true
permission:
  edit: deny
  bash: deny
---

# Code Review Agent

You are an expert code reviewer with deep knowledge of software engineering principles.

## Instructions

- Check for code smells and anti-patterns
- Verify test coverage
- Ensure documentation exists
- Review error handling and security
- Suggest improvements with examples

## Review Checklist

- [ ] Code follows project conventions
- [ ] Tests are comprehensive
- [ ] No security vulnerabilities
- [ ] Documentation is clear
```

### Backend Developer
```markdown
---
description: Node.js/Express API development with database optimization
mode: all
temperature: 0.3
tools:
  read: true
  write: true
  edit: true
  bash: true
  grep: true
  glob: true
permission:
  bash:
    "npm test": allow
    "npm run *": allow
    "git *": ask
    "*": deny
---

# Backend Development Agent

You are a backend development expert specializing in Node.js, Express, and database optimization.

## Focus Areas

- RESTful API design
- Input validation and error handling
- Database query optimization
- Security best practices

## Standards

- Always use async/await
- Implement proper logging
- Validate all inputs
- Use TypeScript interfaces
```

### Test Writer
```markdown
---
description: Writes comprehensive test suites with high coverage
mode: subagent
temperature: 0.2
maxSteps: 50
tools:
  read: true
  write: true
  bash: true
permission:
  bash:
    "npm test*": allow
    "*": deny
---

# Test Writer Agent

You are a testing expert focused on comprehensive test coverage.

## Test Requirements

- Unit tests for all functions
- Edge case coverage
- Proper mocking
- AAA pattern (Arrange, Act, Assert)
- Descriptive test names

## Frameworks

- Vitest for unit tests
- Playwright for E2E
- MSW for API mocking
```

### Documentation Writer (Limited Tools)
```markdown
---
description: Technical documentation and API reference writer
mode: subagent
temperature: 0.5
tools:
  read: true
  write: true
  edit: true
  bash: false
---

# Documentation Agent

You write clear, comprehensive technical documentation.

## Focus

- API reference documentation
- README files
- Architecture docs
- Code comments and JSDoc

## Style

- Clear and concise
- Include examples
- Use proper markdown formatting
- Follow project documentation standards
```

## Tools Configuration

### Available Tools
| Tool | Description |
|------|-------------|
| `read` | Read file contents |
| `write` | Create new files |
| `edit` | Modify existing files |
| `bash` | Execute shell commands |
| `grep` | Search file contents |
| `glob` | Find files by pattern |
| `webfetch` | Fetch web content |
| `websearch` | Search the web |

### Wildcard Patterns
Disable groups of tools with wildcards:
```yaml
tools:
  mymcp_*: false  # Disable all MCP tools starting with mymcp_
```

## Permission Configuration

### Simple Permissions
```yaml
permission:
  edit: ask      # Prompt before editing
  bash: deny     # Block all bash commands
  webfetch: allow  # Allow web fetching
```

### Per-Command Bash Permissions
```yaml
permission:
  bash:
    "git push": ask    # Ask before pushing
    "git *": allow     # Allow other git commands
    "npm test": allow  # Allow testing
    "*": deny          # Deny everything else
```

## Temperature Guidelines

| Temperature | Use Case |
|-------------|----------|
| 0.0-0.2 | Code review, debugging, analysis |
| 0.3-0.5 | General development, refactoring |
| 0.6-1.0 | Documentation, brainstorming, creative work |

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Missing description | Required field | Add description in frontmatter |
| Granting all tools | Security risk | Only grant necessary tools |
| Vague prompt | Ineffective agent | Be specific about domain and tasks |
| Wrong mode | Agent not accessible | Use `all` for flexibility |
| No tool restrictions | Agent can do anything | Use tools/permission to limit scope |

## Best Practices

### Naming
- Use **kebab-case**: `code-reviewer`, not `CodeReviewer`
- Be **specific**: `react-testing-expert`, not `helper`
- Indicate **domain**: `aws-infrastructure`, `mobile-ui-designer`

### Prompts
1. Define expertise area clearly
2. List specific focus areas
3. Specify standards/conventions
4. Provide examples when helpful
5. Set clear expectations

### Security
1. Grant minimum necessary tools
2. Use permissions to restrict dangerous operations
3. Disable bash for read-only agents
4. Use glob patterns for bash permissions
5. Consider maxSteps for long-running agents

## PRPM Integration

### Package Manifest (prpm.json)
```json
{
  "name": "@username/my-agent",
  "version": "1.0.0",
  "description": "My OpenCode agent",
  "format": "opencode",
  "subtype": "agent",
  "files": [".opencode/agent/my-agent.md"],
  "tags": ["opencode", "agent", "development"]
}
```

### Installation
```bash
# Install from registry
prpm install @username/agent-name --format opencode

# Installs to: .opencode/agent/<agent-name>.md
```

### Publishing
```bash
prpm publish
```

## Navigation & Usage

- **Tab key**: Switch between primary agents
- **@ mention**: Invoke subagents (e.g., `@code-reviewer check this function`)
- **<Leader>+Right/Left**: Navigate parent/child sessions

## Troubleshooting

### Agent Not Found
- Check file is in `.opencode/agent/`
- Verify `.md` extension
- Validate YAML frontmatter syntax

### Tools Not Working
- Verify tool names (lowercase in OpenCode)
- Check permission settings
- Ensure mode allows tool access

### Agent Ineffective
- Be more specific in prompt
- Add concrete examples
- Reference team standards
- Structure with markdown headers

---

**Schema Reference**: `packages/converters/schemas/opencode.schema.json`

**Documentation**: https://opencode.ai/docs/agents/
