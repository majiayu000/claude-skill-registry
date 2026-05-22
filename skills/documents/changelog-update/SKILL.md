---
name: changelog-update
description: Generate changelog entries from commits for any project type
user-invocable: false
---

# Changelog Update

## Purpose

Generates changelog entries from git commits, categorizes changes into Added/Changed/Fixed/Breaking sections following configurable changelog format (default: keep-a-changelog), and updates or creates the changelog file for any project type.

## Input Context

Requires:
- **Project Configuration**: Output from `detect-project-type` skill
- **Version**: New version number (e.g., "1.2.0")
- **Custom Message** (optional): User-provided commit message overrides auto-generation
- **Last Tag**: Git tag of previous release (optional)

## Workflow

### 1. Load Changelog Configuration

Use configuration from `detect-project-type`:
- `changelog_file` - Path to changelog file (default: `CHANGELOG.md`)
- `changelog_format` - Format to use (default: `keep-a-changelog`)
- `tag_pattern` - For finding commits since last tag

### 2. Determine Changelog File Path

Use `changelog_file` from configuration:

```bash
changelog_file="CHANGELOG.md"  # from config, can be:
# - CHANGELOG.md (standard)
# - HISTORY.md (alternative)
# - CHANGES.rst (Python projects)
# - NEWS.md (GNU projects)
# - {package}/CHANGELOG.md (monorepos)
```

Check if file exists. If not, create with initial structure based on format:
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).
```

### 3. Gather Commits

Get commits since last release tag:
```bash
if [ -n "$last_tag" ]; then
  git log ${last_tag}..HEAD --oneline --no-merges
else
  # First release - get all commits
  git log --oneline --no-merges
fi
```

For monorepo projects, optionally filter commits by package directory:
```bash
# Filter commits that touched this package only
git log ${last_tag}..HEAD --oneline --no-merges -- packages/my-lib/
```

### 3. Categorize Commits

Parse each commit message and categorize:

**Added (new features):**
- `feat:` or `feat(scope):`
- Commit messages starting with "add", "create", "implement"

**Changed (modifications to existing features):**
- Commit messages starting with "update", "modify", "change", "refactor"
- `refactor:` prefix

**Fixed (bug fixes):**
- `fix:` or `fix(scope):`
- Commit messages starting with "fix", "correct", "resolve"

**Breaking Changes:**
- `BREAKING CHANGE:` in body
- `!` after type (e.g., `feat!:`)
- Extract breaking change description from body

**Uncategorized:**
- Other types (`chore:`, `docs:`, `test:`, `style:`) → skip or place in "Changed"

### 4. Format Changelog Entry

Generate entry following this format:

```markdown
## Version {version} - {date}

### Breaking Changes
- Description of breaking change 1
- Description of breaking change 2

### Added
- New feature description 1
- New feature description 2

### Changed
- Change description 1
- Change description 2

### Fixed
- Bug fix description 1
- Bug fix description 2
```

**Formatting rules:**
- Date format: YYYY-MM-DD (use today's date)
- Strip conventional commit prefixes from descriptions
- Capitalize first letter of each entry
- Remove trailing periods
- Skip empty sections
- If custom message provided, use it for the entire entry

### 5. Insert Entry into Changelog

Read existing changelog file, parse structure, and insert new entry:
- Place after the file header (before any existing version entries)
- Preserve all existing entries unchanged
- Maintain consistent formatting (2 blank lines between versions)

### 6. Generate Commit Message

Create a commit message from the changelog content:
```
Release {scope} v{version}

{changelog-entry-body}

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Output Format

Return:

```
{
  "changelog_path": "plugins/daily-carry/CHANGELOG.md",
  "new_entry": "## Version 1.2.0 - 2026-01-12\n\n### Added\n- New deployment skill\n\n### Fixed\n- Version detection logic",
  "commit_message": "Release plugin:daily-carry v1.2.0\n\nAdded:\n- New deployment skill\n\nFixed:\n- Version detection logic\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
  "categories": {
    "added": 1,
    "changed": 0,
    "fixed": 1,
    "breaking": 0
  },
  "file_created": false
}
```

## Examples

### Example 1: Feature and Fix Commits

**Input:**
- Scope: `plugin:daily-carry`
- Version: `1.2.0`
- Last tag: `daily-carry-v1.1.0`

**Commits:**
```
feat: add deploy-otterstack command
fix: correct git push error handling
docs: update README with examples
```

**Generated Entry:**
```markdown
## Version 1.2.0 - 2026-01-12

### Added
- Add deploy-otterstack command

### Fixed
- Correct git push error handling
```

**Output:**
```
{
  "changelog_path": "plugins/daily-carry/CHANGELOG.md",
  "new_entry": "## Version 1.2.0 - 2026-01-12\n\n### Added\n- Add deploy-otterstack command\n\n### Fixed\n- Correct git push error handling",
  "commit_message": "Release plugin:daily-carry v1.2.0\n\nAdded:\n- Add deploy-otterstack command\n\nFixed:\n- Correct git push error handling\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
  "categories": {
    "added": 1,
    "changed": 0,
    "fixed": 1,
    "breaking": 0
  },
  "file_created": false
}
```

### Example 2: Breaking Change

**Input:**
- Scope: `marketplace`
- Version: `2.0.0`

**Commits:**
```
feat!: change marketplace schema structure

BREAKING CHANGE: marketplace.json now requires plugins array with explicit versions
```

**Generated Entry:**
```markdown
## Version 2.0.0 - 2026-01-12

### Breaking Changes
- marketplace.json now requires plugins array with explicit versions

### Added
- Change marketplace schema structure
```

### Example 3: Custom Message Override

**Input:**
- Scope: `variants`
- Version: `1.2.0`
- Custom message: "Update Android and TypeScript variants with new git workflow patterns"

**Generated Entry:**
```markdown
## Version 1.2.0 - 2026-01-12

- Update Android and TypeScript variants with new git workflow patterns
```

**Commit Message:**
```
Release variants v1.2.0

Update Android and TypeScript variants with new git workflow patterns

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Example 4: First Release (No Commits to Parse)

**Input:**
- Scope: `plugin:new-plugin`
- Version: `1.0.0`
- No last tag

**Generated Entry:**
```markdown
## Version 1.0.0 - 2026-01-12

### Added
- Initial release of new-plugin
```

## Error Handling

- **Git errors**: Return error if git log fails
- **File write errors**: Return error if changelog file cannot be written
- **Invalid date**: Use current system date as fallback
- **Empty commits**: Generate minimal entry with "Initial release" or "Version bump"

## Integration Notes

This skill is invoked by the `/release` command in Phase 3. The command will:
1. Display the generated changelog entry
2. Allow user to edit before finalizing
3. Use the commit message for git operations in Phase 6
