---
name: creating-kiro-agents
description: Use when building custom Kiro AI agents or when user asks for agent configurations - provides JSON structure, tool configuration, prompt patterns, and security best practices for specialized development assistants
---

# Creating Kiro Agents

Expert guidance for creating specialized Kiro AI agents with proper configuration, tools, and security.

## When to Use

**Use when:**
- User asks to create a Kiro agent
- Need specialized AI assistant for specific workflow
- Building domain-focused development tools
- Configuring agent tools and permissions

**Don't use for:**
- Generic AI prompts (not Kiro-specific)
- Project documentation (use steering files instead)
- One-off assistant interactions

## Quick Reference

### Minimal Agent Structure
```json
{
  "name": "agent-name",
  "description": "One-line purpose",
  "prompt": "System instructions",
  "tools": ["fs_read", "fs_write"]
}
```

### File Location
- **Project**: `.kiro/agents/<name>.json`
- **Global**: `~/.kiro/agents/<name>.json`

### Common Tools
- `fs_read` - Read files
- `fs_write` - Write files (requires `allowedPaths`)
- `execute_bash` - Run commands (requires `allowedCommands`)
- MCP server tools (varies by server)

## Core Principles

### 1. Specialization Over Generalization
✅ **Good**: `backend-api-specialist` - Express.js REST APIs
❌ **Bad**: `general-helper` - does everything

### 2. Least Privilege
Grant only necessary tools and paths.

```json
{
  "toolsSettings": {
    "fs_write": {
      "allowedPaths": ["src/api/**", "tests/api/**"]
    },
    "execute_bash": {
      "allowedCommands": ["npm test", "npm run build"]
    }
  }
}
```

### 3. Clear, Structured Prompts

✅ **Good**:
```markdown
You are a backend API expert specializing in Express.js and MongoDB.

## Focus Areas
- RESTful API design
- Security best practices (input validation, auth)
- Error handling with proper status codes
- MongoDB query optimization

## Standards
- Always use async/await
- Implement proper logging
- Validate all inputs
- Use TypeScript interfaces
```

❌ **Bad**: "You are a helpful coding assistant."

## Common Patterns

### Backend Specialist
```json
{
  "name": "backend-dev",
  "description": "Node.js/Express API development with MongoDB",
  "prompt": "Backend development expert. Focus on API design, database optimization, and security.\n\n## Core Principles\n- RESTful conventions\n- Input validation\n- Error handling\n- Query optimization",
  "tools": ["fs_read", "fs_write", "execute_bash"],
  "toolsSettings": {
    "fs_write": {
      "allowedPaths": ["src/api/**", "src/routes/**", "src/models/**"]
    }
  }
}
```

### Code Reviewer
```json
{
  "name": "code-reviewer",
  "description": "Reviews code against team standards",
  "prompt": "You review code for:\n- Quality and readability\n- Security issues\n- Performance problems\n- Standard compliance\n\nProvide constructive feedback with examples.",
  "tools": ["fs_read"],
  "resources": ["file://.kiro/steering/review-checklist.md"]
}
```

### Test Writer
```json
{
  "name": "test-writer",
  "description": "Writes comprehensive Vitest test suites",
  "prompt": "Testing expert using Vitest.\n\n## Test Requirements\n- Unit tests for all functions\n- Edge case coverage\n- Proper mocking\n- AAA pattern (Arrange, Act, Assert)\n- Descriptive test names",
  "tools": ["fs_read", "fs_write"],
  "toolsSettings": {
    "fs_write": {
      "allowedPaths": ["**/*.test.ts", "**/*.spec.ts", "tests/**"]
    }
  }
}
```

