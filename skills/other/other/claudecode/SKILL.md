---
name: claudecode
description: This skill should be used when the user asks "how to use Claude Code", "Claude Code commands", "Claude Code features", "what can Claude Code do", "Claude Code tips", "Claude Code shortcuts", "how to configure Claude Code", or needs guidance on working effectively with Claude Code CLI.
version: 1.0.0
---

# Claude Code

Guide to working effectively with Claude Code CLI.

## Purpose

Provide quick reference for:
- Essential commands and shortcuts
- Configuration and settings
- Best practices for effective prompting
- Plugin and skill development
- Workflow optimization

## Essential Commands

### Slash Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help and available commands |
| `/clear` | Clear conversation history |
| `/compact` | Summarize conversation to save context |
| `/config` | Open configuration settings |
| `/cost` | Show token usage and costs |
| `/doctor` | Diagnose installation issues |
| `/init` | Initialize CLAUDE.md in project |
| `/login` | Authenticate with Anthropic |
| `/logout` | Sign out |
| `/memory` | View/edit memory files |
| `/model` | Switch AI model |
| `/permissions` | Manage tool permissions |
| `/pr-comments` | View PR comments |
| `/review` | Review code changes |
| `/status` | Show current session status |
| `/vim` | Toggle vim keybindings |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel current operation |
| `Ctrl+D` | Exit Claude Code |
| `Ctrl+L` | Clear screen |
| `Ctrl+R` | Search command history |
| `Tab` | Autocomplete files/commands |
| `Up/Down` | Navigate history |
| `Esc` | Cancel input (vim mode) |

## Context Management

### CLAUDE.md Files

Project instructions stored in `CLAUDE.md`:

```markdown
# Project Instructions

## Build Commands
- `npm run build` - Build project
- `npm test` - Run tests

## Code Style
- Use TypeScript strict mode
- Prefer functional components

## Important Files
- `src/config.ts` - Configuration
- `src/types/` - Type definitions
```

**Location Priority:**
1. `./CLAUDE.md` - Current directory (highest)
2. `~/.claude/CLAUDE.md` - Global (lowest)

### Memory Files

Persistent memory across sessions:

```bash
# View memory
/memory

# Memory stored in
~/.claude/memory.md
```

## Tool Permissions

### Permission Levels

| Level | Description |
|-------|-------------|
| `ask` | Ask before each use |
| `allow` | Always allow |
| `deny` | Always deny |

### Configure Permissions

```bash
/permissions

# Or in settings
/config
```

### Common Permission Patterns

```yaml
# Allow running tests
- tool: Bash
  prompt: "run tests"

# Allow npm commands
- tool: Bash
  prompt: "npm"

# Allow git operations
- tool: Bash
  prompt: "git"
```

## Effective Prompting

### Be Specific

```
# Good
"Add error handling to the fetchUser function in src/api/users.ts
that catches network errors and returns a default user object"

# Less effective
"Add error handling to the code"
```

### Provide Context

```
# Good
"The build is failing with 'Cannot find module ./utils'.
Check the import paths in src/components/Header.tsx"

# Less effective
"Fix the build error"
```

### Break Down Complex Tasks

```
# Step by step
1. "First, read the current implementation in src/auth/"
2. "Now add a logout function that clears the session"
3. "Update the tests in tests/auth.test.ts"
```

### Use File References

```
# Reference specific files
"Update @src/config.ts to add a new API endpoint"

# Reference multiple files
"Compare @src/old.ts with @src/new.ts and list differences"
```

## Model Selection

### Available Models

| Model | Best For |
|-------|----------|
| `claude-sonnet` | Fast, everyday tasks (default) |
| `claude-opus` | Complex reasoning, architecture |
| `claude-haiku` | Quick answers, simple tasks |

### Switch Models

```bash
/model opus    # For complex tasks
/model sonnet  # Default balance
/model haiku   # Quick operations
```

## Working with Code

### Read Before Edit

Always read files before modifying:

```
# Claude will read first
"Update the validation in src/forms/login.ts"

# Explicit read
"Read src/forms/login.ts and explain the validation logic"
```

### Incremental Changes

```
# Prefer small, focused changes
"Add input validation to the email field"

# Then
"Add input validation to the password field"

# Rather than
"Rewrite the entire form with validation"
```

### Test After Changes

```
"Run the tests to verify the changes work"

# Or be specific
"Run npm test -- --grep 'login'"
```

## Git Integration

### Common Workflows

```
# Check status
"Show git status"

# Create commit
"Commit these changes with message: Add user validation"

# Create PR
"Create a pull request for this feature"

# Review PR
/review
```

### Commit Best Practices

Claude auto-adds co-author:
```
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Background Tasks

### Run Tasks in Background

```
# Long-running commands
"Run the build in the background"

# Check status
/tasks

# View output
"Show output from task abc123"
```

## Plugins & Skills

### Available Skills

Invoke with slash commands:
```
/commit          # Create git commit
/review          # Review code changes
/pr-comments     # View PR feedback
```

### Custom Skills

Create in `.claude/skills/` or `.windsurf/skills/`:

```
skills/
└── my-skill/
    ├── SKILL.md         # Skill definition
    └── references/      # Supporting docs
```

See `references/skill-development.md` for details.

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Slow responses | Use `/compact` to reduce context |
| Tool denied | Check `/permissions` |
| File not found | Use absolute paths or check cwd |
| API errors | Run `/doctor` |

### Debug Mode

```bash
# Verbose output
claude --debug

# Check configuration
claude --version
/config
```

### Reset Session

```bash
# Clear conversation
/clear

# Fresh start
# Exit and restart claude
```

## Best Practices Summary

1. **Read before writing** - Understand existing code first
2. **Be specific** - Clear instructions get better results
3. **Incremental changes** - Small steps, verify each
4. **Use context files** - Maintain CLAUDE.md for projects
5. **Manage permissions** - Set up trusted patterns
6. **Use the right model** - Opus for complex, Haiku for simple
7. **Compact regularly** - Keep context manageable

## Additional Resources

### Reference Files

- **`references/skill-development.md`** - Creating custom skills
- **`references/hooks.md`** - Event hooks for automation

### External Resources

- GitHub Issues: https://github.com/anthropics/claude-code/issues
- Documentation: `/help` command
