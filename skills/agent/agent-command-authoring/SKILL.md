---
name: agent-command-authoring
description: Create Claude Code slash commands and OpenCode command files that delegate to subagents. Use when creating new commands or refactoring existing ones to follow the delegation pattern.
---

# Agent Command Authoring

Create commands that delegate to subagents for Claude Code and OpenCode.

## When to Use This Skill

Use this skill when:
- Creating a new custom command
- Refactoring an existing command to delegate to a subagent
- Ensuring consistency between Claude Code and OpenCode command implementations

## The Delegation Pattern

Commands should be **thin wrappers** that delegate to subagents (which in turn
delegate to skills):

```
command → subagent → skill
```

**Claude Code command** (`.claude/commands/<name>.md`):
```yaml
---
description: Brief description of what the command does
allowed-tools: Task(subagent-name)
---

Use the `<subagent-name>` subagent to accomplish this task.
```

**OpenCode command** (`.config/opencode/command/<name>.md`):
```yaml
---
description: Brief description of what the command does
agent: <subagent-name>
---

Use the `<subagent-name>` subagent to accomplish this task.
```

## Claude Code Command Structure

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | 1-2 sentence description of what the command does |
| `allowed-tools` | Yes | `Task(subagent-name)` to invoke the subagent |
| `argument-hint` | No | Hint for command arguments (e.g., `[feature_name [subtask_number]]`) |

### allowed-tools Format

For commands that delegate to subagents:
- `Task(subagent-name)` - Invoke a subagent

**Example:**
```yaml
allowed-tools: Task(git-committer)
```

## Naming Conventions

Command names should use the **imperative form** of verbs (telling the agent what to do):

- ✅ `commit`, `stage`, `lint`, `test`, `review`, `reflect`
- ❌ `committing`, `git-committer`, `do-linting`

The imperative form gives commands their characteristic feel:
- "commit" = "perform a commit"
- "stage" = "stage changes"
- "test" = "run tests"

## OpenCode Command Structure

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | 1-2 sentence description of what the command does |
| `agent` | Yes | Name of the subagent to invoke |

**Example:**
```yaml
---
description: Create well-formatted commits using conventional commits style
agent: git-committer
---
```

## Command Body

The command body should be **5-20 lines maximum** and contain only:

```markdown
Use the `<subagent-name>` subagent to accomplish this task.
```

**Do NOT include:**
- Full implementation steps
- Duplicated content between Claude and OpenCode
- More than ~20 lines of content

## Examples

### Minimal Command (Claude Code)

```yaml
---
description: Create well-formatted commits using conventional commits style
allowed-tools: Task(git-committer)
---

Use the `git-committer` subagent to create a well-formatted commit.
```

### Minimal Command (OpenCode)

```yaml
---
description: Create well-formatted commits using conventional commits style
agent: git-committer
---

Use the `git-committer` subagent to create a well-formatted commit.
```

### Command with Arguments (Claude Code)

```yaml
---
description: Generate a PRP
argument-hint: [feature_name]
allowed-tools: Task(prp-generator)
---

Use the `prp-generator` subagent to create a Product Requirements Prompt.
```

## Why This Pattern?

1. **Single source of truth**: Skills contain all implementation content
2. **Easier maintenance**: Changes to skills automatically propagate
3. **Platform consistency**: Commands are thin wrappers with platform-specific frontmatter
4. **Token efficiency**: Subagents load skills progressively via progressive disclosure
5. **No duplication**: Implementation lives in one place (the skill)
6. **Isolation**: Subagents run in their own context with appropriate permissions

## Anti-Pattern to Avoid

**BAD** - Command with full implementation:

```yaml
---
description: Stage changes
allowed-tools: Bash(git add:*)
---

# Staging Changes

Stage relevant changes via `git add`...

1. Run `git status` to check for already staged changes
2. Verify no staged changes exist...
3. Run `git status` again...
4. Carefully review which files are relevant...
5. Stage only the relevant files...
6. Run `git status` again...
```

**BAD** - Command that delegates directly to skill (skipping subagent):

```yaml
---
description: Stage changes via git add
allowed-tools: Skill(git-staging)
---

Use the `git-staging` skill to stage relevant changes.
```

**GOOD** - Command that delegates to subagent:

```yaml
---
description: Stage changes via git add
allowed-tools: Task(git-stager)
---

Use the `git-stager` subagent to stage relevant changes.
```

## Workflow

1. **Check for existing skill**: Identify the skill the command should use
2. **Check for existing subagent**: Look for a subagent that delegates to that skill
   - Claude Code: `.claude/agents/<name>.md`
   - OpenCode: `.config/opencode/agent/<name>.md`
3. **If no subagent exists**: Ask the user if they want one created
   - If yes, use the `subagent-authoring` skill to create it first
   - If no, stop and explain the command cannot be created without a subagent
4. Create/refactor Claude Code command with `allowed-tools: Task(subagent-name)`
5. Create/refactor OpenCode command with `agent: subagent-name`
6. Verify the full chain works: command → subagent → skill

## Missing Subagent Handling

Before creating a command, always verify the target subagent exists:

```bash
# Check Claude Code subagent
ls ~/.claude/agents/<subagent-name>.md

# Check OpenCode subagent
ls ~/.config/opencode/agent/<subagent-name>.md
```

If either file is missing, **ask the user**:

> "The subagent `<subagent-name>` doesn't exist yet. Would you like me to
> create it using the `subagent-authoring` skill before proceeding with
> the command?"

Do NOT create commands that reference non-existent subagents.

## Related Skills

- `subagent-authoring` - For creating subagent definitions that delegate to skills
- `skill-authoring` - For creating skills themselves
