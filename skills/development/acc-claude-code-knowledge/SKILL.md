---
name: acc-claude-code-knowledge
description: Knowledge base for Claude Code formats and patterns. Use when creating or improving commands, agents, skills, or hooks.
---

# Claude Code Knowledge Base

## Quick Reference for Formats

### Commands

**Path:** `.claude/commands/name.md`
**Invocation:** `/name` or `/name arguments`

```yaml
---
description: Required. What the command does.
allowed-tools: Optional. Restrict tools.
model: Optional. opus/sonnet/haiku
argument-hint: Optional. Hint for arguments.
---

Command instructions.

Use $ARGUMENTS to insert user arguments.
```

**Examples of good commands:**

```yaml
---
description: Creates a git commit with meaningful message based on staged changes
---

1. Run `git diff --staged`
2. Analyze changes
3. Generate commit message:
   - Title up to 50 characters
   - Empty line
   - Detailed description
4. Run `git commit -m "..."`
```

```yaml
---
description: Runs code review for specified file or directory
argument-hint: [path to file or directory]
allowed-tools: Read, Grep, Glob
---

Perform code review for: $ARGUMENTS

Check:
- Code quality
- Potential bugs
- Security
- Performance

Output format:
## Critical Issues
## Warnings
## Recommendations
```

---

### Agents

**Path:** `.claude/agents/name.md`
**Invocation:** Automatically or "Use agent name for..."

```yaml
---
name: agent-name  # required
description: Required. When to use the agent.
tools: Optional. All by default.
model: Optional. opus (default) / haiku / sonnet / inherit
permissionMode: Optional. default / acceptEdits / bypassPermissions / plan
skills: Optional. Auto-load skills.
---

Agent system prompt.
```

**Available tools:**
- Read, Write, Edit — file operations
- Bash — execute commands
- Grep, Glob — search
- WebSearch, WebFetch — web
- Task — create subagents (not recursive)
- MCP tools — if configured

**Examples of good agents:**

```yaml
---
name: researcher
description: Researches codebase and gathers information. Use PROACTIVELY before implementing new features.
tools: Read, Grep, Glob, Bash
model: haiku
---

You are a codebase researcher.

## Task
Quickly find and analyze relevant code.

## Process
1. Glob — find files by pattern
2. Grep — find usages/definitions
3. Read — study key files
4. Summarize findings

## Output
- Found files and their roles
- Code patterns
- Recommendations
```

```yaml
---
name: test-writer
description: Creates tests for code. MUST BE USED after writing new functionality.
tools: Read, Write, Bash
model: opus
---

You are a testing specialist.

## Process
1. Read code that needs testing
2. Determine project's test framework
3. Write tests:
   - Unit tests for functions
   - Edge cases
   - Error handling
4. Run tests
5. Fix if failing
```

---

### Skills

**Path:** `.claude/skills/name/SKILL.md`
**Invocation:** `/name` or automatically

```yaml
---
name: skill-name  # lowercase, hyphens, max 64
description: Required. What and when. Max 1024 chars.
allowed-tools: Optional. Restrict.
disable-model-invocation: true  # only user invokes
user-invocable: false  # only Claude invokes
---

Skill instructions.
```

**Skill folder structure:**
```
skill-name/
├── SKILL.md        # required
├── scripts/        # executable code
├── references/     # additional documentation
└── assets/         # templates, resources
```

**Example skill with resources:**

```yaml
---
name: api-design
description: REST API design patterns. Use when creating or reviewing API endpoints.
---

# API Design Patterns

## Principles
- RESTful naming
- Consistent error format
- Proper status codes

For detailed examples see [references/examples.md](references/examples.md)
For templates see [assets/endpoint-template.ts](assets/endpoint-template.ts)
```

---

### Hooks

**Path:** `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./validate.sh"
          }
        ]
      }
    ],
    "PostToolUse": [...],
    "Notification": [...]
  }
}
```

**Events:**
- PreToolUse — before tool execution
- PostToolUse — after execution
- Notification — on notifications

**Matcher:** tool name or pattern

---

## Patterns

### Parallel Agents
Run multiple agents simultaneously:
```
Run in parallel:
1. Task: researcher — study architecture
2. Task: security-scanner — check security
3. Task: performance-analyzer — check performance

Wait for all and combine results.
```

### Progressive Disclosure
Load information as needed:
```
SKILL.md — brief instructions
references/detailed.md — details when needed
scripts/tool.py — execute without reading into context
```

### Chained Agents
Sequential agent work:
```
1. researcher → studies the task
2. planner → creates plan based on research
3. implementer → implements the plan
4. reviewer → reviews implementation
```

---

## Validation

### Checklist for Commands
- [ ] description is filled
- [ ] Path: .claude/commands/*.md
- [ ] $ARGUMENTS if arguments needed
- [ ] Instructions are clear

### Checklist for Agents
- [ ] name and description are filled
- [ ] tools are minimally necessary
- [ ] model is chosen consciously
- [ ] Path: .claude/agents/*.md

### Checklist for Skills
- [ ] name is lowercase with hyphens
- [ ] description < 1024 characters
- [ ] SKILL.md < 500 lines
- [ ] Path: .claude/skills/name/SKILL.md

### Checklist for Hooks
- [ ] JSON is valid
- [ ] matcher is correct
- [ ] command/script exists
- [ ] Path: .claude/settings.json
