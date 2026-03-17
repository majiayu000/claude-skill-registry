---
name: update-docs
description: Update documentation after commits. Syncs README, AGENTS.md, CHANGELOG, and docs/ with code changes. Use after commits or to analyze working tree changes.
argument-hint: [commit-range|--working-tree|--audit]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Update Documentation

Automatically update documentation to reflect code changes. Enforces the "README as landing page" pattern—README should be a concise entry point, with detailed documentation in `docs/`.

## Core Philosophy

> "Your README is not your documentation. It is an overview of your project... a gateway to other pieces of info."

| README.md | docs/ |
|-----------|-------|
| What is this? Why should I care? | How does everything work? |
| Quick start (copy-paste ready) | Step-by-step tutorials |
| Minimal examples | Complete API/command reference |
| Links to detailed docs | In-depth configuration |
| < 300 lines ideal | As long as needed |

## Trigger Modes

1. **Post-commit (automatic)**: Triggered by git hook after commits
2. **Manual with commit range**: `/update-docs HEAD~3..HEAD` to analyze specific commits
3. **Manual with working tree**: `/update-docs --working-tree` to analyze uncommitted changes
4. **Audit mode**: `/update-docs --audit` to check README health and suggest migrations

## Arguments

- No arguments: Analyze the most recent commit (HEAD)
- `HEAD~N..HEAD`: Analyze the last N commits
- `COMMIT1..COMMIT2`: Analyze a specific commit range
- `--working-tree` or `-w`: Analyze uncommitted changes in working tree
- `--audit` or `-a`: Audit README structure and suggest migrations to docs/

## Marker File Detection

When triggered by post-commit hook, check for `.claude/doc-update-pending.json`:

```bash
if [ -f .claude/doc-update-pending.json ]; then
  COMMIT=$(jq -r '.commit_short' .claude/doc-update-pending.json)
fi
```

**After processing, always clean up:**

```bash
rm -f .claude/doc-update-pending.json
```

---

## Workflow

```
Update Docs Progress:
- [ ] Phase 1: Discover and audit documentation structure
- [ ] Phase 2: Detect changes (git diff or working tree)
- [ ] Phase 3: Route updates to correct location
- [ ] Phase 4: Migrate bloated README sections (if needed)
- [ ] Phase 5: Apply updates
- [ ] Phase 6: Update CHANGELOG (if exists)
- [ ] Phase 7: Create docs commit (if changes made)
```

---

## Phase 1: Discover and Audit Documentation Structure

### 1.1 Scan for Documentation Files

```bash
# Primary
README.md, AGENTS.md, CHANGELOG.md, CONTRIBUTING.md

# Secondary (docs/)
docs/*.md, docs/**/*.md

# Config
package.json, pyproject.toml, Cargo.toml
```

### 1.2 Audit README Health

Analyze README.md for signs it needs restructuring:

**Red Flags (README is bloated):**

| Signal | Threshold | Action |
|--------|-----------|--------|
| Total lines | > 500 lines | Recommend migration |
| Commands table | > 20 entries | Move to `docs/commands.md` |
| File structure tree | > 30 lines | Move to `docs/file-structure.md` |
| Configuration section | > 50 lines | Move to `docs/configuration.md` |
| Multiple H2 sections for same topic | Any | Consolidate in docs/ |
| Code blocks | > 10 blocks | Move examples to docs/ |

**Check for these README sections that belong in docs/:**

```markdown
## Commands Reference      → docs/commands.md
## API Reference           → docs/api.md
## Configuration           → docs/configuration.md
## File Structure          → docs/file-structure.md
## Detailed Examples       → docs/examples.md
## Troubleshooting         → docs/troubleshooting.md
## Architecture            → docs/architecture.md
```

### 1.3 Determine Ideal README Structure

A healthy README should have only:

```markdown
# Project Name

One-line description.

## TL;DR / What is this?
2-3 sentences max.

## Quick Start
5-10 lines of copy-paste commands.

## Documentation
- [Commands Reference](docs/commands.md)
- [Configuration](docs/configuration.md)
- [Contributing](CONTRIBUTING.md)

## License
One line.
```

---

## Phase 2: Detect Changes

### For Commit Analysis

```bash
git diff --name-only <range>
git diff --stat <range>
```

### For Working Tree Analysis

```bash
git status --porcelain
git diff
git diff --cached
```

### Categorize Changes

| Category | Examples |
|----------|----------|
| **Skill/Command** | `.claude/skills/`, `.claude/commands/` |
| **Structure** | New directories, renamed files |
| **Configuration** | `package.json`, settings files |
| **Feature** | New functionality |
| **Fix** | Bug fixes |

---

## Phase 3: Route Updates to Correct Location

### Routing Table

| Change Type | Target File | NOT README |
|-------------|-------------|------------|
| New skill/command | `docs/commands.md` | ~~README commands table~~ |
| Skill description changed | `docs/commands.md` | |
| New config option | `docs/configuration.md` | |
| File structure changed | `docs/file-structure.md` | |
| New API endpoint | `docs/api.md` | |
| New workflow pattern | `AGENTS.md` | |
| Quick start broken | `README.md` | (exception) |
| Project description changed | `README.md` | (exception) |
| New major feature | `README.md` (one line) + `docs/` (details) | |

