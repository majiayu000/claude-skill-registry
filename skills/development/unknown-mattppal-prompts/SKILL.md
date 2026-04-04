---
name: skill-creator
description: Create new Claude Code skills with proper SKILL.md structure, frontmatter, and best practices. Use when building new skills for this repository.
---

# Skill Creator

Create well-structured Claude Code skills following best practices.

## Skill Structure

Every skill requires this directory structure:

```
.claude/skills/
└── skill-name/
    ├── SKILL.md          # Required - main skill definition
    └── [supporting.md]   # Optional - reference docs, examples
```

## SKILL.md Format

```markdown
---
name: skill-name
description: Brief description of what the skill does and when to use it. Max 1024 chars.
---

# Skill Title

[Main instructions for Claude when this skill is activated]
```

### Frontmatter Requirements

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | Lowercase letters, numbers, hyphens only. Max 64 chars. |
| `description` | Yes | What it does + when to use it. Max 1024 chars. |
| `allowed-tools` | No | Restrict available tools (e.g., `Read, Grep, Glob`) |

## Writing Effective Descriptions

The description determines when Claude activates the skill. Be specific:

**Good descriptions:**
- "Transform changelogs and user showcases into Twitter posts. Use for social media content with casual voice."
- "Design evidence-based powerlifting programs. Use for strength training, workout planning, progressive overload."

**Bad descriptions:**
- "Helps with content" (too vague)
- "For writing" (won't trigger reliably)

Include:
- Specific functionality and capabilities
- Trigger terms users would mention
- When Claude should activate it

## Skill Content Best Practices

### Structure
```markdown
# Skill Title

Brief context paragraph.

## Context
Who/what this skill represents, target audience.

## [Main Sections]
Core instructions, templates, guidelines.

## Examples
Input/output examples when helpful.

## Quality Checklist
Verification criteria for outputs.
```

### Content Guidelines
- Be specific and actionable
- Include templates and examples
- Define clear output formats
- Add quality checklists when appropriate
- Reference supporting files if needed

## Skill Locations

| Location | Scope | Use Case |
|----------|-------|----------|
| `.claude/skills/` | Project | Team workflows, project-specific |
| `~/.claude/skills/` | Global | Personal workflows across projects |

## Creating a New Skill

1. **Identify the need**: What task should Claude handle automatically?
2. **Define triggers**: What words/contexts should activate it?
3. **Create directory**: `mkdir -p .claude/skills/skill-name`
4. **Write SKILL.md**: Include frontmatter + instructions
5. **Add supporting files**: Optional reference docs
6. **Test activation**: Verify Claude activates on relevant requests

## Example: Minimal Skill

```markdown
---
name: code-review
description: Review code for bugs, security issues, and best practices. Use when asked to review or audit code.
---

# Code Review Skill

Review code systematically for:

## Checklist
- [ ] Logic errors and edge cases
- [ ] Security vulnerabilities (injection, auth, etc.)
- [ ] Performance concerns
- [ ] Code style and readability
- [ ] Error handling

## Output Format
Provide findings as:
1. **Critical**: Must fix before merge
2. **Important**: Should fix soon
3. **Suggestions**: Nice to have improvements
```

## Example: Skill with Tool Restrictions

```markdown
---
name: codebase-explorer
description: Explore and explain codebase structure. Use for understanding unfamiliar code. Read-only.
allowed-tools: Read, Grep, Glob
---

# Codebase Explorer

Analyze codebases without making changes...
```

## Common Patterns

### Voice/Persona Skills
Define character, tone, writing style for consistent outputs.

### Task-Specific Skills
Step-by-step instructions for specific workflows.

### Template Skills
Output formats, document structures, boilerplate.

### Analysis Skills
Checklists, criteria, evaluation frameworks.
