---
name: skill-builder
description: Create, structure, and optimize skills for the FTC Metrics project. Use when creating a new skill, improving an existing skill, or needing guidance on skill design patterns, triggers, frontmatter, and progressive disclosure.
license: MIT
compatibility: [Claude Code]
metadata:
  author: ftcmetrics
  version: "1.0.0"
  category: tools
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(mkdir:*)
---

# FTC Metrics Skill Builder

This skill teaches you how to create high-quality skills for the FTC Metrics project. Skills are knowledge packs that help AI coding agents with specific technologies, patterns, or workflows.

## Quick Reference

| Element | Purpose | Required |
|---------|---------|----------|
| `name` | Unique identifier (kebab-case) | Yes |
| `description` | WHAT it does + WHEN to use it | Yes |
| `license` | Usually MIT | Recommended |
| `compatibility` | Which agents support it | Recommended |
| `metadata` | Author, version, category | Recommended |
| `SKILL.md` | Main instructions (<500 lines) | Yes |

## Skill Categories for FTC Metrics

| Category | Description | Examples |
|----------|-------------|----------|
| `database` | Database and ORM | Prisma, PostgreSQL patterns |
| `api` | Backend API patterns | Hono, authentication, FTC Events API |
| `frontend` | UI components and pages | Next.js, React, Tailwind |
| `analytics` | Stats and calculations | EPA, OPR, match predictions |
| `realtime` | WebSocket and live updates | Soketi, Pusher patterns |
| `tools` | Development utilities | Testing, deployment, skill creation |

## Skill Location

All skills are stored in:
```
.claude/skills/<skill-name>/
├── SKILL.md               # Main instructions (required)
├── API_REFERENCE.md       # Detailed API docs (optional)
├── TROUBLESHOOTING.md     # Common issues (optional)
└── EXAMPLES.md            # Extended examples (optional)
```

## Writing the Description (CRITICAL)

The `description` field determines when your skill activates. It must answer:
1. **WHAT** does this skill do?
2. **WHEN** should Claude use it?

### Good Description

```yaml
description: >-
  Configure and use Prisma 7 ORM with PostgreSQL driver adapters.
  Use when setting up database schemas, migrations, or troubleshooting
  Prisma configuration in the FTC Metrics project.
```

### Bad Description

```yaml
description: Helps with database stuff.
```

### FTC Metrics Trigger Words

Include these in descriptions where relevant:

**Stack:**
- "Prisma", "PostgreSQL", "database", "schema", "migration"
- "Next.js", "React", "Tailwind", "TypeScript"
- "Hono", "API", "endpoint", "middleware"
- "NextAuth", "OAuth", "authentication"
- "Soketi", "WebSocket", "real-time", "Pusher"

**Domain:**
- "FTC", "FIRST Tech Challenge", "scouting", "match data"
- "EPA", "OPR", "analytics", "predictions"
- "teams", "events", "matches", "scores"
- "DECODE", "Into The Deep", "game scoring"

## Frontmatter Reference

```yaml
---
name: your-skill-name              # Required: kebab-case, max 64 chars
description: >-                    # Required: max 1024 chars
  What this skill does.
  Use when [trigger 1], [trigger 2], or [trigger 3].
license: MIT                       # Recommended
compatibility: [Claude Code]       # Array format
metadata:
  author: ftcmetrics
  version: "1.0.0"
  category: database               # See categories above
allowed-tools: Read, Write, Edit   # Optional: restrict tool access
---
```

## Content Structure

### Quick Start Section
Essential setup that 80% of users need.

### Key Concepts
Table of important terms and their meanings.

### Common Patterns
Frequently used code patterns with examples.

### Anti-Patterns
What NOT to do, marked with ❌

### Examples
Good AND Bad examples side by side.

### Reference Documentation
Links to detailed files for on-demand loading.

## Complete SKILL.md Template

```markdown
---
name: your-skill-name
description: >-
  [What this skill does - specific capabilities].
  Use when [trigger 1], [trigger 2], or [trigger 3].
license: MIT
compatibility: [Claude Code]
metadata:
  author: ftcmetrics
  version: "1.0.0"
  category: database | api | frontend | analytics | realtime | tools
---

# [Skill Name]

Brief introduction - what this helps accomplish.

## Quick Start

### Installation/Setup
[How to add dependencies or configure]

### Basic Usage
\`\`\`typescript
// Minimal working example
\`\`\`

## Key Concepts

| Term | Description |
|------|-------------|
| **Term 1** | What it means |
| **Term 2** | What it means |

## Common Patterns

### Pattern 1: [Descriptive Name]
\`\`\`typescript
// Code example
\`\`\`

## Anti-Patterns

- ❌ [Thing to avoid] - [Why it's bad]
- ❌ [Thing to avoid] - [Why it's bad]

## Examples

### Good: [Descriptive title]
\`\`\`typescript
// Working example with comments
\`\`\`

### Bad: [Descriptive title]
\`\`\`typescript
// ❌ What not to do
\`\`\`

## References

- [Official Documentation](https://example.com/docs)
```

## Skill Creation Checklist

Before finalizing your skill:

- [ ] `name` in frontmatter is kebab-case
- [ ] `description` includes WHAT and WHEN triggers
- [ ] `description` includes relevant keywords
- [ ] Under ~500 lines
- [ ] Includes Quick Start section
- [ ] Shows Good AND Bad examples
- [ ] Anti-patterns marked with ❌
- [ ] Code examples are tested

## Creating a New Skill

1. Create directory:
   ```bash
   mkdir -p .claude/skills/your-skill-name
   ```

2. Create SKILL.md with frontmatter and content

3. Test by asking Claude about the skill's topic

4. Claude should use the skill automatically based on triggers
