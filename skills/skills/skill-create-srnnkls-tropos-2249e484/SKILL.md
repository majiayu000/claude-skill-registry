---
name: skill-create
description: Create new Claude Code skills following project patterns and best practices. Use when building new skills, extracting reusable capabilities, or converting commands to skills.
---

# Skill Creation

Create well-structured skills using progressive disclosure and project conventions.

> **Reference:** [best-practices.md](best-practices.md) for comprehensive guidance, [reference.md](reference.md) for project patterns and frontmatter specs.

---

## Workflow

### Step 1: Understand Use Cases

Gather concrete examples of how the skill will be used:

- What tasks will it handle?
- What would users say to trigger it?
- What variations exist?

Skip this step only when usage patterns are already clearly understood.

### Step 2: Plan Contents

Analyze each use case to identify reusable resources:

| Resource Type | When to Use | Example |
|---------------|-------------|---------|
| `scripts/` | Same code rewritten repeatedly | `rotate_pdf.py` |
| `references/` | Domain knowledge Claude needs | `schema.md`, `api.md` |
| `assets/` | Files used in output | `template.html`, `logo.png` |
| `templates/` | Document structure patterns | `report.md` |

### Step 3: Choose Frontmatter

**Required fields:**

```yaml
name: skill-name          # Lowercase, hyphens, max 64 chars
description: |            # Max 1024 chars
  [What it does]. Use when [context].
```

**Optional fields:**

| Field | Purpose | Example |
|-------|---------|---------|
| `context` | Run in forked sub-agent | `context: fork` |
| `agent` | Specify agent type | `agent: haiku` |
| `user-invocable` | Hide from slash menu | `user-invocable: false` |
| `allowed-tools` | Restrict available tools | See reference.md |
| `hooks` | Lifecycle hooks (PreToolUse, PostToolUse, Stop) | See reference.md |

**Naming pattern:** `<namespace>[-<subnamespace>]-<action>`
- `code-debug`, `spec-create`, `git-worktree-use`

**Description format:** Third person, what + when.
- "Generate GitHub issue drafts from spec directories. Use when converting specs to GitHub issues."

### Step 4: Create Structure

```bash
mkdir -p .claude/skills/{skill-name}
```

**Standard structure:**

```
.claude/skills/{skill-name}/
├── SKILL.md              # Main instructions (<500 lines)
├── templates/            # Document templates (.md)
├── scripts/              # Executable code (.sh, .py)
└── references/           # Extended documentation
```

### Step 5: Implement & Test

**Write SKILL.md:**
- Keep under 200 lines (500 max)
- Progressive disclosure: SKILL.md → references/
- Include concrete examples, no emojis
- Reference authoritative docs (don't duplicate)

**Test with real tasks:**
1. Does the description trigger correctly?
2. Can Claude find bundled resources?
3. Does the workflow complete successfully?

---

## Degrees of Freedom

Match specificity to task fragility:

**High freedom** - Multiple approaches valid, context-dependent:
```markdown
## Code review
1. Analyze structure and organization
2. Check for bugs and edge cases
3. Suggest improvements
```

**Low freedom** - Operations fragile, consistency critical:
```markdown
## Database migration
Run exactly: `python scripts/migrate.py --verify --backup`
Do not modify flags.
```

---

## Skill Types

| Type | Characteristics | Examples |
|------|-----------------|----------|
| **Operational** | Multi-step workflow, state changes, document templates | `spec-create`, `spec-archive` |
| **Generation** | Transform input → structured output, format templates | `spec-issues-create` |
| **Guidance** | Imperative instructions, code patterns | `code-implement`, `code-debug` |

---

## Success Criteria

- Name follows `<namespace>[-<subnamespace>]-<action>`
- Description is third person with what + when
- SKILL.md under 200 lines (500 max)
- Workflow steps numbered and actionable
- Templates extracted to separate files
- References point to authoritative sources
- No emojis (text markers only)

---

## Reference

- [best-practices.md](best-practices.md) - Core principles, patterns, checklist
- [reference.md](reference.md) - Project patterns, frontmatter specs, anti-patterns
