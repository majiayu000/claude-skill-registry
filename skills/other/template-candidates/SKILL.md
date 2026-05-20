---
name: template-candidates
context: fork
model: opus
description: Analyse files for ArchitectKB template repository suitability
---

# Skill: Template Candidates

**Command:** `/template-candidates [--category <type>]`
**Model:** 🟡 Sonnet
**Agent:** None (direct execution)

## Purpose

Analyse files in this vault and identify candidates suitable for the ArchitectKB template repository. Performs detailed content analysis to ensure files are generic and reusable.

## When to Use

- After `/template-changelog` identifies new/modified files
- Before running `/template-sync`
- When deciding what features to contribute upstream

## Categories

Filter by category with `--category`:

| Category | Directory | Description |
|----------|-----------|-------------|
| `scripts` | `.claude/scripts/` | Python/Shell automation |
| `skills` | `.claude/skills/` | Skill definitions |
| `schemas` | `.claude/schemas/` | JSON validation schemas |
| `hooks` | `.claude/hooks/` | Pre/post execution hooks |
| `rules` | `.claude/rules/` | Reference documentation |
| `templates` | `Templates/` | Note templates |
| `all` | All above | Full analysis |

## Implementation

### Step 1: Scan for New/Modified Files

Compare with template repo:

```python
VAULT = Path("~/Documents/GitHub/BA-DavidOliver-ObsidianVault").expanduser()
TEMPLATE = Path("~/Documents/GitHub/ArchitectKB").expanduser()

DIRS_TO_COMPARE = [
    ".claude/scripts",
    ".claude/skills",
    ".claude/schemas",
    ".claude/hooks",
    ".claude/rules",
    "Templates",
]
```

### Step 2: Content Analysis

For each candidate file, check for:

#### Disqualifying Content (AUTO-EXCLUDE)

| Pattern | Reason |
|---------|--------|
| `Acme Corp`, `BA-`, `britishairways` | Company-specific |
| `@ba.com`, `atlassian.net/wiki/spaces/BA` | Internal URLs |
| API keys, tokens, passwords | Security risk |
| `/Users/david.oliver/` | Hardcoded personal paths |
| `ERPSystem`, `Alpha`, `Beta`, `DataPlatform`, `AlertHub` | BA-specific projects/systems |
| `notion.so/ba-workspace` | Internal integrations |

#### Qualifying Content (GOOD SIGNS)

| Pattern | Reason |
|---------|--------|
| Generic variable names | `$VAULT_PATH`, `${PROJECT}` |
| Configuration via environment | `os.environ.get()` |
| Template placeholders | `{{company}}`, `<your-org>` |
| Well-documented functions | Docstrings, comments |
| Error handling | Try/except, validation |

### Step 3: Scoring System

Score each file 0-100:

| Score | Classification | Action |
|-------|----------------|--------|
| 90-100 | **Ready** | Can sync directly |
| 70-89 | **Minor edits** | Small sanitisation needed |
| 50-69 | **Needs work** | Significant generalisation required |
| 0-49 | **Not suitable** | Too specific or contains secrets |

### Step 4: Generate Report

Output a structured report:

```markdown
# Template Candidates Report

Generated: 2026-02-01

## Summary

| Category | Ready | Minor Edits | Needs Work | Excluded |
|----------|-------|-------------|------------|----------|
| scripts  | 3     | 2           | 1          | 4        |
| skills   | 5     | 3           | 2          | 1        |
| ...      |       |             |            |          |

## Ready for Sync (Score 90+)

### .claude/scripts/archive-orphan-attachments.py
- **Score:** 95
- **Status:** Ready
- **Notes:** Fully generic, no company references

### .claude/schemas/location.schema.json
- **Score:** 100
- **Status:** Ready
- **Notes:** Pure schema, no customisation needed

## Minor Edits Needed (Score 70-89)

### .claude/skills/sync-notion/SKILL.md
- **Score:** 75
- **Status:** Minor edits
- **Issues:**
  - Line 23: Contains hardcoded database ID
  - Line 45: References BA-specific workspace
- **Fix:** Replace with placeholder variables

## Excluded (Score <50)

### .claude/scripts/sync-ba-confluence.py
- **Score:** 20
- **Reason:** Entirely BA-specific integration
- **Action:** Do not sync

## Recommended Actions

1. Run `/template-sync` for 8 ready files
2. Edit 5 files with minor issues
3. Review 3 files needing significant work
```

## Output Location

Save report to: `.claude/reports/template-candidates-YYYY-MM-DD.md`

## Related Skills

- `/template-changelog` - Generate changelog entries
- `/template-sync` - Execute the sync
