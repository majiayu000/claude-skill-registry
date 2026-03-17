---
name: nav-release
description: Validate and release Navigator plugin to marketplace. Auto-invoke when user says "release plugin", "publish navigator", "create release", or "deploy new version".
allowed-tools: Read, Bash, Grep, Glob, AskUserQuestion
version: 1.0.0
---

# Navigator Release Skill

Validate plugin integrity and release to marketplace with all safety checks.

## Why This Exists

After v5.1.0 incident where nav-profile was referenced in plugin.json but never committed, causing install failures. This skill ensures:
- All referenced skills exist and are committed
- Version consistency across all files
- Tag created AFTER all commits
- Post-release verification

## When to Invoke

**Auto-invoke when**:
- User says "release plugin", "publish navigator"
- User says "create release", "deploy new version"
- User says "release vX.Y.Z"

**DO NOT invoke if**:
- Just committing changes (no release)
- Updating documentation only
- Testing locally

## Execution Steps

### Step 1: Pre-Release Validation [CRITICAL]

**Run validation script**:

```bash
python3 functions/release_validator.py --check-all
```

This validates:
1. All skills in plugin.json exist
2. All skill files are committed (not untracked)
3. Version consistency across files
4. No uncommitted changes in skills/

**If validation fails**: STOP and fix issues before proceeding.

### Step 2: Display Validation Results

Show validation summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NAVIGATOR RELEASE VALIDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Skills Check:
  [x] nav-loop          ✓ exists, committed
  [x] nav-profile       ✓ exists, committed
  [x] nav-diagnose      ✓ exists, committed
  ...

Version Check:
  plugin.json:      5.1.0 ✓
  marketplace.json: 5.1.0 ✓
  CLAUDE.md:        5.1.0 ✓
  README.md:        5.1.0 ✓

Git Status:
  Uncommitted skills: 0 ✓
  Untracked skills:   0 ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDATION: PASSED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 3: Confirm Version

**Ask user to confirm version**:

```
Ready to release Navigator vX.Y.Z

This will:
1. Commit any pending changes
2. Push to origin/main
3. Create git tag vX.Y.Z
4. Create GitHub release

Proceed? [Y/n]
```

### Step 4: Execute Release

**If confirmed**, run release sequence:

```bash
# 1. Commit if needed
git add .
git commit -m "chore(release): prepare vX.Y.Z" || true

# 2. Push to origin
git push origin main

# 3. Create tag (AFTER push)
git tag -a vX.Y.Z -m "Navigator vX.Y.Z: [description]"
git push origin vX.Y.Z

# 4. Create GitHub release
gh release create vX.Y.Z --title "Navigator vX.Y.Z" --notes-file RELEASE-NOTES-vX.Y.Z.md
```

### Step 5: Post-Release Verification

**Verify tag contains all skills**:

```bash
python3 functions/release_validator.py --verify-tag vX.Y.Z
```

**Clear local cache** (for testing):

```bash
rm -rf ~/.claude/plugins/cache/navigator-marketplace/
```

**Instruct user to test**:

```
Release complete! To verify:

1. Run: /plugin install navigator
2. Check plugin list shows vX.Y.Z
3. Verify no errors in plugin details

If errors occur, see: .agent/sops/deployment/plugin-release.md
```

---

## Predefined Functions

### functions/release_validator.py

Validates plugin integrity before release:

```bash
# Check all skills exist and are committed
python3 functions/release_validator.py --check-all

# Verify specific version
python3 functions/release_validator.py --check-version 5.1.0

# Verify tag contents
python3 functions/release_validator.py --verify-tag v5.1.0
```

---

## Error Handling

**Missing skill detected**:
```
❌ VALIDATION FAILED

Missing skills:
  - skills/nav-profile/ (referenced in plugin.json but not found)

Fix: Create the skill or remove from plugin.json
```

**Uncommitted skills detected**:
```
❌ VALIDATION FAILED

Uncommitted skills:
  - skills/nav-loop/ (modified)
  - skills/nav-profile/ (untracked)

Fix: git add skills/ && git commit -m "Add missing skills"
```

**Version mismatch detected**:
```
❌ VALIDATION FAILED

Version mismatch:
  plugin.json:      5.1.0
  marketplace.json: 5.0.0  ← MISMATCH
  CLAUDE.md:        5.1.0

Fix: Update marketplace.json to 5.1.0
```

---

## Success Criteria

Release is successful when:
- [ ] All skills validated (exist + committed)
- [ ] Version consistent across all files
- [ ] Git tag created after all commits
- [ ] GitHub release published
- [ ] Test installation succeeds (no errors)

---

## Quick Reference

```bash
# Full release with validation
"Release Navigator v5.2.0"

# Just validate (no release)
"Validate plugin for release"

# Fix after failed release
"Fix release tag v5.1.0"
```

---

## Related

- **SOP**: `.agent/sops/deployment/plugin-release.md`
- **Config**: `.claude-plugin/plugin.json`
- **Marketplace**: `.claude-plugin/marketplace.json`
