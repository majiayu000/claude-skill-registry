---
name: custom-slash-commands
description: Guide for creating custom Claude Code slash commands - shortcuts for frequently-used prompts and workflows. Use when creating reusable prompts, automating common tasks, or building team workflows. Covers frontmatter, arguments, bash execution, and namespacing.
allowed-tools: ["Read", "Write", "Bash", "Glob"]
---

# Custom Slash Commands

Create reusable prompts and workflows as slash commands that Claude Code can execute on demand.

## Quick Reference

| Element | Requirement |
|---------|-------------|
| Location (project) | `.claude/commands/name.md` |
| Location (user) | `~/.claude/commands/name.md` |
| Filename | Lowercase with hyphens, `.md` extension |
| Invocation | `/command-name [arguments]` |
| Precedence | Project commands override user commands |

## Frontmatter Options

| Field | Purpose | Default |
|-------|---------|---------|
| `allowed-tools` | Tools the command can use | Inherits from conversation |
| `argument-hint` | Hint shown in autocomplete | None |
| `description` | Brief description | First line of prompt |
| `model` | Force specific model | Inherits from conversation |
| `hooks` | Lifecycle-scoped hooks (PreToolUse, PostToolUse, Stop) | None |
| `disable-model-invocation` | Prevent Skill tool access | false |

## Command vs Skill Decision Guide

| Choose Command When | Choose Skill When |
|---------------------|-------------------|
| Simple prompt fits one file | Complex workflow needs multiple files |
| You want explicit `/invoke` | Claude should auto-discover |
| Quick template or reminder | Scripts and utilities needed |
| Single-file instructions | Team needs detailed guidance |

**Rule of thumb:** If it fits in one file and you want explicit control, use a command. If it needs structure or auto-discovery, use a Skill.

## File Structure

### Project Commands (Team-Shared)

```
.claude/
  commands/
    commit.md           # /commit
    review.md           # /review
    frontend/
      component.md      # /component (project:frontend)
      test.md           # /test (project:frontend)
    backend/
      endpoint.md       # /endpoint (project:backend)
      test.md           # /test (project:backend)
```

### User Commands (Personal)

```
~/.claude/
  commands/
    standup.md          # /standup (user)
    journal.md          # /journal (user)
    tools/
      format.md         # /format (user:tools)
```

## Core Patterns

### Pattern 1: Simple Prompt Command

```markdown
# .claude/commands/review.md
Review this code for:
- Security vulnerabilities
- Performance issues
- Code style violations
```

Usage: `/review`

### Pattern 2: Command with Arguments

```markdown
# .claude/commands/fix-issue.md
---
argument-hint: <issue-number>
description: Fix a GitHub issue by number
---

Fix issue #$ARGUMENTS following our coding standards.
Check the issue description and implement the fix.
```

Usage: `/fix-issue 123`

### Pattern 3: Positional Arguments

```markdown
# .claude/commands/review-pr.md
---
argument-hint: [pr-number] [priority] [assignee]
description: Review pull request with priority
---

Review PR #$1 with priority $2 and assign to $3.
Focus on security, performance, and code style.
```

Usage: `/review-pr 456 high alice`

### Pattern 4: Bash Execution

```markdown
# .claude/commands/commit.md
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit with context
---

## Context

- Current git status: !`git status`
- Staged changes: !`git diff --cached`
- Recent commits: !`git log --oneline -5`

## Task

Create a commit message based on the staged changes.
Follow conventional commit format.
```

Usage: `/commit`

### Pattern 5: File References

```markdown
# .claude/commands/compare.md
---
argument-hint: <file1> <file2>
description: Compare two files
---

Compare the following files and highlight differences:

File 1: @$1
File 2: @$2

Focus on:
- API changes
- Breaking changes
- Logic differences
```

Usage: `/compare src/old.ts src/new.ts`

### Pattern 6: Tool Restrictions

```markdown
# .claude/commands/analyze.md
---
allowed-tools: Read, Glob, Grep
description: Analyze code without making changes
---

Analyze the codebase for patterns and issues.
Do NOT modify any files - read-only analysis.
```

