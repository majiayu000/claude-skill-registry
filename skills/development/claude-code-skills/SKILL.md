---
name: claude-code-skills
description: Comprehensive reference for creating Claude Code skills with progressive disclosure, SKILL.md structure, resources/ organization, frontmatter specification, and best practices for modular capability development.
---

# Claude Code Skills — Meta Reference

This skill provides the definitive reference for creating, organizing, and maintaining Claude Code skills. Use this when building new skills or improving existing skill architecture.

---

## Quick Reference

| Component | Purpose | Required |
|-----------|---------|----------|
| `SKILL.md` | Main reference file with frontmatter | Yes |
| `resources/` | Detailed documentation | Recommended |
| `templates/` | Reusable code templates | Optional |
| `data/sources.json` | Curated external links | Recommended |

## Skill Structure

```text
skills/
└── skill-name/
    ├── SKILL.md           # Main reference (required)
    ├── README.md          # Usage notes (optional)
    ├── resources/         # Detailed docs
    │   ├── patterns.md
    │   └── examples.md
    ├── templates/         # Code templates
    │   └── starter.md
    └── data/
        └── sources.json   # External references
```

---

## SKILL.md Template

```markdown
---
name: skill-name
description: One-line description of what this skill provides and when to use it
---

# Skill Name — Quick Reference

Brief overview of the skill's purpose and value.

---

## Quick Reference

| Task | Tool/Method | When to Use |
|------|-------------|-------------|
| Task 1 | Tool A | Context for usage |

## When to Use This Skill

Claude should invoke this skill when a user requests:

- Use case 1
- Use case 2
- Use case 3

---

## Core Concepts

### Concept 1

Explanation with code example:

\`\`\`language
code example
\`\`\`

### Concept 2

Additional patterns...

---

## Navigation

**Resources**
- [resources/skill-patterns.md](resources/skill-patterns.md) — Common patterns
- [resources/skill-validation.md](resources/skill-validation.md) — Validation criteria

**Related Skills**
- [../claude-code-agents/SKILL.md](../claude-code-agents/SKILL.md) — Agent creation
```

---

## Progressive Disclosure

Skills use **progressive disclosure** to optimize token usage:

| Layer | Content | Token Cost |
|-------|---------|------------|
| **Metadata** | Name + description only | ~100 tokens |
| **SKILL.md** | Quick reference, patterns | <5K tokens |
| **resources/** | Deep dives, full examples | On-demand |

**Pattern**: SKILL.md provides overview → Resources provide depth

### When to Split Content

| Keep in SKILL.md | Move to resources/ |
|------------------|-------------------|
| Decision trees | Full API references |
| Quick commands | Step-by-step tutorials |
| Common patterns | Edge case handling |
| 1-2 code examples | Complete implementations |

---

## Frontmatter Specification

```yaml
---
name: string          # Required: lowercase-kebab-case, matches folder name
description: string   # Required: One line, explains when Claude should use it
---
```

**Name rules**:
- Use kebab-case: `ai-llm`, not `AI_LLM_Engineering`
- Match folder name exactly
- Be specific: `software-backend` not `backend`

**Description rules**:
- Single line, under 200 characters
- Include key technologies/concepts
- End with context of when to use

---

## Skill Categories

| Category | Prefix | Examples |
|----------|--------|----------|
| AI/ML | `ai-` | `ai-llm`, `ai-ml-data-science` |
| Software | `software-` | `software-backend`, `software-frontend` |
| Operations | `ops-` | `ops-devops-platform` |
| Data | `data-` | `data-lake-platform`, `data-sql-optimization` |
| Quality | `quality-` | `quality-debugging`, `qa-docs-coverage` |
| Developer Tools | `dev-`, `git-` | `dev-api-design`, `git-commit-message`, `dev-workflow-planning` |
| Product | `product-` | `product-management`, `docs-ai-prd` |
| Document | `document-` | `document-pdf`, `document-xlsx` |
| Testing | `testing-`, `qa-testing-` | `qa-testing-playwright`, `qa-testing-strategy` |
| Marketing | `marketing-` | `marketing-social-media`, `marketing-seo-technical` |
| Claude Code | `claude-code-` | `claude-code-agents`, `claude-code-skills` |

---

## sources.json Schema

```json
{
  "metadata": {
    "title": "Skill Name - Sources",
    "description": "Brief description",
    "last_updated": "YYYY-MM-DD",
    "skill": "skill-name"
  },
  "category_name": [
    {
      "name": "Resource Name",
      "url": "https://example.com/docs",
      "description": "What this covers",
      "add_as_web_search": true
    }
  ]
}
```

**Categories** should group logically:
- `official_documentation`
- `tutorials`
- `community_resources`
- `tools_and_libraries`

---

## Quality Checklist

```text
SKILL VALIDATION CHECKLIST

Frontmatter:
[ ] name matches folder name (kebab-case)
[ ] description is concise and actionable

Structure:
[ ] SKILL.md under 5K characters (progressive disclosure)
[ ] resources/ for detailed content
[ ] data/sources.json with curated links

Content:
[ ] Quick reference table at top
[ ] "When to Use" section present
[ ] Code examples are copy-paste ready
[ ] Related skills linked at bottom

Quality:
[ ] >40% operational content (code, tables, checklists)
[ ] <50% prose paragraphs
[ ] All URLs are live (no 404s)
[ ] Sources updated within 6 months
```

---

## Multi-Tech vs Single-Tech Skills

### Single-Tech Skill

```text
software-backend/
├── SKILL.md              # Node.js focus
└── resources/
    └── nodejs-patterns.md
```

### Multi-Tech Skill

```text
software-backend/
├── SKILL.md              # Overview + decision tree
├── resources/
│   ├── nodejs-patterns.md
│   ├── go-patterns.md
│   ├── rust-patterns.md
│   └── python-patterns.md
└── templates/
    ├── nodejs/
    ├── go/
    ├── rust/
    └── python/
```

---

## Navigation

**Resources**
- [resources/skill-patterns.md](resources/skill-patterns.md) — Common skill patterns
- [resources/skill-validation.md](resources/skill-validation.md) — Validation criteria
- [data/sources.json](data/sources.json) — Official documentation links

**Related Skills**
- [../claude-code-agents/SKILL.md](../claude-code-agents/SKILL.md) — Agent creation
- [../claude-code-commands/SKILL.md](../claude-code-commands/SKILL.md) — Command creation
- [../claude-code-hooks/SKILL.md](../claude-code-hooks/SKILL.md) — Hook automation
