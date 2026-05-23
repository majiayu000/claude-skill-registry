---
name: command-creator
description: 'Create Claude Code custom slash commands with proper structure, frontmatter, and best practices. Use this skill whenever the user wants to create a new command, add a slash command, build a custom command, or mentions "create-command", "new command", "add command", or "make a command" for Claude Code. Also trigger when the user wants to turn a workflow into a reusable command.'
---

# Command Creator

Create Claude Code custom slash commands with proper structure and best practices.

## Understanding Commands

Claude Code commands are Markdown files with YAML frontmatter that define reusable workflows invoked via `/command-name`. They live in specific locations depending on scope:

- **Project-level**: `.claude/commands/` in the project root (shared via git)
- **User-level**: `~/.claude/commands/` (personal, available everywhere)
- **Categorized**: Nest under subdirectories for namespacing (e.g., `gh/review-pr.md` becomes `/gh:review-pr`)

## Process

### 1. Clarify Intent

Before writing anything, understand:
- What should the command do? (single clear purpose)
- Who uses it — just this user, or the whole team? (determines project vs user-level)
- Does it need arguments? What kind?
- What tools does it need access to?
- Is there a category it belongs to? (e.g., `gh` for GitHub, `cc` for Claude Code meta-commands)

### 2. Write the Command

Every command file follows this structure:

```markdown
---
description: Brief description shown in command list
argument-hint: [expected-arguments]
allowed-tools: Tool1, Tool2, Bash(prefix:*)
---

# Command Name

What this command does and when to use it.

## Process:

Step-by-step instructions for the agent to follow.

## Your Task:

Act on "$ARGUMENTS" following these guidelines.
```

#### Frontmatter fields

| Field | Required | Purpose |
|-------|----------|---------|
| `description` | Yes | Short description shown when listing commands |
| `argument-hint` | No | Hint for expected arguments (shown in autocomplete) |
| `allowed-tools` | No | Restrict which tools the command can use |

#### Key conventions

- **`$ARGUMENTS`** is replaced with whatever the user types after the command name. Always reference it in the "Your Task" section so the command acts on user input.
- **`allowed-tools`** uses patterns: exact names (`Read`, `Write`), or prefix globs for Bash (`Bash(git:*)`, `Bash(npm:*)`).
- Keep commands **focused and single-purpose** — one command, one job.
- Write instructions in the **imperative form** ("Analyze the code", not "You should analyze the code").
- Include **concrete examples** of usage and expected behavior.

### 3. Choose the Right Location

| Scope | Path | When to use |
|-------|------|-------------|
| Project (shared) | `.claude/commands/` | Team workflows, project-specific tasks |
| Project (categorized) | `.claude/commands/<category>/` | Grouped commands (e.g., `gh/`, `db/`) |
| User (personal) | `~/.claude/commands/` | Personal productivity, cross-project tools |

### 4. Validate

After creating the command file:
- Verify the YAML frontmatter parses correctly (no syntax errors)
- Confirm the file is in the right directory
- Check that `$ARGUMENTS` is referenced if the command accepts input
- Ensure `allowed-tools` includes everything the command needs

## Example: A Simple Command

```markdown
---
description: Review a pull request with detailed analysis
argument-hint: [PR-number-or-URL]
allowed-tools: Bash(gh:*), Read, Grep, Glob
---

# Review PR

Perform a thorough code review of a GitHub pull request.

## Process:

1. Fetch PR details and diff using `gh pr view` and `gh pr diff`
2. Read changed files for full context
3. Analyze changes for:
   - Correctness and potential bugs
   - Code style consistency
   - Missing tests or edge cases
   - Security concerns
4. Provide a structured review summary

## Your Task:

Review PR "$ARGUMENTS" following these guidelines. If no PR number is given,
use `gh pr list` to show recent PRs and ask which one to review.
```

## Best Practices

- **Descriptive names**: The filename becomes the command name — make it clear (`fix-issue.md` not `fi.md`)
- **Graceful argument handling**: Always handle the case where `$ARGUMENTS` is empty
- **Minimal tool permissions**: Only list tools the command actually needs in `allowed-tools`
- **Follow existing patterns**: Look at other commands in the same directory for conventions
- **Test before shipping**: Try the command with different inputs to verify it works

## Your Task

Create a new command based on "$ARGUMENTS":

1. If the purpose is unclear, ask clarifying questions
2. Determine the appropriate location and category
3. Create the command file with proper structure
4. Explain what was created and how to use it
