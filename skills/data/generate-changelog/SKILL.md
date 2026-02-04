---
name: generate-changelog
description: Generate changelog entries from git commits, plan files, or structured data. Use for version releases, creating CHANGELOG.md sections, or documenting changes between versions.
allowed-tools: Read, Bash
---

# Generate Changelog

Automatically generate changelog entries following Keep a Changelog format. **Note:** CHANGELOG.md for the main repo is maintained by Release Please. Use this skill for ad-hoc changelog text (e.g. a different format or a one-off report).

## When to Use

- Version release workflows
- Creating CHANGELOG.md sections
- Documenting changes between versions
- Generating release notes
- Summarizing work completed

## Instructions

### Step 1: Gather Change Data

Accept change information from various sources.

**Expected Input**:

- `version`: String (e.g., "0.8.0")
- `date`: String (ISO-8601 or YYYY-MM-DD)
- `source`: String (git|plan-file|manual)
- `sourceData`: Object (git range, plan file path, or manual entries)

**Source Types**:

- **git**: Parse git log between two refs
- **plan-file**: Extract from plan file metadata
- **manual**: User-provided entries

### Step 2: Parse Changes

Extract and categorize changes.

**Categories** (Keep a Changelog standard):

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes

**Git Commit Parsing**:

- Parse conventional commit format (feat:, fix:, etc.)
- Extract scope and description
- Map commit type to changelog category

### Step 3: Group and Deduplicate

Group changes by category and remove duplicates.

**Grouping Rules**:

- feat → Added
- fix → Fixed
- security → Security
- refactor, perf → Changed
- docs → Changed (if significant)
- chore → Omit (unless breaking change)

### Step 4: Format Changelog Section

Create formatted changelog section.

**Format**:

```markdown
## [Version] - Date

### Added

- New feature 1
- New feature 2

### Fixed

- Bug fix 1
- Bug fix 2

### Changed

- Change 1
```

### Step 5: Return Formatted Changelog

Return complete changelog section ready for insertion.

**Expected Output**:

```markdown
## [0.8.0] - 2025-10-17

### Added

- Dark mode toggle for user preferences
- OAuth2 authentication support

### Fixed

- Memory leak in connection pool
- CORS configuration error

### Changed

- Migrated to v2 authentication API
- Optimized query performance
```

## Error Handling

- **No Changes Found**: Return empty changelog with note
- **Invalid Git Range**: Return error with git command output
- **Invalid Plan File**: Return error describing issue
- **Unparseable Commits**: Include as "Changed" with raw message

## Examples

### Example 1: Generate from Git Range

**Input**:

```json
{
  "version": "0.8.0",
  "date": "2025-10-17",
  "source": "git",
  "sourceData": {
    "fromRef": "v0.7.0",
    "toRef": "HEAD"
  }
}
```

**Git Commits**:

```
feat(auth): add OAuth2 support
fix(api): resolve memory leak
docs: update API documentation
chore(deps): bump dependencies
```

**Output**:

```markdown
## [0.8.0] - 2025-10-17

### Added

- Add OAuth2 support (auth)

### Fixed

- Resolve memory leak (api)

### Changed

- Update API documentation
```

### Example 2: Generate from Plan File

**Input**:

```json
{
  "version": "0.8.0",
  "date": "2025-10-17",
  "source": "plan-file",
  "sourceData": {
    "planFile": ".version-update-plan.json"
  }
}
```

**Plan File Content**:

```json
{
  "changes": {
    "added": ["Dark mode toggle", "User profiles"],
    "fixed": ["Login redirect bug", "Dashboard crash"],
    "changed": ["Improved performance"]
  }
}
```

**Output**:

```markdown
## [0.8.0] - 2025-10-17

### Added

- Dark mode toggle
- User profiles

### Fixed

- Login redirect bug
- Dashboard crash

### Changed

- Improved performance
```

### Example 3: Manual Entries

**Input**:

```json
{
  "version": "0.8.0",
  "date": "2025-10-17",
  "source": "manual",
  "sourceData": {
    "added": ["New payment gateway integration"],
    "fixed": ["Cart calculation error"],
    "security": ["Fixed XSS vulnerability in search"]
  }
}
```

**Output**:

```markdown
## [0.8.0] - 2025-10-17

### Added

- New payment gateway integration

### Fixed

- Cart calculation error

### Security

- Fixed XSS vulnerability in search
```

### Example 4: Empty Changelog

**Input**:

```json
{
  "version": "0.8.0",
  "date": "2025-10-17",
  "source": "git",
  "sourceData": {
    "fromRef": "v0.7.0",
    "toRef": "v0.7.0"
  }
}
```

**Output**:

```markdown
## [0.8.0] - 2025-10-17

No changes in this release.
```

## Validation

- [ ] Parses conventional commits correctly
- [ ] Maps commit types to changelog categories
- [ ] Groups changes by category
- [ ] Formats according to Keep a Changelog
- [ ] Handles empty changelogs
- [ ] Deduplicates entries
- [ ] Includes scope in entries when present
- [ ] Handles manual entries

## Supporting Files

- `commit-mapping.json`: Conventional commit to changelog category mapping
