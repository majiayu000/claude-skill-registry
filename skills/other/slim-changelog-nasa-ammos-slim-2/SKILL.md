---
name: slim-changelog
description: Create and maintain human-readable changelogs for software projects using Keep a Changelog standards. Use when creating project changelogs, documenting releases, managing version history, or establishing transparent communication about software changes for users and contributors.
---

# Changelog Writer

## Overview

A changelog is a vital tool for documenting significant changes in software over time in a format accessible **to humans**. Unlike developer-oriented commit messages or GitHub's auto-generated release notes, changelogs focus on **feature changes** rather than code-level details, making them essential for transparency and user communication.

This skill helps you create and maintain professional `CHANGELOG.md` files following the [Keep a Changelog](https://keepachangelog.com) standard, ensuring your project's evolution is clearly communicated to users, contributors, and stakeholders.

## When to Use This Skill

- **Starting a new project** that needs version tracking and change documentation
- **Preparing for software releases** and need to communicate changes clearly
- **Establishing transparency** in software development and release cycles
- **Complementing GitHub releases** with human-readable feature summaries
- **Onboarding contributors** who need to understand project evolution
- **Meeting documentation requirements** for enterprise or open-source projects

## Prerequisites

- **Semantic versioning familiarity**: Understanding of version numbering (MAJOR.MINOR.PATCH)
- **Markdown knowledge**: Basic Markdown formatting for consistent documentation
- **Release process awareness**: Understanding of your project's release workflow

## Why Changelogs Matter

**Q: Why maintain a `CHANGELOG.md` if GitHub has auto-generated release notes?**

**A: They are complementary tools serving different audiences:**

- **GitHub releases**: Commit-oriented, developer-focused, platform-dependent
- **Changelogs**: Feature-oriented, user-focused, platform-independent

Changelogs ensure:
- **Future-proof accessibility** of change information
- **Broader audience understanding** beyond developers
- **Feature-centric communication** rather than commit-level details
- **Independence from code hosting platforms**

## Workflow

### Step 1: Team Agreement

Before implementing changelogs, discuss their importance with your team:

- **Value proposition**: Explain benefits for transparency and user communication
- **Maintenance responsibility**: Assign ownership for changelog updates
- **Integration timing**: Decide when to update (during development, at release, etc.)
- **Audience consideration**: Define who the changelog serves (users, contributors, stakeholders)

### Step 2: Create the Changelog

1. **Copy the template**:
   ```bash
   cp assets/CHANGELOG.md CHANGELOG.md
   ```

2. **Customize the header**:
   - Replace project-specific information
   - Ensure Keep a Changelog and Semantic Versioning references remain

3. **Add your first release entry**:
   - Replace `[INSERT SEMANTIC VERSION...]` with actual version (e.g., `[1.0.0] - 2024-01-15`)
   - Fill in the change categories with actual changes

### Step 3: Maintain the Changelog

For each release, add a new section above previous releases:

```markdown
## [1.1.0] - 2024-02-15

### Added
- New dashboard feature for user analytics
- Export functionality for reports

### Changed
- Improved performance of search queries
- Updated user interface design

### Fixed
- Fixed login issue with special characters
- Resolved memory leak in background processing

### Removed
- Deprecated legacy API endpoints
```

### Step 4: Integrate with Documentation

1. **Link from README.md**:
   ```markdown
   ## Changelog

   See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.
   ```

2. **Reference in release communications**:
   - Include changelog excerpts in release announcements
   - Link to changelog from GitHub releases
   - Reference in project documentation

## Keep a Changelog Best Practices

### Standard Categories

Use these categories consistently:

- **Added**: New features and functionality
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Features removed in this version
- **Fixed**: Bug fixes
- **Security**: Security-related changes

### Writing Guidelines

1. **Write for humans**: Use clear, non-technical language when possible
2. **Focus on impact**: Explain what users will experience, not implementation details
3. **Group related changes**: Organize similar changes together
4. **Be specific**: Avoid vague descriptions like "various improvements"
5. **Include breaking changes**: Clearly mark and explain breaking changes

### Version Management

- **Use semantic versioning**: MAJOR.MINOR.PATCH format
- **Keep dates consistent**: Use YYYY-MM-DD format
- **Latest first**: Most recent changes at the top
- **Unreleased section**: Track upcoming changes before release

## Template Usage

The provided `CHANGELOG.md` template includes:

- **Header**: Standard Keep a Changelog format
- **Version section**: Template for release entries
- **Change categories**: Added, Changed, Removed sections
- **Placeholders**: `[INSERT...]` markers for easy customization

### Customization Steps

1. **Replace placeholders**: Fill in all `[INSERT...]` sections
2. **Add relevant categories**: Include Deprecated, Fixed, Security if needed
3. **Update project information**: Customize header if project-specific details needed
4. **Establish format consistency**: Maintain formatting across all entries

## Examples and References

### Demo Implementations
- [Terraformly Changelog](https://github.com/riverma/terraformly/blob/main/CHANGELOG.md) - Real project example
- [Keep a Changelog Example](https://github.com/olivierlacan/keep-a-changelog/blob/main/CHANGELOG.md) - Reference implementation

### Additional Resources
- [Keep a Changelog](https://keepachangelog.com) - Official standard and examples
- [Semantic Versioning](https://semver.org) - Version numbering guidelines
- [SLIM Documentation](https://nasa-ammos.github.io/slim/docs/guides/documentation/change-log/) - Comprehensive changelog guide

## Common Patterns

### Breaking Changes
```markdown
### Changed
- **BREAKING**: Authentication now requires API keys (see migration guide)
- Updated user permissions model
```

### Security Updates
```markdown
### Security
- Fixed XSS vulnerability in user input validation
- Updated dependencies to address security advisories
```

### Deprecation Notices
```markdown
### Deprecated
- Legacy API endpoints (will be removed in v2.0.0)
- Old configuration format (use new YAML format)
```

## Assets Available

- **`CHANGELOG.md`**: Complete Keep a Changelog template with standard sections and placeholders for easy customization

## Troubleshooting

**Q: How often should I update the changelog?**
A: Update for every release, or maintain an "Unreleased" section for ongoing changes.

**Q: What if I forgot to document changes in previous releases?**
A: You can retroactively add changelog entries, but mark them clearly as retrospective updates.

**Q: Should I include every small change?**
A: Focus on user-facing changes. Minor bug fixes and internal refactoring may not need detailed changelog entries.

**Q: How do I handle breaking changes?**
A: Mark them clearly with **BREAKING** labels and provide migration guidance or links to documentation.
