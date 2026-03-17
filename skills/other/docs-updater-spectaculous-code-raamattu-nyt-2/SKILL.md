---
name: docs-updater
description: Expert assistant for keeping documentation synchronized with code changes in the KR92 Bible Voice project. Use when updating API docs, maintaining architecture diagrams, syncing README, updating CLAUDE.MD, or generating documentation from code.
invocable: true
cron: true
---

# Docs Updater

Keep documentation in sync with code. Generates concise, user-friendly summaries.

## Context Files (Read First)

For current state, read from `Docs/context/`:
- `Docs/context/conventions.md` - Documentation standards
- `Docs/context/repo-structure.md` - File organization
- `Docs/ai/CHANGELOG.md` - Recent changes to sync

## Quick Summary Format

Every doc should start with a **TL;DR section** for human readers:

```markdown
# Document Title

> **TL;DR:** [1-2 sentence summary of what this covers]
>
> **Key Points:**
> - [Most important fact 1]
> - [Most important fact 2]
> - [Most important fact 3]
>
> **Quick Links:** [Table](#tables) | [RPC](#rpc-functions) | [Edge Functions](#edge-functions)
```

## Documentation Files

| Doc | Purpose | Update Trigger |
|-----|---------|----------------|
| `CLAUDE.MD` | AI context | Architecture changes |
| `README.md` | Project overview | Feature/setup changes |
| `Docs/TODO.md` | Tracked tasks | New tasks, completed work |
| `Docs/01-PRD.md` | Requirements | Vision changes |
| `Docs/02-DESIGN.md` | Architecture | System design changes |
| `Docs/03-API.md` | API contracts | DB/RPC/Edge changes |
| `Docs/06-AI-ARCHITECTURE.md` | AI system | AI feature changes |
| `Docs/07-ADMIN-GUIDE.md` | Admin panel | Admin changes |
| `Docs/13-SUBSCRIPTION-SYSTEM.md` | Plans/quotas | Subscription changes |

## TODO List Management

The project TODO list is at `Docs/TODO.md`. Use this for tracking:
- Deferred tasks (waiting on dependencies like URLs, assets)
- Future improvements
- Known issues to fix later

### Adding Tasks

```markdown
## Category Name

- [ ] **Task title** — Brief description
- [ ] **Another task** — Description with context
```

### Completing Tasks

Change `- [ ]` to `- [x]` and optionally add completion date:

```markdown
- [x] **Task title** — Completed 2026-02-03
```

## Cron/Scheduled Invocation

This skill supports automated execution for documentation audits.

### Invocation Modes

**Manual:** `claude /docs-updater "check api docs are current"`

**Scheduled (cron):** Set up with CI/CD or cron job:
```bash
# Weekly docs audit (Sundays at midnight)
0 0 * * 0 claude --skill docs-updater --task "audit" --output report.md

# Pre-release docs check
claude --skill docs-updater --task "release-check" --output docs-status.md
```

### Supported Tasks

| Task | Description | Output |
|------|-------------|--------|
| `audit` | Check all docs for staleness | Markdown report |
| `release-check` | Pre-release documentation verification | Pass/fail + issues |
| `sync-schemas` | Update docs from database schema | Updated doc files |
| `generate-api` | Generate API docs from Edge Functions | API documentation |

### Audit Report Format

```markdown
# Documentation Audit Report
Generated: 2026-01-08

## Summary
- Total docs: 15
- Up-to-date: 12
- Needs update: 3
- Critical: 1

## Issues Found

### Critical
- [ ] `03-API.md`: Missing `token_pools` table (added 2026-01-07)

### Warnings
- [ ] `02-DESIGN.md`: Edge Function list outdated
- [ ] `07-ADMIN-GUIDE.md`: Missing Subscriptions page section

## Recommendations
1. Run `sync-schemas` to update API docs
2. Add new admin page to guide
```

## Writing User-Friendly Summaries

### Good Summary (DO)
```markdown
> **TL;DR:** Token-based quota system limits AI usage per subscription plan.
>
> **Key Points:**
> - Users get tokens per 6-hour window (Guest: 50, Pro: 500)
> - Each AI operation costs fixed tokens (Search: 20, Study: 100)
> - Admin can adjust all limits via `/admin/subscriptions`
```

### Bad Summary (DON'T)
```markdown
## Overview
This document describes the token pool subscription system architecture
which was redesigned from a complex per-feature quota model...
```

## Update Workflow

1. **Identify change type** → Which docs affected?
2. **Update TL;DR first** → Most critical information
3. **Update details** → Tables, examples, diagrams
4. **Cross-reference** → Update related docs
5. **Update changelog** → If significant (see criteria below)
6. **Validate** → Run audit task

### Changelog Decision

