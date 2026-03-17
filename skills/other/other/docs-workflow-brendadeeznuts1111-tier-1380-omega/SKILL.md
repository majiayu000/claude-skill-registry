---
name: docs-workflow
description: |
  Four slash commands for documentation lifecycle: /docs, /docs-init, /docs-update, /docs-claude. Create, maintain, and audit CLAUDE.md, README.md, and docs/ structure with smart templates.

  Use when: starting new projects, maintaining documentation, auditing docs for staleness, or ensuring CLAUDE.md matches project state.
user-invocable: true
---

# docs-workflow

**Last Updated**: 2026-01-11
**Purpose**: Manage project documentation throughout its lifecycle

---

## Overview

This skill helps you:
- **Initialize** documentation for new projects (CLAUDE.md, README.md, docs/)
- **Maintain** CLAUDE.md to match actual project state
- **Audit** all docs for staleness, broken links, outdated versions

## Commands

| Command | Purpose |
|---------|---------|
| `/docs` | Main entry - shows available subcommands |
| `/docs-init` | Create CLAUDE.md + README.md + docs/ structure |
| `/docs-update` | Audit and maintain all documentation |
| `/docs-claude` | Smart CLAUDE.md maintenance only |

## Quick Start

### New Project

```bash
# In a new project directory
/docs-init
```

This will:
1. Detect project type (Cloudflare Workers, Next.js, generic)
2. Create CLAUDE.md from appropriate template
3. Create README.md if missing
4. Optionally scaffold docs/ directory

### Existing Project

```bash
# Audit all documentation
/docs-update

# Or just maintain CLAUDE.md
/docs-claude
```

---

## What Gets Created

### CLAUDE.md

Project-specific context for Claude Code, including:
- Project overview and tech stack
- Development setup commands
- Architecture overview
- Key file locations
- Common tasks and workflows

**Templates available:**
- `CLAUDE-cloudflare.md` - Cloudflare Workers + Vite + D1 projects
- `CLAUDE-nextjs.md` - Next.js App Router projects
- `CLAUDE-generic.md` - Any other project type

### README.md

Standard README with:
- Project name and description
- Installation/setup instructions
- Usage examples
- Configuration
- Contributing guidelines

### docs/ Directory (Optional)

Scaffolded documentation structure:
- `docs/ARCHITECTURE.md` - System architecture
- `docs/API.md` - API documentation
- `docs/DATABASE.md` - Database schema

---

## Smart Maintenance

### /docs-claude Features

The CLAUDE.md maintenance command checks:

1. **Tech Stack Match**
   - Does CLAUDE.md list technologies that match package.json?
   - Are versions mentioned still accurate?

2. **Referenced Files**
   - Do paths mentioned in CLAUDE.md still exist?
   - Are there new important files not mentioned?

3. **Section Freshness**
   - Is "Last Updated" date recent?
   - Are there outdated patterns or commands?

4. **Critical Rules**
   - For detected tech stack, are important rules present?
   - E.g., Cloudflare project should mention wrangler.jsonc patterns

### /docs-update Features

Full documentation audit including:

1. **Date Freshness**
   - Compare doc dates against git history
   - Flag docs not updated in >30 days

2. **Version References**
   - Check npm package versions mentioned
   - Suggest updates for outdated versions

3. **Broken Links**
   - Verify internal markdown links
   - Check that referenced files exist

4. **Redundancy**
   - Identify duplicate content across files
   - Suggest consolidation

5. **Orphaned Files**
   - Find docs not referenced anywhere
   - Suggest archiving or deletion

---

## Project Type Detection

The skill auto-detects project type by looking for:

| Indicator | Project Type |
|-----------|-------------|
| `wrangler.jsonc` or `wrangler.toml` | Cloudflare Workers |
| `next.config.js` or `next.config.ts` | Next.js |
| Neither | Generic |

Additional indicators influence template content:
- `package.json` dependencies (React, Vite, etc.)
- Database config files (drizzle.config.ts, prisma/schema.prisma)
- Auth config (clerk, better-auth)

---

## Integration with Other Skills

- **project-workflow**: Use `/docs-init` after `/plan-project` to add documentation
- **project-planning**: Generated `IMPLEMENTATION_PHASES.md` referenced in CLAUDE.md
- **cloudflare-worker-base**: Cloudflare template includes Workers-specific patterns

---

## Best Practices

### When to Run Each Command

| Situation | Command |
|-----------|---------|
| New project | `/docs-init` |
| After major changes | `/docs-claude` |
| Before release | `/docs-update` |
| Monthly maintenance | `/docs-update` |

### CLAUDE.md Guidelines

1. **Keep it current** - Update "Last Updated" when making changes
2. **Focus on project-specific** - Don't duplicate generic tech docs
3. **Include common tasks** - Commands you run frequently
4. **Reference, don't duplicate** - Link to docs/ for detailed content

---

## Templates

Templates are located in `templates/` within this skill:

```
templates/
├── CLAUDE-cloudflare.md    # Cloudflare Workers projects
├── CLAUDE-nextjs.md        # Next.js projects
├── CLAUDE-generic.md       # Generic projects
└── README-template.md      # Standard README
```

Templates use placeholders:
- `{{PROJECT_NAME}}` - Detected from package.json or folder name
- `{{DATE}}` - Current date
- `{{TECH_STACK}}` - Detected technologies
