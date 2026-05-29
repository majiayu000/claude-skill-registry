---
document_name: "release-management.skill.md"
location: ".claude/skills/release-management.skill.md"
codebook_id: "CB-SKILL-RELEASE-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for planning and executing releases"
skill_metadata:
  category: "delivery"
  complexity: "intermediate"
  estimated_time: "30-60 min per release"
  prerequisites:
    - "Approved PRs ready"
    - "Version determined"
category: "skills"
status: "active"
tags:
  - "skill"
  - "release"
  - "delivery"
ai_parser_instructions: |
  This skill defines procedures for release management.
  Section markers: === SECTION ===
  Procedure markers: === PROCEDURE: NAME ===
---

# Release Management Skill

=== PURPOSE ===

This skill provides procedures for planning and executing releases. Used by the Delivery Lead for all release-related work.

---

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(delivery-lead) @ref(CB-AGENT-DELIVERY-001) | Primary skill for releases |

---

=== PREREQUISITES ===

Before using this skill:
- [ ] All PRs for release are merged
- [ ] Tests passing on main branch
- [ ] Version number determined (@skill(versioning))
- [ ] Changelog updated (@skill(changelog-maintenance))

---

=== PROCEDURE: Release Checklist ===

**Purpose:** Ensure complete release process

**Pre-Release:**
- [ ] All planned issues closed
- [ ] All PRs merged to main
- [ ] CI/CD pipeline passing
- [ ] Changelog updated for version
- [ ] Version number determined
- [ ] Release notes drafted
- [ ] Stakeholders notified

**Release:**
- [ ] Create release branch (if needed)
- [ ] Update version in code/package
- [ ] Commit version bump
- [ ] Create git tag
- [ ] Create GitHub release
- [ ] Trigger deployment (coordinate with DevOps)

**Post-Release:**
- [ ] Verify deployment successful
- [ ] Announce release
- [ ] Close milestone
- [ ] Archive release notes
- [ ] Log in buildlog with `#commit`

---

=== PROCEDURE: Create Git Tag ===

**Purpose:** Tag release in git

**Steps:**
1. Ensure on main branch with latest code
2. Create annotated tag:
   ```bash
   git tag -a v1.2.3 -m "Release v1.2.3"
   ```
3. Push tag:
   ```bash
   git push origin v1.2.3
   ```

**Tag Naming:**
- Production: `v1.2.3`
- Pre-release: `v1.2.3-beta.1`, `v1.2.3-rc.1`

---

=== PROCEDURE: Create GitHub Release ===

**Purpose:** Create release in GitHub

**Steps:**
1. Go to Releases > Draft a new release
2. Select the tag created
3. Set release title: `v1.2.3`
4. Add release notes (use @ref(CB-TPL-RELEASE-001))
5. Mark as pre-release if applicable
6. Publish release

**Release Notes Structure:**
```markdown
## Highlights
- Key feature or fix

## What's Changed
[Auto-generated from PRs or from CHANGELOG]

## Breaking Changes
[If any]

## Upgrade Notes
[Migration steps if needed]

## Contributors
@contributor1, @contributor2
```

---

=== PROCEDURE: Hotfix Release ===

**Purpose:** Emergency release for critical fixes

**Steps:**
1. Create hotfix branch from tag:
   ```bash
   git checkout -b hotfix/v1.2.4 v1.2.3
   ```
2. Apply fix
3. Bump patch version
4. Update changelog
5. Merge to main
6. Create tag and release
7. Document in buildlog with `#resolution`

---

=== PROCEDURE: Rollback ===

**Purpose:** Revert to previous version

**Steps:**
1. Identify target version to rollback to
2. Notify stakeholders
3. Coordinate with DevOps for deployment rollback
4. Document rollback reason
5. Create issue for fix
6. Log in buildlog with `#issue-encountered`

---

=== ANTI-PATTERNS ===

### Incomplete Releases
**Problem:** Missing changelog, notes, or tags
**Solution:** Use release checklist every time

### Undocumented Hotfixes
**Problem:** Emergency fixes not properly tracked
**Solution:** Even hotfixes need changelog and notes

### Manual Deployments
**Problem:** Deploying without automation
**Solution:** Coordinate with DevOps for automated deployment

---

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(changelog-maintenance) | Changelog updated before release |
| @skill(versioning) | Version determined before release |
| @skill(deployment) | DevOps executes deployment |
