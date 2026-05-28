---
name: schemas
description: YAML frontmatter schemas for Claude Code agents and commands. Use when creating or validating agent/command files.
---

# Frontmatter Schemas

## Agent Frontmatter

```yaml
---
name: agent-name               # Required: lowercase-with-hyphens
description: |                 # Required: detailed with examples
  Use this agent when [scenario]. Examples:
  (1) "Task description" - launches agent for X
  (2) "Task description" - launches agent for Y
  (3) "Task description" - launches agent for Z
model: sonnet                  # Required: sonnet | opus | haiku
color: purple                  # Optional: purple | cyan | green | orange | blue | red
tools: TodoWrite, Read, Write  # Required: comma-separated, space after comma
skills: skill1, skill2         # Optional: referenced skills
---
```

### Field Reference

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| `name` | Yes | `lowercase-with-hyphens` | Agent identifier |
| `description` | Yes | Multi-line string | 3-5 usage examples |
| `model` | Yes | `sonnet`, `opus`, `haiku` | AI model to use |
| `color` | No | See colors below | Terminal color |
| `tools` | Yes | Tool list | Available tools |
| `skills` | No | Skill list | Referenced skills |

### Color Guidelines

| Color | Agent Type | Examples |
|-------|------------|----------|
| `purple` | Planning | architect, api-architect |
| `green` | Implementation | developer, ui-developer |
| `cyan` | Review | reviewer, designer |
| `orange` | Testing | test-architect, tester |
| `blue` | Utility | cleaner, api-analyst |
| `red` | Critical/Security | (rarely used) |

### Tool Patterns by Agent Type

**Orchestrators (Commands):**
- Must have: `Task`, `TodoWrite`, `Read`, `Bash`
- Often: `AskUserQuestion`, `Glob`, `Grep`
- Never: `Write`, `Edit`

**Planners:**
- Must have: `TodoWrite`, `Read`, `Write` (for docs)
- Often: `Glob`, `Grep`, `Bash`

**Implementers:**
- Must have: `TodoWrite`, `Read`, `Write`, `Edit`
- Often: `Bash`, `Glob`, `Grep`

**Reviewers:**
- Must have: `TodoWrite`, `Read`
- Often: `Glob`, `Grep`, `Bash`
- Never: `Write`, `Edit`

---

## Command Frontmatter

```yaml
---
description: |                 # Required: workflow description
  Full description of what this command does.
  Workflow: PHASE 1 → PHASE 2 → PHASE 3
allowed-tools: Task, Bash      # Required: comma-separated
skills: skill1, skill2         # Optional: referenced skills
---
```

### Field Reference

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| `description` | Yes | Multi-line | Command purpose and workflow |
| `allowed-tools` | Yes | Tool list | Tools command can use |
| `skills` | No | Skill list | Referenced skills |

---

## Validation Checklist

### Agent Frontmatter
- [ ] Opening `---` present
- [ ] `name` is lowercase-with-hyphens
- [ ] `description` includes 3+ examples
- [ ] `model` is valid (sonnet/opus/haiku)
- [ ] `tools` is comma-separated with spaces
- [ ] Closing `---` present
- [ ] No YAML syntax errors

### Command Frontmatter
- [ ] Opening `---` present
- [ ] `description` explains workflow
- [ ] `allowed-tools` includes Task for orchestrators
- [ ] Closing `---` present
- [ ] No YAML syntax errors

---

## Common Errors

### Invalid YAML Syntax
```yaml
# WRONG - missing colon
name agent-name

# CORRECT
name: agent-name
```

### Incorrect Tool Format
```yaml
# WRONG - no spaces after commas
tools: TodoWrite,Read,Write

# CORRECT
tools: TodoWrite, Read, Write
```

### Missing Examples
```yaml
# WRONG - too generic
description: Use this agent for development tasks.

# CORRECT
description: |
  Use this agent when implementing TypeScript features. Examples:
  (1) "Create a user service" - implements service with full CRUD
  (2) "Add validation" - adds Zod schemas to endpoints
  (3) "Fix type errors" - resolves TypeScript compilation issues
```
