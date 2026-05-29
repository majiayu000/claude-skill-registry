---
name: version-changelog-patterns
description: When checking if skill content matches current library/framework version.
version: 1.0.0
tokens: ~350
confidence: high
sources:
  - https://semver.org/
  - https://keepachangelog.com/
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [versioning, changelog, updates, skills]
---

## When to Use
When checking if skill content matches current library/framework version.

## Patterns

### Version Check Strategy
```bash
# Search for latest version
"[library] latest version 2025"
"[library] npm OR pypi OR crates"

# Find changelog
"[library] changelog OR releases"
"[library] site:github.com releases"
```

### Changelog Locations by Platform
```
npm packages:
  - npmjs.com/package/[name]?activeTab=versions
  - github.com/[org]/[repo]/releases

Python:
  - pypi.org/project/[name]/#history
  - github.com/[org]/[repo]/blob/main/CHANGELOG.md

GitHub:
  - /releases (preferred)
  - /blob/main/CHANGELOG.md
  - /blob/main/HISTORY.md
```

### Breaking Changes Keywords
```
Search for:
  - "BREAKING CHANGE"
  - "breaking:"
  - "deprecated"
  - "removed in [version]"
  - "migration guide"
  - "upgrade guide"
```

### SemVer Quick Reference
```
MAJOR.MINOR.PATCH (e.g., 2.1.3)

MAJOR: Breaking changes (APIs removed/changed)
MINOR: New features (backward compatible)
PATCH: Bug fixes only

⚠️ Pre-1.0: Any change can be breaking
⚠️ Check for ^ vs ~ in dependencies
```

## Anti-Patterns
- Assuming patch versions have no impact
- Ignoring peer dependency changes
- Not checking release date (old = risky)
- Skipping alpha/beta/rc notes

## Verification Checklist
- [ ] Current version identified
- [ ] Skill assumes correct version
- [ ] No breaking changes since skill creation
- [ ] Deprecation warnings checked
