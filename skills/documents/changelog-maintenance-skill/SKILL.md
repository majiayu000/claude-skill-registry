---
document_name: "changelog-maintenance.skill.md"
location: ".claude/skills/changelog-maintenance.skill.md"
codebook_id: "CB-SKILL-CHANGELOG-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for maintaining CHANGELOG.md following keepachangelog.org"
skill_metadata:
  category: "delivery"
  complexity: "simple"
  estimated_time: "5-15 min"
  prerequisites:
    - "Git commit history"
    - "PR descriptions"
category: "skills"
status: "active"
tags:
  - "skill"
  - "changelog"
  - "delivery"
ai_parser_instructions: |
  This skill defines procedures for changelog maintenance.
  Follows keepachangelog.org format.
  Section markers: === SECTION ===
  Procedure markers: === PROCEDURE: NAME ===
---

# Changelog Maintenance Skill

=== PURPOSE ===

This skill provides procedures for maintaining CHANGELOG.md following the [Keep a Changelog](https://keepachangelog.org) format. The Delivery Lead OWNS this artifact exclusively.

---

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(delivery-lead) @ref(CB-AGENT-DELIVERY-001) | Exclusive owner of CHANGELOG.md |

---

=== PREREQUISITES ===

Before using this skill:
- [ ] Access to git history
- [ ] List of changes since last release
- [ ] PR descriptions available

---

=== PROCEDURE: Changelog Entry ===

**Template:** @ref(CB-TPL-CHANGELOG-001)

**Categories (in this order):**
1. **Added** - New features
2. **Changed** - Changes in existing functionality
3. **Deprecated** - Soon-to-be removed features
4. **Removed** - Now removed features
5. **Fixed** - Bug fixes
6. **Security** - Vulnerability fixes

**Entry Format:**
```markdown
## [1.2.3] - 2026-01-04

### Added
- New user authentication flow (#123)
- Support for dark mode (#124)

### Changed
- Updated dashboard layout (#125)

### Fixed
- Login timeout issue (#126)
- Form validation on mobile (#127)

### Security
- Patched XSS vulnerability in comments (#128)
```

---

=== PROCEDURE: Update Unreleased Section ===

**Purpose:** Track changes before release

**Steps:**
1. Open CHANGELOG.md
2. Add entry under `## [Unreleased]` section
3. Use appropriate category
4. Link to PR/issue: `(#123)`
5. Keep entries concise but descriptive

**Example:**
```markdown
## [Unreleased]

### Added
- New export to CSV feature (#145)

### Fixed
- Memory leak in dashboard (#146)
```

---

=== PROCEDURE: Create Release Section ===

**Purpose:** Finalize changelog for release

**Steps:**
1. Copy `[Unreleased]` contents
2. Create new version section below `[Unreleased]`
3. Clear `[Unreleased]` section
4. Add version number and date
5. Add comparison link at bottom
6. Commit changelog update

**Comparison Links (at bottom of file):**
```markdown
[Unreleased]: https://github.com/org/repo/compare/v1.2.3...HEAD
[1.2.3]: https://github.com/org/repo/compare/v1.2.2...v1.2.3
[1.2.2]: https://github.com/org/repo/compare/v1.2.1...v1.2.2
```

---

=== PROCEDURE: Gather Changes ===

**Purpose:** Identify all changes since last release

**Steps:**
1. Find last release tag:
   ```bash
   git describe --tags --abbrev=0
   ```
2. List commits since tag:
   ```bash
   git log v1.2.2..HEAD --oneline
   ```
3. Review merged PRs since last release
4. Categorize each change
5. Write concise descriptions
6. Link to PRs/issues

---

=== CHANGELOG FORMAT ===

**Full File Structure:**
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.org/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.3] - 2026-01-04

### Added
- Feature description (#123)

### Changed
- Change description (#124)

### Fixed
- Fix description (#125)

## [1.2.2] - 2026-01-01
...

[Unreleased]: https://github.com/org/repo/compare/v1.2.3...HEAD
[1.2.3]: https://github.com/org/repo/compare/v1.2.2...v1.2.3
```

---

=== ANTI-PATTERNS ===

### Auto-Generated Only
**Problem:** Using only git commit messages
**Solution:** Curate entries for human readability

### Missing Links
**Problem:** No PR/issue references
**Solution:** Always link to PR or issue number

### Vague Descriptions
**Problem:** "Various bug fixes"
**Solution:** Specific, user-focused descriptions

### Wrong Categories
**Problem:** Bug fix listed as "Changed"
**Solution:** Use correct category for each entry

---

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(release-management) | Changelog finalized before release |
| @skill(versioning) | Version determines section header |
