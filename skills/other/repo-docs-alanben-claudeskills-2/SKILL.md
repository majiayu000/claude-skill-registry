---
name: repo-docs
description: Update and maintain core repository documentation files (README.md, CHANGELOG.md, LICENSE, CONTRIBUTING.md) before commits or releases. Use when users need to update documentation to reflect code changes, prepare for releases, or ensure documentation consistency.
---

# Repository Documentation Updates

This skill helps update core repository documentation files before committing changes or creating releases.

## When to Use This Skill

Use this skill when:
- Preparing to commit changes and need to update documentation
- Creating a release and need to update CHANGELOG
- Documentation is out of sync with code changes
- Need to add or update core repository files (README, CHANGELOG, LICENSE, CONTRIBUTING)

## Core Documentation Files

### README.md
Primary documentation file covering:
- Project overview and purpose
- Setup and installation instructions
- Basic usage examples
- Development guidelines
- Links to additional documentation

**Common updates:**
- Add new features or capabilities
- Update installation steps
- Revise configuration instructions
- Add or update examples

### CHANGELOG.md
Chronological record of changes following [Keep a Changelog](https://keepachangelog.com/) format.

**Structure:**
```markdown
# Changelog

## [Unreleased]
### Added
- New features not yet released

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes

## [X.Y.Z] - YYYY-MM-DD
### Added
- Feature descriptions

### Changed
- Modification descriptions

### Fixed
- Bug fix descriptions
```

**Common updates:**
- Move items from Unreleased to new version section
- Add new version entry with date
- Document new features, changes, and fixes
- Add version comparison links at bottom

### LICENSE
Legal terms for code usage and distribution.

**Common updates:**
- Update copyright year
- Change license type (requires project decision)
- Update copyright holder

### CONTRIBUTING.md
Guidelines for contributors.

**Typical sections:**
- How to report issues
- Development workflow
- Code submission process
- Testing requirements
- Communication channels

**Common updates:**
- Update workflow steps
- Revise standards or requirements
- Update contact information
- Add new guidelines

## Workflow for Release Preparation

When preparing a release:

1. **Review changes since last release**
   - Check git log or PR history
   - Identify user-facing changes
   - Note breaking changes or deprecations

2. **Update CHANGELOG.md**
   - Create new version section: `[X.Y.Z] - YYYY-MM-DD`
   - Move items from Unreleased to new version
   - Categorize: Added, Changed, Deprecated, Removed, Fixed, Security
   - Add version comparison link

3. **Update README.md if needed**
   - Add new features to overview
   - Update version numbers
   - Revise examples if API changed
   - Update dependencies list

4. **Update LICENSE if needed**
   - Update copyright year
   - Verify copyright holder

5. **Review CONTRIBUTING.md**
   - Ensure workflow is current
   - Update any changed processes

## Workflow for Regular Commits

Before committing changes:

1. **Identify documentation impact**
   - Does change affect usage?
   - Are there new features?
   - Did configuration change?
   - Are there breaking changes?

2. **Update CHANGELOG.md Unreleased section**
   - Add to appropriate category (Added/Changed/Fixed)
   - Be specific and user-focused
   - Note if breaking change

3. **Update README.md if needed**
   - Add new features
   - Update examples
   - Revise configuration steps

## Best Practices

- **Keep CHANGELOG current** - Update with each change, not at release time
- **Be specific** - "Added user authentication" not "Made improvements"
- **User perspective** - Document what users see, not internal refactoring
- **Version format** - Follow Semantic Versioning (MAJOR.MINOR.PATCH)
- **Date format** - Use ISO 8601 (YYYY-MM-DD)
- **Categorize correctly** - Use standard categories (Added, Changed, Fixed, etc.)
- **Link commits** - Reference commit SHAs or PR numbers when helpful

## Output Format

Generate updated documentation files directly in `/mnt/user-data/outputs/` with:
- Proper markdown formatting
- Consistent structure
- Current information
- Clear, concise descriptions
