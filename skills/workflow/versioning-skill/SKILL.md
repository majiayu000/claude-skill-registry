---
document_name: "versioning.skill.md"
location: ".claude/skills/versioning.skill.md"
codebook_id: "CB-SKILL-VERSION-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for semantic versioning decisions"
skill_metadata:
  category: "delivery"
  complexity: "intermediate"
  estimated_time: "5-10 min"
  prerequisites:
    - "List of changes"
    - "Current version"
category: "skills"
status: "active"
tags:
  - "skill"
  - "versioning"
  - "semver"
  - "delivery"
ai_parser_instructions: |
  This skill defines procedures for semantic versioning.
  Follows semver.org specification.
  Section markers: === SECTION ===
  Procedure markers: === PROCEDURE: NAME ===
---

# Versioning Skill

=== PURPOSE ===

This skill provides procedures for determining version numbers following [Semantic Versioning](https://semver.org). Used by the Delivery Lead for all version decisions.

---

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(delivery-lead) @ref(CB-AGENT-DELIVERY-001) | Primary skill for versioning |

---

=== PREREQUISITES ===

Before using this skill:
- [ ] Current version number known
- [ ] List of changes since last release
- [ ] Understanding of breaking changes

---

=== SEMVER FORMAT ===

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Examples:
1.0.0       - Initial stable release
1.2.3       - Normal release
2.0.0       - Major/breaking release
1.2.3-beta.1  - Pre-release
1.2.3-rc.1    - Release candidate
```

---

=== PROCEDURE: Determine Version Bump ===

**Decision Tree:**

```
Are there breaking changes?
├── YES → MAJOR bump (1.x.x → 2.0.0)
└── NO → Are there new features?
         ├── YES → MINOR bump (1.2.x → 1.3.0)
         └── NO → PATCH bump (1.2.3 → 1.2.4)
```

**When to MAJOR (X.0.0):**
- Incompatible API changes
- Removal of features
- Changes requiring migration
- Breaking schema changes

**When to MINOR (x.Y.0):**
- New features (backwards compatible)
- New endpoints/methods
- Significant enhancements
- Deprecation notices

**When to PATCH (x.y.Z):**
- Bug fixes
- Security patches
- Performance improvements
- Documentation fixes

---

=== PROCEDURE: Breaking Change Detection ===

**Purpose:** Identify if changes are breaking

**Check for:**
- [ ] API endpoint removed or renamed
- [ ] Required parameter added
- [ ] Response format changed
- [ ] Database schema incompatible
- [ ] Configuration format changed
- [ ] Removed deprecated features
- [ ] Changed default behavior

**If ANY checked → Breaking change → MAJOR bump**

---

=== PROCEDURE: Pre-release Versioning ===

**Purpose:** Version pre-release software

**Pre-release Types:**
- `alpha` - Early testing, unstable
- `beta` - Feature complete, testing
- `rc` - Release candidate, final testing

**Format:**
```
1.2.3-alpha.1
1.2.3-alpha.2
1.2.3-beta.1
1.2.3-rc.1
1.2.3-rc.2
1.2.3 (final)
```

**Rules:**
- Pre-release < release (1.2.3-rc.1 < 1.2.3)
- Increment suffix number for iterations
- Clear pre-release for final version

---

=== PROCEDURE: Initial Release ===

**Purpose:** First public release versioning

**Options:**
- `0.1.0` - Initial development (API may change)
- `1.0.0` - First stable release

**0.x.x Rules:**
- API may change at any time
- MINOR can have breaking changes
- Use for pre-production software

**Moving to 1.0.0:**
- When API is stable
- When used in production
- When ready for public commitment

---

=== PROCEDURE: Version in Code ===

**Purpose:** Update version in project files

**Common Locations:**
- `package.json` (Node.js)
- `Cargo.toml` (Rust)
- `pyproject.toml` (Python)
- `version.txt` or `VERSION`
- Application constants

**Steps:**
1. Determine new version
2. Update all version locations
3. Commit with message: `chore: bump version to 1.2.3`
4. Tag commit

---

=== ANTI-PATTERNS ===

### Breaking Without Major
**Problem:** Breaking changes in minor/patch
**Solution:** Always major bump for breaking changes

### Feature in Patch
**Problem:** New features in patch releases
**Solution:** New features require minor bump

### Skipping Versions
**Problem:** Jumping from 1.0.0 to 1.5.0
**Solution:** Sequential versioning (1.0.0 → 1.1.0)

### Inconsistent Pre-release
**Problem:** Using "beta1" instead of "beta.1"
**Solution:** Follow semver pre-release format

---

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(changelog-maintenance) | Version determines changelog section |
| @skill(release-management) | Version needed for release |