### Frontend Specialist
```json
{
  "name": "frontend-dev",
  "description": "React/Next.js development with TypeScript",
  "prompt": "Frontend expert in React, Next.js, and TypeScript.\n\n## Focus\n- Component architecture\n- Performance optimization\n- Accessibility (WCAG)\n- Responsive design",
  "tools": ["fs_read", "fs_write"],
  "toolsSettings": {
    "fs_write": {
      "allowedPaths": ["src/components/**", "src/app/**", "src/styles/**"]
    }
  }
}
```

## Advanced Configuration

### MCP Servers
```json
{
  "mcpServers": {
    "database": {
      "command": "mcp-server-postgres",
      "args": ["--host", "localhost"],
      "env": {
        "DB_URL": "${DATABASE_URL}"
      }
    },
    "fetch": {
      "command": "mcp-server-fetch",
      "args": []
    }
  },
  "tools": ["fs_read", "db_query", "fetch"],
  "allowedTools": ["fetch"]
}
```

### Lifecycle Hooks
```json
{
  "hooks": {
    "agentSpawn": ["git fetch origin", "npm run db:check"],
    "userPromptSubmit": ["git status --short"]
  }
}
```

### Resource Loading
```json
{
  "resources": [
    "file://.kiro/steering/api-standards.md",
    "file://.kiro/steering/security-policy.md"
  ]
}
```

## Workflow

1. **Clarify Requirements**
   - What domain/task?
   - What tools needed?
   - What file paths?
   - What standards to follow?

2. **Design Configuration**
   - Choose appropriate pattern
   - Set tool restrictions
   - Write clear prompt
   - Reference steering files

3. **Create Agent File**
   ```bash
   # Create in project
   touch .kiro/agents/my-agent.json

   # Or global
   touch ~/.kiro/agents/my-agent.json
   ```

4. **Test Agent**
   ```bash
   kiro agent use my-agent
   kiro "What can you help me with?"
   ```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Granting all tools | Security risk | Only grant necessary tools |
| Vague prompts | Ineffective agent | Be specific about domain and standards |
| No path restrictions | Agent can modify any file | Use `allowedPaths` for `fs_write` |
| Generic names | Hard to find/remember | Use descriptive names: `react-component-creator` |
| Missing description | Unclear purpose | Add one-sentence description |
| Multiple domains | Unfocused agent | Create separate specialized agents |

## Best Practices

### Naming
- Use **kebab-case**: `backend-specialist`, not `BackendSpecialist`
- Be **specific**: `react-testing-expert`, not `helper`
- Indicate **domain**: `aws-infrastructure`, `mobile-ui-designer`

### Prompts
1. Define expertise area clearly
2. List specific focus areas
3. Specify standards/conventions
4. Provide pattern examples
5. Set clear expectations

### Security
1. Grant minimum necessary tools
2. Restrict file paths with `allowedPaths`
3. Whitelist commands with `allowedCommands`
4. Use `allowedTools` for safe operations
5. Validate all configurations

## Troubleshooting

### Agent Not Found
- Check file is in `.kiro/agents/`
- Verify `.json` extension
- Validate JSON syntax (use JSON validator)

### Tools Not Working
- Verify tool names (check spelling)
- Check `allowedPaths` restrictions
- Ensure MCP servers are installed
- Review `allowedTools` list

### Prompt Ineffective
- Be more specific about tasks
- Add concrete examples
- Reference team standards
- Structure with markdown headers

## Integration with PRPM

```bash
# Install Kiro agent from registry
prpm install @username/agent-name --as kiro --subtype agent

# Publish your agent
prpm init my-agent --subtype agent
# Edit canonical format, then:
prpm publish
```

## Real-World Impact

**Effective agents:**
- Save time on repetitive tasks
- Enforce team standards automatically
- Reduce context switching
- Provide consistent code quality
- Enable workflow automation

**Example**: A `test-writer` agent that only writes to test files prevents accidental modification of source code while ensuring comprehensive test coverage.

---

**Key Takeaway**: Specialize agents for specific domains, restrict tools to minimum necessary, and write clear prompts with concrete standards.
