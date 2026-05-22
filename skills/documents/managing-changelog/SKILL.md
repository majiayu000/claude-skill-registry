---
name: managing-changelog
description: Creates, updates, and maintains CHANGELOG.md files following Common Changelog and Keep a Changelog standards. Use when creating changelogs, adding release entries, updating unreleased sections, validating changelog format, or user mentions 'changelog', 'release notes', 'version history', 'add to changelog', 'update changelog', 'create changelog', 'change log format', or needs to document version changes.
allowed-tools: Read, Write, Edit
---

# Managing Changelog

Create and maintain CHANGELOG.md files following standard formats (Common Changelog + Keep a Changelog).

## When to Use

Activate when:
- Creating new CHANGELOG.md
- Adding release entry
- Updating Unreleased section
- Validating changelog format
- User: "changelog", "release notes", "version history", "add to changelog", "update changelog"

## Core Workflows

| ID | Purpose | Trigger |
|----|---------|---------|
| WF1 | Create CHANGELOG.md | Initial setup |
| WF2 | Add Release Entry | New version |
| WF3 | Update Unreleased | Pre-release changes |
| WF4 | Validate Format | Quality check |
| WF5 | Promote Prerelease | Stabilize alpha/beta/rc |

### WF1: Create CHANGELOG.md

**Purpose**: Initialize new changelog file

**When**: No CHANGELOG.md exists, explicit request

**Steps**:

1. **Choose format**
   - Ask user: Common Changelog (strict, references, authors) or Keep a Changelog (simpler)
   - Default: Common Changelog

2. **Write initial structure**
   ```markdown
   # Changelog

   All notable changes documented here.
   Format: [Common Changelog](https://common-changelog.org) / [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
   Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

   ## [Unreleased]

   [unreleased]: https://github.com/owner/repo/compare/vX.X.X...HEAD
   ```

3. **Confirm creation**

### WF2: Add Release Entry

**Purpose**: Add new version entry

**When**: New release, version bump, explicit request

**Execution**:

1. **Gather info**
   - Version: semver-valid (e.g., 1.2.3)
   - Date: YYYY-MM-DD (ISO 8601)
   - Changes: from git log, HISTORY.md, or user input

2. **Process changes** (improve quality)
   - **Remove noise**: Exclude dotfiles (.gitignore), dev deps, style tweaks, doc formatting | Include: refactorings, runtime changes, code style using new features, new docs
   - **Rephrase**: Align terminology, add missing details, remove irrelevant specifics
   - **Merge related**: Combine multi-commit changes (e.g., bump same dep twice → single entry)
   - **Skip no-ops**: Exclude negated changes (reverts)
   - **Keep brief**: One line per change, details in references

3. **Categorize changes**
   ```
   Common Changelog: Changed, Added, Removed, Fixed
   Keep a Changelog: Changed, Added, Deprecated, Removed, Fixed, Security
   ```

4. **Format entry** (Common Changelog example)
   ```markdown
   ## [1.2.3] - 2025-11-26

   ### Changed

   - **Breaking:** refactor API to use async/await ([#45](url)) (Author)
   - Improve performance of data processing ([abc123](url))

   ### Added

   - Add support for JSON export ([#42](url), [#43](url))

   ### Fixed

   - Fix memory leak in cache ([#44](url)) (Author)

   [1.2.3]: https://github.com/owner/repo/releases/tag/v1.2.3
   ```

5. **Add notice** (if needed)
   - First release: `_First release._`
   - Yanked: `_This release was yanked due to [issue]._`
   - Upgrade guide: `_If upgrading: see UPGRADING.md._`
   - Place after heading, before change groups

6. **Insert entry**
   - Place after `## [Unreleased]` section
   - Update unreleased link if exists

7. **Move unreleased content** (if exists)
   - Migrate changes from Unreleased → new release
   - Clear Unreleased section

### WF3: Update Unreleased

**Purpose**: Add changes to Unreleased section

**When**: Pre-release changes, ongoing work

**Steps**:

