---
name: memory-system
description: Automatic documentation memory system for AI agents. Ensures context is loaded at session start and documentation is updated after changes.
autoload: true
---

# Memory System Skill

This skill implements an automatic "memory palace" for Claude Code by ensuring:

1. Context is loaded at session start
2. Documentation is checked before relevant tasks
3. Documentation is updated after completing work

## Quick Reference Map

Before starting any task, check these files based on the work type:

| Task Type       | Check First                                                       | Update After              |
| --------------- | ----------------------------------------------------------------- | ------------------------- |
| **Backend API** | `quikadmin/CLAUDE.md`, `docs/reference/api/endpoints.md`          | Same files                |
| **Frontend**    | `quikadmin-web/CLAUDE.md`, `docs/reference/`                      | Same files                |
| **Database**    | `prisma/schema.prisma`, `docs/reference/database/schema.md`       | Same files                |
| **Auth**        | `docs/explanation/security-model.md`, `.claude/skills/auth-flow/` | Same files                |
| **Deployment**  | `docs/how-to/deployment/`                                         | Same files                |
| **New Feature** | `docs/tutorials/`, `docs/how-to/`                                 | Create new docs if needed |
| **Bug Fix**     | `docs/how-to/troubleshooting/`                                    | Update if common issue    |

## Documentation Update Triggers

### ALWAYS Update Documentation When:

1. **API Changes**
   - Adding/modifying/removing endpoints
   - Changing request/response schemas
   - Update: `docs/reference/api/endpoints.md`

2. **Environment Variables**
   - Adding new env vars
   - Update: `docs/reference/configuration/environment.md`, `.env.example`

3. **Database Schema**
   - Running migrations
   - Update: `docs/reference/database/schema.md`

4. **Architecture Changes**
   - Modifying system structure
   - Update: `docs/reference/architecture/system-overview.md`

5. **New Patterns**
   - Establishing new code patterns
   - Update: Relevant `CLAUDE.md` file

## Pre-Task Checklist (Mental Model)

Before starting significant work, mentally run through:

```
□ Have I read the relevant CLAUDE.md?
□ Do I know where to find related documentation?
□ Will this change require doc updates?
□ Is there existing documentation I should follow?
```

## Post-Task Checklist

After completing work:

```
□ Did I change any API endpoints? → Update endpoints.md
□ Did I add environment variables? → Update environment.md
□ Did I change database schema? → Update schema.md
□ Did I establish new patterns? → Update CLAUDE.md
□ Did I fix a common issue? → Consider adding to troubleshooting
```

## Documentation Links Index

### Essential Context (Read These First)

- `CLAUDE.local.md` - Project overview, quick commands
- `quikadmin/CLAUDE.md` - Backend context (optimized)
- `quikadmin-web/CLAUDE.md` - Frontend context

### Reference (Look Up When Needed)

- `docs/reference/api/endpoints.md` - API documentation
- `docs/reference/architecture/system-overview.md` - System design
- `docs/reference/database/schema.md` - Database models
- `docs/reference/configuration/environment.md` - All env vars

### How-To (Problem-Solving)

- `docs/how-to/development/local-setup.md` - Setup guide
- `docs/how-to/development/testing.md` - Testing guide
- `docs/how-to/troubleshooting/` - Common issues

### Understanding (Background)

- `docs/explanation/security-model.md` - Auth architecture
- `docs/explanation/data-flow.md` - Data pipeline
- `docs/explanation/architecture-decisions.md` - Why decisions were made

## Meta-Prompt: Self-Reminder

When working on this project, I should:

1. **Before starting**: Check if there's existing documentation for what I'm about to do
2. **During work**: Note what documentation might need updating
3. **After completing**: Update relevant documentation before marking task done
4. **When unsure**: Check `docs/.meta/inventory.json` for documentation locations

## Invocation

This skill is designed to be automatically loaded. When you need documentation guidance:

```
/memory-system
```

Or ask:

- "What documentation should I check for [task]?"
- "What should I update after [change]?"
