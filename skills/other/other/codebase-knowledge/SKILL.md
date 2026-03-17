---
name: codebase-knowledge
description: Provides cached knowledge about project domains. Maps files by domain, tracks connections between components, records recent commits. Use before implementing to understand affected areas.
allowed-tools: Read, Glob, Grep
---

# Codebase Knowledge - Domain Mapping System

## Purpose

This skill provides cached knowledge about project domains:

- **Maps** files by domain/feature area
- **Tracks** connections between components
- **Records** recent commits per area
- **Caches** architecture decisions

---

## How It Works

### Domain Files Location

```
.claude/skills/codebase-knowledge/domains/
├── [domain-name].md    # One file per domain
└── ...
```

### Domain File Template

```markdown
# [Domain Name]

## Last Update

- **Date:** YYYY-MM-DD
- **Commit:** [hash]

## Files

### Frontend

- `app/[path]/page.tsx` - Description
- `components/[path]/*.tsx` - Description

### Backend

- `server/trpc/routers/[name].router.ts` - Router
- `server/db/models/[name].model.ts` - Model

### Types/Schemas

- `lib/validators/[name].ts` - Zod schemas

## Connections

- **[other-domain]:** How they connect

## Recent Commits

| Hash   | Date       | Description       |
| ------ | ---------- | ----------------- |
| abc123 | YYYY-MM-DD | feat: description |

## Attention Points

- [Special rules, gotchas, etc]
```

---

## Workflow

### BEFORE Implementation

1. **Identify** which domain is affected
2. **Read** `domains/[domain].md` file
3. **Check** affected files listed
4. **Verify** recent commits for context
5. **Note** connections with other domains

### AFTER Implementation

1. **Update** the domain file
2. **Add** new commit to "Recent Commits"
3. **Add/remove** files if changed
4. **Update** connections if affected

---

## Commands

### Check Recent Commits by Domain

```bash
git log --oneline -10 -- [list of domain files]
```

### Check Uncommitted Changes

```bash
git diff --name-status main..HEAD
```

### Create New Domain File

```bash
# Copy template
cp .claude/skills/codebase-knowledge/TEMPLATE.md .claude/skills/codebase-knowledge/domains/[name].md
```

---

## Rules

### MANDATORY

1. **READ domain before implementing** - Always check cached knowledge
2. **UPDATE after implementing** - Keep cache current
3. **VERIFY connections** - Changes may affect other domains
4. **RECORD commits** - Maintain history

### FORBIDDEN

1. **Ignore cached knowledge** - It exists to accelerate development
2. **Leave outdated** - Old docs are worse than none
3. **Modify without recording** - Every commit should be noted

---

## Integration with Agents

The **analyzer** agent MUST use this skill:

1. Check which domain is affected
2. Read domain file for context
3. Report affected files and connections
4. Update domain after implementation

---

## Version

- **v2.0.0** - Generic template (no project-specific domains)
