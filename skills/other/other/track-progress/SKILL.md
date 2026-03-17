---
name: track-progress
description: Record completed development work to changelog and progress tracking. Updates What's New and tracks initiative progress.
---

# Track Progress Skill

Records completed development work to changelog and progress views.

## Database Support

The script writes to **both** local (Docker) and Neon (production) databases when configured:
- `DATABASE_URL_LOCAL` - Local PostgreSQL (Docker)
- `DATABASE_URL_NEON` - Neon production database

This ensures changelog and progress entries stay in sync across environments.

## When to Use

Invoke with `/track-progress` after completing development work to:
- Add entry to What's New page (changelog) - for **user-facing features only**
- Add entry to Review > Progress (initiatives/action items) - for **all major work**

## Quick Start

### Catchup Mode (Recommended)

Scan git history and create entries for missed commits:

```bash
npx tsx database/track-progress.ts --catchup
```

This will:
1. Find the last changelog date
2. Scan all commits since then
3. Route commits automatically:
   - `feat`, `fix` (user-facing) → **changelog + progress**
   - `feat(admin)`, `test`, `refactor` → **progress only**
   - `style` → **skip**
4. Check for duplicates
5. Ask for confirmation before creating

### Manual Entry

For a single feature/fix:

```bash
npx tsx database/track-progress.ts \
  --title "Feature Name" \
  --desc "Brief description" \
  --items "item1,item2,item3" \
  --category feature
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--catchup` | Scan git history for missed commits | - |
| `--yes` | Auto-confirm in catchup mode | false |
| `--title` | Initiative/release title | required (unless --catchup) |
| `--desc` | Description | same as title |
| `--items` | Comma-separated action items | none |
| `--version` | Release version | today (YYYY-MM-DD) |
| `--category` | feature, fix, improvement | feature |
| `--no-changelog` | Skip changelog entry | false |
| `--no-progress` | Skip progress entry | false |
| `--publish` | Publish changelog immediately | false |

## Routing Logic

The catchup mode automatically routes commits based on type and scope:

| Commit Type | Scope | Changelog | Progress |
|-------------|-------|-----------|----------|
| `feat` | (none) | ✓ | ✓ |
| `fix` | (none) | ✓ | ✓ |
| `feat` | admin, test, infra | | ✓ |
| `fix` | admin, test, webhook | | ✓ |
| `test`, `chore`, `refactor`, `docs` | any | | ✓ |
| `style` | any | | |

## Examples

### Catchup Mode

```bash
# Interactive - shows proposed entries, asks for confirmation
npx tsx database/track-progress.ts --catchup

# Auto-confirm - creates entries without prompting
npx tsx database/track-progress.ts --catchup --yes
```

**Output:**
```
=== Catchup Mode ===

Last changelog entry: 2026-01-17
Found 8 commits since 2026-01-17

--- Proposed Entries ---

2026-01-19: Add subscription plan management
  → changelog + progress [feature]
    ★ [feat] Add dynamic plan management in admin
    ○ [test] Add subscription API tests

2026-01-24: Update landing page header
  → progress only [improvement]
    ○ [chore] Minor header cleanup

--- Summary ---
Changelog entries: 1
Progress entries: 2
Duplicates skipped: 0

Create these entries? (y/n):
```

### Manual Entries

**User-facing feature (goes to both):**
```bash
npx tsx database/track-progress.ts \
  --title "Global View Dashboard" \
  --desc "Cross-project view showing aggregated data" \
  --items "Add types,Create API,Build UI,Add tests"
```

**Admin feature (progress only):**
```bash
npx tsx database/track-progress.ts \
  --title "Admin analytics dashboard" \
  --items "Add charts,Create API,Build page" \
  --no-changelog
```

**Bug fix for users:**
```bash
npx tsx database/track-progress.ts \
  --title "Fix login timeout" \
  --category fix
```

## Where It Appears

| System | Audience | URL |
|--------|----------|-----|
| **Changelog** | App users | `/admin/changelog` → publish → `/changelog`, `/whats-new` |
| **Progress** | Project tracking | `/review?view=progress` (system project) |
| **Milestones** | Visual markers | `/review?view=progress` timeline |

**Notes:**
- Progress entries are **initiatives only** (no individual action items) to keep the view focused
- **Milestones** are auto-created for user-facing features (🚀 for features, 🔧 for fixes)
- Commit details are captured in the initiative description

## Duplicate Detection

The catchup mode checks existing titles in both changelog_items and initiatives tables. Duplicates are shown but skipped:

```
2026-01-17: Changelog & Testing (DUPLICATE - skip)
  → changelog + progress [feature]
```