After updating docs, add a changelog entry if ANY of these apply:
- New feature or capability added
- Database schema changed (tables, columns, migrations)
- API changed (RPC, Edge Function, breaking change)
- Major refactoring (hooks, components extracted/split)
- Bug fix with user-visible impact

Skip changelog for: typo fixes, comment updates, minor doc rewording.

---

## Lean Changelog (Database)

**Primary changelog system** - stored in `admin.changelog_entries` table.

> **IMPORTANT:** The table is in `admin` schema, NOT `public` or `bible_schema`.
> Use MCP tool: `mcp__plugin_supabase_supabase__execute_sql`

### Table Schema

```
admin.changelog_entries
├── id: uuid (auto-generated)
├── date: date (defaults to CURRENT_DATE)
├── description: text (required)
├── category: text (default: 'feature')
├── importance: integer (default: 3)
├── version_id: uuid (optional, links to changelog_versions)
├── created_at: timestamptz (auto)
└── created_by: uuid (optional)
```

### Quick Add (SQL)

```sql
-- Minimal (uses defaults: date=today, category='feature', importance=3)
INSERT INTO admin.changelog_entries (description)
VALUES ('Added verse annotation dialog with tags and notes');

-- With explicit values
INSERT INTO admin.changelog_entries (date, description, category, importance)
VALUES ('2026-01-23', 'Supabase typing infrastructure', 'infrastructure', 2);
```

### Importance Levels

| Level | Label | When to Use |
|-------|-------|-------------|
| **1** | Saavutus | Plan completed, major milestone, bundled tasks |
| **2** | Tärkeä | Significant feature, important fix, refactoring |
| **3** | Normaali | Standard change (default) |
| **4** | Tekninen | Minor technical detail |

### Achievement Rules

**Always Level 1:**
- Plan was made and implemented
- Multiple related tasks bundled as one
- Major refactoring or new system

**Always Level 2:**
- Refactoring (use 1 if major)
- New user-visible feature
- Important bug fix

**Skip changelog:** Typo fixes, comments, failed attempts.

### Categories

`feature` | `fix` | `refactor` | `infrastructure` | `docs` | `chore`

### Admin UI

Manage at `/admin/changelog` → "Muutokset" tab.

> **Full guide:** See [references/ai-changelog-guide.md](references/ai-changelog-guide.md)

---

## Detailed Changelog (Markdown)

For verbose documentation, use `Docs/ai/CHANGELOG.md`.

### When to Add Changelog Entries

Add entries for significant changes:
- New features implemented
- Database schema changes (new tables, columns, migrations)
- API changes (new RPCs, Edge Functions, signature changes)
- Breaking changes
- Major refactoring (hook extractions, component splits)
- Bug fixes with significant impact
- New admin pages or tools

### Entry Format

```markdown
## [TAG] Short Descriptive Title

### Summary
One paragraph describing what changed and why.

**Date:** YYYY-MM-DD

### Problem
Why was this change needed? What was the motivation?

### Solution
What was implemented? High-level approach.

### Files Created
- `path/to/new-file.ts` - Brief description

### Files Modified
- `path/to/existing-file.ts` - What changed

### Impact
- **Files:** N (number of files affected)
- **Breaking:** Yes/No
- **Migration:** migration_filename.sql (if applicable)

---
```

### Tags

Use these tags to categorize changes:

| Tag | Use For |
|-----|---------|
| `[FEATURE]` | New user-facing features |
| `[SCHEMA]` | Database table/column changes |
| `[API]` | RPC or Edge Function changes |
| `[COMPONENT]` | React component refactoring |
| `[BREAKING]` | Breaking changes (often combined with others) |
| `[FIX]` | Bug fixes with significant impact |
| `[REFACTOR]` | Code restructuring without behavior change |
| `[ADMIN]` | Admin panel additions/changes |

### Creating Releases

When releasing a new version:

1. Add release header at top of changelog (after main title):
   ```markdown
   ## v1.X.0 - YYYY-MM-DD

   Brief summary of this release.

   ---
   ```

2. Group unreleased changes under the new version header
3. Mark breaking changes clearly with `[BREAKING]` tag

### Changelog Tasks

| Task | Description | Output |
|------|-------------|--------|
| `log-change` | Add new entry to changelog | Updated CHANGELOG.md |
| `release` | Create new version release header | Version header added |

### Admin Dashboard

The changelog can be viewed and edited at `/admin/changelog`:
- View/edit changelog content
- See GitHub commit status (commits since last update)
- Create new version releases with auto-increment

## References

- **AI changelog guide**: See [references/ai-changelog-guide.md](references/ai-changelog-guide.md)
- **Update examples**: See [references/examples.md](references/examples.md)
- **Doc templates**: See [references/templates.md](references/templates.md)
- **Quality checklist**: See [references/checklist.md](references/checklist.md)
