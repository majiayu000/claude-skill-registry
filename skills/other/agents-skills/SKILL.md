---
name: agents-skills
description: Reference for creating AI agent skills with SKILL.md structure. Use when building or improving modular skill files for Claude Code or Codex.
---

# Agent Skills - Meta Reference

This skill provides the definitive reference for creating, organizing, and maintaining agent skills. Use this when building new skills or improving existing skill architecture.

## Quick Reference

| Component | Purpose | Required |
|-----------|---------|----------|
| `SKILL.md` | Main reference file with frontmatter | Yes |
| `scripts/` | Executable code (prefer running) | Optional |
| `references/` | Documentation (loaded on-demand) | Recommended |
| `assets/` | Output files (templates, icons) | Optional |
| `data/sources.json` | Curated external links | Recommended |

**Cross-Platform**: Agent Skills are designed to be portable across runtimes (Claude Code, Codex CLI, Gemini CLI, VS Code Copilot).

## Skill Structure

```text
skills/
	└── skill-name/
	    ├── SKILL.md           # Main reference (required)
	    ├── scripts/           # Executable code (Python/Bash) - prefer running; read only to patch/review
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

- `scripts/` - Executable code; prefer running scripts and consuming output (read only when you need to modify/review)
- `references/` - Documentation loaded into context when the agent needs it
- `assets/` - Files used in generated output (not loaded into context)
 
Notes:
- Prefer executing scripts instead of pasting large code into context; read scripts only when you need to modify or review them.

## SKILL.md Template

```markdown
---
name: skill-name
description: One-line description of what this skill provides and when to use it (include trigger keywords here)
---

# Skill Name - Quick Reference

Brief overview of the skill's purpose and value.

## Quick Reference

| Task | Tool/Method | When to Use |
|------|-------------|-------------|
| Task 1 | Tool A | Context for usage |

## Scope (Optional)

Keep this brief; the primary trigger mechanism is the frontmatter `description`.

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
- [../agents-subagents/SKILL.md](../agents-subagents/SKILL.md) - Agent creation
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

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `name` | string | Yes | Kebab-case, must match folder name |
| `description` | string | Yes | Primary trigger — runtime reads this to decide invocation |
| `argument-hint` | string | No | Autocomplete hint shown in `/` menu (e.g. `[issue-number]`) |
| `disable-model-invocation` | bool | No | `true` prevents auto-triggering; user must invoke with `/` |
| `user-invocable` | bool | No | `false` hides from `/` menu; still loads as background context |
| `allowed-tools` | string | No | Comma-separated tool allowlist (e.g. `Read, Grep, Glob`) |
| `context` | string | No | Set to `fork` to run skill body in a subagent |
| `agent` | string | No | Subagent type when `context: fork` (e.g. `Explore`, `Plan`) |
| `model` | string | No | Model override (`opus`, `sonnet`, `haiku`) |
| `hooks` | object | No | Lifecycle hooks scoped to this skill |
| `license` | string | No | License identifier |
| `compatibility` | string | No | Platform/version notes (1-500 chars) |
| `metadata` | object | No | Author, version, mcp-server |

See [references/frontmatter-reference.md](references/frontmatter-reference.md) for full specification, examples, and string substitutions.

**Name rules**:
- Use kebab-case: `ai-llm`, not `AI_LLM_Engineering`
- Match folder name exactly
- Be specific: `software-backend` not `backend`
- No `claude` or `anthropic` in names (reserved words)
- No XML angle brackets (`<` `>`) in any frontmatter value

**Description rules** (PRIMARY TRIGGER):
- The runtime uses descriptions to decide which skills to auto-invoke
- Format: `[What it does]. Use when [trigger phrases].`
- Target ~150 chars when library has 50+ skills (budget: 2% of context window, ~16K chars shared across ALL skill descriptions)
- Include key technologies/concepts as trigger keywords
- Single-line YAML only — no multiline `>-`

**String substitutions** (usable in skill body):
- `$ARGUMENTS` / `$ARGUMENTS[N]` / `$N` — user-provided arguments from `/skill-name arg1 arg2`
- `${CLAUDE_SESSION_ID}` — current session identifier
- `${CLAUDE_SKILL_DIR}` — absolute path to this skill's directory

**Dynamic context injection**: Use `` !`command` `` in the skill body to inject command output at load time.

## Skill Categories

| Category | Prefix | Examples |
|----------|--------|----------|
| AI/ML | `ai-` | `ai-llm`, `ai-ml-data-science` |
| Software | `software-` | `software-backend`, `software-frontend` |
| Operations | `ops-` | `ops-devops-platform` |
| Data | `data-` | `data-lake-platform`, `data-sql-optimization` |
| Quality | `qa-` | `qa-debugging`, `qa-docs-coverage` |
| Developer Tools | `dev-` | `dev-api-design`, `dev-git-commit-message`, `dev-workflow-planning` |
| Product | `product-` | `product-management`, `docs-ai-prd` |
| Document | `document-` | `document-pdf`, `document-xlsx` |
| Testing | `testing-`, `qa-testing-` | `qa-testing-playwright`, `qa-testing-strategy` |
| Marketing | `marketing-` | `marketing-social-media`, `marketing-seo` |
| Agents/Tools | `agents-` | `agents-subagents`, `agents-skills`, `agents-hooks` |

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
[ ] Frontmatter `description` includes trigger keywords
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
- [references/anthropic-skills-guide.md](references/anthropic-skills-guide.md) - Anthropic's official skill-building guide (distilled)
- [references/frontmatter-reference.md](references/frontmatter-reference.md) - Complete frontmatter field specification
- [references/skill-patterns.md](references/skill-patterns.md) - Common skill patterns
- [references/skill-validation.md](references/skill-validation.md) - Validation criteria
- [data/sources.json](data/sources.json) - Official documentation links

**Related Skills**

- [../agents-subagents/SKILL.md](../agents-subagents/SKILL.md) - Agent creation
- [../agents-hooks/SKILL.md](../agents-hooks/SKILL.md) - Hook automation
- [../agents-mcp/SKILL.md](../agents-mcp/SKILL.md) - MCP server integration

## Fact-Checking

- Use web search/web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.
