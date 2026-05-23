---
name: slash-commands
description: Create custom slash commands for Claude Code. Use when users want to create, modify, or understand slash commands for Claude Code CLI tool. Slash commands are markdown files that define reusable prompts and workflows with custom behavior, parameters, and tool access controls.
---

# Slash Commands

Create custom slash commands for Claude Code that enable reusable workflows and specialized prompts.

## Overview

Slash commands are custom commands for Claude Code that control Claude's behavior during interactive sessions. They are markdown files with frontmatter that define specialized prompts, workflows, and tool configurations.

Commands are triggered by typing `/command-name [arguments]` in Claude Code.

## Command Structure

Every slash command is a markdown file with:

1. **YAML frontmatter** - Metadata defining behavior
2. **Markdown body** - The prompt/instructions for Claude

### Frontmatter Fields

```yaml
---
description: Brief description of what the command does
allowed-tools: [Bash, Edit]  # Optional: restrict tool access
argument-hint: <arg1> <arg2>  # Optional: show expected arguments
model: claude-sonnet-4-20250514  # Optional: specify model
---
```

**Field details:**

- `description` - Brief description shown in `/help` (uses first line of prompt if omitted)
- `allowed-tools` - List of tools the command can use (inherits from conversation if omitted)
  - Built-in tools: `Bash`, `Edit`, `View`, `CreateFile`
  - MCP tools: Use format `mcp__servername__toolname` or `mcp__servername` to approve all tools from a server
- `argument-hint` - Shows expected parameters in autocomplete (e.g., `<filename>` or `add <id> | remove <id> | list`)
- `model` - Specific model string to use for this command

### Command Body (The Prompt)

The markdown body is the actual prompt sent to Claude. Use argument placeholders:

- `$ARGUMENTS` - All arguments as a single string
- `$1`, `$2`, `$3`, etc. - Individual positional arguments

**Context references:**

- `@filename.ext` - Include file contents in prompt
- `!command` - Execute bash command and include output (requires `Bash` in `allowed-tools`)

## Command Locations

### Project-Level Commands

**Location:** `.claude/commands/`

Stored in the project repository, shared with team, version controlled.

**Example:** `.claude/commands/optimize.md` creates `/optimize` command

Shows as "(project)" in `/help`

### User-Level Commands

**Location:** `~/.claude/commands/`

Personal commands available across all projects.

**Example:** `~/.claude/commands/security-review.md` creates `/security-review` command

Shows as "(user)" in `/help`

### Subdirectories for Organization

Organize commands in subdirectories:

- `.claude/commands/frontend/component.md` → `/component` (project:frontend)
- `.claude/commands/backend/api.md` → `/api` (project:backend)
- `~/.claude/commands/personal/todo.md` → `/todo` (user:personal)

Note: Conflicts between user and project commands are not supported.

## Common Patterns

### Simple Prompt Template

```markdown
---
description: Optimize code for performance
---

Analyze the following code for performance issues and suggest optimizations:

$ARGUMENTS
```

### Command with File Context

```markdown
---
description: Review security of specified file
argument-hint: <filepath>
allowed-tools: [View]
---

Review @$1 for security vulnerabilities. Focus on:
- Input validation
- Authentication/authorization  
- SQL injection risks
- XSS vulnerabilities
```

### Command with Bash Execution

```markdown
---
description: Show git status and suggest next steps
allowed-tools: [Bash]
---

Current git status:
!git status

!git log --oneline -5

Analyze the current state and suggest appropriate next steps.
```

### Multi-Argument Command

```markdown
---
description: Create a new component
argument-hint: <component-name> <type>
allowed-tools: [CreateFile, Edit]
---

Create a new $2 component named $1.

Component name: $1
Type: $2

Follow project conventions and include:
- Proper imports
- TypeScript types
- Basic structure
- Example usage
```

### MCP Tool Integration

```markdown
---
description: Search GitHub issues
allowed-tools: [mcp__github__search_issues, mcp__github__get_issue]
argument-hint: <search-query>
---

Search GitHub issues for: $ARGUMENTS

Provide a summary of relevant issues and suggest next actions.
```

## Workflow for Creating Commands

1. **Identify the repetitive task** - What do you find yourself asking Claude to do repeatedly?

2. **Choose command scope** - Project-level (`.claude/commands/`) or user-level (`~/.claude/commands/`)?

3. **Create the markdown file** - Name it `command-name.md`

4. **Write frontmatter** - Add description, tools, and argument hints

5. **Write the prompt** - Include clear instructions and use argument placeholders

6. **Test the command** - Run `/command-name [args]` in Claude Code

7. **Iterate** - Refine based on real usage

## Tips for Effective Commands

**Be specific:** Clear, detailed prompts produce better results than vague ones.

**Use context:** Reference files with `@` and include relevant code/docs in the prompt.

**Restrict tools thoughtfully:** Limit tool access to only what's needed for security and focus.

**Add argument hints:** Help users know what parameters to provide.

**Include examples:** Show expected format for complex inputs.

**Organize with subdirectories:** Group related commands for discoverability.

**Version control project commands:** Share `.claude/commands/` with your team via git.

## Resources

See references/examples.md for complete working examples including:
- Code review command
- Component generator  
- Test writer
- Documentation updater
- Git workflow helper
- API schema validator
