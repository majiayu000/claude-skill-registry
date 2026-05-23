---
name: subagent-builder
description: Create and configure custom subagents in Claude Code. Use when user asks to create a new subagent, needs specialized AI assistance with specific tool restrictions or permissions, implements task-specific workflows with isolated context, sets up domain-specific agents with custom prompts, or creates subagents with hooks or validation rules
---

# Subagent Builder

## Overview

Create custom subagents—specialized AI assistants with isolated context windows, custom system prompts, specific tool access, and independent permissions. Subagents delegate specialized work while keeping verbose output out of your main conversation.

## Quick Start

### Create via /agents Command (Recommended)

1. Run `/agents` in Claude Code
2. Select **Create new agent**
3. Choose scope: **User-level** (all projects) or **Project-level** (current project only)
4. Select **Generate with Claude** and describe the subagent
5. Review/edit the generated configuration
6. Select tools, model, and color
7. Save and use immediately

### Create Manually

Create a `.md` file in the appropriate directory with YAML frontmatter and system prompt:

- **Project subagent**: `.claude/agents/agent-name.md`
- **User subagent**: `~/.claude/agents/agent-name.md`

```markdown
---
name: my-agent
description: What this agent does and when to use it
tools: Read, Grep, Glob
model: sonnet
---

You are a specialized agent for [specific task].

When invoked:
1. First step
2. Second step
3. Third step
```

## Subagent Creation Workflow

### Step 1: Define Purpose

Identify the subagent's specific role. Answer:

- **What task** will this subagent handle?
- **What problem** does it solve?
- **When should** Claude delegate to it?

Write a clear `description` field—this is Claude's primary signal for when to delegate.

**Good description**: "Expert code reviewer. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code."

**Poor description**: "Reviews code" (too vague, no trigger guidance)

### Step 2: Choose Scope

Decide where the subagent should be available:

| Scope | Location | Use Case |
|-------|----------|----------|
| **Project** | `.claude/agents/` | Codebase-specific workflows, team collaboration |
| **User** | `~/.claude/agents/` | Personal agents available in all projects |
| **CLI flag** | `--agents` JSON | Session-only, automation scripts |

### Step 3: Configure Capabilities

Set tool access based on what the subagent needs:

**Read-only analysis** (code reviewers, researchers):
```yaml
tools: Read, Grep, Glob, Bash
```

**Code modification** (debuggers, optimizers):
```yaml
tools: Read, Edit, Bash, Grep, Glob
```

**Restricted access** (database readers with validation):
```yaml
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
```

**Full access** (rare, use cautiously):
```yaml
# Inherits all tools from main conversation
# No tools field needed
```

### Step 4: Write System Prompt

The markdown body becomes the subagent's system prompt. Keep it:

- **Task-focused**: Specific to the subagent's role
- **Actionable**: Clear steps and checklists
- **Concise**: Under 5k words (progressive disclosure for complex agents)

Structure:
1. Role definition
2. When invoked behavior
3. Process/workflow
4. Output format

**Example structure**:
```markdown
You are a ROLE specializing in DOMAIN.

When invoked:
1. First action
2. Second action
3. Third action

Process:
- Step 1 with details
- Step 2 with details

For each TASK:
- OUTPUT 1
- OUTPUT 2

Focus on OUTCOME.
```

### Step 5: Choose Model

Select the appropriate model for the task:

| Model | Best For |
|-------|----------|
| `haiku` | Fast, routine tasks (reading files, simple analysis) |
| `sonnet` | Balanced capability and speed (most subagents) |
| `opus` | Complex reasoning, deep analysis |
| `inherit` | Consistency with main conversation |

### Step 6: Set Permissions (Optional)

Use `permissionMode` to control permission handling:

```yaml
permissionMode: acceptEdits  # Auto-accept file edits
```

For dynamic control, use hooks—see [configuration.md](references/configuration.md) for details.

## Common Patterns

### Pattern 1: Read-Only Analyst

Subagents that analyze without modifying. Use for code reviews, research, documentation generation.