### Pattern 7: Model Override

```markdown
# .claude/commands/quick-answer.md
---
model: claude-3-5-haiku-20241022
description: Quick answer using faster model
---

Quickly answer: $ARGUMENTS

Be concise. No code changes.
```

### Pattern 8: Command with Hooks

```markdown
# .claude/commands/deploy.md
---
description: Deploy with pre-flight validation
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/preflight-check.sh"
          once: true
  Stop:
    - hooks:
        - type: command
          command: "./scripts/notify-deploy.sh"
---

Deploy the current branch to the staging environment.
Ensure all tests pass before deploying.
```

Hooks in commands are lifecycle-scoped and only active during command execution.

## Namespacing

Subdirectories group related commands and appear in descriptions:

| File Path | Command | Description Shows |
|-----------|---------|-------------------|
| `.claude/commands/deploy.md` | `/deploy` | (project) |
| `.claude/commands/frontend/deploy.md` | `/deploy` | (project:frontend) |
| `~/.claude/commands/deploy.md` | `/deploy` | (user) |
| `~/.claude/commands/tools/deploy.md` | `/deploy` | (user:tools) |

**Conflict Resolution:**
- Project commands override user commands with same name
- Same-name commands in different subdirectories coexist (distinguished by description)

## Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `$ARGUMENTS` | All arguments as single string | `"123 high-priority"` |
| `$1`, `$2`, ... | Individual positional arguments | `$1="123"`, `$2="high-priority"` |
| `!`command`` | Bash output (requires allowed-tools) | `!`git status`` |
| `@path` | File contents reference | `@src/main.ts` |

## Workflow: Creating a Command

### Prerequisites

- [ ] Identify the repeated prompt or workflow
- [ ] Decide: project or user scope
- [ ] Plan arguments if dynamic

### Steps

1. **Create command file**
   - [ ] Choose location (`.claude/commands/` or `~/.claude/commands/`)
   - [ ] Name file (lowercase, hyphens, `.md`)
   - [ ] Add frontmatter if needed

2. **Write command content**
   - [ ] Clear instructions for Claude
   - [ ] Add argument placeholders if needed
   - [ ] Include bash execution if needed

3. **Test**
   - [ ] Run `/help` to verify command appears
   - [ ] Execute command with test arguments
   - [ ] Verify output is as expected

### Validation Checklist

- [ ] Filename is lowercase with hyphens
- [ ] Command appears in `/help`
- [ ] Arguments work correctly
- [ ] Bash execution has `allowed-tools`
- [ ] Description is helpful

## Skill Tool Integration

Claude can invoke custom commands and skills programmatically via the `Skill` tool (replaces the deprecated `SlashCommand` tool).

**Requirements for Skill tool invocation:**
- Must have `description` in frontmatter
- Cannot be a built-in command
- Not blocked by `disable-model-invocation: true`

**Character budget:** Default 15,000 characters. Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var.

**To encourage usage:**
```markdown
# In CLAUDE.md
Run /write-test when starting to write tests.
```

**To disable:**
```yaml
---
disable-model-invocation: true
---
```

### Permission Rules

Control which commands Claude can invoke via the Skill tool:

| Pattern | Meaning |
|---------|---------|
| `Skill(/commit)` | Exact match (no arguments) |
| `Skill(/review-pr:*)` | Prefix match (any arguments) |
| `Skill(/deploy:*)` | Prefix match |

```json
// settings.json
{
  "permissions": {
    "allow": ["Skill(/commit)", "Skill(/review-pr:*)"],
    "deny": ["Skill(/deploy:*)"]
  }
}
```

**Migration:** If you have existing `SlashCommand` permission rules, update them to use `Skill`.

## Security Considerations

- [ ] Be careful with `allowed-tools: Bash(*)` - prefer specific patterns
- [ ] Don't expose secrets in command files
- [ ] Review project commands before committing
- [ ] Consider `disable-model-invocation` for sensitive commands

## Reference Files

| File | Contents |
|------|----------|
| [EXAMPLES.md](./EXAMPLES.md) | 8+ copy-paste ready examples |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Common issues and solutions |
