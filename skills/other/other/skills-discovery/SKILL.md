---
name: skills-discovery
description: Search for and install Agent Skills that give you specialized capabilities. Before starting work, ask might a skill exist that handles this better than my base knowledge? If the task involves specific technologies, frameworks, file formats, or expert domains. Search proactively, even if the user doesn't mention skills. Skills encode best practices, tools, and techniques you wouldn't otherwise have. Also use when users explicitly ask to find, install, or manage skills.
---

# Skills Discovery

You can extend your capabilities by discovering and installing Agent Skills from the claude-plugins.dev registry. Skills provide specialized knowledge, tools, and techniques for specific technologies, frameworks, and domains.

## When to search for skills

First, check if an installed skill matches the task. If not, search the registry—specialized skills may exist that you haven't installed yet.

Before starting any non-trivial task, ask yourself:

1. Do I have a skill for this? → Use it
2. Might one exist that I don't have? → Search the registry

Search proactively when:

- The task involves specific technologies, frameworks, or file formats
- You're about to do something where best practices matter (testing, deployment, APIs, documentation)
- The domain is specialized (PDF processing, data pipelines, ML workflows)
- You notice yourself about to give generic advice where expert patterns would help

Also search when users explicitly ask to find, install, or manage skills.

## Discovery workflow

Use the registry API for search (the CLI's search command is interactive and not suitable for programmatic use):

```bash
curl "https://claude-plugins.dev/api/skills?q=QUERY&limit=20&offset=0"
```

**Parameters:**

- `q`: Search query (e.g., "frontend", "python", "pdf")
- `limit`: Results per page (max 100)
- `offset`: Pagination offset

**Response structure:**

```json
{
  "skills": [
    {
      "id": "...",
      "name": "skill-name",
      "namespace": "@owner/repo/skill-name",
      "sourceUrl": "https://github.com/...",
      "description": "...",
      "author": "...",
      "installs": 123,
      "stars": 45
    }
  ],
  "total": 100,
  "limit": 10,
  "offset": 0
}
```

## Search strategies

The registry indexes skill names, descriptions, and tags. Construct queries that match how skill authors describe their work.

**Query construction:**

- Use 1-3 specific terms (too broad = noise, too narrow = misses)
- Prefer widely-used terminology over project-specific jargon
- Technology + task often outperforms either alone
- If results are poor, broaden or try synonyms

## Installation

Determine which client the user is working in before installing. If unclear, ask.

**Supported clients:**

- `claude-code` — Claude Code CLI
- `codex` — Codex
- `cursor` — Cursor editor
- `amp` - amp CLI
- `opencode` - OpenCode CLI
- `goose` - Goose CLI
- `github` — VSCode/ github
- `vscode` — VS Code
- `letta` — Letta CLI
- **Client selection:**

```bash
npx skills-installer install @owner/repo/skill-name --client claude-code  # default
npx skills-installer install @owner/repo/skill-name --client cursor
npx skills-installer install @owner/repo/skill-name --client vscode
```

**Scope selection:**

```bash
npx skills-installer install @owner/repo/skill-name  # global (default)
npx skills-installer install @owner/repo/skill-name --local  # project-specific
```

**Combined:**

```bash
npx skills-installer install @owner/repo/skill-name --client cursor --local
```

**Defaults:**

- Client: `claude-code`
- Scope: global

## Management

```bash
# List installed skills
npx skills-installer list

# Uninstall a skill
npx skills-installer uninstall @owner/repo/skill-name
```

## Presenting results to users

When you find relevant skills:

1. Show 3-5 most relevant results maximum
2. Include: name, namespace, description, stars, installs
3. Explain how each skill helps with their _specific_ task
4. Prioritize those with high installs
5. Always ask for confirmation before installing
6. Offer to help directly if no good skill exists or user declines

## Examples

**Example: Proactive suggestion**

User: "I need to create a Django REST API"

```bash
curl "https://claude-plugins.dev/api/skills?q=django&limit=10"
```

Present suggestion:

```
I found some skills that could help:

1. django-rest-framework-expert (@anthropics/claude-code/django-rest-framework-expert)
   Description: Django REST API development with best practices
   ⭐ 234 stars • 1,567 installs

Would you like me to install this, or help you directly without installing a skill?
```

**Example: Explicit search request**

User: "find skills for Python"

```bash
curl "https://claude-plugins.dev/api/skills?q=python&limit=10"
```

Present results and ask which to install.

## API reference

| Endpoint                                 | Description       |
| ---------------------------------------- | ----------------- |
| `GET /api/skills/search?q=QUERY`         | Search skills     |
| `GET /api/skills/@owner/repo/skill-name` | Get skill details |

**Web registry:** https://claude-plugins.dev/skills

## Troubleshooting

**No results found:**

- Try broader search terms
- Browse web registry: https://claude-plugins.dev/skills

**Installation fails:**

- Verify namespace format: `@owner/repo/skill-name`
- Check skill exists in registry
- Verify directory permissions

**Skill not activating:**

- User may need to restart their client
- Verify correct installation directory
- Confirm SKILL.md exists in installation path