### README-Only Updates (Exceptions)

Only update README.md directly for:

1. **TL;DR / Description** — What the project is
2. **Quick Start** — Minimal getting-started commands
3. **Links section** — Adding links to new docs/ files
4. **License** — License changes
5. **Badges** — Build status, version badges

### Create docs/ Files If Missing

If routing requires a docs/ file that doesn't exist:

1. Create the file with a standard template
2. Add a link to it from README.md
3. Migrate any existing content from README to the new file

**Template for new docs/ file:**

```markdown
# {Title}

{Brief description of what this document covers.}

## Overview

{Content migrated from README or new content}

---

*This documentation is auto-maintained. Last updated: {date}*
```

---

## Phase 4: Migrate Bloated README Sections

If Phase 1 audit found README sections that should be in docs/, migrate them.

See [MIGRATION.md](MIGRATION.md) for:
- Section patterns to look for (Commands, Configuration, API, etc.)
- Step-by-step migration process
- Before/after examples
- Confirmation prompts for large migrations

---

## Phase 5: Apply Updates

### 5.1 Update docs/ Files

For each routed update:

1. Read the target docs/ file
2. Find the relevant section
3. Apply the update (add/modify/remove)
4. Preserve formatting and structure

### 5.2 Update README Links

If new docs/ files were created, add links to README:

```markdown
## Documentation

- [Commands Reference](docs/commands.md)
- [Configuration Guide](docs/configuration.md)  ← NEW
- [File Structure](docs/file-structure.md)
```

### 5.3 Update AGENTS.md (Conservative)

Only update AGENTS.md when:
- New workflow patterns are introduced
- Integration points change (hooks, verification)
- Operating principles need clarification

**Do NOT auto-update:**
- Nuanced guidance sections
- Project-specific conventions
- Editorial content

---

## Phase 6: Update CHANGELOG

If `CHANGELOG.md` exists, append entries.

### Format Detection

Detect format from existing file:
- **Keep a Changelog** (most common)
- **Conventional Changelog**
- **Simple list**

### Entry Generation

```markdown
## [Unreleased]

### Added
- New `docs/commands.md` for detailed command reference

### Changed
- Migrated commands table from README to docs/

### Fixed
- Fixed broken link in docs/setup.md
```

**Rules:**
- Only user-facing changes
- Past tense ("Added", "Fixed")
- One line per entry

---

## Phase 7: Create Documentation Commit

### Verify Changes

```bash
git status --porcelain
git diff --stat
```

### Summary Report

```
Documentation Updates
=====================

Migrations:
  - README.md → docs/commands.md (142 lines moved)

New files:
  - docs/commands.md (created)

Modified:
  - README.md (replaced section with link)
  - CHANGELOG.md (added entry)

Changes: +156 -142
```

### Create Commit

```bash
git add <files>
git commit -m "docs: restructure documentation (README as landing page)

- Migrated commands table to docs/commands.md
- README now links to detailed docs
- Added CHANGELOG entry

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Edge Cases

### No docs/ Directory
- Create `docs/` directory
- Create initial files as needed
- Add `.gitkeep` if empty

### README Has No Clear Sections
- Skip migration
- Only add new content to docs/
- Suggest manual restructuring

### docs/ File Already Exists with Different Content
- Append new content to existing file
- Don't overwrite existing sections
- Warn if potential conflict

### README Is Already Minimal
- Great! Just route new updates to docs/
- No migration needed

### Stale Marker File
- Check if marker references old commit
- Ask user how to proceed
- Always clean up marker

---

## Configuration (Optional)

Projects can customize via `.claude/doc-sync-config.json`. See [CONFIGURATION.md](CONFIGURATION.md) for full schema.

Key options:
- `readme.maxLines`: Warn threshold (default: 300)
- `routing.*`: Customize target docs/ files
- `autoMigrate`: If true, migrations happen without asking

---

## Audit Mode (`--audit`)

When run with `--audit`, perform a full health check:

```
README Health Audit
===================

File: README.md
Lines: 847 (⚠️  > 500 recommended)

Sections that should be in docs/:
  ⚠️  "Commands Reference" (156 lines) → docs/commands.md
  ⚠️  "File Structure" (43 lines) → docs/file-structure.md
  ⚠️  "Configuration" (89 lines) → docs/configuration.md
  ✓  "Quick Start" (12 lines) — OK in README
  ✓  "License" (2 lines) — OK in README

Missing docs/ files:
  ✗  docs/commands.md (would receive 156 lines)
  ✗  docs/configuration.md (would receive 89 lines)

Recommendations:
  1. Run /update-docs --migrate to restructure
  2. README would go from 847 → ~150 lines
  3. Creates 3 new files in docs/

Run migration? [Y/n]
```

---

## Integration with Post-Commit Hook

See `POST_COMMIT_HOOK.md` for installation.

When triggered by hook:
- Analyze only the most recent commit
- Route updates to correct docs/ files
- Auto-migrate if `autoMigrate: true` in config
- Create follow-up commit

---

## Final Cleanup

**Always run at the end:**

```bash
rm -f .claude/doc-update-pending.json
```