```yaml
tools: Read, Grep, Glob, Bash
```

**Examples**: Code reviewer, documentation analyzer, security auditor

### Pattern 2: Fixer/Modifier

Subagents that analyze and modify code. Use for debugging, optimization, refactoring.

```yaml
tools: Read, Edit, Bash, Grep, Glob
```

**Examples**: Debugger, optimizer, refactoring specialist

### Pattern 3: Domain Specialist

Subagents for specialized domains with explicit model selection for capable analysis.

```yaml
model: sonnet
tools: Bash, Read, Write
```

**Examples**: Data scientist, database analyst, API integrator

### Pattern 4: Restricted Access

Subagents with tool access but validation via hooks.

```yaml
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
```

**Examples**: Database reader (read-only queries), API caller (rate-limited)

### Pattern 5: Isolated Execution

Subagents for verbose operations to keep output out of main context.

```yaml
model: sonnet
tools: Bash, Read
```

**Examples**: Test runner, log analyzer, documentation generator

## Best Practices

### Write Effective Descriptions

The `description` field is critical—Claude uses it to decide when to delegate. Include:

- **What** the subagent does
- **When** to use it (specific triggers)
- **Use proactively** to encourage automatic delegation

**Example**:
```yaml
description: Security auditor for finding vulnerabilities. Use proactively after code changes or when working with authentication, authorization, or user input handling.
```

### Limit Tool Access

Grant only necessary permissions. This:

- Improves security
- Keeps subagents focused
- Prevents accidental modifications

Default to read-only tools unless modification is essential.

### Design Focused Subagents

Each subagent should excel at **one** specific task. Multiple focused subagents are better than one general-purpose subagent.

**Good**: `code-reviewer`, `security-auditor`, `performance-profiler`
**Avoid**: `do-everything-agent`

### Use Proactive Delegation

Include "use proactively" in descriptions to encourage automatic delegation:

```yaml
description: Test runner that executes test suites and reports failures. Use proactively after code changes.
```

### Check Into Version Control

For project subagents (`.claude/agents/`), commit them to version control so:

- Team members can use them
- Changes are tracked
- Knowledge is shared

## Progressive Disclosure

For complex subagents with extensive documentation:

1. **Keep SKILL.md lean** (<5k words, <500 lines)
2. **Move details to references** - Create separate files for:
   - Advanced configurations
   - Domain-specific patterns
   - Extensive examples
3. **Link from main prompt** - Reference when relevant

This skill demonstrates this pattern:
- **SKILL.md**: Core workflow and common patterns
- **references/examples.md**: Concrete subagent examples
- **references/configuration.md**: Complete configuration reference

## Resources

### references/examples.md

Concrete examples of subagents for common patterns:

- Code reviewer (read-only)
- Debugger (read/write)
- Data scientist (domain-specific)
- Database reader (restricted access)
- Test runner (isolated execution)
- Documentation generator
- Performance optimizer

Use these as starting points or inspiration.

### references/configuration.md

Complete reference for subagent configuration:

- All frontmatter fields and their purposes
- Tool access control patterns
- Permission modes and when to use each
- Model selection guidelines
- Skills in subagents
- Hooks configuration (PreToolUse, PostToolUse, Stop, SubagentStart, SubagentStop)
- Subagent scope and priority rules
- Disabling specific subagents

### assets/templates/

Template files for common subagent patterns:

- `readonly-analyst.template.md` - For read-only analysis tasks
- `readwrite-fixers.template.md` - For agents that modify code
- `domain-specialist.template.md` - For domain-specific expertise

Copy and customize these templates to quickly create new subagents.

## Next Steps

After creating a subagent:

1. **Test it**: "Use the [agent-name] agent to [task]"
2. **Iterate**: Refine the prompt and configuration based on usage
3. **Share**: Commit project subagents to version control
4. **Chain**: Use multiple subagents in sequence for complex workflows

For more subagent usage patterns, see the main Claude Code documentation on working with subagents.
