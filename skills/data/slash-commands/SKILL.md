---
name: slash-commands
description: Best practices for creating Claude Code slash commands. Use this skill when creating, editing, or improving custom slash commands for Claude Code. Covers frontmatter configuration, dynamic features ($ARGUMENTS, bash execution, file references), command patterns (git workflows, multi-agent orchestration, code review), and helps decide when to use slash commands vs skills vs subagents.
---

# Claude Code Slash Commands

This skill provides guidance for creating effective custom slash commands in Claude Code.

## Quick Reference

**Locations:**
- Project commands: `.claude/commands/` (shared via git)
- Personal commands: `~/.claude/commands/` (user-specific)

**File format:** Markdown (`.md`) with optional YAML frontmatter

**Command name:** Derived from filename (`commit.md` → `/commit`)

## Frontmatter Options

See `references/frontmatter.md` for complete documentation.

Essential fields:
```yaml
---
allowed-tools: Bash(git add:*), Bash(git commit:*)  # Tool permissions
description: Brief description shown in /help        # Required for model invocation
argument-hint: "[branch-name] [commit-type]"        # Shown in autocomplete
model: claude-haiku-4-5                             # Override session model
disable-model-invocation: true                      # Prevent auto-invocation
---
```

## Dynamic Features

### Arguments

**All arguments:** `$ARGUMENTS` captures everything after the command
```markdown
Fix issue #$ARGUMENTS following our coding standards
# /fix-issue 123 high-priority → "123 high-priority"
```

**Positional:** `$1`, `$2`, `$3`... for specific arguments
```markdown
Review PR #$1 with priority $2 and assign to $3
# /review-pr 456 high alice → $1="456", $2="high", $3="alice"
```

### Bash Context Injection

Use `!` prefix to execute bash and inject output as context:
```markdown
## Context
- Current git status: !`git status`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`
```

**Important:** Requires `allowed-tools` with `Bash` tool in frontmatter.

### File References

Use `@` prefix to include file contents:
```markdown
Review the implementation in @src/utils/helpers.js
Compare @src/old-version.js with @src/new-version.js
```

## Command Patterns

See `references/patterns.md` for detailed patterns with full examples.

### Pattern 1: Simple Task

For quick, focused operations:
```markdown
---
description: Analyze code for performance issues
---

Analyze this code for performance issues and suggest optimizations.
Focus on: time complexity, memory usage, unnecessary operations.
```

### Pattern 2: Git Workflow

For git operations with context:
```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context
- Current git status: !`git status`
- Current git diff: !`git diff HEAD`
- Current branch: !`git branch --show-current`

## Your task
Based on the above changes, create a single commit with an appropriate message.
```

### Pattern 3: Multi-Agent Orchestration

For complex tasks requiring parallel work:
```markdown
---
allowed-tools: Bash(gh:*), TodoWrite
description: Find duplicate GitHub issues
---

Find duplicates for issue $ARGUMENTS.

Follow these steps precisely:
1. Use an agent to view the issue and return a summary
2. Launch 5 parallel agents to search for duplicates using diverse keywords
3. Feed results into another agent to filter false positives
4. Comment on the issue with up to 3 likely duplicates

Notes (tell your agents too):
- Use `gh` for GitHub interactions
- Do not use other tools beyond `gh`
```

### Pattern 4: Structured Review

For comprehensive analysis workflows:
```markdown
---
description: "Comprehensive code review"
argument-hint: "[review-aspects]"
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Task"]
---

# Code Review

**Review Aspects (optional):** "$ARGUMENTS"

## Workflow:
1. **Determine Scope** - Check git status for changed files
2. **Run Reviews** - Execute applicable review agents
3. **Aggregate Results** - Summarize findings by severity
4. **Provide Action Plan** - Organize fixes by priority
```

## Writing Guidelines

1. **Use imperative language:** "Create", "Execute", "Based on..."
2. **Be explicit about constraints:** Include what NOT to do
3. **Specify output format:** Provide templates for structured output
4. **Enable multi-tool efficiency:** Tell Claude it can use multiple tools in one response
5. **Include a Notes section:** For edge cases and important constraints

## When to Use Slash Commands vs Skills vs Subagents

See `references/decision-guide.md` for detailed comparison.

**Quick decision framework:**

| Use Case | Best Choice |
|----------|-------------|
| Quick, repeatable task you trigger manually | Slash Command |
| Complex workflow with scripts/templates | Skill |
| Parallel execution with isolated context | Subagent |
| Team-shared workflow checked into git | Slash Command |
| Domain expertise Claude should auto-discover | Skill |
| Specialized role (security auditor, etc.) | Subagent |

**Key distinctions:**
- **Commands:** User-invoked (`/command`), simple prompts, manual trigger
- **Skills:** Model-invoked (Claude decides), rich context, scripts/assets
- **Subagents:** Own context window, parallel work, delegated tasks

## Templates

Use templates in `assets/templates/` as starting points:
- `simple-command.md` - Basic single-purpose command
- `git-workflow.md` - Git operations with context injection
- `multi-agent.md` - Orchestration with parallel agents
- `review-command.md` - Comprehensive review workflow

## Best Practices from Anthropic

1. **Granular tool permissions:** Use wildcards for flexibility
   ```yaml
   allowed-tools: Bash(git add:*), Bash(git commit:*)
   ```

2. **Context injection:** Pre-load relevant state with bash execution

3. **Clear task structure:** Use `## Your task` or `## Your Task` section

4. **Explicit constraints:** Include prohibitions
   ```markdown
   Do not use any other tools or do anything else.
   Do not send any other text or messages besides these tool calls.
   ```

5. **Output format specification:** Provide exact templates for structured output

6. **Agent instructions:** When using subagents, include notes they should follow
   ```markdown
   Notes (be sure to tell this to your agents, too):
   - Use `gh` for GitHub interactions
   - Make a todo list first
   ```
