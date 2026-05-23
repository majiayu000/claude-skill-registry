---
name: creating-commands
description: Expert knowledge on creating slash commands for Claude Code. Use when designing or creating slash command .md files, understanding command arguments, or implementing bash execution.
allowed-tools: Read, Grep, Glob
---

# Creating Slash Commands

This Skill provides comprehensive knowledge about creating effective slash commands in Claude Code.

## What Are Slash Commands?

Slash commands are user-invoked operations that start with `/`. When executed, they expand to a full prompt that Claude processes. They're different from subagents (which are automatically invoked) - slash commands require explicit user action.

## File Structure

**Project commands**: `.claude/commands/{command-name}.md`
**Personal commands**: `~/.claude/commands/{command-name}.md`

**Format**:
```yaml
---
description: Brief description of what this command does
argument-hint: [arg1] [arg2]  # Optional
allowed-tools: Bash(git:*), Read, Write  # Optional
model: haiku  # Optional
disable-model-invocation: false  # Optional
---

Command prompt that Claude will execute.
Can use $ARGUMENTS or $1, $2, $3, etc.
```

## YAML Frontmatter Fields

### Optional Fields (All Are Optional)

**description** (string)
- Brief description shown in `/help`
- If omitted, uses first line of prompt
- Keep concise (one sentence)

**argument-hint** (string)
- Shows expected arguments in autocomplete
- Examples: `[filename]`, `[message]`, `add [tag] | remove [tag]`
- Helps users know what to provide

**allowed-tools** (comma-separated string)
- Tools this command can use
- If omitted, inherits from conversation
- Use for command-specific restrictions

**model** (string)
- Specific model: `sonnet`, `opus`, `haiku`
- If omitted, inherits from conversation
- Use `haiku` for simple/fast commands

**disable-model-invocation** (boolean)
- If `true`, prevents SlashCommand tool from calling this command
- Default: `false`
- Use to keep commands user-only

## Command Arguments

### Using $ARGUMENTS (All Arguments)

Captures everything after the command name:

```yaml
---
description: Fix issue following coding standards
---

Fix issue #$ARGUMENTS following our coding standards
```

Usage:
```
/fix-issue 123 high-priority
# $ARGUMENTS becomes "123 high-priority"
```

### Using $1, $2, $3 (Positional Arguments)

Access specific arguments individually:

```yaml
---
description: Review PR with priority and assignee
argument-hint: [pr-number] [priority] [assignee]
---

Review PR #$1 with priority $2 and assign to $3.
Focus on security, performance, and code style.
```

Usage:
```
/review-pr 456 high alice
# $1="456", $2="high", $3="alice"
```

### When to Use Which

**Use $ARGUMENTS**:
- Flexible, variable-length input
- Natural language descriptions
- Unknown number of args

**Use $1, $2, $3**:
- Fixed structure
- Specific fields needed
- Build complex prompts with arg positioning

## Bash Command Execution

Execute bash commands before the prompt runs using `!` prefix.

### Basic Execution

```yaml
---
allowed-tools: Bash(git:*)
---

## Current Status

Git status: !`git status`

## Your Task

Based on the above status, create a commit.
```

The `!` commands run first, output is included in prompt context.

### Multiple Commands

```yaml
---
allowed-tools: Bash(git:*), Bash(docker:*)
---

## Context

- Git status: !`git status`
- Docker status: !`docker ps`
- Current branch: !`git branch --show-current`

## Task

Deploy the current branch.
```

### Required: allowed-tools

**Must** include Bash tool permissions:

```yaml
---
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

Current changes: !`git diff HEAD`
```

Specify exact commands or use wildcards:
- `Bash(git:*)` - All git commands
- `Bash(git status:*), Bash(git diff:*)` - Specific commands only

## File References

Include file contents using `@` prefix:

```yaml
---
description: Review implementation
---

Review the implementation in @src/utils/helpers.js

Compare @src/old-version.js with @src/new-version.js
```

When command runs, files are automatically included in context.

## Extended Thinking

