---
name: project-release
description: Releases ris-claude-code project - handles versioning, changelog, READMEs, tags, and GitHub releases. Use when releasing a new version or when asked to release.
---

# Project Release

Releases ris-claude-code with semantic versioning, changelog updates, and GitHub releases.

## Pre-release Checklist

Copy and check off:

```
- [ ] All changes committed
- [ ] Version bump determined
- [ ] READMEs need update? (only if skills list changed)
- [ ] All skill folders have SKILL.md + READMEs
```

## Version Rules

| Change | Bump | Example |
|--------|------|---------|
| New skill/component | MINOR | 1.5.1 → 1.6.0 |
| Update existing skill | PATCH | 1.5.1 → 1.5.2 |
| Bug fix, docs only | PATCH | 1.5.1 → 1.5.2 |

Get current version:

```bash
git describe --tags --abbrev=0
```

## Files Decision Matrix

| Condition | CHANGELOG | READMEs |
|-----------|-----------|---------|
| Any release | Update | Check below |
| Skills list changed (add/remove) | Update | Update both |
| Skills list unchanged | Update | Skip |

## Release Workflow

### Step 1: Update CHANGELOG.md

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature

### Changed
- Updated feature

### Fixed
- Bug fix
```

Update comparison links at bottom:

```markdown
[Unreleased]: https://github.com/serejaris/ris-claude-code/compare/vX.Y.Z...HEAD
[X.Y.Z]: https://github.com/serejaris/ris-claude-code/compare/vPREV...vX.Y.Z
```

### Step 2: Update READMEs (if needed)

Only if skills list changed. Update both:
- `README.md` (English)
- `README.ru.md` (Russian)

### Step 3: Commit

```bash
git add -A && git commit -m "docs: update changelog for vX.Y.Z"
```

### Step 4: Tag

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

### Step 5: Push

```bash
git push && git push --tags
```

### Step 6: GitHub Release

```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z — Short Description" \
  --notes "$(cat <<'EOF'
## Added/Changed
- Item 1
- Item 2

**Full Changelog**: https://github.com/serejaris/ris-claude-code/compare/vPREV...vX.Y.Z
EOF
)"
```

## Post-release Verification

```
- [ ] Tag visible: git tag -l | tail -1
- [ ] Release on GitHub: gh release view vX.Y.Z
- [ ] CHANGELOG links work
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgot CHANGELOG links | Add [X.Y.Z] comparison link at bottom |
| Wrong version bump | New skill = MINOR, update = PATCH |
| READMEs updated unnecessarily | Only update if skills LIST changed |
| Missing release notes | Use template above |
| Forgot to push tags | `git push --tags` separately |
