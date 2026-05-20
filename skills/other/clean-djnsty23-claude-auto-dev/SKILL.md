---
name: clean
description: Removes temporary screenshots, old backups, stale handoffs, and auto-active flags. Use when project has accumulated temp files.
triggers:
  - clean
allowed-tools: Bash, Glob
model: opus
user-invocable: true
---

# Clean

Remove Claude Code artifacts and temporary files.

## Data Safety: Move, Do Not Delete

Files found in the project root (`prd-archive-*.json`, `prd-backup-*.json`, `handoff-*.md`, `AUDIT-*.md`) are moved to `.claude/` subdirectories, not deleted. Deleting them destroys sprint history. The move step runs first before any deletion.

## Process (Follow This Order)

### Step 1: Move stray files from root (first)

```bash
mkdir -p .claude/archives .claude/handoffs .claude/reports
mv prd-backup-*.json .claude/archives/ 2>/dev/null
mv prd-archive-*.json .claude/archives/ 2>/dev/null
mv handoff-*.md .claude/handoffs/ 2>/dev/null
mv AUDIT-*.md .claude/reports/ 2>/dev/null
mv *-report.md .claude/reports/ 2>/dev/null
```

PowerShell:
```powershell
New-Item -ItemType Directory -Force -Path .claude\archives, .claude\handoffs, .claude\reports | Out-Null
Move-Item prd-backup-*.json .claude\archives\ -Force -ErrorAction SilentlyContinue
Move-Item prd-archive-*.json .claude\archives\ -Force -ErrorAction SilentlyContinue
Move-Item handoff-*.md .claude\handoffs\ -Force -ErrorAction SilentlyContinue
Move-Item AUDIT-*.md .claude\reports\ -Force -ErrorAction SilentlyContinue
Move-Item *-report.md .claude\reports\ -Force -ErrorAction SilentlyContinue
```

### Step 2: Delete expendable files (only from .claude/ subdirs)

| Target | Path | Rule |
|--------|------|------|
| Screenshots | `.claude/screenshots/*.png` | Delete all |
| Auto flag | `.claude/auto-active` | Delete if stale |
| Playwright | `.playwright-mcp/` | Delete all |
| Backups | `.claude/archives/prd-backup-*.json` | Delete if older than 7 days |
| Handoffs | `.claude/handoffs/handoff-*.md` | Delete if older than 7 days |
| Reports | `.claude/reports/*.md` | Delete if older than 7 days |

### Step 3: Archives — list only, do not auto-delete

List `.claude/archives/prd-archive-*.json` older than 30 days. Ask user before deleting. If user does not confirm, do not delete.

### Step 4: Report

Show what was moved and what was deleted. Separate the two lists.

## Rules

- Do not delete `prd-archive-*.json` or `prd-backup-*.json` from project root — move them
- Do not auto-delete archives — prompt user first
- Do not touch source code, prd.json, or config files
- Report what was moved vs what was deleted