Trigger extended thinking by including keywords:

```yaml
---
description: Solve complex algorithm problem
---

Think carefully about this algorithm optimization problem: $ARGUMENTS

Consider multiple approaches before implementing.
```

Keywords that trigger thinking: "think carefully", "consider", "analyze deeply"

## Command Patterns

### Simple Action Commands

```yaml
---
description: Run all tests
allowed-tools: Bash(pytest:*)
---

Run the complete test suite:
!`pytest -v`

Report results and any failures.
```

### Context Gathering Commands

```yaml
---
description: Analyze current work
allowed-tools: Bash(git:*)
---

## Current Work Context

- Branch: !`git branch --show-current`
- Status: !`git status --short`
- Recent commits: !`git log --oneline -5`
- Uncommitted changes: !`git diff HEAD --stat`

Summarize what I'm currently working on.
```

### Workflow Commands

```yaml
---
description: Create feature branch from issue
argument-hint: [issue-number]
allowed-tools: Bash(gh:*), Bash(git:*)
---

## Issue Details

!`gh issue view $1 --json title,body`

## Task

1. Create branch: `issue-$1-{description}`
2. Check out the branch
3. Summarize the issue for me
```

### Validation Commands

```yaml
---
description: Validate code before commit
allowed-tools: Bash(git:*), Bash(npm:*), Bash(pytest:*)
---

## Pre-Commit Checks

1. Run linter: !`npm run lint`
2. Run tests: !`pytest`
3. Check types: !`npm run type-check`
4. Git status: !`git status`

Report any issues that need fixing before commit.
```

### Generation Commands

```yaml
---
description: Generate API endpoint
argument-hint: [resource-name]
---

Create a complete REST API endpoint for: $1

Include:
- Model definition
- Schema (Create, Update, Response)
- CRUD operations
- Endpoints (GET, POST, PUT, DELETE)
- Tests
```

## Tool Restrictions

### Git Commands Only

```yaml
---
allowed-tools: Bash(git:*), Read, Write
---

Safe git operations command.
```

### Read-Only Command

```yaml
---
allowed-tools: Read, Grep, Glob
---

Analysis command that doesn't modify files.
```

### Specific Commands

```yaml
---
allowed-tools: Bash(docker compose up:*), Bash(docker compose down:*)
---

Docker management command with limited operations.
```

## Model Selection

### Haiku for Simple Commands

```yaml
---
model: haiku
---

Quick file listing: !`ls -la`
```

Fast, economical for simple tasks.

### Sonnet for Standard Commands

```yaml
# Omit model field - uses conversation model (usually sonnet)
---
description: Standard complexity command
---
```

### Opus for Complex Commands

```yaml
---
model: opus
---

Analyze architecture and suggest improvements: $ARGUMENTS
```

Deep reasoning for complex tasks.

## Examples

### Example 1: Simple Git Commit

```yaml
---
description: Create git commit with message
argument-hint: [message]
allowed-tools: Bash(git:*)
---

Create a git commit:

Message: $ARGUMENTS

Steps:
1. Stage all changes: `git add .`
2. Commit with message
3. Show commit hash and summary
```

### Example 2: Test Runner

```yaml
---
description: Run specific test file
argument-hint: [test-file]
allowed-tools: Bash(pytest:*)
---

Run tests in: $1

!`pytest $1 -v`

Analyze failures and suggest fixes.
```

### Example 3: Context-Heavy Command

```yaml
---
description: Prepare for code review
allowed-tools: Bash(git:*), Read
---

## Code Review Preparation

### Changes
!`git diff main..HEAD --stat`

### Commits
!`git log main..HEAD --oneline`

### Modified Files
!`git diff main..HEAD --name-only`

Summarize changes for code review and suggest review focus areas.
```

### Example 4: Branching Workflow

```yaml
---
description: Create feature branch from issue
argument-hint: [issue-number]
allowed-tools: Bash(gh:*), Bash(git:*)
---

## Issue #$1 Details

!`gh issue view $1 --json title,body,labels`

## Task

1. Create branch: `issue-$1-{short-description}`
2. Switch to branch
3. Print next steps for working on this issue
```

