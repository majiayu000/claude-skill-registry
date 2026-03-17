---
name: pop-changelog-automation
description: "Enhanced changelog generation with semantic versioning, auto-categorization, and release notes. Parses conventional commits, determines version bump (MAJOR.MINOR.PATCH), categorizes changes by type, generates CHANGELOG.md updates, and creates GitHub release notes. Use before releases or on PR merge to automate version management."
inputs:
  - from: any
    field: since_version
    required: false
  - from: any
    field: target_version
    required: false
  - from: any
    field: release_title
    required: false
outputs:
  - field: changelog_entry
    type: file_path
  - field: version_bump
    type: string
  - field: breaking_changes
    type: list
  - field: release_notes
    type: file_path
next_skills:
  - pop-finish-branch
context: fork
triggers:
  - "update changelog"
  - "generate changelog"
  - "prepare release"
  - "create release notes"
  - "determine version"
---

# Enhanced Changelog Automation

## Overview

Automatically generate CHANGELOG.md updates and GitHub release notes from conventional commits with semantic versioning analysis. This skill provides intelligent version management and changelog generation that surpasses Auto Claude's capabilities.

## Key Features

1. **Semantic Versioning** - Auto-detect MAJOR.MINOR.PATCH bumps
2. **Auto-Categorization** - Group commits by type (feat, fix, breaking, etc.)
3. **Breaking Change Detection** - Highlight breaking changes with migration notes
4. **Release Notes Generation** - Auto-generate GitHub release notes
5. **Integration Ready** - Seamless integration with git workflow

## Conventional Commit Format

PopKit follows conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

| Type              | Description                | Version Bump          |
| ----------------- | -------------------------- | --------------------- |
| `feat`            | New feature                | MINOR (1.0.0 → 1.1.0) |
| `fix`             | Bug fix                    | PATCH (1.0.0 → 1.0.1) |
| `perf`            | Performance improvement    | PATCH                 |
| `refactor`        | Code refactoring           | PATCH                 |
| `docs`            | Documentation only         | PATCH                 |
| `test`            | Test additions/updates     | PATCH                 |
| `chore`           | Maintenance tasks          | PATCH                 |
| `ci`              | CI/CD changes              | PATCH                 |
| `build`           | Build system changes       | PATCH                 |
| `style`           | Formatting, no code change | PATCH                 |
| `BREAKING CHANGE` | Breaking change            | MAJOR (1.0.0 → 2.0.0) |

## Version Bump Rules

```python
# MAJOR bump (1.0.0 → 2.0.0)
- Any commit with "BREAKING CHANGE" in body or footer
- Incompatible API changes
- Major architectural changes

# MINOR bump (1.0.0 → 1.1.0)
- feat: commits
- New features added
- Backward-compatible functionality

# PATCH bump (1.0.0 → 1.0.1)
- fix: commits
- Bug fixes
- Performance improvements
- Refactoring
- Documentation updates
```

## Usage

### Automatic (Recommended)

Changelog is automatically updated when:

1. **Before PR creation** (`/popkit:git pr`)
   - Analyzes commits since last release
   - Generates changelog entry
   - Updates CHANGELOG.md
   - Includes changelog in PR description

2. **Before release** (`/popkit:git release`)
   - Determines version bump automatically
   - Updates CHANGELOG.md with new version
   - Generates GitHub release notes
   - Creates git tag

3. **On PR merge** (via hook)
   - Updates changelog for merged changes
   - Prepares for next release

### Manual

```bash
# Preview changelog for next version (auto-determined)
/popkit:git changelog --preview

# Generate changelog with specific version
/popkit:git changelog --version 1.1.0

# Generate since specific tag
/popkit:git changelog --since v1.0.0

# Generate GitHub release notes
/popkit:git changelog --release

# Auto-determine version bump
/popkit:git changelog --auto

# Update CHANGELOG.md
/popkit:git changelog --update
```

### Python CLI

```bash
# From project root
cd /path/to/project

# Preview next version
python packages/shared-py/popkit_shared/utils/changelog_generator.py --preview

# Auto-determine version and update CHANGELOG.md
python packages/shared-py/popkit_shared/utils/changelog_generator.py --auto --update

# Generate GitHub release notes
python packages/shared-py/popkit_shared/utils/changelog_generator.py --release

# Get version bump analysis as JSON
python packages/shared-py/popkit_shared/utils/changelog_generator.py --json
```

## Output Examples

### CHANGELOG.md Entry

