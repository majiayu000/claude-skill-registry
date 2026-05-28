---
name: template-changelog
context: fork
model: opus
description: Generate changelog for ArchitectKB template contributions
---

# Skill: Template Changelog

**Command:** `/template-changelog`
**Model:** 🟡 Sonnet
**Agent:** None (direct execution)

## Purpose

Compare this vault with the ArchitectKB template repository and generate changelog entries for features that could be contributed back.

## When to Use

- Before syncing changes to the template repo
- During quarterly vault reviews
- After implementing significant new features
- To track what's diverged between vaults

## Template Repository

Location: `~/Documents/GitHub/ArchitectKB/`
GitHub: https://github.com/DavidROliverBA/ArchitectKB

## Implementation

### Step 1: Compare File Inventories

Compare these directories between vaults:

| Directory | Content Type |
|-----------|--------------|
| `.claude/scripts/` | Python/Shell scripts |
| `.claude/skills/` | Skill definitions |
| `.claude/schemas/` | JSON schemas |
| `.claude/hooks/` | Pre/post hooks |
| `.claude/rules/` | Reference documentation |
| `Templates/` | Note templates |

### Step 2: Categorise Differences

For each file, determine:

1. **New** - Exists in this vault but not in template
2. **Modified** - Exists in both but content differs
3. **Removed** - Exists in template but not here (rare, usually intentional)

### Step 3: Filter for Template-Worthy Changes

A change is template-worthy if:

- ✅ Generic (no BA-specific references)
- ✅ Reusable across organisations
- ✅ Well-documented
- ✅ Tested and working

Exclude:

- ❌ BA-specific integrations (Notion sync with BA databases)
- ❌ Personal workflow preferences
- ❌ Experimental/incomplete features
- ❌ Files containing credentials or internal URLs

### Step 4: Generate Changelog Entries

Use [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [Unreleased]

### Added
- New `/archive-attachments` skill for orphaned attachment cleanup
- `archive-orphan-attachments.py` script with manifest tracking
- New `location.schema.json` for Location entity type

### Changed
- Updated `frontmatter-validator.py` to support seven-pillar ontology
- Enhanced `tag-taxonomy.md` with workstream hierarchy

### Fixed
- Fixed hardcoded paths in scheduled task scripts
```

## Execution Script

Run this comparison:

```bash
#!/bin/bash
VAULT=~/Documents/GitHub/BA-DavidOliver-ObsidianVault
TEMPLATE=~/Documents/GitHub/ArchitectKB

echo "=== New in Vault (not in Template) ==="
for dir in .claude/scripts .claude/skills .claude/schemas .claude/hooks .claude/rules; do
    echo "--- $dir ---"
    comm -23 <(ls "$VAULT/$dir" 2>/dev/null | sort) <(ls "$TEMPLATE/$dir" 2>/dev/null | sort)
done

echo ""
echo "=== Modified (different content) ==="
for dir in .claude/scripts .claude/skills .claude/schemas .claude/hooks .claude/rules; do
    for file in "$VAULT/$dir"/*; do
        name=$(basename "$file")
        if [ -f "$TEMPLATE/$dir/$name" ]; then
            if ! diff -q "$file" "$TEMPLATE/$dir/$name" > /dev/null 2>&1; then
                echo "$dir/$name"
            fi
        fi
    done
done
```

## Output

Generate a markdown report with:

1. **Summary stats** - New/Modified/Unchanged counts
2. **Changelog entries** - Ready to paste into CHANGELOG.md
3. **Candidate list** - Files recommended for `/template-sync`
4. **Exclusions** - Files skipped with reasons

## Related Skills

- `/template-candidates` - Detailed analysis of what to sync
- `/template-sync` - Execute the sync operation
