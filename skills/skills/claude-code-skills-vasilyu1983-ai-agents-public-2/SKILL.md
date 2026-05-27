---
name: claude-code-skills
description: Comprehensive reference for creating Claude Code skills with progressive disclosure, SKILL.md structure, references/ organization, frontmatter specification, and best practices for modular capability development.
---

# Claude Code Skills - Meta Reference

This skill provides the definitive reference for creating, organizing, and maintaining Claude Code skills. Use this when building new skills or improving existing skill architecture.

## Quick Reference

| Component | Purpose | Required |
|-----------|---------|----------|
| `SKILL.md` | Main reference file with frontmatter | Yes |
| `scripts/` | Executable code (runs, not loaded) | Optional |
| `references/` | Documentation (loaded on-demand) | Recommended |
| `assets/` | Output files (templates, icons) | Optional |
| `data/sources.json` | Curated external links | Recommended |

**Cross-Platform**: Agent Skills standard adopted by Claude Code, Codex CLI, Gemini CLI, and VS Code Copilot. Skills are portable across platforms.

## Skill Structure

```text
skills/
└── skill-name/
    ├── SKILL.md           # Main reference (required)
    ├── scripts/           # Executable code (Python/Bash) - runs, not loaded
    │   └── validate.py
    ├── references/        # Documentation loaded into context on-demand
    │   ├── patterns.md
    │   └── examples.md
    ├── assets/            # Files for OUTPUT (templates, icons, fonts)
    │   └── template.html
    └── data/
        └── sources.json   # External references
```

**Directory purposes**:

- `scripts/` - Executable code; output consumed, code never loads into context
- `references/` - Documentation loaded into context when the agent needs it
- `assets/` - Files used in generated output (not loaded into context)

## SKILL.md Template

```markdown
---
name: skill-name
description: One-line description of what this skill provides and when to use it
---

# Skill Name - Quick Reference

Brief overview of the skill's purpose and value.

## Quick Reference

| Task | Tool/Method | When to Use |
|------|-------------|-------------|
| Task 1 | Tool A | Context for usage |

## When to Use This Skill

The assistant should invoke this skill when a user requests:

- Use case 1
- Use case 2
- Use case 3

## Core Concepts

### Concept 1

Explanation with code example:

\`\`\`language
code example
\`\`\`

### Concept 2

Additional patterns...

## Navigation

**Resources**
- [references/skill-patterns.md](references/skill-patterns.md) - Common patterns
- [references/skill-validation.md](references/skill-validation.md) - Validation criteria

**Related Skills**
- [../claude-code-agents/SKILL.md](../claude-code-agents/SKILL.md) - Agent creation
```

## Progressive Disclosure

Skills use **progressive disclosure** to optimize token usage:

| Layer | Content | Token Cost |
|-------|---------|------------|
| **Discovery** | Name + description only | ~50 tokens |
| **Activation** | Full SKILL.md body | 2K-5K tokens |
| **Execution** | scripts/, references/, assets/ | On-demand |

**Pattern**: SKILL.md provides overview -> Resources load only when needed

**Limits**: Keep SKILL.md under **500 lines** (<5K tokens)

### When to Split Content

| Keep in SKILL.md | Move to references/ |
|------------------|-------------------|
| Decision trees | Full API references |
| Quick commands | Step-by-step tutorials |
| Common patterns | Edge case handling |
| 1-2 code examples | Complete implementations |

## Frontmatter Specification

```yaml
---
name: string                        # Required: lowercase-kebab-case, matches folder name
description: string                 # Required: PRIMARY trigger mechanism (50-300 chars)
disable-model-invocation: boolean   # Optional: Only user can invoke (for /deploy, /commit)
user-invocable: boolean             # Optional: false = background knowledge only
---
```

**Name rules**:
- Use kebab-case: `ai-llm`, not `AI_LLM_Engineering`
- Match folder name exactly
- Be specific: `software-backend` not `backend`

**Description rules** (PRIMARY TRIGGER):
- Description is the primary triggering mechanism - the runtime uses it to decide when to invoke
- Include "when to use" context HERE, not in the body
- Single line, 50-300 characters
- Include key technologies/concepts as trigger keywords

**Optional frontmatter**:
- `disable-model-invocation: true` - Only user can invoke (for workflows with side effects: `/commit`, `/deploy`, `/send-slack`)
- `user-invocable: false` - Not user-invocable (background knowledge only; runtime-dependent)

## Skill Categories

| Category | Prefix | Examples |
|----------|--------|----------|
| AI/ML | `ai-` | `ai-llm`, `ai-ml-data-science` |
| Software | `software-` | `software-backend`, `software-frontend` |
| Operations | `ops-` | `ops-devops-platform` |
| Data | `data-` | `data-lake-platform`, `data-sql-optimization` |
| Quality | `qa-` | `qa-debugging`, `qa-docs-coverage` |
| Developer Tools | `dev-`, `git-` | `dev-api-design`, `git-commit-message`, `dev-workflow-planning` |
| Product | `product-` | `product-management`, `docs-ai-prd` |
| Document | `document-` | `document-pdf`, `document-xlsx` |
| Testing | `testing-`, `qa-testing-` | `qa-testing-playwright`, `qa-testing-strategy` |
| Marketing | `marketing-` | `marketing-social-media`, `marketing-seo-complete` |
| Claude Code | `claude-code-` | `claude-code-agents`, `claude-code-skills` |

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

## Quality Checklist

```text
SKILL VALIDATION CHECKLIST

Frontmatter:
[ ] name matches folder name (kebab-case)
[ ] description is concise and actionable

Structure:
[ ] SKILL.md under 500 lines (split into references/ if needed)
[ ] references/ for detailed content
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

## Multi-Tech vs Single-Tech Skills

### Single-Tech Skill

```text
software-backend/
├── SKILL.md              # Node.js focus
└── references/
    └── nodejs-patterns.md
```

### Multi-Tech Skill

```text
software-backend/
├── SKILL.md              # Overview + decision tree
├── references/
│   ├── nodejs-patterns.md
│   ├── go-patterns.md
│   ├── rust-patterns.md
│   └── python-patterns.md
└── assets/
    ├── nodejs/
    ├── go/
    ├── rust/
    └── python/
```

## Navigation

**Resources**
- [references/skill-patterns.md](references/skill-patterns.md) - Common skill patterns
- [references/skill-validation.md](references/skill-validation.md) - Validation criteria
- [data/sources.json](data/sources.json) - Official documentation links

**Related Skills**
- [../claude-code-agents/SKILL.md](../claude-code-agents/SKILL.md) - Agent creation
- [../claude-code-commands/SKILL.md](../claude-code-commands/SKILL.md) - Command creation
- [../claude-code-hooks/SKILL.md](../claude-code-hooks/SKILL.md) - Hook automation
