---
name: subagent-authoring
description: Create subagent definitions for Claude Code and OpenCode that delegate to skills. Use when creating new subagents or refactoring existing ones to follow the delegation pattern.
---

# Subagent Authoring

Create subagents that delegate to skills for Claude Code and OpenCode.

## When to Use This Skill

Use this skill when:
- Creating a new subagent definition
- Refactoring an existing agent to delegate to a skill
- Ensuring consistency between Claude Code and OpenCode agent implementations

## The Delegation Pattern

Agents should be **thin wrappers** that delegate all implementation to skills:

**Claude Code agent** (`.claude/agents/<name>.md`):
```yaml
---
name: agent-name
description: Brief description of what the agent does
tools: Read, Grep, Glob, Skill(skill-name), ...
---

Use the `<skill-name>` skill to accomplish this task.
```

**OpenCode agent** (`.config/opencode/agent/<name>.md`):
```yaml
---
description: Brief description of what the agent does
mode: subagent
tools:
  read: true
  grep: true
  glob: true
  skill: true
permission:
  bash:
    ...
---

Use the `<skill-name>` skill to accomplish this task.
```

## Claude Code Agent Structure

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Agent identifier (lowercase, no spaces) |
| `description` | Yes | 1-2 sentence description of what the agent does |
| `tools` | Yes | List of tools and skills the agent can use |
| `model` | No | Specific model to use (e.g., `sonnet`) |

### tools Format

- `Read`, `Write`, `Edit`, `Grep`, `Glob`, `Bash` - Core tools
- `Skill(skill-name)` - Load a skill
- `Bash(command:*)` - Allow bash command with any arguments (note the colon)

**Bash permission syntax** (Claude Code uses colons, not spaces):
```yaml
# Allow git commit with any arguments
Bash(git commit:*)

# Allow all git commands
Bash(git:*)

# Allow specific script
Bash(~/.claude/skills/my-skill/scripts/helper.py:*)
```

**Example:**
```yaml
tools: Read, Grep, Glob, Bash(git status:*), Bash(git commit:*), Skill(code-linting)
```

**Documentation**: https://docs.anthropic.com/en/docs/claude-code/settings#tool-permissions

## Naming Conventions

Subagent names should be **agent nouns** formed with the **-er suffix** (meaning "one who does X"):

- ✅ `git-committer`, `git-stager`, `code-linter`, `test-runner`, `task-implementer`
- ❌ `git-commit`, `commit-helper`, `committing-agent`

The `-er` suffix creates agent/instrument nouns:
- committer = one who commits
- stager = one who stages
- implementer = one who implements

## OpenCode Agent Structure

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | 1-2 sentence description |
| `mode` | Yes | Agent mode (`subagent`, `primary`) |
| `tools` | Yes | Map of tool names to boolean enablement |
| `permission` | Yes | Map of tool categories to permission rules |

### tools Format

```yaml
tools:
  read: true
  grep: true
  glob: true
  bash: true
  edit: false
  write: false
  skill: true
```

### Common tool mappings

| Claude Tool | OpenCode Equivalent |
|-------------|---------------------|
| `Read` | `read: true` |
| `Write` | `write: true` |
| `Edit` | `edit: true` |
| `Grep` | `grep: true` |
| `Glob` | `glob: true` |
| `Bash` | `bash: true` |
| `Skill(x)` | `skill: true` |

## Agent Body

The agent body should be **5-20 lines maximum** and contain only:

```markdown
Use the `<skill-name>` skill to accomplish this task.
```

**Do NOT include:**
- Full implementation steps
- Duplicated content between Claude and OpenCode
- More than ~20 lines of content

## Examples

### Minimal Agent (Claude)

```yaml
---
name: code-linter
description: Code linting specialist
tools: Read, Grep, Glob, Bash, Skill(code-linting)
---

Use the `code-linting` skill to run linters.
```

### Minimal Agent (OpenCode)

```yaml
---
description: Code linting specialist
mode: subagent
tools:
  read: true
  grep: true
  glob: true
  bash: true
  skill: true
---

Use the `code-linting` skill to run linters.
```

### Agent with Bash Permissions (OpenCode)

OpenCode uses spaces in permission patterns (unlike Claude Code which uses colons):

```yaml
---
description: Run tests
mode: subagent
tools:
  bash: true
  read: true
  grep: true
  glob: true
  skill: true
permission:
  bash:
    "*": "ask"
    "pytest *": "allow"
    "npm test": "allow"
    "git status": "allow"
    "git commit *": "allow"
---

Use the `test-running` skill to run tests.
```

**Documentation**: https://opencode.ai/docs/permissions

### Primary Mode Agent (OpenCode)

```yaml
---
description: Orchestrates development workflow
mode: primary
tools:
  read: true
  write: true
  edit: true
  bash: true
  grep: true
  glob: true
  todowrite: true
  todoread: true
---

Use the `task-orchestration` skill to orchestrate the development workflow.
```

## Mode Selection

| Mode | Use When |
|------|----------|
| `subagent` | Agent is invoked by another agent or command |
| `primary` | Agent is the main agent handling the conversation |

## Why This Pattern?

1. **Single source of truth**: Skills contain all implementation content
2. **Easier maintenance**: Changes to skills automatically propagate
3. **Platform consistency**: Agents are thin wrappers with platform-specific config
4. **Token efficiency**: Skills load progressively via progressive disclosure
5. **No duplication**: Implementation lives in one place

## Anti-Pattern to Avoid

**BAD** - Agent with full implementation:

```yaml
---
name: code-linter
description: Code linting specialist
tools: Read, Grep, Glob, Bash
---

You are a senior code reviewer responsible for ensuring that code changes pass
all linters...

## When to Use This Agent PROACTIVELY

Always use immediately after:
- Creating new source code files
- Modifying existing code...

## What This Agent Does

1. **Discovers** all appropriate linters...
2. **Runs** formatting checks...
3. **Auto-fixes** issues...
4. **Reports** remaining issues...

## Linting Process

Run linters according to repository guidelines. First look for linting
commands in the following order:
...
```

**GOOD** - Agent that delegates:

```yaml
---
name: code-linter
description: Code linting specialist
tools: Read, Grep, Glob, Bash, Skill(code-linting)
---

Use the `code-linting` skill to run linters.
```

## Workflow

1. Create the skill first (or identify existing skill to use)
2. Create/refactor Claude agent with proper frontmatter and delegation
3. Create/refactor OpenCode agent with matching content and platform-specific config
4. Verify both agents delegate correctly

## Related Skills

- `agent-command-authoring` - For creating commands that delegate to skills
- `skill-authoring` - For creating skills themselves
