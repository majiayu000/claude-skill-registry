---
name: create-command
description: Create a new Claude Code slash command with proper YAML frontmatter structure. Use when the user wants to add a custom slash command to a plugin. Handles command file creation with description, argument hints, allowed tools, and all advanced features.
---

# Create Command Skill

Create new Claude Code slash commands with proper configuration and advanced features.

## Command Types

### Project Commands
Commands stored in your repository and shared with your team.

**Location**: `.claude/commands/` or `plugins/<plugin>/commands/`

Shows "(project)" in `/help`.

### Personal Commands
Commands available across all your projects.

**Location**: `~/.claude/commands/`

Shows "(user)" in `/help`.

## Command File Format

Commands are markdown files with YAML frontmatter:

```markdown
---
description: Short description shown in /help
argument-hint: <required-arg> [optional-arg]
---

# Command Name

Instructions for Claude when this command is invoked...
```

## Frontmatter Fields

| Field | Purpose | Default |
|-------|---------|---------|
| `description` | Brief description of the command | Uses first line from prompt |
| `argument-hint` | Arguments shown in autocomplete | None |
| `allowed-tools` | List of tools the command can use | Inherits from conversation |
| `model` | Specific model string | Inherits from conversation |
| `disable-model-invocation` | Prevent SlashCommand tool from calling | false |

## Argument Placeholders

### All Arguments: `$ARGUMENTS`

Captures all arguments passed to the command:

```markdown
---
description: Fix a GitHub issue
argument-hint: <issue-number> [priority]
---

Fix issue #$ARGUMENTS following our coding standards.

# Usage: /fix-issue 123 high-priority
# $ARGUMENTS becomes: "123 high-priority"
```

### Positional Arguments: `$1`, `$2`, etc.

Access specific arguments individually:

```markdown
---
description: Review pull request
argument-hint: <pr-number> <priority> <assignee>
---

Review PR #$1 with priority $2 and assign to $3.
Focus on security, performance, and code style.

# Usage: /review-pr 456 high alice
# $1 = "456", $2 = "high", $3 = "alice"
```

## Bash Command Execution

Execute bash commands before the slash command runs using the `!` prefix.

**IMPORTANT**: You MUST include `allowed-tools` with the `Bash` tool.

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current git status: !`git status`
- Current git diff: !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
```

## File References

Include file contents using the `@` prefix:

```markdown
---
description: Review implementation
---

# Reference a specific file
Review the implementation in @src/utils/helpers.js

# Reference multiple files
Compare @src/old-version.js with @src/new-version.js
```

## Namespacing

Organize commands in subdirectories. The subdirectory appears in the description but not the command name.

```
.claude/commands/
├── frontend/
│   └── component.md    # Creates /component (project:frontend)
└── backend/
    └── api.md          # Creates /api (project:backend)
```

## Argument Hint Conventions

| Syntax | Meaning |
|--------|---------|
| `<name>` | Required argument |
| `[name]` | Optional argument |
| `[--flag]` | Optional flag |
| `[--option <value>]` | Optional flag with value |
| `""` or omit | No arguments |

## Examples

### Simple Command

```markdown
---
description: Show project status overview
---

Show a summary of the current project status including:
- Git branch and recent commits
- Open issues and PRs
- Build status
```

### Command with Tools

```markdown
---
allowed-tools: Bash(npm:*), Bash(yarn:*)
description: Run tests with coverage
argument-hint: [--watch] [--coverage]
---

Run the test suite with the following options:
- If --watch is passed, run in watch mode
- If --coverage is passed, generate coverage report

Use npm or yarn based on the lock file present.
```

### Git Commit Command

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a conventional commit
argument-hint: [message]
---

## Context

- Current status: !`git status --short`
- Staged changes: !`git diff --cached --stat`
- Recent commits: !`git log --oneline -5`

## Task

Create a git commit following conventional commit format:
- type(scope): description
- Types: feat, fix, docs, style, refactor, test, chore

If $ARGUMENTS is provided, use it as the commit message.
Otherwise, analyze the changes and generate an appropriate message.
```

### Deploy Command

```markdown
---
allowed-tools: Bash(docker:*), Bash(kubectl:*)
description: Deploy to environment
argument-hint: <environment> [--dry-run]
model: claude-sonnet-4-20250514
---

Deploy to $1 environment.

## Pre-flight checks
- Verify current branch: !`git branch --show-current`
- Check for uncommitted changes: !`git status --porcelain`

## Process
1. Build Docker image
2. Push to registry
3. Update Kubernetes deployment
4. Verify rollout status

If --dry-run is in $ARGUMENTS, only show what would be done.
```

### Code Review Command

```markdown
---
description: Review code changes
argument-hint: [file-path]
---

Review the code for:
- Security vulnerabilities
- Performance issues
- Code style violations
- Best practices

If a file path is provided ($1), focus on that file.
Otherwise, review all changed files:
!`git diff --name-only HEAD~1`

Reference style guide: @.claude/STYLE_GUIDE.md
```

## Thinking Mode

Include extended thinking keywords to trigger deeper analysis:

```markdown
---
description: Analyze architecture deeply
---

Think step by step about the architecture of this codebase.
Consider:
- Design patterns used
- Potential improvements
- Scalability concerns
```

## SlashCommand Tool Integration

For commands to be invocable by Claude via the SlashCommand tool:

1. **Must have `description`** frontmatter field
2. **Use `disable-model-invocation: true`** to prevent automatic invocation
3. **Built-in commands** (like `/compact`) are NOT supported

### Permission Rules

```
SlashCommand:/commit           # Exact match only
SlashCommand:/review-pr:*      # Prefix match with any arguments
```

## File Location

| Type | Location |
|------|----------|
| Plugin commands | `plugins/<plugin>/commands/<name>.md` |
| Project commands | `.claude/commands/<name>.md` |
| Personal commands | `~/.claude/commands/<name>.md` |

The filename (without `.md`) becomes the slash command name.

## Slash Commands vs Skills

| Aspect | Slash Commands | Skills |
|--------|---------------|--------|
| **Complexity** | Simple prompts | Complex capabilities |
| **Structure** | Single .md file | Directory with SKILL.md + resources |
| **Discovery** | Explicit (`/command`) | Automatic (context-based) |
| **Files** | One file only | Multiple files, scripts, templates |

**Use slash commands** when:
- You invoke the same prompt repeatedly
- The prompt fits in a single file
- You want explicit control over when it runs

**Use Skills** when:
- Claude should discover automatically
- Multiple files or scripts needed
- Complex workflows with validation