1. **Read current CHANGELOG.md**

2. **Add to Unreleased** (if section exists, else create)
   ```markdown
   ## [Unreleased]

   ### Added

   - New feature description ([#XX](url))
   ```

3. **Use Edit tool** to append changes

### WF4: Validate Format

**Purpose**: Check changelog follows standards

**When**: Before release, quality check, explicit request

**Checks**:

```
Structure:
- [ ] File named CHANGELOG.md
- [ ] First-level heading: # Changelog
- [ ] Versions sorted latest-first
- [ ] Version format: ## [X.Y.Z] - YYYY-MM-DD
- [ ] Date format: YYYY-MM-DD (ISO 8601)

Categories (Common Changelog):
- [ ] Only: Changed, Added, Removed, Fixed

Categories (Keep a Changelog):
- [ ] Only: Changed, Added, Deprecated, Removed, Fixed, Security

Content:
- [ ] Changes use imperative mood (Add, Fix, Update not Added, Fixed, Updated)
- [ ] Breaking changes prefixed: **Breaking:**
- [ ] References included (commits, PRs, issues)
- [ ] Links at bottom: [X.Y.Z]: url

Common Issues:
- ⚠ Commit log dumps (verbatim copying)
- ⚠ Missing dates
- ⚠ Inconsistent categories
- ⚠ Vague descriptions
```

Report issues + suggestions

### WF5: Promote Prerelease

**Purpose**: Convert prerelease to stable release

**When**: Promoting alpha/beta/rc to stable

**Approaches**:

**A. Copy content** (default)
- Copy changes from prerelease(s) → release
- Merge related, rephrase, clean as per WF2
- Write as if prereleases don't exist

**B. Skip entry** (internal testing only)
- No changelog for internal CI/CD test releases
- Only for non-public prereleases

**C. Refer to prerelease** (private projects, lengthy QA)
- Add notice: `_Stable release based on [X.Y.Z-rc.N]._`
- Use when all stakeholders familiar with prerelease content
- Example:
  ```markdown
  ## [3.1.0] - 2021-07-05

  _Stable release based on [3.1.0-rc.2]._

  ## [3.1.0-rc.2] - 2021-07-04

  ### Fixed
  - Fix localization (a11eb73)
  ```

**Decision**: Use A unless B or C explicitly needed

## Format Reference

### Common Changelog Format

**Heading**:
```markdown
## [X.Y.Z] - YYYY-MM-DD
```

**Categories** (order):
1. Changed - changes in existing functionality
2. Added - new functionality
3. Removed - removed functionality
4. Fixed - bug fixes

**Notice format** (optional, after heading):
```markdown
## [X.Y.Z] - YYYY-MM-DD

_Single-sentence notice with emphasis._

### Category...
```
- Use for: first release, yanked, essential upgrade guides
- Only one per release
- Examples: `_First release._`, `_Yanked due to security issue._`, `_See UPGRADING.md._`

**Change format**:
```markdown
- [**Breaking:**|**Subsystem:**] <Imperative verb> <description> ([refs](url)) (Authors)
```

**References** (after change, same line):
- **Commits**: `([abc123](url))` or submodule: `([owner/name@abc123](url))`
- **PRs/Issues**: `([#123](url))` or external: `([owner/name#123](url))`
- **External tickets**: `([JIRA-837](url))`
- **Multiple same type**: `([#1](url), [#2](url))` not `([#1](url)) ([#2](url))`
- **Rule**: Max 2 refs, pick best starting point (prefer PR over issue if both exist)

**Authors** (after references):
- Format: `(Name1, Name2)` or `(#refs; Name1, Name2)` with semicolon separator
- Example: `- Fix loop ([#194](url)) (Alice)` or `- Fix loop ([#194](url), [#195](url); Alice, Bob)`
- Omit if single contributor project
- Bot changes: credit human who merged PR
- **Security**: Only usernames or real names allowed - NO email addresses, API keys, tokens, file paths, or personal information

