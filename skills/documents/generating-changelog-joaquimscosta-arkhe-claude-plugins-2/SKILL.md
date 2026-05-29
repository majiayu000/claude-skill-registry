---
name: generating-changelog
description: Analyzes git commit history and generates professional changelogs with semantic versioning, conventional commit support, and multiple output formats (Keep a Changelog, Conventional, GitHub). Use when editing CHANGELOG.md, CHANGELOG.txt, or HISTORY.md files, preparing release notes, creating releases, bumping versions, updating changelog, documenting changes, writing release notes, tracking changes, version bump, tag release, or when user mentions "changelog", "release notes", "version history", "release", "semantic versioning", or "conventional commits".
---

# Git Changelog Generation

Automatically analyze git commit history and generate comprehensive changelogs following industry-standard formats.

## Auto-Invoke Triggers

This skill automatically activates when:

1. **Editing changelog files**: `CHANGELOG.md`, `CHANGELOG.txt`, `HISTORY.md`
2. **Mentioning keywords**: "changelog", "release notes", "version", "semantic versioning"
3. **Git tagging operations**: Creating or discussing version tags
4. **Release preparation**: Discussing release preparation or deployment

## What This Skill Delivers

When invoked, this skill provides:

### 1. Git History Analysis Report
- Commit range analysis (since last tag or specified range)
- Commit categorization by type (feat, fix, docs, etc.)
- Semantic version bump recommendation (MAJOR, MINOR, PATCH)
- Breaking changes detection
- Author and PR number extraction

### 2. Formatted Changelog
Choose from multiple formats:
- **Keep a Changelog** (default) - Industry standard, human-friendly
- **Conventional** - Follows Conventional Commits specification
- **GitHub** - GitHub-style release notes with PR links

### 3. Update Strategy
- Append to existing CHANGELOG.md (preserves history)
- Overwrite with fresh changelog
- Create new version section
- Merge with existing sections

## Common Use Cases

### Project Types
- **Microservices**: Track changes across multiple services
- **Frontend Applications**: UI updates and features
- **API Development**: REST API versioning and breaking changes
- **Infrastructure**: Deployment, CI/CD, DevOps updates
- **Documentation**: Technical docs, API docs, guides

### Conventional Commit Examples
The skill recognizes standard commit conventions:
```
feat: add new authentication endpoint
fix: resolve token expiration issue
docs: update API documentation
refactor: optimize database queries
perf: improve calculation performance
test: add integration tests
build: upgrade framework version
ci: configure automated testing
chore: update dependencies
```

### Monorepo Support
The skill handles monorepo structures:
- Service-specific changelogs (e.g., `services/api/CHANGELOG.md`)
- Frontend changelog (`frontend/CHANGELOG.md`)
- Root changelog (project-wide changes)

## Technical Features

### Conventional Commits Support
Automatically categorizes commits by type:
- `feat:` → Features section
- `fix:` → Bug Fixes section
- `docs:` → Documentation section
- `style:` → Code Style section
- `refactor:` → Refactoring section
- `perf:` → Performance section
- `test:` → Testing section
- `build:` → Build System section
- `ci:` → CI/CD section
- `chore:` → Other Changes section

### Semantic Versioning Detection
Automatically suggests version bumps:
- **MAJOR** (x.0.0): Contains `BREAKING CHANGE:` or exclamation mark suffix
- **MINOR** (0.x.0): Contains `feat:` commits
- **PATCH** (0.0.x): Contains only `fix:` commits

### Breaking Changes Detection
Identifies breaking changes from:
- `BREAKING CHANGE:` footer in commit message
- Exclamation mark after commit type (example: feat!: or fix!:)
- Manual annotation in commit body

### GitHub Integration
Extracts from commit messages:
- Pull request numbers (#123)
- Issue references (#456)
- Author information
- Commit SHAs

## Output Example

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-10-22

### Added
- Keyword competition scoring algorithm for market analysis (#123)
- Multi-currency support for revenue calculations (#124)
- OpenSearch faceted search with Valkey caching (#125)

### Fixed
- JWT token expiration issue in user-service (#126)
- Race condition in favorite-service list operations (#127)
- Memory leak in trend-service ARIMA calculations (#128)

### Changed
- Upgraded Spring Boot to 3.4.3 across all services (#129)
- Optimized search-service query performance (40% improvement) (#130)
- Refactored supply-analytics-service ETL pipeline (#131)

### Security
- Updated Jackson to fix CVE-2025-12345 (#132)

### Performance
- Reduced trend-service calculation time from 2.5s to 0.8s (#133)

## [1.1.0] - 2025-09-15

...
```

## Progressive Disclosure

This is **Level 1** documentation (skill overview).

For more details, see:
- **Level 2**: `WORKFLOW.md` - Step-by-step methodology
- **Level 3**: `EXAMPLES.md` - Real-world usage examples
- **Level 4**: `TROUBLESHOOTING.md` - Common issues and solutions

## Usage

### Via Command
```bash
/changelog
/changelog --since v1.1.0 --version 1.2.0
/changelog --format github --append
```

### Auto-Invoke
The skill activates automatically when:
```bash
# Editing changelog
vim CHANGELOG.md

# Discussing releases
"I need to prepare release notes for version 1.2.0"

# Git tagging
"Let's create a changelog for the v1.2.0 tag"
```

## Integration with Development Workflow

### Pre-Release Workflow
1. Developer: `git tag v1.2.0-rc1`
2. Skill auto-invokes: Analyzes commits since v1.1.0
3. Skill generates: Draft changelog with categorized changes
4. Developer reviews: Edits descriptions, adds context
5. Developer: `/changelog --append --version 1.2.0`
6. Skill updates: CHANGELOG.md with final content
7. Developer commits: Changelog as part of release

### Service-Specific Releases
```bash
# Generate changelog for specific service
cd services/api
/changelog --output CHANGELOG.md --since v1.0.0
```

### Monorepo Root Changelog
```bash
# Generate project-wide changelog
/changelog --output CHANGELOG.md --format keepachangelog
```

## Quality Standards

- **Conventional Commits**: 100% recognition of conventional commit format
- **Semantic Versioning**: Automatic MAJOR/MINOR/PATCH detection
- **Breaking Changes**: Clear highlighting of breaking changes
- **PR Linking**: Automatic GitHub PR number extraction
- **Date Formatting**: ISO 8601 dates (YYYY-MM-DD)
- **Markdown Formatting**: Valid markdown with proper headers
- **No Claude Code Footer**: Never include Claude Code attribution in changelog entries unless explicitly requested by user

## See Also

- `doc-coauthoring` skill - Collaborative documentation workflow
- `/code-explain` - Explain complex code sections
- `diagramming` skill or `/diagram` command - Generate diagrams (e.g., release flow diagrams)

## Version

1.0.0
