---
name: bump-version
description: Bump version numbers across all DecentPaste config files (package.json, Cargo.toml, tauri.conf.json, downloads.json). Use for version updates without building.
---

# Bump Version

Update version (x.x.x) across all config files.

## Files

| File                                                     | Field                                       |
|----------------------------------------------------------|---------------------------------------------|
| `decentpaste-app/package.json`                           | `"version"`                                 |
| `decentpaste-app/src-tauri/Cargo.toml`                   | `version`                                   |
| `decentpaste-app/src-tauri/tauri.conf.json`              | `"version"`                                 |
| `website/downloads.json`                                 | `version`, `tag` (v-prefix), asset URLs     |
| `decentpaste-app/src-tauri/gen/apple/...project.pbxproj` | `MARKETING_VERSION` (if iOS project exists) |

## Workflow

1. Read current version from `tauri.conf.json`
2. Ask new version (validate: `^\d+\.\d+\.\d+$`)
3. Edit all 4 files (`replace_all: true` for downloads.json URLs)
4. If `gen/apple/` exists, update Share Extension: `sed -i '' 's/MARKETING_VERSION = OLD;/MARKETING_VERSION = NEW;/g' ...project.pbxproj`
5. List updated files, remind to commit
