---
name: commands-creator
description: Guide for creating and managing slash commands in Claude Code. Use when (1) creating new slash commands, (2) learning command syntax and features, (3) deciding between commands vs skills, (4) implementing advanced command features (arguments, hooks, bash execution), or (5) organizing and managing command libraries.
---

# Commands Creator

This skill provides guidance for creating and managing slash commands in Claude Code. Slash commands are Markdown files that define frequently used prompts and workflows for Claude to execute.

## Quick Start

### Create a Project Command

```bash
mkdir -p .claude/commands
echo "Review this code for security vulnerabilities:" > .claude/commands/security-review.md
```

Usage: `/security-review`

### Create a Personal Command

```bash
mkdir -p ~/.claude/commands
echo "Explain this code in simple terms:" > ~/.claude/commands/explain.md
```

Usage: `/explain`

## Commands vs Skills

Use slash commands for:
- Quick, frequently used prompts
- Simple prompt snippets you use often
- Prompt reminders or templates
- Frequently used instructions that fit in one file

Use Skills for:
- Complex workflows with multiple steps
- Capabilities requiring scripts or utilities
- Knowledge organized across multiple files
- Team workflows you want to standardize

See [skills-vs-commands.md](https://docs.anthropic.com/en/docs/claude-code/slash-commands#skills-vs-slash-commands) for detailed comparison.

## Command Creation Process

1. **Analyze requirements**: What do you want the command to do?
2. **Choose scope**: Project (`.claude/commands/`) or Personal (`~/.claude/commands/`)
3. **Write frontmatter**: Add metadata (description, allowed-tools, etc.)
4. **Write prompt content**: Define what Claude should execute
5. **Test the command**: Invoke it and verify behavior
6. **Iterate**: Refine based on usage

## Command Types

### Project Commands
- Stored in `.claude/commands/`
- Shared with your team via git
- Shown as `(project)` in `/help`

### Personal Commands
- Stored in `~/.claude/commands/`
- Available across all projects
- Shown as `(user)` in `/help`

**Priority**: Project commands take precedence over personal commands if both have the same name.

### Plugin Commands
- Provided by plugins
- Automatically available when plugin is enabled
- Can be namespaced: `/plugin-name:command-name`

### MCP Commands
- Dynamically discovered from connected MCP servers
- Format: `/mcp__<server-name>__<prompt-name>`
- Managed via `/mcp` command

See [command-types.md](references/command-types.md) for detailed information.

## Command Scope: Project vs Personal

### Use Project Commands When:
- The command is project-specific
- You want to share with your team
- The workflow should be version-controlled

### Use Personal Commands When:
- The command is a general-purpose utility
- You want it available across all projects
- The workflow is personal to your development style

## Basic Syntax

```
/<command-name> [arguments]
```

### Command Name
- Derived from the Markdown filename (without `.md` extension)
- Must be unique within scope
- Can be namespaced using subdirectories

### Arguments
- Optional parameters passed to the command
- Use placeholders in command content:
  - `$ARGUMENTS`: All arguments as a single string
  - `$1`, `$2`, `$3`: Individual positional arguments

See [syntax-and-arguments.md](references/syntax-and-arguments.md) for detailed syntax and argument handling.

## Frontmatter

Command files support frontmatter for metadata:

```yaml
---
description: Brief description of the command
allowed-tools: Bash(git add:*), Bash(git status:*)
argument-hint: [message]
---
```

### Common Frontmatter Fields

| Field | Purpose | Default |
|-------|---------|---------|
| `description` | Brief description | First line of prompt |
| `allowed-tools` | Tools command can use | Inherits from conversation |
| `argument-hint` | Arguments expected | None |
| `model` | Specific model to use | Inherits from conversation |
| `disable-model-invocation` | Block Skill tool invocation | false |
| `hooks` | Command-scoped hooks | None |

See [frontmatter-reference.md](references/frontmatter-reference.md) for complete frontmatter reference.

## Advanced Features

### Bash Command Execution
Execute bash commands before the slash command runs:

```yaml
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

Current git status: !`git status`
```

Use `!` prefix to include bash command output in command context.

### File References
Include file contents using `@` prefix:

```
Review the implementation in @src/utils/helpers.js
```

### Hooks
Define hooks scoped to command execution:

```yaml
---
description: Deploy to staging
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-deploy.sh"
          once: true
---

Deploy to staging environment.
```

### Thinking Mode
Trigger extended thinking by including extended thinking keywords in the command content.

See [advanced-features.md](references/advanced-features.md) for detailed advanced features.

## Namespacing

Organize commands in subdirectories:

```
.claude/commands/
├── frontend/
│   ├── review.md          # Creates /review (project:frontend)
│   └── test.md            # Creates /test (project:frontend)
└── backend/
    ├── review.md          # Creates /review (project:backend)
    └── deploy.md          # Creates /deploy (project:backend)
```

Subdirectories appear in the command description but don't affect the command name.

## Command Discovery and Autocomplete

- Type `/` at any position to see available commands
- Autocomplete works anywhere in input, not just at the beginning
- Commands are discovered from:
  - Project commands: `.claude/commands/`
  - Personal commands: `~/.claude/commands/`
  - Plugin commands (when plugins are enabled)
  - MCP commands (when MCP servers are connected)

## Skill Tool Integration

The `Skill` tool allows Claude to programmatically invoke commands during conversations. To encourage Claude to use a specific command, reference it in prompts or `CLAUDE.md`:

```
> Run /review before committing changes.
```

Commands with `disable-model-invocation: true` cannot be invoked via the `Skill` tool.

See [best-practices.md](references/best-practices.md) for usage patterns and recommendations.

## Command Examples

Basic command:

```markdown
---
description: Review code for security vulnerabilities
---

Review this code for security vulnerabilities:
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization issues
- Input validation problems
```

Command with arguments:

```markdown
---
argument-hint: [type] [description]
description: Create a git commit
---

Create a git commit with type "$1" and description "$2".

Commit format: $1: $2
```

Command with bash execution:

```yaml
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a commit from staged changes
---

## Current status
!git status

## Changes to commit
!git diff --cached

Create a meaningful commit message for these changes.
```

See [examples.md](references/examples.md) for more examples.

## Common Built-in Commands

Claude Code provides 35+ built-in commands. Common ones include:

| Command | Purpose |
|---------|---------|
| `/help` | Get usage help |
| `/clear` | Clear conversation history |
| `/context` | Visualize current context usage |
| `/cost` | Show token usage statistics |
| `/config` | Open Settings interface |
| `/memory` | Edit `CLAUDE.md` memory files |
| `/model` | Select or change AI model |
| `/plan` | Enter plan mode |
| `/review` | Request code review |

Built-in commands are **not** available through the `Skill` tool.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Command not found | Check filename matches command name |
| Arguments not working | Verify placeholder syntax ($1, $2, $ARGUMENTS) |
| Bash execution failing | Add command to `allowed-tools` |
| Project command ignored | Personal command may have same name (project takes precedence) |

## Reference Files

- [command-types.md](references/command-types.md) - Detailed information on command types
- [syntax-and-arguments.md](references/syntax-and-arguments.md) - Syntax and argument handling
- [frontmatter-reference.md](references/frontmatter-reference.md) - Complete frontmatter reference
- [advanced-features.md](references/advanced-features.md) - Bash execution, hooks, thinking mode
- [best-practices.md](references/best-practices.md) - Naming, namespacing, permissions
- [examples.md](references/examples.md) - Additional command examples