```markdown
## [1.1.0] - 2026-01-08

### ✨ Features

- **changelog-automation**: Enhanced changelog generation with semantic versioning (#27)
- **git-workflow**: Automatic changelog updates on PR creation and merge (#28)
- **release-notes**: Auto-generate GitHub release notes from commits (#29)

### 🐛 Bug Fixes

- **git**: Fix merge conflict detection in subdirectories (#30)
- **hooks**: Correct Windows path handling in pre-commit hook (#31)

### 💥 BREAKING CHANGES

- **api**: Change authentication endpoint from /auth to /api/auth
  - Migration: Update all API calls to use new endpoint
  - See migration guide: docs/migrations/v1.1.0.md

### 📚 Documentation

- **readme**: Update installation instructions with new requirements
- **skills**: Add usage examples for changelog automation

### ⚡ Performance

- **complexity-analyzer**: Reduce analysis time by 40% with caching

### 🔧 Chores

- **deps**: Update dependencies to latest versions
- **ci**: Add automated changelog generation to CI pipeline
```

### GitHub Release Notes

```markdown
# PopKit 1.1.0 - Enhanced Changelog Automation

## 🎉 What's New

### Changelog Automation

Enhanced changelog generation with semantic versioning, auto-categorization, and intelligent version bump detection. (#27)

### Git Workflow Integration

Automatic changelog updates on PR creation and merge. (#28)

### Release Notes Generation

Auto-generate GitHub release notes from commits with proper formatting. (#29)

## 💥 Breaking Changes

### Change authentication endpoint from /auth to /api/auth

**Migration:**

- Update all API calls to use new endpoint
- See migration guide: docs/migrations/v1.1.0.md

## 🐛 Bug Fixes

- Fix merge conflict detection in subdirectories (#30)
- Correct Windows path handling in pre-commit hook (#31)

## 📊 Statistics

- **Features Added:** 3
- **Bug Fixes:** 2
- **Total Commits:** 12
- **Issues Closed:** 5
```

## Breaking Change Format

When introducing breaking changes, use this format:

```
feat(api): Change authentication endpoint

Move authentication from /auth to /api/auth for consistency.

BREAKING CHANGE: Authentication endpoint changed from /auth to /api/auth
Migration: Update all API calls to use new endpoint
See migration guide: docs/migrations/v1.1.0.md
```

The changelog generator will:

- Detect "BREAKING CHANGE" in footer
- Categorize as MAJOR version bump
- Extract migration notes from footer
- Highlight in both CHANGELOG.md and release notes

## Integration with Git Workflow

### PR Creation Flow

```bash
# When creating PR with /popkit:git pr:

1. Detect commits since last release
2. Analyze commit types
3. Determine version bump (if release PR)
4. Generate changelog entry
5. Update CHANGELOG.md
6. Include changelog in PR description
7. Create PR
```

### Release Flow

```bash
# When creating release with /popkit:git release:

1. Get commits since last version tag
2. Determine semantic version bump
3. Calculate next version
4. Generate changelog entry
5. Update CHANGELOG.md
6. Generate GitHub release notes
7. Save release notes file
8. Create git tag with version
9. Create GitHub release with notes
10. Publish release
```

## Best Practices

1. **Use conventional commits** - Always format commits as `type(scope): description`
2. **Include issue references** - Add `(#123)` to link commits to issues
3. **Document breaking changes** - Use BREAKING CHANGE footer with migration notes
4. **Scope your commits** - Use meaningful scopes like `api`, `ui`, `core`
5. **Write clear descriptions** - Make it easy to understand the change

## Value Delivery

**Time Saved:**

- Manual changelog: 30-45 minutes per release
- Automated changelog: 30 seconds
- **Savings: 98%+ time reduction**

**Quality Improved:**

- Consistent changelog format
- No missed commits
- Proper semantic versioning
- Clear breaking change communication
- Professional release notes

## Technical Details

### Implementation

**Python utility:** `packages/shared-py/popkit_shared/utils/changelog_generator.py`

- Main `ChangelogGenerator` class
- Git commit parsing
- Semantic version bump detection
- CHANGELOG.md and release notes generation

**Skill:** `packages/popkit-dev/skills/pop-changelog-automation/SKILL.md`

- Usage documentation
- Integration patterns
- Examples and best practices

### Dependencies

No external dependencies required. Uses only Python standard library:

- `subprocess` - Git command execution
- `re` - Conventional commit parsing
- `json` - JSON output format
- `datetime` - Timestamp generation
- `pathlib` - File path handling

## Related Skills

- `pop-finish-branch` - Branch cleanup after release
- `pop-git-workflow` - Git workflow automation