**Prefixes** (bold):
- **Breaking**: `- **Breaking:** change description`
- **Subsystem**: `- **UI:** change description` or `- **Installer (breaking):** change`
- Sort: breaking first per category, then by importance, then latest-first

**Links** (bottom):
```markdown
[X.Y.Z]: https://github.com/owner/repo/releases/tag/vX.Y.Z
[unreleased]: https://github.com/owner/repo/compare/vX.Y.Z...HEAD
```

### Keep a Changelog Format

**Heading**: Same as Common Changelog

**Categories** (order):
1. Added
2. Changed
3. Deprecated
4. Removed
5. Fixed
6. Security

**Change format** (simpler):
```markdown
- <Description starting with capital>
```

**Unreleased section**:
```markdown
## [Unreleased]

### Added

- Feature coming soon
```

## Guiding Principles

**From Common Changelog**:
- Changelogs for humans
- Communicate impact of changes
- Sort by importance
- Skip unimportant content
- Link changes to further info

**From Keep a Changelog**:
- Humans, not machines
- Entry for every version
- Group same types
- Versions linkable
- Latest first
- Show release dates
- Follow Semantic Versioning

## Anti-patterns

**Avoid**:
- Verbatim git log dumps
- Vague descriptions ("fix stuff")
- Missing dates or wrong format
- Inconsistent categories
- No references/context
- Past tense (use imperative: Add not Added in change text)
- **Security violations**: API keys, tokens, passwords, email addresses, file paths with personal info, or sensitive data in changelog content

## Tool Usage

**Read**: Load existing CHANGELOG.md or HISTORY.md
**Write**: Create new CHANGELOG.md
**Edit**: Update existing changelog (add entries, update sections)

## Integration

**GitHub Actions** (auto-create GitHub releases from CHANGELOG.md):
```yaml
name: Release
on: { push: { tags: ['*'] } }
permissions: { contents: write }
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: docker://antonyurchenko/git-release:latest
        env: { GITHUB_TOKEN: '${{ secrets.GITHUB_TOKEN }}' }
```

**Workflow integration**:
- Release: Update before tagging (WF2)
- PR merge: Add to Unreleased (WF3)
- Version bump: Move Unreleased → release (WF2)
- Prerelease: Use WF6 approaches

## Examples

**Common Changelog**:
```markdown
# Changelog

## [2.1.0] - 2025-11-26

### Changed

- **Breaking:** refactor config to use YAML ([#45](url)) (Alice)

### Added

- Add dark mode support ([#42](url), [#43](url))

### Fixed

- Fix memory leak in parser ([abc123](url))

[2.1.0]: https://github.com/owner/repo/releases/tag/v2.1.0
```

**Keep a Changelog**:
```markdown
# Changelog

## [2.1.0] - 2025-11-26

### Added

- Dark mode support for UI

### Changed

- Config now uses YAML instead of JSON (breaking change)

### Fixed

- Memory leak in parser

[2.1.0]: https://github.com/owner/repo/releases/tag/v2.1.0
```

## Migration Examples

**HISTORY.md → CHANGELOG.md**:

Input (HISTORY.md):
```markdown
## VERSION: 2.0.0
date: 2025-11-26
type: update
change_summary: Major refactoring

CHANGES:
- Refactored API to async/await
- Added JSON export
- Fixed memory leaks
```

Output (CHANGELOG.md):
```markdown
## [2.0.0] - 2025-11-26

### Changed

- **Breaking:** refactor API to use async/await

### Added

- Add JSON export support

### Fixed

- Fix memory leaks in cache

[2.0.0]: https://github.com/owner/repo/releases/tag/v2.0.0
```

## Quick Reference

| Task | Workflow | Output |
|------|----------|--------|
| Create | WF1 | Initial CHANGELOG.md |
| Add release | WF2 | ## [X.Y.Z] - DATE |
| Update ongoing | WF3 | Append to Unreleased |
| Validate | WF4 | Format compliance check |
| Promote prerelease | WF5 | Alpha/beta/rc → stable |