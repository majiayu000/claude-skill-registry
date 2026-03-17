---
name: version
description: V1.0 - Release version management checklist for hs-cli-conductor. Use when bumping versions or preparing releases.
hooks:
  PostToolUse:
    - matcher: "Read|Write|Edit"
      hooks:
        - type: prompt
          prompt: |
            If a file was read, written, or edited in the version skill directory (path contains '.claude/skills/version'), verify that history logging occurred.
            
            Check if History/{YYYY-MM-DD}.md exists and contains an entry for this interaction with:
            - Format: "## HH:MM - {Action Taken}"
            - One-line summary
            - Accurate timestamp (obtained via `Get-Date -Format "HH:mm"` command, never guessed)
            
            If history entry is missing or incomplete, provide specific feedback on what needs to be added.
            If history entry exists and is properly formatted, acknowledge completion.
  Stop:
    - matcher: "*"
      hooks:
        - type: prompt
          prompt: |
            Before stopping, if version skill was used (check if any files in .claude/skills/version directory were modified), verify that the interaction was logged:
            
            1. Check if History/{YYYY-MM-DD}.md exists in version skill directory
            2. Verify it contains an entry with format "## HH:MM - {Action Taken}" where HH:MM was obtained via `Get-Date -Format "HH:mm"` (never guessed)
            3. Ensure the entry includes a one-line summary of what was done
            
            If history entry is missing:
            - Return {"decision": "block", "reason": "History entry missing. Please log this interaction to History/{YYYY-MM-DD}.md"}
            
            If history entry exists:
            - Return {"decision": "approve"}
---

# Version Management

Release version checklist for hs-cli-conductor using **Semantic Versioning** (major.minor.patch).

## Version Bump Checklist

When releasing a new version, update ALL of these locations:

### 1. Changelog

- [ ] **`CHANGELOG.md`** (root) - Add entry under `[Unreleased]` or new version section
- Format: Keep a Changelog standard (<https://keepachangelog.com>)
- Include: Added, Changed, Fixed, Removed sections as needed

### 2. Package Files

- [ ] **`package.json`** (root) - `"version": "x.y.z"`
- [ ] **`admin/package.json`** - `"version": "x.y.z"` (keep in sync)

### 3. UI Version Displays

- [ ] **`admin/src/components/TitleBar.tsx`**
  - Line ~69: Alert message `Version x.y.z`
  - Line ~139: Title bar display `Vx.y`

### 4. Build Configuration

- [ ] **`admin/electron-builder.json5`** - Uses `${version}` from admin/package.json (auto-resolved)
- [ ] Verify output directory: `release/${version}/`

## Quick Command

To bump version across all files:

```powershell
# Replace OLD_VERSION with current, NEW_VERSION with target
$old = "0.1.0"; $new = "0.2.0"

# Update package.json files
(Get-Content package.json) -replace "`"version`": `"$old`"", "`"version`": `"$new`"" | Set-Content package.json
(Get-Content admin/package.json) -replace "`"version`": `"$old`"", "`"version`": `"$new`"" | Set-Content admin/package.json

# TitleBar requires manual review for display format
```

## Current State

**Note:** Version inconsistency detected during skill creation:

- Root `package.json`: 0.1.0
- Admin `package.json`: 0.0.0
- TitleBar alert: 0.1.0
- TitleBar display: V1.0

**Recommendation:** Align all versions before next release.
