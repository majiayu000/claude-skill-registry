---
name: readmes
description: "Check all READMEs for accuracy and consistency across the meta-repo"
model: claude-haiku-4-5-20251001
allowed-tools: Read, Edit, Glob, Grep
---

# /readmes

Comprehensive review and update of all README.md files in the meta-repo.

## Usage

```bash
/readmes    # Review all READMEs in ideas/ directory
```

## Scope

**Includes:**
- `ideas/[project]/README.md` - All project overviews
- `ideas/[project]/apps/*/README.md` - Multi-app project READMEs
- Root-level documentation files

**Excludes:**
- `spaces/` directory (code repos have their own maintenance)
- Build artifacts, node_modules, etc.

## Execution Flow

### 1. Discover All READMEs
```bash
Glob: ideas/**/README.md
```

### 2. Review Each README

For each README, technical-writer agent checks:
- **Status accuracy**: Matches CLAUDE.md Current Projects?
- **Date accuracy**: Is "Last Updated" current?
- **Link validity**: Are all links working?
- **Content completeness**: Required sections present?
- **Consistency**: Formatting matches standards?

### 3. Update READMEs

- Fix outdated status indicators
- Update dates to current date
- Fix broken links
- Add missing sections
- Standardize formatting

### 4. Report Results

Summary includes:
- READMEs reviewed (count)
- Updates made (list of files)
- Issues requiring manual attention

## What Gets Checked

| Aspect | Validation |
|--------|------------|
| **Status** | Matches CLAUDE.md |
| **Dates** | "Last Updated" is accurate |
| **Links** | Internal refs work |
| **Structure** | Has required sections |
| **Consistency** | Follows template |

## When to Use

- After major project updates
- Before project reviews/demos
- Monthly documentation maintenance
- After status changes in CLAUDE.md

## Notes

- **Read then write**: Agent reads each file before making changes
- **Preserves content**: Only updates metadata and known sections
- **Non-destructive**: Doesn't remove custom content
- **Idempotent**: Safe to run multiple times

## Integration

```
Update CLAUDE.md status → /readmes → Verify changes
```