### Example 5: Multi-Step Workflow

```yaml
---
description: Complete issue and create PR
argument-hint: [issue-number]
allowed-tools: Bash(git:*), Bash(gh:*)
---

## Current Status

Branch: !`git branch --show-current`
Status: !`git status --short`

## Task

Complete issue #$1 workflow:
1. Ensure all changes committed
2. Push branch to origin
3. Create PR linking to issue #$1
4. Provide PR URL
```

## Command Organization

### Flat Structure

```
.claude/commands/
├── create-branch.md
├── review-pr.md
├── run-tests.md
└── deploy.md
```

Simple, no subdirectories needed.

### With Subdirectories

```
.claude/commands/
├── git/
│   ├── create-branch.md
│   └── create-pr.md
└── testing/
    ├── run-tests.md
    └── coverage.md
```

Subdirectories organize but don't affect command names:
- `/create-branch` works regardless of subdirectory
- Description shows "(project:git)" or "(user:testing)"

## Best Practices

### 1. Clear Descriptions

```yaml
# Good
description: Run all tests and report failures

# Bad
description: Tests
```

### 2. Helpful Argument Hints

```yaml
# Good
argument-hint: [pr-number] [priority] [assignee]

# Bad
argument-hint: [args]
```

### 3. Specific Tool Permissions

```yaml
# Good
allowed-tools: Bash(git status:*), Bash(git add:*), Bash(git commit:*)

# Risky
allowed-tools: Bash(*)
```

### 4. Context Before Instructions

```yaml
# Good
## Current State
!`git status`

## Task
Create commit

# Bad (no context)
Create commit for: $ARGUMENTS
```

### 5. Use Heredocs for Commit Messages

```yaml
# Good
git commit -m "$(cat <<'EOF'
$ARGUMENTS
EOF
)"

# Bad
git commit -m "$ARGUMENTS"  # Formatting issues
```

## Testing Commands

### Test Manually

```
/your-command arg1 arg2
```

### Test Argument Substitution

```
/review-pr 123 high alice
# Verify $1, $2, $3 substituted correctly
```

### Test Bash Execution

Verify `!` commands run and output appears in prompt.

## Troubleshooting

### Command Not Found

**Problem**: `/mycommand` doesn't work

**Check**:
1. File exists at `.claude/commands/mycommand.md`
2. Filename matches command (no typos)
3. Restart Claude Code after creating

### Arguments Not Substituting

**Problem**: `$1` appears literally in output

**Check**:
1. Using `$1` in prompt content (not frontmatter)
2. Provided arguments when calling command
3. No escaping of `$` character

### Bash Commands Not Running

**Problem**: `!` commands don't execute

**Check**:
1. `allowed-tools` includes Bash permissions
2. Command has `!` prefix and backticks: `!`command``
3. Command syntax is valid

### Permission Denied

**Problem**: Command can't use certain tools

**Check**:
1. `allowed-tools` includes needed tools
2. Tool names spelled correctly
3. Bash command patterns match allowed list

## Validation Checklist

Before finalizing a command:

- [ ] Description is clear and concise
- [ ] Argument hints provided (if using args)
- [ ] Tool permissions specified (if using tools)
- [ ] Arguments use proper format ($ARGUMENTS or $1, $2, etc.)
- [ ] Bash commands have `!` and backticks
- [ ] Bash permissions match commands used
- [ ] Heredocs used for multi-line strings
- [ ] File tested with sample arguments

## Summary

**Essential Elements**:
1. Clear description (what it does)
2. Argument hints (what to provide)
3. Proper argument substitution ($ARGUMENTS or $1-$9)
4. Tool permissions (if using tools)
5. Context gathering (using `!` for bash)

**Success Criteria**:
- Command shows in `/help`
- Arguments substitute correctly
- Bash commands execute
- Claude produces expected result
- Tool permissions work
