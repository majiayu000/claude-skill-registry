---
name: changelog-manager
description: Manages changelog entries following Keep a Changelog format with CalVer versioning. Analyzes changes and generates appropriate changelog descriptions.
allowed-tools: Read, Write, Edit, Bash
user-invocable: true
---

# Changelog Manager Skill

## Purpose

This skill manages changelog entries in CHANGELOG.md following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format with [Calendar Versioning](https://calver.org/).

## Core Capabilities

### 1. Changelog Entry Generation

- Analyze current changes and commits
- Generate appropriate changelog descriptions
- Support Korean and English languages
- Extract ticket IDs from branch names
- Follow Keep a Changelog categories

### 2. Change Analysis

- Review git commits since last release
- Identify changed files and their purposes
- Categorize changes appropriately
- Generate concise but informative descriptions

### 3. Format Compliance

- Maintain Keep a Changelog format
- Use CalVer (YYYY.MM.MICRO) versioning
- Include JIRA ticket linking
- Preserve existing format and conventions

## Versioning Strategy

This plugin uses [Calendar Versioning](https://calver.org/) with format `YYYY.Minor.Patch`.

**Examples**:
- `2026.1.0` - First minor release in 2026
- `2026.1.1` - First patch release
- `2026.2.0` - Second minor release in 2026

## Changelog Categories

Based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/):

- **Added**: New features, endpoints, functionality
- **Changed**: Changes in existing functionality, improvements, updates
- **Fixed**: Bug fixes, error corrections, issue resolutions
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Security**: Security fixes

## Entry Format

```markdown
- [TICKET-ID](JIRA-URL) Description in specified language
```

**Korean Example**:
```markdown
- [SYN-1234](https://jira.example.com/browse/SYN-1234) 사용자 인증 기능 추가
```

**English Example**:
```markdown
- [SYN-1234](https://jira.example.com/browse/SYN-1234) Add user authentication feature
```

## Workflow

### 1. Extract Ticket ID

**From branch name**:
```bash
git branch --show-current
# Example: feature/SYN-1234-user-authentication
# Extract: SYN-1234
```

**Pattern**: `(PROJ-\d+)` where PROJ is project prefix

### 2. Analyze Changes

**Review commits**:
```bash
git log --oneline --since="$(git describe --tags --abbrev=0)"
```

**Review changed files**:
```bash
git diff --name-status $(git describe --tags --abbrev=0)..HEAD
```

### 3. Generate Description

**Based on**:
- Commit messages
- Changed files
- Code diff analysis
- User input if needed

**Guidelines**:
- Be concise but informative
- Focus on "what" not "how"
- Use active voice
- Mention affected components

### 4. Add to CHANGELOG.md

**Location**: Under `## [Unreleased]` in appropriate category

**Format**:
```markdown
## [Unreleased] - yyyy-mm-dd

### Added
- [TICKET-ID](JIRA-URL) New feature description

### Changed
- [TICKET-ID](JIRA-URL) Updated feature description

### Fixed
- [TICKET-ID](JIRA-URL) Bug fix description
```

## Parameters

- `type`: Changelog category (added/changed/fixed/deprecated/removed/security)
- `lang`: Description language (korean/english)
- `ticket`: Ticket ID (optional, auto-extracted from branch if not provided)

## Integration

This skill is invoked by:
- `/add-changelog` command - Manual changelog entry addition

## Best Practices

### Do:
- ✅ Follow Keep a Changelog format
- ✅ Use CalVer versioning
- ✅ Include ticket IDs with links
- ✅ Write clear, concise descriptions
- ✅ Maintain chronological order (newest first)
- ✅ Group related changes together

### Don't:
- ❌ Mix multiple unrelated changes in one entry
- ❌ Use vague descriptions
- ❌ Forget ticket ID linking
- ❌ Break existing format
- ❌ Add duplicate entries

## Example Usage

**Add new feature (Korean)**:
```
User: /add-changelog --type added
Skill: Analyzes changes → Generates description → Adds to CHANGELOG.md
Result: - [SYN-1234](URL) 사용자 프로필 이미지 업로드 기능 추가
```

**Fix bug (English)**:
```
User: /add-changelog --type fixed --lang eng
Skill: Analyzes changes → Generates description → Adds to CHANGELOG.md
Result: - [SYN-1235](URL) Fix profile image upload validation error
```

## Error Handling

- **No ticket ID found**: Ask user to provide ticket ID
- **CHANGELOG.md not found**: Create new CHANGELOG.md with proper format
- **No Unreleased section**: Add Unreleased section
- **Invalid category**: Default to "Added" or ask user

## File Structure

```
CHANGELOG.md format:

# Changelog

## [Unreleased] - yyyy-mm-dd

### Added
### Changed
### Fixed

## [2026.1.0] - 2026-01-15

### Added
- Feature 1
- Feature 2

### Changed
- Change 1
```
